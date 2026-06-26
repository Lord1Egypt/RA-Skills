# 气体监测设备示例配置

## 配置说明

这是一个典型的可燃气体监测设备配置示例。

## 核心配置

```python
# config/config.py

# ========== 设备信息 ==========
PROJECT_NAME = "gas-monitor-demo"
PROJECT_VERSION = "1.0.0"
MANUFACTURER_NAME = "XX 科技有限公司"
MANUFACTURER_ID = "400-XXX-XXXX"

# ========== 平台地址 ==========
URL_REPORT = "https://gas-platform.example.com/api/data"
URL_OTA = "https://ota.example.com/firmware"

# ========== 上报频率 ==========
REPORT_INTERVAL_SEC = 60  # 1 分钟上报一次

# ========== Modbus 配置 ==========
MODBUS_UART = 2
MODBUS_BAUDRATE = 9600  # 气体传感器常用波特率

# ========== 传感器配置 ==========
SENSOR_MAX_COUNT = 8    # 8 个气体探头
SENSOR_BASE_ADDR = 1000
SENSOR_STAT_ADDR = 2000

# ========== LED 引脚 ==========
LED_NET_PIN = 36
LED_MODBUS_PIN = 44
```

## 传感器类型

- 可燃气体 (CH4)
- 一氧化碳 (CO)
- 硫化氢 (H2S)
- 氧气 (O2)

## 报警阈值

- 低报：25% LEL
- 高报：50% LEL

## 部署说明

1. 修改 `URL_REPORT` 为实际平台地址
2. 确认 Modbus 波特率与传感器一致
3. 上传 8 个文件到设备 `/usr` 目录
4. 运行测试
