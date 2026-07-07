# JARVIS Ultimate Core 🧠👁️👂🤖

An integrated Mechatronics and AI personal assistant system combining **Computer Vision**, **Natural Language Processing (NLP)**, and **IoT Hardware Control**. This project bridges the gap between software intelligence and physical hardware actuation.

## ✨ Core Features

* **👁️ Dynamic Face ID:** Real-time facial recognition that dynamically loads the user's reference image without hardcoding it, ensuring privacy and seamless setup.
* **🎯 Real-Time Object Detection (YOLOv8):** Scans the environment to identify specific objects (e.g., cell phones) with optimized Frame Skipping algorithms to maintain high CPU performance and real-time execution.
* **🗣️ Accessibility-Focused Voice Control:** Engineered with a lightweight, single-syllable voice command architecture (e.g., "on", "off", "bye"). This inclusive design ensures maximum responsiveness and provides an effortless, stutter-friendly user experience.
* **⚙️ Hardware Actuation & UI (ESP32):** Communicates with an ESP32 microcontroller via Serial. Includes an OLED SSD1306 display for a premium visual UI and a Servo motor for physical interaction upon visual triggers.

## 🛠️ Hardware Requirements

* PC/Laptop with Webcam and Microphone.
* **ESP32 Microcontroller** (Connected via USB on `COM4` - configurable).
* **SSD1306 OLED Display** (128x64) via I2C.
* **Servo Motor** (Connected to Pin 18).

## 🗂️ Repository Structure

\`\`\`text
├── jarvis_ultimate.py        # The Master Python AI Script
├── requirements.txt          # Specific library versions for system stability
├── .gitignore                # Excludes heavy AI models and cache
└── ESP32_Hardware/
    └── ESP32_Hardware.ino    # C++ firmware for the ESP32 hardware node
\`\`\`

## 🚀 Installation & Setup

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/JimmyHadad/jarvis-ultimate-core.git
   cd jarvis-ultimate-core
   \`\`\`

2. **Install locked dependencies:**
   *(Note: Specific versions like `numpy==1.26.4` and `opencv-python==4.9.0.80` are strictly locked to prevent dlib and YOLO compatibility issues).*
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Flash the ESP32:**
   * Open `ESP32_Hardware.ino` in the Arduino IDE.
   * Install the `Adafruit_SSD1306`, `Adafruit_GFX`, and `ESP32Servo` libraries.
   * Upload the code to your ESP32 board.

4. **Run the Core System:**
   \`\`\`bash
   python jarvis_ultimate.py
   \`\`\`

## 💡 How it Works
1. Upon launch, a GUI prompts you to select your ID photo.
2. The AI loads its visual and auditory models while establishing a handshake with the ESP32.
3. The system operates continuously:
   * Speak **"off"** to pause vision processing, **"on"** to resume, or **"bye"** to shut down safely.
   * If the camera detects the targeted object (e.g., Cell phone), the ESP32 updates the OLED display to alert the user and actuates the Servo motor simultaneously.
