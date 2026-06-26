# QuecPython Modbus IoT 设备技能

## 技能说明

**技能名称**: quecpython-modbus-iot  
**版本**: 1.0.0  
**作者**: 天津安信华瑞科技有限公司  
**描述**: 基于移远 QuecPython 平台的 Modbus IoT 设备通用框架，支持传感器数据采集、4G 网络传输、云平台对接、OTA 升级等功能。

---

## 触发条件

当用户提到以下需求时激活此技能：

- 需要在 QuecPython 设备上开发 Modbus 数据采集程序
- 需要将传感器数据上报到云平台
- 需要定制 IoT 设备的通信协议
- 需要修改设备上报频率、平台地址等配置
- 需要基于现有框架开发新的 IoT 应用
- 提到移远模组、QuecPython、EC200U、EC600N 等关键词

---

## 核心功能

### 1. 数据采集
- Modbus RTU 协议实现
- 支持 32 个传感器设备
- 自动扫描在线传感器
- 状态数据 + 浓度数据读取

### 2. 网络通信
- 4G LTE 网络连接
- 自动重连机制
- 信号强度监测
- NTP 时间同步

### 3. 数据上报
- HTTP/HTTPS 协议
- JSON 格式数据
- 失败自动重试
- 基于 IMEI 的错时上报

### 4. 系统管理
- 硬件看门狗保护
- 电源状态监测
- LED 状态指示
- OTA 远程固件升级

---

## 使用流程

### 步骤 1: 复制模板

将技能模板复制到用户项目目录：

```bash
# 从技能模板创建新项目
cp -r ~/.easyclaw/skills/quecpython-modbus-iot/template/ ~/projects/your-project/
```

### 步骤 2: 修改配置

编辑 `config/config.py` 文件，修改以下关键参数：

```python
# ========== 必须修改的配置 ==========

# 1. 数据上报平台地址
URL_REPORT = "https://your-platform.com/api/data"  # 客户平台地址
URL_OTA = "https://your-ota-server.com/ota"         # OTA 服务器地址

# 2. 设备信息
PROJECT_NAME = "your-project-name"                  # 项目名称
PROJECT_VERSION = "1.0.0"                           # 版本号
MANUFACTURER_NAME = "Your Company Name"             # 厂商名称
MANUFACTURER_ID = "your-contact-phone"              # 联系电话

# 3. 上报频率 (秒)
REPORT_INTERVAL_SEC = 60  # 60 秒 = 1 分钟，可根据需求调整

# ========== 根据硬件修改的配置 ==========

# 4. Modbus 通信参数
MODBUS_UART = 2              # UART 端口 (1/2/3)
MODBUS_BAUDRATE = 9600       # 波特率 (根据传感器调整)

# 5. LED 引脚
LED_NET_PIN = 36             # 网络指示灯 GPIO
LED_MODBUS_PIN = 44          # Modbus 指示灯 GPIO

# ========== 可选修改的配置 ==========

# 6. 传感器配置
SENSOR_MAX_COUNT = 32        # 最大传感器数量 (1-32)
SENSOR_BASE_ADDR = 1000      # 浓度数据起始地址
SENSOR_STAT_ADDR = 2000      # 状态数据起始地址

# 7. 重试次数
MODBUS_RETRY_MAX = 5         # Modbus 重试次数
HTTP_RETRY_MAX = 2           # HTTP 重试次数
```

### 步骤 3: 定制传感器协议 (如需要)

如果传感器协议与默认不同，修改 `src/sensor_device.py`：

```python
# 修改状态码解析
def read_status(self):
    result = self.modbus.read_registers(1, 2000 + self.addr, 1)
    status_value = result['data'][0]
    
    # 根据你的传感器协议修改状态码
    if status_value == 0:
        # 正常
        pass
    elif status_value == 1:
        # 你的自定义状态
        self.level_1_alarm = 1
    # ... 更多状态
```

### 步骤 4: 定制数据格式 (如需要)

如果平台数据格式不同，修改 `src/data_reporter.py`：

```python
def report_sensor_data(self, net_info, sensor_stat, sensor_dens, sys_stat):
    # 修改数据格式
    body = {
        # 根据你的平台协议修改字段
        'device_id': net_info.get('IMEI', ''),
        'timestamp': utime.time(),
        'sensors': sensor_stat,
        # ...
    }
```

