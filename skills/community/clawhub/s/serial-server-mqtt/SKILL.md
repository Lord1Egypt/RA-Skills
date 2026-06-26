---
name: sp501lw-mqtt
description: SP501LW 串口网关纯 MQTT 管理技能——支持串口透传和 Modbus RTU 数据采集两种工作模式，通过 MQTT 完全控制设备，支持自定义主题和 Broker。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [python3]
    install:
      - kind: pip
        package: paho-mqtt
        bins: []
    emoji: "🔌"
    homepage: https://github.com/likong-iot/sp501lw-mqtt-skill
    skillKey: sp501lw-mqtt
    always: false
---

# SP501LW 串口网关纯 MQTT 管理技能

通过 MQTT 协议完全控制立控 SP501LW 串口网关（网络-串口桥接网关）。支持：
- **串口透传模式**（mqtt_tcp）：AI 当作虚拟串口使用
- **数据采集模式**（modbus_rtu）：AI 当作 Modbus RTU 数据采集器

## 核心概念（必读）

## 当前实现状态（v1.0.0）

`sp501lw_mqtt.py` 当前**已实现**命令（可直接使用）：

- `add`
- `list`
- `remove`
- `update`
- `set-mode`
- `send`
- `listen`
- `set-poll-time`
- `set-serial`
- `add-modbus`
- `edit-modbus`
- `remove-modbus`

以下命令在本文档中属于**规划能力**，当前脚本尚未实现：

- `receive`
- `enable-modbus` / `disable-modbus`
- `import-modbus` / `export-modbus`
- `set-mqtt` / `set-network` / `scan-wifi`
- `ota` / `ota-progress` / `restart` / `reset`
- `info` / `sys` / `mode-info` / `mqtt-info` / `net-info` / `serial-info`

### 1. 设备标识（--id）

`--id` 是设备的**逻辑标识符**，可以是：
- 设备 MAC 地址
- 用户自定义的名称（如 "生产线网关"）
- 任何字符串标识

**重要**：`--id` 不绑定到具体的 MAC 地址或主题，用户可以随时修改主题配置，`--id` 仍然有效。

### 2. MQTT 主题概念

根据 mqtt.md，设备有两个重要主题：

| 名称 | 功能 | 方向 | mqtt.md 对应 |
|------|------|------|-------------|
| **cmd-topic** | 命令主题 | ↓ 下行（AI→设备） | mqtt_pub_topic |
| **data-topic** | 数据主题 | ↑ 上行（设备→AI） | mqtt_sub_topic |

**注意**：mqtt.md 的 pub/sub 是从设备角度命名的，这里使用功能角度的命名，更直观：
- `--cmd-topic`：我们**发送命令**的主题
- `--data-topic`：我们**接收数据**的主题

### 3. 三个工作模式

| 模式 | 说明 | AI 角色 | 用途 |
|------|------|--------|------|
| **mqtt_tcp** | 原始数据透传 | 虚拟串口 | 实时控制连接到设备的串口设备 |
| **modbus_tcp** | Modbus TCP 代理 | 虚拟串口 + 代理 | 通过设备控制 Modbus TCP 从站 |
| **modbus_rtu** | Modbus RTU 自动轮询 | 数据采集器 | 设备自动周期性采集 Modbus 从站数据 |

### 4. `poll_time` 与 `interval_time` 不是一回事（重点）

在 `modbus_rtu` 模式中，这两个参数经常被混淆，请务必区分：

| 参数 | 配置命令 | 作用层级 | 含义 |
|------|----------|----------|------|
| `poll_time` | `set-poll-time` | **网关级** | 整个 Modbus 轮询任务的一轮周期（毫秒） |
| `interval_time` | `add-modbus` / `edit-modbus` 的 `--interval` | **条目级** | 某一条 Modbus 命令自己的间隔（毫秒） |

关键点：
- `set-poll-time` 改的是网关全局轮询周期，不会替代每条 `modbus_items[].interval_time`。
- `--interval` 改的是条目自身节奏，不会自动修改全局 `poll_time`。
- 固件会校验并可能自动上调 `poll_time`（例如小于最小可执行时间时会被抬高），因此最终生效值以设备运行结果为准。

---

## 设备本地记录格式

设备信息存储在 `devices.json`：

