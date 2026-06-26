---
name: ax100-gas-reporter
description: >
  This skill should be used when the user wants to generate, customize, or deploy
  QuecPython code for reading gas detector data from an Anxin Huarui AX100 series
  controller via Modbus RTU and reporting it to a customer's HTTP platform at a
  configurable interval. Trigger this skill whenever the user mentions AX100 气体控制器,
  Modbus 上报, QuecPython 数采, 气体探测 HTTP 上报, or asks to adapt the reporting
  code to a new platform URL or reporting frequency.
---

# AX100 气体探测控制器 HTTP 上报技能

## 技能用途

本技能基于安信华瑞 AX100 系列气体报警控制器 + 移远通信（Quectel）QuecPython 模组，
提供一套完整的「读取传感器数据 → 组包 → HTTP 上报」程序模板。

使用场景：
- 为新客户定制上报地址和上报频率
- 调整上报 JSON 格式以符合不同平台协议
- 修改 Modbus 寄存器地址以适配其他控制器型号
- 在已有基础上添加新的传感器类型或扩展字段

---

## 资源清单

- **`assets/template/`** — 完整可运行的 QuecPython 代码模板（5个文件）
- **`references/code_guide.md`** — 各文件职责、所有配置项含义、JSON 格式说明、状态码表

---

## 工作流程

### 第一步：了解定制需求

在开始写代码前，向用户确认以下关键信息（未提供的项不要假设）：

1. **上报 URL** — 客户平台接收数据的 HTTP 接口地址（必须）
2. **上报频率** — 多少分钟上报一次（默认 3 分钟）
3. **设备标识** — 厂商名称、终端型号（可选，若不改则保留模板默认值）
4. **JSON 格式** — 客户平台是否有自己的协议格式？若有，需要用户提供字段说明
5. **寄存器地址** — 控制器型号是否标准 AX100？若是非标，需要用户提供寄存器地址表
6. **OTA 地址** — 是否需要 OTA 升级功能？若不需要，将 `URL_OTA` 设为空字符串

### 第二步：读取参考文档

读取 `references/code_guide.md`，了解：
- 所有 `config.py` 配置项的含义和默认值
- `build_payload()` 组装的 JSON 结构
- 状态码映射表

### 第三步：生成定制代码

以 `assets/template/` 中的 5 个文件为基础进行定制：

#### 只修改 config.py 的场景（最常见）
直接输出修改后的 `config.py`，其余4个文件照搬模板。

需要修改的典型字段：
```python
URL_CLIENT        = "https://客户平台地址/接口路径"   # 必改
URL_OTA           = ""                                # 不需要OTA则留空
REPORT_CYCLE_MIN  = 5    # 按客户约定的频率（分钟）
MANUFACTURER      = "xxx公司"
TERMINAL_TYPE     = "型号"
FW_VERSION        = "版本号"
```

#### 需要修改 JSON 格式的场景
修改 `main.py` 中的 `build_payload()` 函数，按客户平台协议重新组装字典。
保持其他函数（`check_network`, `http_post`, `check_ota`, `init`, `loop`）不变。

#### 需要修改寄存器地址的场景
只修改 `config.py` 中的 `REG_*` 常量，`sensor.py` 中所有地址均从 config 读取，无需改动。

### 第四步：输出交付物

向用户输出需要修改的文件（通常只有 `config.py`，其余不变的文件注明"使用模板原文"即可）。

同时提示用户：
- 将所有 `.py` 文件上传到模组 `/usr/` 目录（使用 QPYcom 工具）
- 确认 `main.py` 已在模组启动脚本中设为自动运行

---

## 常见定制示例

### 示例一：换上报地址 + 改频率
```
用户：上报地址改成 https://api.xxx.com/gas/upload，每5分钟上报一次
```
→ 只修改 `config.py`：
```python
URL_CLIENT       = "https://api.xxx.com/gas/upload"
REPORT_CYCLE_MIN = 5
```

### 示例二：客户平台要求不同的 JSON 格式
```
用户：客户平台要的格式是 {"imei":"...","sensors":[{"id":1,"val":0.0,"status":2}]}
```
→ 修改 `main.py` 中的 `build_payload()` 函数，按新格式重组字典。
→ `config.py` 中 URL 和周期照常配置。

### 示例三：控制器寄存器地址不同
```
用户：这个控制器探头状态起始地址是 0x0200，浓度起始地址是 0x0201
```
→ 只修改 `config.py`：
```python
REG_SENSOR_STAT_BASE = 0x0200
REG_SENSOR_DENS_BASE = 0x0201
```

---

## 代码部署说明（提示用户）

1. 工具：使用 QPYcom（移远官方 PC 工具）连接模组
2. 上传路径：所有 `.py` 文件 → 模组 `/usr/` 目录
3. 自动运行：在 QPYcom「文件」标签页中，将 `main.py` 设为 `auto run`
4. 日志查看：通过 QPYcom 串口终端查看 `print` 输出，定位问题

---

## 注意事项

- `config.py` 中 `WDT_TIMEOUT_SEC` 建议设为 `REPORT_CYCLE_MIN × 60 × 3`，留足余量
- `URL_OTA` 若为空字符串，需在 `check_ota()` 调用前加空值判断（已在模板中处理）
- 不同移远模组的 GPIO 引脚编号不同，`LED_NET_PIN` / `LED_BUS_PIN` 需对照硬件图纸确认
- Modbus 从机地址 `MODBUS_SLAVE` 默认为 1，若控制器地址不同需修改
