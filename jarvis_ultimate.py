import cv2
import face_recognition
import warnings
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
from ultralytics import YOLO
import threading
import os
import time
import serial
import speech_recognition as sr

# 1. Ignore warnings
warnings.filterwarnings("ignore")

# 2. Setup Boss's Photo (Jimmy)
print("JARVIS INITIALIZATION: Please select your photo...")
root = tk.Tk()
root.withdraw() 
file_path = filedialog.askopenfilename(title="Select Jimmy's Photo", filetypes=[("Images", "*.jpg *.jpeg *.png")])

if not file_path:
    print("\n[ERROR]: No image selected. Shutting down.")
    exit()

print("Loading facial features...")
try:
    pil_image = Image.open(file_path).convert("RGB")
    boss_image = np.array(pil_image)
    
    encodings = face_recognition.face_encodings(boss_image)
    if len(encodings) == 0:
        print("\n[ERROR]: No face detected in the image.")
        exit()
    boss_face_encoding = encodings[0]
except Exception as e:
    print(f"\n[ERROR]: Image issue! Details: {e}")
    exit()

known_face_encodings = [boss_face_encoding]
known_face_names = ["Jimmy"]

# 3. Setup ESP32
try:
    esp32 = serial.Serial('COM4', 9600, timeout=1)
    time.sleep(2) 
    print("ESP32 Connected on COM4!")
except Exception:
    esp32 = None
    print("WARNING: ESP32 not found on COM4. Running without hardware.")

# 4. Voice and Commands (Ear and Mouth)
running = True
vision_enabled = True

def jarvis_speak(text):
    print(f"JARVIS: {text}")
    command = f'''PowerShell -Command "Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.SelectVoiceByHints('Female'); $s.Speak('{text}')"'''
    threading.Thread(target=lambda: os.system(command), daemon=True).start()

def ear_worker():
    global vision_enabled, running
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("[SYSTEM]: JARVIS Ear is active and ready.")
    except Exception as e:
        print(f"[MICROPHONE ERROR]: {e}")
        return
    
    while running:
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
                text = recognizer.recognize_google(audio).lower()
                print(f"[HEARD]: {text}")
                
                # --- Lightweight voice commands for easier pronunciation ---
                
                # 1. Shutdown command (saying "bye" or "end" is enough)
                if "bye" in text or "end" in text:
                    jarvis_speak("Goodbye, sir.")
                    running = False
                    break
                
                # 2. Pause vision command (saying "off" or "wait")
                elif "off" in text or "wait" in text:
                    jarvis_speak("Vision off.")
                    vision_enabled = False
                
                # 3. Resume vision command (saying "on" or "go")
                elif "on" in text or "go" in text:
                    jarvis_speak("Vision on.")
                    vision_enabled = True
                    
        except:
            pass

# Start the ear thread
threading.Thread(target=ear_worker, daemon=True).start()

# 5. Load Visual Brain (YOLO)
print("Loading AI Object Detection Model...")
model = YOLO('yolov8n.pt')

print("Starting Camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR]: Camera not working.")
    running = False

jarvis_speak("Systems online. Ready, sir.")

# Performance and logic variables
process_this_frame = True
face_locations = []
face_names = []
last_scene_objects = set()
last_speak_time = 0
cooldown = 4 
has_greeted_boss = False 

# 6. The Main Loop
while running:
    success, frame = cap.read()
    if not success:
        break

    if vision_enabled:
        # a. Object detection and drawing (YOLO)
        results = model(frame, stream=True, conf=0.5, verbose=False)
        current_scene_objects = set()
        for r in results:
            frame = r.plot()
            for box in r.boxes:
                class_id = int(box.cls[0])
                current_scene_objects.add(model.names[class_id])

        # b. Face recognition (Frame skipping for performance)
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    name = known_face_names[matches.index(True)]
                face_names.append(name)

        process_this_frame = not process_this_frame
        current_time = time.time()

        # c. Interaction and speech
        if "Jimmy" in face_names and not has_greeted_boss:
            jarvis_speak("Welcome, Jimmy.")
            has_greeted_boss = True

        if current_scene_objects != last_scene_objects and (current_time - last_speak_time > cooldown):
            if 'cell phone' in current_scene_objects and esp32 is not None:
                esp32.write(b'1')
            
            objects_to_say = current_scene_objects.copy()
            if 'person' in objects_to_say:
                objects_to_say.remove('person')
                
            if len(objects_to_say) > 0:
                objects_names = ", ".join(objects_to_say)
                # Shortened the output to the object's name directly for faster response
                jarvis_speak(f"{objects_names}") 
            
            last_scene_objects = current_scene_objects.copy()
            last_speak_time = current_time

        # d. Draw face bounding boxes
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4; right *= 4; bottom *= 4; left *= 4
            color = (0, 255, 0) if name == "Jimmy" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 3)
            cv2.putText(frame, name, (left, top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
        annotated_frame = frame
    else:
        annotated_frame = frame.copy()
        cv2.putText(annotated_frame, "VISION PAUSED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("JARVIS Ultimate Core", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if esp32 is not None:
    esp32.close()