```json
{
  "我的网关": {
    "id": "a1b2c3d4e5f6",
    "cmd_topic": "/public/a1b2c3d4e5f6/publish",
    "data_topic": "/public/a1b2c3d4e5f6/subscribe",
    "broker_host": "mqtt.likong-iot.com",
    "broker_port": 1883,
    "broker_username": "public",
    "broker_password": "Aa123456",
    "last_seen": "2026-04-01T12:00:00"
  }
}
```

---

## ⚠️ 重要：重启与配置分离

### 哪些操作会导致设备重启？

以下操作会导致设备在 **5-30 秒内重启**，重启期间设备离线，**无法接收新指令**：

| 操作 | 说明 | 重启延迟 |
|------|------|--------|
| `set-mode` | 切换工作模式 | 设备重启 5-30 秒 |
| `set-poll-time` | 修改轮询周期 | 设备重启 5-30 秒 |
| `set-serial` | 修改串口参数 | 设备重启 5-30 秒 |
| `add-modbus` | 添加轮询项 | 设备重启 5-30 秒 |
| `edit-modbus` | 编辑轮询项 | 设备重启 5-30 秒 |
| `remove-modbus` | 删除轮询项 | 设备重启 5-30 秒 |

### 哪些操作不会重启？

以下操作**不会导致设备重启**，可以立即执行：

| 操作 | 说明 |
|------|------|
| `send` | 发送串口数据 |
| `listen` | 监听设备数据 |

### 正确的操作流程

```bash
# 第一步：执行配置操作（会重启）
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "我的网关"
# ← 返回：设备将在 5-30 秒内重启

# 第二步：等待设备重启完成（CRITICAL！）
sleep 30

# 第三步：执行普通操作（不会重启，可以立即执行）
python3 sp501lw_mqtt.py send --id "我的网关" --data "fffff" --format text

# 继续其他操作（无需等待）
python3 sp501lw_mqtt.py listen --id "我的网关"
```

---

## 命令参考（含规划）

> 注意：本节包含“已实现命令”和“规划命令”。请以“当前实现状态”章节为准。

### 1. 设备注册（第一次使用）

```bash
# 添加设备（注册到本地）
python3 sp501lw_mqtt.py add \
  --id "我的网关" \
  --cmd-topic "/public/a1b2c3d4e5f6/publish" \
  --data-topic "/public/a1b2c3d4e5f6/subscribe" \
  [--broker-host mqtt.likong-iot.com] \
  [--broker-port 1883] \
  [--username public] \
  [--password Aa123456]

# 列出已保存的设备
python3 sp501lw_mqtt.py list

# 删除设备
python3 sp501lw_mqtt.py remove --id "我的网关"

# 更新设备信息（修改主题或 Broker）
python3 sp501lw_mqtt.py update --id "我的网关" \
  --cmd-topic "/new/cmd/topic" \
  --data-topic "/new/data/topic"
```

### 2. 工作模式控制

```bash
# 切换到 mqtt_tcp 模式（原始串口透传）
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "我的网关"

# 切换到 modbus_tcp 模式（Modbus TCP 代理）
python3 sp501lw_mqtt.py set-mode modbus_tcp --id "我的网关"

# 切换到 modbus_rtu 模式（RTU 数据采集）
python3 sp501lw_mqtt.py set-mode modbus_rtu --id "我的网关"
# ← 设备自动重启，需等待 5-30 秒
```

### 3. 串口透传（mqtt_tcp/modbus_tcp 模式）

在这个模式下，**AI 当作虚拟串口使用设备**，就像直接操作串口一样。

```bash
# 发送串口数据（文本格式）
python3 sp501lw_mqtt.py send --id "我的网关" \
  --data "AT+RST" \
  --format text

# 发送串口数据（HEX 格式）
python3 sp501lw_mqtt.py send --id "我的网关" \
  --data "010301006400BD" \
  --format hex

# 实时监听（持续接收所有上报数据）
python3 sp501lw_mqtt.py listen --id "我的网关" \
  --timeout 120 \
  [--format text/hex]
  # Ctrl+C 停止监听
```

**实际使用示例**：

