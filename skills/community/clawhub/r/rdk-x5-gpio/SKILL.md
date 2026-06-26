---
name: rdk-x5-gpio
description: "控制 RDK X5 40pin 排针接口：GPIO 数字输入/输出、PWM 舵机/电机/LED 呼吸灯、I2C 传感器通信、SPI 总线、UART 串口、CAN 总线。Use when the user wants to control GPIO pins, drive servos/motors/LEDs with PWM, communicate with I2C/SPI sensors, use UART serial, configure CAN bus, or check 40pin pinout. Provides commands and wiring guidance, not full script authoring. Do NOT use for camera (use rdk-x5-camera), network (use rdk-x5-network), or AI inference (use rdk-x5-ai-detect)."
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    compatibility:
      platform: rdk-x5
---

# RDK X5 GPIO — 40pin 外设控制

RDK X5 40pin 排针兼容树莓派引脚定义，支持 GPIO / PWM / I2C / SPI / UART / CAN。

## 前置准备

```bash
# GPIO 库（系统已预装 Hobot.GPIO）
pip3 show Hobot.GPIO

# 引脚功能复用配置（v3.3.3+ 支持自动复用）
sudo srpi-config
# → Interface Options → 选择需要的总线
```

## 操作步骤

### 1. GPIO 数字输出

```python
import Hobot.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)   # 高电平
time.sleep(1)
GPIO.output(11, GPIO.LOW)    # 低电平
GPIO.cleanup()
```

### 2. GPIO 数字输入

```python
import Hobot.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
print(f"Pin 12: {GPIO.input(12)}")
GPIO.cleanup()
```

### 3. PWM 控制（舵机/LED）

```python
import Hobot.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
pwm = GPIO.PWM(32, 50)       # 50Hz = 舵机标准频率
pwm.start(7.5)               # 中位（占空比 7.5%）
time.sleep(1)
pwm.ChangeDutyCycle(2.5)     # 0°
time.sleep(1)
pwm.ChangeDutyCycle(12.5)    # 180°
time.sleep(1)
pwm.stop()
GPIO.cleanup()
```
v3.4.1+ 支持多路 PWM 同时输出。

### 4. I2C 扫描与读写

```bash
ls /dev/i2c-*                             # 查看总线
sudo i2cdetect -y 1                       # 扫描总线 1
sudo i2cget -y 1 0x48 0x00               # 读寄存器
sudo i2cset -y 1 0x48 0x01 0xFF          # 写寄存器
```

### 5. SPI 通信

```bash
ls /dev/spidev*
pip3 install spidev
```
```python
import spidev
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
resp = spi.xfer2([0x01, 0x02, 0x03])
print(resp)
spi.close()
```

### 6. UART 串口

```bash
ls /dev/ttyS*
```
```python
import serial
ser = serial.Serial('/dev/ttyS1', 115200, timeout=1)
ser.write(b'Hello RDK X5\n')
print(ser.readline())
ser.close()
```

### 7. CAN 总线

```bash
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up
cansend can0 123#DEADBEEF          # 发送
candump can0                       # 接收
```

## /app/40pin_samples 示例

```bash
cd /app/40pin_samples
sudo python3 simple_out.py         # GPIO 输出
sudo python3 simple_pwm.py         # PWM
sudo python3 button_event.py       # 按钮事件
sudo python3 test_i2c.py           # I2C
sudo python3 test_spi.py           # SPI
sudo python3 test_serial.py        # UART
```

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| `Permission denied` | 未用 sudo 或引脚被占用 | `sudo` 运行脚本 |
| I2C 扫描无设备 | 总线未启用或接线错误 | `srpi-config` 启用 I2C；检查 SDA/SCL 接线 |
| PWM 无输出 | 引脚复用冲突 | `srpi-config` 确认引脚已配置为 PWM 功能 |
| CAN 无法 up | 内核模块未加载 | `sudo modprobe can_raw`；检查 `/boot/config.txt` |
