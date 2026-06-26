# 温湿度监测设备示例配置

## 配置说明

这是一个仓库温湿度监测设备配置示例。

## 核心配置

```python
# config/config.py

# ========== 设备信息 ==========
PROJECT_NAME = "warehouse-temp-humidity"
PROJECT_VERSION = "1.0.0"
MANUFACTURER_NAME = "XX 智能科技"
MANUFACTURER_ID = "010-XXXXXXX"

# ========== 平台地址 ==========
URL_REPORT = "https://warehouse-iot.example.com/api/temp"
URL_OTA = "https://ota.example.com/firmware"

# ========== 上报频率 ==========
REPORT_INTERVAL_SEC = 300  # 5 分钟上报一次 (温湿度变化慢)

# ========== Modbus 配置 ==========
MODBUS_UART = 2
MODBUS_BAUDRATE = 9600

# ========== 传感器配置 ==========
SENSOR_MAX_COUNT = 16   # 16 个温湿度传感器
SENSOR_BASE_ADDR = 0    # 温湿度传感器地址从 0 开始
SENSOR_STAT_ADDR = 100  # 状态寄存器地址

# ========== LED 引脚 ==========
LED_NET_PIN = 36
LED_MODBUS_PIN = 44
```

## 传感器类型

- 温湿度一体传感器
- RS485 接口
- Modbus RTU 协议

## 测量范围

- 温度：-40°C ~ +80°C
- 湿度：0% ~ 100% RH

## 报警阈值

- 温度低报：< 5°C
- 温度高报：> 35°C
- 湿度低报：< 30% RH
- 湿度高报：> 80% RH

## 特殊配置

需要修改 `sensor_device.py` 中的状态解析逻辑，适配温湿度传感器协议。