### 步骤 5: 部署到设备

将以下 8 个文件复制到 QuecPython 设备的 `/usr` 目录：

```
/usr/
├── config.py              ← 从 config/config.py 复制
├── main.py                ← 从 src/main.py 复制
├── led_control.py         ← 从 src/led_control.py 复制
├── modbus_rtu.py          ← 从 src/modbus_rtu.py 复制
├── sensor_device.py       ← 从 src/sensor_device.py 复制
├── network_manager.py     ← 从 src/network_manager.py 复制
├── system_manager.py      ← 从 src/system_manager.py 复制
└── data_reporter.py       ← 从 src/data_reporter.py 复制
```

---

## 配置参数说明

### 核心配置

| 参数 | 说明 | 默认值 | 必须修改 |
|------|------|--------|----------|
| `URL_REPORT` | 数据上报平台地址 | 天津安信华瑞平台 | ✅ |
| `URL_OTA` | OTA 升级服务器地址 | 天津安信华瑞 OTA | ✅ |
| `PROJECT_NAME` | 项目名称 | tuoan_demo_shenzhen | ✅ |
| `PROJECT_VERSION` | 项目版本 | 2026.3.26 tuoan-dingzhi | ✅ |
| `REPORT_INTERVAL_SEC` | 上报频率 (秒) | 60 | ✅ |

### 硬件配置

| 参数 | 说明 | 默认值 | 按需修改 |
|------|------|--------|----------|
| `MODBUS_UART` | UART 端口号 | 2 | 根据硬件 |
| `MODBUS_BAUDRATE` | Modbus 波特率 | 9600 | 根据传感器 |
| `LED_NET_PIN` | 网络 LED 引脚 | 36 | 根据硬件 |
| `LED_MODBUS_PIN` | Modbus LED 引脚 | 44 | 根据硬件 |

### 传感器配置

| 参数 | 说明 | 默认值 | 按需修改 |
|------|------|--------|----------|
| `SENSOR_MAX_COUNT` | 最大传感器数 | 32 | 根据实际 |
| `SENSOR_BASE_ADDR` | 浓度数据起始地址 | 1000 | 根据协议 |
| `SENSOR_STAT_ADDR` | 状态数据起始地址 | 2000 | 根据协议 |

---

## 常见定制场景

### 场景 1: 修改上报频率为 5 分钟

```python
# config/config.py
REPORT_INTERVAL_SEC = 300  # 300 秒 = 5 分钟
```

### 场景 2: 修改平台地址

```python
# config/config.py
URL_REPORT = "https://api.mycompany.com/iot/data"
URL_OTA = "https://ota.mycompany.com/firmware"
```

### 场景 3: 修改波特率为 19200

```python
# config/config.py
MODBUS_BAUDRATE = 19200
```

### 场景 4: 只使用 8 个传感器

```python
# config/config.py
SENSOR_MAX_COUNT = 8
```

### 场景 5: 关闭调试输出 (生产环境)

```python
# config/config.py
DEBUG_ENABLE = False
DEBUG_MODBUS = False
DEBUG_NETWORK = False
DEBUG_HTTP = False
```

### 场景 6: 修改数据格式

在 `src/data_reporter.py` 中修改 `report_sensor_data()` 方法：

```python
# 原格式
body = {
    'id': timestamp,
    'time': time_str,
    'unit_code': net_info.get('IMEI', ''),
    # ...
}

# 修改为新格式
body = {
    'deviceId': net_info.get('IMEI', ''),
    'timestamp': timestamp,
    'data': {
        'sensors': sensor_stat,
        'densities': sensor_dens
    }
    # ...
}
```

---

## 项目结构

```
quecpython-modbus-iot/
├── SKILL.md                 # 技能说明 (本文件)
├── README.md                # 技能介绍
├── template/                # 项目模板
│   ├── config/             # 配置文件
│   │   ├── __init__.py
│   │   └── config.py       # ⚙️ 主配置
│   ├── src/                # 源代码
│   │   ├── main.py         # 🚀 主程序
│   │   ├── led_control.py  # 💡 LED 控制
│   │   ├── modbus_rtu.py   # 🔌 Modbus 协议
│   │   ├── sensor_device.py# 📡 传感器管理
│   │   ├── network_manager.py # 🌐 网络管理
│   │   ├── system_manager.py  # 🖥️ 系统管理
│   │   └── data_reporter.py   # 📤 数据上报
│   └── docs/               # 文档
│       ├── README.md       # 项目说明
│       ├── 部署指南.md
│       ├── 配置说明.md
│       └── 调试指南.md
└── examples/               # 示例配置
    ├── example-gas/        # 气体监测示例
    ├── example-temp/       # 温湿度监测示例
    └── example-water/      # 水质监测示例
```

