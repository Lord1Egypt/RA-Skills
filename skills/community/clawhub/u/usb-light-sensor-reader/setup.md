# Setup — USB Light Sensor Reader

## Prerequisites

- USB light sensor connected to `/dev/ttyUSB0`
- Python 3 with `pyserial` installed
- User in `dialout` group (for serial port access)

## Quick Start

```bash
# Install dependencies
pip3 install pyserial

# Add user to dialout group (if needed)
sudo usermod -a -G dialout $USER

# Test sensor
python3 sensor.py
```

## Usage Examples

### Basic Reading

```python
from sensor import Sensor

sensor = Sensor(port='/dev/ttyUSB0')
if sensor.connect():
    lux = sensor.read_lux()
    print(f"Light: {lux:.2f} lux")
    sensor.disconnect()
```

### Continuous Monitoring

```python
from sensor import Sensor
import time

sensor = Sensor()
sensor.connect()

try:
    while True:
        lux = sensor.read_lux()
        print(f"\r{lux:.2f} lux", end='', flush=True)
        time.sleep(1)
except KeyboardInterrupt:
    sensor.disconnect()
```

### Threshold Detection

```python
from sensor import Sensor

sensor = Sensor()
sensor.connect()

lux = sensor.read_lux()

if sensor.is_dark(threshold=100):
    print("Environment is dark")
elif sensor.is_bright(threshold=500):
    print("Environment is bright")
else:
    print(f"Light level: {lux:.2f} lux")

sensor.disconnect()
```

### Custom Filter Size

```python
# Larger filter = smoother but slower response
sensor = Sensor(filter_size=10)  # 10-sample moving average
sensor.connect()
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Permission denied` | `sudo usermod -a -G dialout $USER`, then logout/login |
| `Connection failed` | Check `ls /dev/ttyUSB*` for device |
| Returns `None` | Wait 1 second after connect, sensor is warming up |
| Data not changing | Check sensor exposure, may need calibration |

## Sensor Protocol

Sensor outputs: `brightness: XXX.XXLux\r\n`
- Port: `/dev/ttyUSB0`
- Baudrate: `9600`
- Format: Text line with lux value