```bash
# 场景：通过 mqtt_tcp 模式读取连接到设备的 Modbus 从站寄存器

# 终端 1：启动监听
python3 sp501lw_mqtt.py listen --id "我的网关" --format hex
# 等待从站响应...

# 终端 2：发送 Modbus 读命令（Slave 1, 读寄存器 100-109）
python3 sp501lw_mqtt.py send --id "我的网关" \
  --data "010301006400BD" \
  --format hex

# 终端 1 会收到：
# [RX] 01 03 14 00 01 02 03 04 ...（从站响应）
```

### 4. 数据采集配置（modbus_rtu 模式）

在这个模式下，**AI 当作可配置的 Modbus RTU 数据采集器**，配置设备自动周期性采集数据。

```bash
# 设置全局轮询周期（单位毫秒）
python3 sp501lw_mqtt.py set-poll-time 30000 --id "我的网关"
  # 范围：1000-3600000 ms（1秒~1小时）
  # 修改后设备自动重启
  # 这是网关级 poll_time（整轮周期），不是条目 --interval
  # 设备会自动校验并可能上调该值

# 添加轮询项（配置一个数据采集任务）
python3 sp501lw_mqtt.py add-modbus --id "我的网关" \
  --slave-addr 1 \                    # Modbus 从站地址（1-247）
  --function-code 3 \                 # 功能码（1-6）
  --register-addr 0 \                 # 起始寄存器地址（0-65535）
  --register-num 2 \                  # 读取寄存器数量（1-125）
  --interval 5000 \                   # 这个项的 interval_time（条目级间隔，毫秒）
  --timeout 1000 \                    # 响应超时（毫秒）
  --data-format Float \               # 数据格式（HEX/Signed/Unsigned/Float/Long/Double）
  --report-format mqtt \              # 上报方式（mqtt/tcp/http）
  --baud-rate 9600 \                  # 串口波特率（300-921600）
  --data-bit 8 \                      # 数据位（5/6/7/8）
  --stop-bit 1 \                      # 停止位（1/1.5/2）
  --check-bit None                    # 校验位（None/Odd/Even）

# 编辑轮询项（修改已有项的参数）
python3 sp501lw_mqtt.py edit-modbus --id "我的网关" \
  --index 0 \
  --interval 3000 \
  --data-format Float

# 删除轮询项（移除一个采集任务）
python3 sp501lw_mqtt.py remove-modbus --id "我的网关" --index 0

# 启用/禁用轮询项（暂停或恢复采集，不删除配置）
python3 sp501lw_mqtt.py enable-modbus --id "我的网关" --index 0
python3 sp501lw_mqtt.py disable-modbus --id "我的网关" --index 0

# 导入轮询配置（从 JSON 文件批量导入）
python3 sp501lw_mqtt.py import-modbus --id "我的网关" --file config.json

# 导出轮询配置（当前配置备份到 JSON 文件）
python3 sp501lw_mqtt.py export-modbus --id "我的网关" --file backup.json
```

### 5. 设备端 MQTT 配置（规划，当前脚本未实现）

配置设备**内部**连接的 MQTT Broker 参数：

```bash
# 配置 MQTT Broker 参数
python3 sp501lw_mqtt.py set-mqtt --id "我的网关" \
  --server mqtt.example.com \
  --port 1883 \
  --username admin \
  --password pass123 \
  --qos 1 \
  --retain 0 \
  [--enable 1]
  # 修改后设备自动重启
```

### 6. 设备端串口配置（已实现）

配置设备**串口**的参数：

```bash
# 配置串口参数
python3 sp501lw_mqtt.py set-serial --id "我的网关" \
  --baud-rate 9600 \
  --data-bit 8 \
  --stop-bit 1 \
  --check-bit None \
  [--frame-len 512] \
  [--frame-time 50]
  # 修改后设备自动重启
```

### 7. 设备端网络配置（规划，当前脚本未实现）

配置设备的**网络连接**（WiFi 或以太网）：

```bash
# 配置 WiFi
python3 sp501lw_mqtt.py set-network --id "我的网关" \
  --mode wifi \
  --ssid "MyWiFi" \
  --password "password123"

# 配置以太网（DHCP）
python3 sp501lw_mqtt.py set-network --id "我的网关" \
  --mode ethernet \
  --dhcp 1

# 配置以太网（静态 IP）
python3 sp501lw_mqtt.py set-network --id "我的网关" \
  --mode ethernet \
  --dhcp 0 \
  --static-ip 192.168.1.100 \
  --static-netmask 255.255.255.0 \
  --static-gateway 192.168.1.1 \
  --static-dns1 8.8.8.8 \
  --static-dns2 8.8.4.4

# 扫描附近的 WiFi 网络
python3 sp501lw_mqtt.py scan-wifi --id "我的网关"
```