---

## 模块说明

### 核心模块

| 模块 | 功能 | 是否可修改 |
|------|------|------------|
| `config.py` | 配置参数 | ✅ 必须修改 |
| `main.py` | 主程序逻辑 | ⚠️ 一般不改 |
| `modbus_rtu.py` | Modbus 协议 | ⚠️ 协议不变不改 |
| `sensor_device.py` | 传感器管理 | ✅ 根据传感器修改 |
| `data_reporter.py` | 数据上报 | ✅ 根据平台修改 |

### 辅助模块

| 模块 | 功能 | 是否可修改 |
|------|------|------------|
| `led_control.py` | LED 控制 | ❌ 无需修改 |
| `network_manager.py` | 网络管理 | ❌ 无需修改 |
| `system_manager.py` | 系统管理 | ❌ 无需修改 |

---

## 数据格式

### 默认上报格式

```json
{
  "id": 1711600000,
  "time": "2026-03-28 09:00:00",
  "unit_code": "863950067267346",
  "sys_stat": {
    "main_power_fail": 0,
    "back_power_fail": 0,
    "has_alarm": 0,
    "has_fail": 0
  },
  "sensor_stat": [
    {
      "sensor_index": 1,
      "sensor_addr": 0,
      "level_1_alarm": 0,
      "level_2_alarm": 0,
      "com_error": 0,
      "sensor_fail": 0
    }
  ],
  "sensor_dens": [
    {
      "sensor_index": 1,
      "sensor_addr": 0,
      "sensor_dense": 15
    }
  ],
  "collections": {
    "IMEI": "863950067267346",
    "signal_power": 20,
    "error_code": 0,
    "gas_sensor_state": 0
  }
}
```

---

## 调试方法

### 1. 启用调试输出

```python
# config/config.py
DEBUG_ENABLE = True
DEBUG_MODBUS = True
DEBUG_NETWORK = True
DEBUG_HTTP = True
```

### 2. 测试 Modbus 通信

```python
from modbus_rtu import ModbusRTU
modbus = ModbusRTU(2, 9600, 8, 0, 1, 0)
result = modbus.read_registers(1, 0, 1)
print("电池状态:", result)
```

### 3. 测试网络

```python
from network_manager import NetworkManager
net = NetworkManager("test", "1.0")
if net.wait_connected(30):
    info = net.get_network_info()
    print("IMEI:", info['IMEI'])
    print("信号:", info['signal_power'])
```

### 4. 测试上报

```python
from data_reporter import DataReporter
from led_control import LED
led = LED(36)
reporter = DataReporter(URL_REPORT, URL_OTA, led)
test_data = '{"test": 1}'
result = reporter.post(test_data, URL_REPORT)
print("上报结果:", result)
```

---

## 常见问题

### Q: 如何修改上报频率？
**A**: 修改 `config.py` 中的 `REPORT_INTERVAL_SEC` 参数

### Q: 如何更换平台地址？
**A**: 修改 `config.py` 中的 `URL_REPORT` 和 `URL_OTA`

### Q: 传感器读取失败？
**A**: 检查 `MODBUS_BAUDRATE` 是否与传感器一致，检查 RS485 接线

### Q: 网络连不上？
**A**: 检查 SIM 卡、天线，查看信号强度 `net.csqQueryPoll()`

### Q: 如何添加新传感器类型？
**A**: 修改 `sensor_device.py` 中的状态解析逻辑

---

## 技术支持

- **技能作者**: 天津安信华瑞科技有限公司
- **联系电话**: 18513099902
- **适用平台**: 移远 QuecPython (EC200U/EC600N 等)

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-03-28 | 初始版本，气体监测设备框架 |

---

## 许可证

Copyright © 2026 天津安信华瑞科技有限公司

---

*使用此技能前，请确保你有 QuecPython 开发环境和兼容的硬件设备。*
