# QuecPython Modbus IoT 设备技能

## 技能概述

**这是一个通用的 QuecPython IoT 设备开发框架技能**，基于移远 QuecPython 平台，支持 Modbus RTU 传感器数据采集、4G 网络传输、云平台对接等功能。

通过这个技能，你可以快速定制自己的 IoT 设备，将传感器数据按照约定频率发送到客户指定的平台地址。

---

## 🎯 适用场景

- ✅ 气体监测设备 (可燃气体、有毒气体)
- ✅ 温湿度监测
- ✅ 水质监测 (PH 值、浊度、溶解氧)
- ✅ 电力监测 (电压、电流、功率)
- ✅ 工业传感器数据采集
- ✅ 任何需要 Modbus RTU + 4G 上报的场景

---

## 🚀 快速开始

### 1. 激活技能

当需要开发 QuecPython IoT 设备时，直接说：

> "帮我基于 quecpython-modbus-iot 技能创建一个新项目"

或

> "我需要把传感器数据上报到云平台，用 QuecPython"

### 2. 创建项目

技能会自动：

1. 复制模板到你的工作区
2. 生成项目结构
3. 提示你修改配置

### 3. 修改配置

编辑 `config/config.py`：

```python
# 必须修改的 3 个核心参数
URL_REPORT = "https://your-platform.com/api/data"  # 客户平台
PROJECT_NAME = "your-project"                       # 项目名称
REPORT_INTERVAL_SEC = 60                            # 上报频率 (秒)
```

### 4. 部署到设备

将 8 个 `.py` 文件上传到 QuecPython 设备的 `/usr` 目录。

---

## 📋 核心功能

| 功能 | 说明 | 可定制 |
|------|------|--------|
| **数据采集** | Modbus RTU 协议，支持 32 个传感器 | ✅ 传感器协议 |
| **网络通信** | 4G LTE，自动重连 | ❌ 固定 |
| **数据上报** | HTTP/HTTPS，JSON 格式 | ✅ 数据格式 |
| **上报频率** | 可配置 (默认 60 秒) | ✅ 完全可配 |
| **平台地址** | 可配置客户平台 | ✅ 完全可配 |
| **OTA 升级** | 远程固件升级 | ✅ 可定制 |
| **看门狗** | 硬件保护 | ❌ 固定 |
| **LED 指示** | 网络/通信状态 | ✅ 引脚可配 |

---

## 🔧 可定制内容

### 必须定制

| 参数 | 位置 | 说明 |
|------|------|------|
| `URL_REPORT` | config.py | 客户数据接收平台地址 |
| `URL_OTA` | config.py | OTA 升级服务器地址 |
| `PROJECT_NAME` | config.py | 项目名称 |
| `PROJECT_VERSION` | config.py | 项目版本号 |
| `REPORT_INTERVAL_SEC` | config.py | 数据上报频率 (秒) |

### 按需定制

| 参数 | 位置 | 说明 |
|------|------|------|
| `MODBUS_BAUDRATE` | config.py | Modbus 波特率 |
| `SENSOR_MAX_COUNT` | config.py | 传感器数量 |
| `LED_NET_PIN` | config.py | LED 引脚 |
| 数据格式 | data_reporter.py | JSON 字段结构 |
| 传感器协议 | sensor_device.py | 状态码解析 |

---

## 📁 项目结构

```
your-project/
├── config/
│   ├── __init__.py
│   └── config.py          ⚙️ 核心配置 (必须修改)
├── src/
│   ├── main.py            🚀 主程序
│   ├── led_control.py     💡 LED 控制
│   ├── modbus_rtu.py      🔌 Modbus 协议
│   ├── sensor_device.py   📡 传感器管理 (按需改)
│   ├── network_manager.py 🌐 网络管理
│   ├── system_manager.py  🖥️ 系统管理
│   └── data_reporter.py   📤 数据上报 (按需改)
└── docs/
    ├── README.md          📖 项目说明
    ├── 部署指南.md         📦 部署步骤
    ├── 配置说明.md         ⚙️ 配置参数
    └── 调试指南.md         🔧 调试方法
```

---

## 💡 使用示例

### 示例 1: 气体监测设备

```python
# config/config.py
PROJECT_NAME = "gas-monitor-beijing"
PROJECT_VERSION = "1.0.0"
URL_REPORT = "https://gas-platform.com/api/data"
REPORT_INTERVAL_SEC = 60  # 1 分钟上报一次
MODBUS_BAUDRATE = 9600
SENSOR_MAX_COUNT = 8      # 8 个气体探头
```

### 示例 2: 温湿度监测

```python
# config/config.py
PROJECT_NAME = "temp-humidity-warehouse"
URL_REPORT = "https://warehouse-iot.com/api/temp"
REPORT_INTERVAL_SEC = 300  # 5 分钟上报一次
SENSOR_MAX_COUNT = 16      # 16 个温湿度传感器
```

### 示例 3: 水质监测

```python
# config/config.py
PROJECT_NAME = "water-quality-river"
URL_REPORT = "https://epb.gov.cn/api/water"
REPORT_INTERVAL_SEC = 900  # 15 分钟上报一次
# 需要修改 sensor_device.py 中的协议解析
```

---

## 🛠️ 开发流程

```
1. 激活技能
   ↓
2. 创建项目 (自动复制模板)
   ↓
3. 修改 config.py (必须)
   - URL_REPORT
   - PROJECT_NAME
   - REPORT_INTERVAL_SEC
   ↓
4. 修改传感器协议 (如需要)
   - sensor_device.py
   ↓
5. 修改数据格式 (如需要)
   - data_reporter.py
   ↓
6. 部署到设备
   ↓
7. 联调测试
```

---

## 📊 上报数据格式

### 默认格式

```json
{
  "id": 1711600000,
  "time": "2026-03-28 09:00:00",
  "unit_code": "863950067267346",
  "sys_stat": { /* 系统状态 */ },
  "sensor_stat": [ /* 传感器状态 */ ],
  "sensor_dens": [ /* 传感器浓度 */ ],
  "collections": { /* 网络信息 */ }
}
```

### 自定义格式

在 `data_reporter.py` 中修改 `report_sensor_data()` 方法。

---

## 🔍 调试支持

技能提供完整的调试支持：

1. **调试开关** - 在 config.py 中启用
2. **日志输出** - 详细的运行日志
3. **交互式调试** - 支持 REPL 测试
4. **故障排查** - 文档中有详细指南

---

## 📞 技术支持

- **技能作者**: 天津安信华瑞科技有限公司
- **联系电话**: 18513099902
- **适用硬件**: 移远 EC200U/EC600N 等 QuecPython 模组

---

## 📝 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-03-28 | 初始版本 |

---

## ⚖️ 许可证

Copyright © 2026 天津安信华瑞科技有限公司

---

*使用此技能，你可以快速定制自己的 IoT 设备，无需从零开始开发。*
