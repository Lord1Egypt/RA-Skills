# USB Light Sensor Reader

A skill for reading light intensity from USB-connected light sensors with real-time monitoring, filtering, and threshold detection.

## Features

- **Real-time Monitoring** - Continuous light intensity readings
- **Moving Average Filter** - 5-sample smoothing for stable readings
- **Threshold Detection** - Dark/bright environment detection
- **Raw Data Access** - Option to read unfiltered values

## Requirements

- Python 3
- USB light sensor connected to `/dev/ttyUSB0`
- `pyserial` package
- User in `dialout` group (Linux)

## Installation

```bash
npx clawhub install usb-light-sensor-reader
```

## Quick Start

```python
from sensor import Sensor

# Initialize and connect
sensor = Sensor(port='/dev/ttyUSB0')
sensor.connect()

# Read light intensity
lux = sensor.read_lux()
print(f"Light: {lux:.2f} lux")

# Check environment
if sensor.is_dark():
    print("Environment is dark")

# Disconnect when done
sensor.disconnect()
```

## API Reference

### Class: `Sensor`

#### Constructor

```python
Sensor(port='/dev/ttyUSB0', baudrate=9600, timeout=1, filter_size=5)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `port` | `/dev/ttyUSB0` | Serial port |
| `baudrate` | `9600` | Baud rate |
| `timeout` | `1` | Timeout in seconds |
| `filter_size` | `5` | Moving average window size |

#### Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `connect()` | Connect to sensor | `bool` |
| `disconnect()` | Disconnect from sensor | `None` |
| `read_lux()` | Read filtered light intensity | `float` |
| `read_raw()` | Read unfiltered light intensity | `float` |
| `get_lux()` | Get latest reading | `float` |
| `is_dark(threshold=100)` | Check if dark | `bool` |
| `is_bright(threshold=500)` | Check if bright | `bool` |

## Sensor Protocol

Sensor outputs format: `brightness: XXX.XXLux\r\n`

| Setting | Value |
|---------|-------|
| Port | `/dev/ttyUSB0` |
| Baudrate | `9600` |
| Format | Text line with lux value |

## Usage Examples

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

### Custom Threshold

```python
from sensor import Sensor

sensor = Sensor()
sensor.connect()

# Custom threshold for dark detection
if sensor.is_dark(threshold=50):
    print("Very dark environment")

sensor.disconnect()
```

### Larger Filter for Smoother Readings

```python
# 10-sample moving average for smoother data
sensor = Sensor(filter_size=10)
sensor.connect()
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Permission denied` | Run `sudo usermod -a -G dialout $USER`, then logout/login |
| `Connection failed` | Check `ls /dev/ttyUSB*` for device |
| Returns `None` | Wait 1 second after connect for sensor warmup |
| Data not changing | Check sensor exposure, may need calibration |

## License

MIT
