# ⚡ S2 Energy: Edge & Hardware Setup Guide / 边缘与硬件部署指南

## 1. Nano-scale Edge Vision Setup (For Step A - Vision Inventory)
To enable the "foolproof" photo inventory method without sending private images to cloud LLMs, S2 employs a Nano-scale Edge CNN.

**Hardware**: Any Edge Server (Raspberry Pi 3/4, NAS, or ESP32-S3).
**Dependencies**:
```bash
pip install tflite-runtime opencv-python-headless numpy

Deployment Steps:

    Download a quantized MobileNet SSD model trained on the COCO dataset (Size: ~3MB).

    When the user passes an image path via --method vision, the Python script loads the .tflite model.

    The model instantly draws bounding boxes over items like tv, refrigerator, or microwave.

    The script maps these generic COCO classes to our strict S2 wattage dictionaries.

    Privacy Absolute: The photo is processed in RAM and destroyed. Zero bytes leave your local network.

2. Smart Breaker RS485 Integration (For Step E)

    Install an S2-compatible Smart Distribution Box with Modbus/RS485.

    Wire the RS485 A/B terminals to your Edge Server.

    The read_breaker action passively polls Modbus registers. Actuation (cutting power) must be handled by the Agent's separate decision loop.