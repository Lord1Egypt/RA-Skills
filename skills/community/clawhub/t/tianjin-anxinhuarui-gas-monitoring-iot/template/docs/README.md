# 拓安气体监测设备 - 嵌入式软件

## 项目概述

天津安信华瑞科技有限公司的拓安气体监测设备嵌入式软件，基于移远 QuecPython 平台开发。

### 功能特性

- ✅ Modbus RTU 传感器数据采集
- ✅ 4G 网络数据传输
- ✅ 云平台数据上报
- ✅ OTA 远程升级
- ✅ 看门狗保护
- ✅ LED 状态指示
- ✅ 断线重连
- ✅ 错误重试机制

---

## 目录结构

```
tuoan-gas-project/
├── config/                  # 配置文件目录
│   ├── __init__.py         # 配置包初始化
│   └── config.py           # 主配置文件
├── src/                     # 源代码目录
│   ├── main.py             # 主程序入口
│   ├── led_control.py      # LED 控制模块
│   ├── modbus_rtu.py       # Modbus 通信模块
│   ├── sensor_device.py    # 传感器管理模块
│   ├── network_manager.py  # 网络管理模块
│   ├── system_manager.py   # 系统管理模块
│   └── data_reporter.py    # 数据上报模块
├── docs/                    # 文档目录
│   ├── README.md           # 项目说明 (本文件)
│   ├── 部署指南.md          # 部署说明
│   ├── 配置说明.md          # 配置参数说明
│   └── 调试指南.md          # 调试方法
└── README.md               # 项目总览
```

---

## 快速开始

### 1. 配置参数

编辑 `config/config.py` 文件，修改以下必要参数：

```python
# Modbus 配置
MODBUS_UART = 2              # UART 端口
MODBUS_BAUDRATE = 9600       # 波特率

# 上报平台
URL_REPORT = "https://iot.tranthing.com/..."  # 数据上报地址
URL_OTA = "https://..."                       # OTA 升级地址

# 设备信息
PROJECT_NAME = "tuoan_demo_shenzhen"
PROJECT_VERSION = "2026.3.26 tuoan-dingzhi"
```

### 2. 部署到设备

将所有 `.py` 文件复制到 QuecPython 设备的 `/usr` 目录：

```
/usr/
├── config.py               # 从 config/config.py 复制
├── main.py                 # 主程序
├── led_control.py
├── modbus_rtu.py
├── sensor_device.py
├── network_manager.py
├── system_manager.py
└── data_reporter.py
```

### 3. 运行程序

设备上电自动运行，或手动执行：

```python
import main
main.main()
```

---

## 模块说明

### 核心模块

| 模块 | 功能 | 说明 |
|------|------|------|
| `main.py` | 主程序 | 系统初始化、主循环调度 |
| `config.py` | 配置 | 所有参数集中管理 |
| `modbus_rtu.py` | 通信 | Modbus RTU 协议实现 |
| `sensor_device.py` | 传感器 | 传感器扫描、数据读取 |

### 辅助模块

| 模块 | 功能 |
|------|------|
| `led_control.py` | LED 指示灯控制 |
| `network_manager.py` | 4G 网络连接管理 |
| `system_manager.py` | 看门狗、电源状态 |
| `data_reporter.py` | HTTP 上报、OTA |

---

## 技术规格

### 硬件要求

- 移远 QuecPython 模组 (EC200U/EC600N 等)
- GPIO36、GPIO44 用于 LED 指示
- UART2 用于 Modbus 通信

### 软件依赖

- QuecPython 运行时
- 内置模块：`machine`, `utime`, `ujson`, `request`, `net`, `sim`, `modem`

### 通信协议

- **Modbus RTU**: RS485 接口，9600 波特率
- **HTTP/HTTPS**: JSON 格式数据上报
- **OTA**: 远程固件升级

---

## 数据格式

### 上报数据结构

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

## 状态码说明

### 传感器状态

| 值 | 含义 |
|----|------|
| 0 | 正常 |
| 2 | 低报警 |
| 3 | 高报警 |
| 4 | 传感器故障 |
| 7 | 通讯错误 |

### 设备主状态

| 值 | 含义 |
|----|------|
| 0x02 | 正常 |
| 0x08 | 无传感器 |
| 0x11 | 主电故障 |
| 0x12 | 备电故障 |
| 0x13 | 传感器故障 |
| 0x14 | 高报 |
| 0x15 | 低报 |

---

## 常见问题

### Q: Modbus 读取失败？
**A:** 检查波特率、UART 端口号、RS485 接线

### Q: 网络连不上？
**A:** 检查 SIM 卡、天线、信号强度

### Q: 数据不上报？
**A:** 检查 URL 是否正确，服务器是否可达

### Q: 设备频繁重启？
**A:** 检查看门狗是否按时喂狗，电源是否稳定

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2026.3.26 | 2026-03-28 | 重构版，模块化设计 |
| 2026.3.26 之前 | - | 原版 monolithic 代码 |

---

## 联系方式

- **厂商**: 天津安信华瑞科技有限公司
- **电话**: 18513099902

---

## 许可证

Copyright © 2026 天津安信华瑞科技有限公司
