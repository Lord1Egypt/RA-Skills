---
name: rdkx5-app-resources
description: "Access to RDK X5 /app folder resources including GPIO, multimedia, AI samples. Invoke when user wants to run embedded demos or control hardware on RDK X5."
---

# RDK X5 App Resources Skill

This skill provides access to embedded hardware resources in `/app` folder on D-Robotics RDK X5 boards, including GPIO control, I2C/SPI communication, video capture, media processing, and AI inference.

## ⚠️ Important: Use System Python (NOT conda)

**Most of these resources require system Python, NOT conda environment!**

The D-Robotics board has `hobot_dnn` and other libraries installed in system Python (`/usr/bin/python3.10`), but NOT in conda environments.

**Always use system Python to run these scripts:**

```bash
# ✅ Correct - use system Python
/usr/bin/python3.10 /app/pydev_demo/01_basic_sample/test_resnet18.py

# ❌ Wrong - conda environment does NOT have hobot_dnn
python /app/pydev_demo/01_basic_sample/test_resnet18.py  # will fail!
```

If you accidentally use conda Python, you'll get errors like:
```
ModuleNotFoundError: No module named 'hobot_dnn'
```

## Available Resources

### 1. 40pin GPIO Samples (`/app/40pin_samples/`)

Python-based GPIO control using `Hobot.GPIO` library:

| File | Description |
|------|-------------|
| `simple_out.py` | Basic GPIO output (LED control) |
| `simple_input.py` | Basic GPIO input (read pin state) |
| `simple_pwm.py` | PWM output (e.g., motor speed control) |
| `button_event.py` | Button event handling |
| `button_interrupt.py` | Button interrupt handling |
| `button_led.py` | Button controlling LED |
| `test_i2c.py` | I2C communication test |
| `test_spi.py` | SPI communication test |
| `test_serial.py` | Serial/UART communication test |
| `test_all_pins.py` | All pins test |

### 2. Character Device Demos (`/app/cdev_demo/`)

C-based device driver examples:

| Directory | Description |
|-----------|-------------|
| `v4l2/` | V4L2 video capture |
| `vio_capture/` | Video input capture |
| `vio2display/` | Video to display output |
| `vio2encoder/` | Video encoding |
| `rtsp2display/` | RTSP stream to display |
| `vps/` | Video Processing System |
| `bpu/` | BPU (Brain Processing Unit) demos |
| `decode2display/` | Decode to display |

### 3. Multimedia Samples (`/app/multimedia_samples/`)

C/C++ multimedia processing examples:

| Directory | Description |
|-----------|-------------|
| `sample_codec/` | Audio/Video encoding & decoding |
| `sample_dsp/` | DSP processing |
| `sample_gdc/` | Geometric Distortion Correction |
| `sample_gpu_2d/` | 2D GPU operations |
| `sample_hbmem/` | High Bandwidth Memory |
| `sample_isp/` | Image Signal Processor (camera tuning) |
| `sample_osd/` | On-Screen Display |
| `sample_pipeline/` | Media pipeline processing |
| `sample_usb/` | USB camera support |
| `sample_vin/` | Video Input |
| `sample_vot/` | Video Output |
| `sample_vse/` | Video Sync Engine |
| `sunrise_camera/` | Sunrise camera modules |
| `vp_sensors/` | Vision platform sensors |
| `chip_base_test/` | Chip baseline tests |
| `utils/` | Utility tools |

### 4. Python AI Samples (`/app/pydev_demo/`)

Python-based AI model inference examples:

| Directory | Description |
|-----------|-------------|
| `01_basic_sample/` | Basic usage |
| `02_usb_camera_sample/` | USB camera inference |
| `03_mipi_camera_sample/` | MIPI camera inference |
| `04_segment_sample/` | Image segmentation |
| `05_web_display_camera_sample/` | Web display camera |
| `06_yolov3_sample/` | YOLOv3 object detection |
| `07_yolov5_sample/` | YOLOv5 object detection |
| `08_decode_rtsp_stream/` | RTSP stream decoding |
| `09_yolov5x_sample/` | YOLOv5x object detection |
| `10_ssd_mobilenetv1_sample/` | SSD MobileNetV1 detection |
| `11_centernet_sample/` | CenterNet object detection |
| `12_yolov5s_v6_v7_sample/` | YOLOv5s v6/v7 variants |

Model files are linked from `/app/model/basic` (or `/opt/hobot/model/x5/basic`).

### 5. ISP Tuning Tool (`/app/tuning_tool/`)

Image Signal Processor tuning tools:

| File | Description |
|------|-------------|
| `isp_tuning` | ISP tuning executable |
| `run_tuning.sh` | Tuning launch script |
| `tuning_cfg/` | Tuning configuration files |

## Quick Reference

### Running Python Samples - ALWAYS use system Python!

```bash
# ✅ CORRECT - Use system Python (/usr/bin/python3.10)
# These have hobot_dnn and other D-Robotics libraries

/usr/bin/python3.10 /app/40pin_samples/simple_out.py
/usr/bin/python3.10 /app/40pin_samples/button_led.py
/usr/bin/python3.10 /app/40pin_samples/test_i2c.py
/usr/bin/python3.10 /app/40pin_samples/test_spi.py
/usr/bin/python3.10 /app/40pin_samples/test_serial.py

/usr/bin/python3.10 /app/pydev_demo/01_basic_sample/test_resnet18.py
/usr/bin/python3.10 /app/pydev_demo/07_yolov5_sample/main.py
/usr/bin/python3.10 /app/pydev_demo/08_decode_rtsp_stream/main.py
```

### Building C/C++ Demos

```bash
# Build multimedia samples
cd /app/multimedia_samples/
make

# Build character device demos
cd /app/cdev_demo/v4l2/
make
```

### Running ISP Tuning

```bash
cd /app/tuning_tool/
./run_tuning.sh
```

## GPIO Pin Reference

- **Pin 37** - BOARD编码模式下的 GPIO37 (对应 WPI 25)
- Uses `Hobot.GPIO` library (D-Robotics GPIO wrapper)
- Modes: `GPIO.BOARD`, `GPIO.BCM`, `GPIO.WPI`

## Important Notes

1. **⚠️ ALWAYS use system Python** - `/usr/bin/python3.10`, NOT conda
2. **Hardware Access**: Most operations require root privileges or proper hardware permissions
3. **Pin Numbers**: Use BOARD encoding (physical pin numbers) or BCM encoding (Broadcom)
4. **Library**: Uses `Hobot.GPIO` which is D-Robotics' GPIO wrapper
5. **Cleanup**: Always call `GPIO.cleanup()` when done
6. **Models**: Pre-trained models are in `/app/model/basic/`
7. **Scope**: This skill covers `/app` folder resources only. For system commands and other RDK X5 features, refer to official documentation.

## Use Cases

- Control LEDs, motors, relays via GPIO
- Read button/switch states
- Communicate with I2C sensors (temperature, IMU, etc.)
- Interface with SPI devices
- Capture video from camera modules (USB, MIPI)
- Video encoding/decoding
- RTSP video streaming
- Run AI inference (YOLO, SSD, CenterNet, segmentation)
- ISP camera tuning
- Video pipeline processing

---

**Note**: This skill focuses on `/app` folder sample resources. It is not a complete RDK X5 operation guide.