### 8. OTA 固件升级（规划，当前脚本未实现）

```bash
# 升级设备固件
python3 sp501lw_mqtt.py ota --id "我的网关" \
  --url "http://10.0.0.50/sp501lw_v2.0.0.bin"

# 查询 OTA 进度（0-100）
python3 sp501lw_mqtt.py ota-progress --id "我的网关"

# 设备重启（配置修改需要重启才能生效）
python3 sp501lw_mqtt.py restart --id "我的网关"

# 恢复出厂设置（⚠️ 需确认，所有配置将被清除）
python3 sp501lw_mqtt.py reset --id "我的网关"
```

### 9. 信息查询（规划，当前脚本未实现）

```bash
# 查询工作模式和 Modbus 项统计
python3 sp501lw_mqtt.py mode-info --id "我的网关"
# 返回：当前工作模式、轮询周期、Modbus 项总数等

# 查询设备 MQTT 配置和连接状态
python3 sp501lw_mqtt.py mqtt-info --id "我的网关"
# 返回：Broker 地址、端口、用户名、QoS、连接状态等

# 查询设备网络信息
python3 sp501lw_mqtt.py net-info --id "我的网关"
# 返回：IP 地址、网关、DNS、DHCP 状态、连接方式等

# 查询设备串口配置
python3 sp501lw_mqtt.py serial-info --id "我的网关"
# 返回：波特率、数据位、停止位、校验位等

# 查询设备基本信息
python3 sp501lw_mqtt.py info --id "我的网关"
# 返回：MAC 地址、IP、固件版本、运行时间等

# 查询系统信息
python3 sp501lw_mqtt.py sys --id "我的网关"
# 返回：内存、堆状态、NVS 使用率等
```

---

## 典型使用场景

### 场景 A：mqtt_tcp 模式 - AI 控制串口设备

```bash
# 第一次使用：注册设备
python3 sp501lw_mqtt.py add \
  --id "测试设备" \
  --cmd-topic "/public/a1b2c3d4e5f6/publish" \
  --data-topic "/public/a1b2c3d4e5f6/subscribe"

# 确保在 mqtt_tcp 模式
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "测试设备"

# 使用设备（就像使用串口一样）

# 终端 1：启动监听，等待数据
python3 sp501lw_mqtt.py listen --id "测试设备" --format hex

# 终端 2：发送 Modbus 读寄存器命令
python3 sp501lw_mqtt.py send --id "测试设备" \
  --data "010301006400BD" \
  --format hex

# 终端 1 收到：
# [RX] 01 03 14 00 01 02 03 04 ...（从站响应）
```

### 场景 B：modbus_rtu 模式 - AI 配置数据采集器

```bash
# 切换到采集模式
python3 sp501lw_mqtt.py set-mode modbus_rtu --id "测试设备"
sleep 20  # 等待重启

# 设置轮询周期（全局）
python3 sp501lw_mqtt.py set-poll-time 60000 --id "测试设备"
sleep 15  # 等待重启
  # 注意：这里只改全局 poll_time，不会改每个条目的 --interval

# 配置采集任务 1：从站 1，读温度（寄存器 0-1，Float 格式）
python3 sp501lw_mqtt.py add-modbus --id "测试设备" \
  --slave-addr 1 \
  --function-code 3 \
  --register-addr 0 \
  --register-num 2 \
  --interval 5000 \
  --timeout 1000 \
  --data-format Float

# 配置采集任务 2：从站 2，读压力（寄存器 0-1，Unsigned 格式）
python3 sp501lw_mqtt.py add-modbus --id "测试设备" \
  --slave-addr 2 \
  --function-code 3 \
  --register-addr 0 \
  --register-num 2 \
  --interval 10000 \
  --timeout 1000 \
  --data-format Unsigned

# 查看配置
python3 sp501lw_mqtt.py mode-info --id "测试设备"

# 监听采集数据（会定期收到采集结果）
python3 sp501lw_mqtt.py listen --id "测试设备" --format json
```

### 场景 C：使用自定义 Broker 和主题

