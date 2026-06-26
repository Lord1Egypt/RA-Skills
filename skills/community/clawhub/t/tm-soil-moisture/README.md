# 🌱 文冠果智慧农业助手 (AgriBrain Skill)

> **版本**: 1.0.0
> **适配平台**: ClawHub / PicoClaw / MCP Client
> **核心功能**: 本地化农业多层传感器数据解析、区域墒情聚合分析与智能灌溉决策支持。

## 📖 项目简介

TM Soil Moisture Skill 是一个专为**文冠果 (Shiny-leaved yellowhorn)** 种植设计的智慧农业 MCP 技能插件。它通过读取本地 SQLite 数据库中由底层传感器上报的 JSON 数据，实时解析地下 10cm-100cm 的多层土壤温度、湿度信息，并结合地理位置与模拟气象预测，提供科学的灌溉决策。

本插件完全基于**本地化运行**，无需依赖云端 API（除气象补充数据外），确保农业核心数据的绝对隐私与极低延迟。

## 🚀 核心能力

1. **多层土壤剖面解析**: 自动解析包含 `Soil_Temp10`~`100` 和 `Soil_Humi10`~`100` 的复杂 JSON 负载，自动提取设备电量和定位信息，构建 3D 墒情剖面。
2. **全域墒情聚合 (`calculate_depth_average`)**: 动态提取所有在线设备最新数据，计算特定土层深度的全域平均温湿度。
3. **智能决策引擎 (`check_irrigation_advice`)**: 聚焦文冠果核心根系层 (20-40cm)，结合干旱阈值（<15% 重度，<25% 中度）与模拟降水概率，输出“立即灌溉”、“适量补水”或“暂缓灌溉”指令。
4. **设备健康监测**: 实时追踪设备电量 (`power`) 与信号强度 (`GPRS_RSSI`)。

## 🛠️ 技术架构与数据字典

### 运行环境
- **语言**: Python 3.8+
- **依赖库**: `sqlite3`, `mcp` (仅当通过 MCP Server / ClawHub 加载时需安装)
- **数据库路径**: 默认 `/usr/apps/config/agri.db` (可通过代码常量修改)

### 传感器 JSON 负载字典
数据库表 `device_data` 的 `data` 字段（兼容 `type` 字段容错机制）存储以下格式的 JSON 数据：

| 字段名 | 描述 | 示例值 |
|---|---|---|
| `gprs_ccid` | 设备的唯一识别序列号 (SN) | `89860812192320386208` |
| `Soil_Temp[N]` | N厘米深度的土壤温度 (℃) | `"Soil_Temp40": 6.25` |
| `Soil_Humi[N]` | N厘米深度的土壤体积含水率 (%) | `"Soil_Humi40": 27.86` |
| `Soil_FH_C[N]` | N厘米深度土壤电导率/频率 | `"Soil_FH_C40": 140661760` |
| `power` | 电池电压 (V)，正常>3.6V | `"power": 4.133` |
| `GPRS_RSSI` | GPRS 信号强度 | `"GPRS_RSSI": 31` |
| `geo` | 经纬度定位对象 | `{"lon": "106.19", "lat": "34.65"}` |

---

## 💻 安装与使用指南

### 1. 独立命令行测试 (CLI Mode)
无需启动完整的 MCP 服务器，你可以通过命令行直接验证核心逻辑：

```bash
# 查询指定设备最新剖面数据
python pico_claw_brain.py --query 89860812192320386208

# 统计农场 50cm 深度均值
python pico_claw_brain.py --avg 50

# 获取特定地块灌溉建议
python pico_claw_brain.py --advice 89860812192320386208
```

### 2. 作为 MCP 插件运行 (ClawHub / 宿主模式)
在支持 MCP (Model Context Protocol) 的宿主环境（如 ClawHub, Trae, Cursor 等）中，可以直接将此脚本作为 Server 启动，以暴露标准 Tool：

```bash
# 首先确保安装了 mcp 包
pip install mcp

# 启动 MCP 服务，供大语言模型调用
python pico_claw_brain.py --mcp
```
宿主加载后将自动注册以下 3 个工具：
- `query_device_data_tool(sn)`
- `calculate_depth_average_tool(depth)`
- `check_irrigation_advice_tool(sn)`
