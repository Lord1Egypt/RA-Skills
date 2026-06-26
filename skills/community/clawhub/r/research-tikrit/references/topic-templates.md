# Topic Templates — CS & Math Research (Tikrit University)

These are ready-made content outlines for the most common graduation project topics
seen at the College of Computer Science and Mathematics. Use them to guide chapter
content generation.

---

## Template A: Smart Mobile Robot / Robotic Arm

### Chapter Two topics to cover:
- Robotics overview and history
- Types of robotic arms (Cartesian, Cylindrical, Articulated, SCARA, etc.)
- Arduino UNO R3 — specifications, pin layout
- Servo motors — types (SG90, MG996R), control via PWM
- DC motors + L298N motor driver
- Tracked / wheeled chassis
- Object detection overview → CNN → YOLO (v5/v8)
- ESP32-CAM module

### Chapter Three phases:
1. Dataset collection and preprocessing (Roboflow, split: 70/20/10)
2. YOLO model training (epochs: 100, image size: 640×640, batch: 16)
3. Robotic arm assembly
4. Embedded control system (Arduino code, joystick interface)
5. Mobile base development and integration
6. System testing

### Key result metrics:
- Precision, Recall, mAP@0.5, mAP@0.5:0.95

---

## Template B: CNN-Based Image Recognition / Signature Verification

### Chapter Two topics:
- Pattern recognition fundamentals
- Artificial Neural Networks (ANN) basics
- Convolutional Neural Networks (CNN) — layers: Conv, Pooling, Flatten, Dense
- Activation functions (ReLU, Sigmoid, Softmax)
- Signature verification approaches: offline vs online
- Dataset description (CEDAR, UTSig, or custom)
- Transfer learning (if used: VGG16, ResNet, EfficientNet)
- Google Colab as training environment

### Chapter Three phases:
1. Dataset collection and preprocessing (resizing, normalization, augmentation)
2. Model architecture design
3. Training (epochs, batch size, optimizer: Adam)
4. Evaluation methodology

### Key result metrics:
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix description
- False Acceptance Rate (FAR), False Rejection Rate (FRR) for signature projects

---

## Template C: Smart Home System

### Chapter Two topics:
- IoT fundamentals
- Microcontrollers: Arduino Uno, ESP8266 (NodeMCU), ESP32
- Sensors: DHT11 (temperature/humidity), PIR (motion), LDR (light), rain sensor, flame sensor
- Actuators: servo motors, relays, LEDs
- Communication: WiFi (ESP8266/ESP32), Bluetooth, Telegram Bot API
- MQTT protocol (if used)
- Flask / PHP web dashboard

### Chapter Three phases:
1. Hardware assembly and wiring
2. Sensor calibration and testing
3. Arduino/microcontroller programming
4. WiFi bridge or direct connection setup
5. Dashboard / bot development
6. Integration testing

### Key result metrics:
- Response time (ms)
- Sensor accuracy vs datasheet spec
- System uptime / reliability

---

## Template D: Networking / Protocol Implementation (TCP/UDP)

### Chapter Two topics:
- OSI model — all 7 layers with functions
- TCP/IP model — 4 layers
- Transport Layer in depth:
  - TCP: connection-oriented, three-way handshake (SYN → SYN-ACK → ACK),
    reliability, flow control, congestion control
  - UDP: connectionless, speed advantages, use cases
- Socket programming concepts (server/client model)
- Comparison table: TCP vs UDP

### TCP vs UDP Comparison Table:
| Feature | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | No guarantee |
| Speed | Slower | Faster |
| Use cases | HTTP, FTP, Email | Video streaming, DNS, VoIP |
| Header size | 20 bytes | 8 bytes |

### Chapter Three phases:
1. Software environment (Python/C++, IDE)
2. Server socket implementation
3. Client socket implementation
4. Data transmission testing
5. Performance measurement

---

## Template E: Database / Management Information System

### Chapter Two topics:
- Database fundamentals (RDBMS vs NoSQL)
- Entity-Relationship (ER) model
- Normalization (1NF, 2NF, 3NF)
- SQL fundamentals (SELECT, INSERT, UPDATE, DELETE, JOIN)
- System development methodologies (Waterfall, Agile)
- Frontend technologies used (HTML, CSS, PHP, JavaScript)
- Backend / server technology

### Chapter Three phases:
1. Requirements analysis
2. ER diagram design
3. Database schema implementation
4. System interface design
5. Module implementation
6. Testing

---

## Template F: Cybersecurity / Network Security

### Chapter Two topics:
- CIA triad (Confidentiality, Integrity, Availability)
- Types of attacks (DoS, MITM, Phishing, SQL Injection, etc.)
- Encryption: symmetric (AES, DES) vs asymmetric (RSA)
- Hashing (MD5, SHA-256)
- Firewalls, IDS/IPS
- VPN fundamentals
- Specific technology used in the project

### Common result metrics:
- Encryption/decryption time
- Key strength analysis
- Detection rate (for IDS projects)