```bash
# 注册设备到自定义 Broker 和主题
python3 sp501lw_mqtt.py add \
  --id "公司网关" \
  --cmd-topic "/mycompany/devices/gateway/cmd" \
  --data-topic "/mycompany/devices/gateway/data" \
  --broker-host mqtt.mycompany.com \
  --broker-port 8883 \
  --username company_user \
  --password company_pass

# 后续所有操作都会使用这个配置
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "公司网关"
python3 sp501lw_mqtt.py listen --id "公司网关"
```

### 场景 D：备份和恢复配置

```bash
# 备份当前的 Modbus 轮询配置
python3 sp501lw_mqtt.py export-modbus --id "测试设备" \
  --file modbus_backup_$(date +%Y%m%d_%H%M%S).json

# 在新设备上恢复配置
python3 sp501lw_mqtt.py import-modbus --id "新设备" \
  --file modbus_backup_20260401_120000.json
```

---

## 错误处理和常见问题

### 问题 1：MQTT 连接失败

**表现**：命令返回 "无法连接 MQTT Broker"

**解决**：
1. 检查 Broker 地址是否正确
2. 检查网络连接
3. 检查用户名/密码是否正确
4. 尝试更新设备信息：
   ```bash
   python3 sp501lw_mqtt.py update --id <ID> \
     --broker-host <新地址> \
     --username <用户名> \
     --password <密码>
   ```

### 问题 2：命令超时

**表现**：命令等待响应超过指定时间

**可能原因**：
- 设备离线
- 网络延迟较大
- 下发的命令格式不正确

**解决**：
1. 检查设备是否在线
2. 增加超时时间：`--timeout 10`
3. 检查命令格式是否正确

### 问题 3：Modbus 轮询不工作

**表现**：modbus_rtu 模式下没有收到采集数据

**可能原因**：
- 从站地址或功能码错误
- 串口波特率不匹配
- 混淆了 `poll_time`（全局）和 `--interval`（条目）
- `poll_time` 被设备自动抬高后，实际节奏与预期不一致

**解决**：
1. 检查从站地址（1-247）
2. 检查功能码（通常 3 = 读保持寄存器）
3. 检查串口参数：`python3 sp501lw_mqtt.py serial-info --id <ID>`
4. 分别检查两个参数：全局 `set-poll-time` 与条目 `--interval`
5. 用 mqtt_tcp 模式手动测试：
   ```bash
   python3 sp501lw_mqtt.py send --id <ID> \
     --data "010301006400BD" \
     --format hex
   ```

---

## 安装和设置

### 1. 安装

```bash
# 方法 1：通过 ClawHub
npx clawhub@latest install sp501lw-mqtt

# 方法 2：手动安装
pip3 install paho-mqtt>=2.0.0
```

### 2. 获取帮助

```bash
# 查看所有命令
python3 sp501lw_mqtt.py --help

# 查看特定命令的帮助
python3 sp501lw_mqtt.py add --help
python3 sp501lw_mqtt.py set-mode --help
```

---

## 关键术语表

| 术语 | 说明 |
|------|------|
| **id** | 设备标识（用户定义，不绑定 MAC） |
| **cmd-topic** | 命令主题（我们发送命令的地方）= mqtt_pub_topic |
| **data-topic** | 数据主题（我们接收数据的地方）= mqtt_sub_topic |
| **mqtt_tcp** | 原始串口透传模式，AI 当作虚拟串口 |
| **modbus_tcp** | Modbus TCP 代理模式 |
| **modbus_rtu** | Modbus RTU 采集器模式，AI 当作数据采集器 |
| **poll-time** | 网关级轮询周期（整轮周期，毫秒） |
| **interval-time** | 条目级命令间隔（`modbus_items[].interval_time`，毫秒） |
| **slave-addr** | Modbus 从站地址（1-247） |
| **function-code** | Modbus 功能码（1-6） |
| **data-format** | 数据格式（HEX/Signed/Unsigned/Float/Long/Double） |

---

## 协议文档参考

- MQTT 消息格式：遵循 mqtt.md
- Modbus 协议：标准 Modbus RTU 协议
- 配置识别：`{"action":"config","data":{...}}`
- 响应 ACK：`{"code":200,"msg":"config updated"}`

---

## 许可证和支持

MIT License

如有问题，请提交 Issue 或联系技术支持。
