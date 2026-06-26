# 水质监测设备示例配置

## 配置说明

这是一个河流/污水水质监测设备配置示例。

## 核心配置

```python
# config/config.py

# ========== 设备信息 ==========
PROJECT_NAME = "water-quality-monitor"
PROJECT_VERSION = "1.0.0"
MANUFACTURER_NAME = "XX 环保科技"
MANUFACTURER_ID = "0755-XXXXXXX"

# ========== 平台地址 ==========
URL_REPORT = "https://epb.gov.cn/api/water-quality"
URL_OTA = "https://ota.example.com/firmware"

# ========== 上报频率 ==========
REPORT_INTERVAL_SEC = 900  # 15 分钟上报一次

# ========== Modbus 配置 ==========
MODBUS_UART = 2
MODBUS_BAUDRATE = 9600

# ========== 传感器配置 ==========
SENSOR_MAX_COUNT = 6    # 6 参数水质传感器
SENSOR_BASE_ADDR = 0
SENSOR_STAT_ADDR = 100

# ========== LED 引脚 ==========
LED_NET_PIN = 36
LED_MODBUS_PIN = 44
```

## 监测参数

- PH 值
- 浊度 (NTU)
- 溶解氧 (DO)
- 电导率 (EC)
- 温度
- 氨氮

## 上报数据格式

需要修改 `data_reporter.py`，适配环保部门的数据格式标准。

## 特殊要求

- 需要支持 HJ 212-2017 协议 (可选)
- 需要数据标记 (正常/维护/故障)
- 需要支持远程校准指令
