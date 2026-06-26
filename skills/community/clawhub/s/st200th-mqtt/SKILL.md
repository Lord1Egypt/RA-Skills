---
name: st200th-mqtt
description: 立控 ST200TH 温湿度变送器全功能管理技能——查询温湿度/气压/海拔、查看设备信息(IP/型号/固件)、修改配置、补偿校准、重启设备、OTA升级。支持多设备管理，首次使用记住 MAC 后续免输入。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [python3]
    install:
      - kind: uv
        package: paho-mqtt
        bins: []
    emoji: "🌡️"
    homepage: https://docv2.likong-iot.com/products/transmitters/ST200TH/mqtt
    skillKey: st200th
    always: false
---

# ST200TH 温湿度变送器全功能管理

通过 MQTT 协议管理立控（LIKONG）ST200TH 系列温湿度变送器。支持查询传感器数据、查看/修改设备配置、补偿校准、重启、恢复出厂、OTA升级等全部功能。

协议文档：https://docv2.likong-iot.com/products/transmitters/ST200TH/mqtt

## 核心规则

1. **必须有设备 MAC 地址。** 首次使用时询问用户并用 `add` 保存，后续自动使用。
2. **每次收到用户请求时先 `list`**，有设备则直接操作，无设备则引导添加。
3. **多设备时**根据用户意图选择：指定名称/MAC → `--mac`；全部 → `--all`；不明确 → 列出让用户选。
4. **危险操作**（reset 恢复出厂、ota 升级）必须先让用户确认。
5. **回复精炼**，用户问温湿度就只答温湿度，追问时再补充其他。

## 脚本路径

```
{{SKILL_DIR}}/st200th_mqtt.py
```

---

## 完整命令参考

### 1. 查询传感器数据与系统信息 — `query`

查询温度、湿度、气压、海拔，以及设备IP、型号、固件版本、运行时间、MAC地址、网络连接方式、协议启用状态等。

```bash
# 单设备（已保存仅一个时自动选择）
python3 {{SKILL_DIR}}/st200th_mqtt.py query

# 指定设备
python3 {{SKILL_DIR}}/st200th_mqtt.py query --mac <MAC>

# 查询所有已保存设备
python3 {{SKILL_DIR}}/st200th_mqtt.py query --all

# JSON 输出（适合程序解析）
python3 {{SKILL_DIR}}/st200th_mqtt.py query --json
python3 {{SKILL_DIR}}/st200th_mqtt.py query --all --json
```

**返回数据包含：**

| 分组 | 字段 | 含义 | 单位 |
|------|------|------|------|
| data | temperature | 温度 | °C |
| data | humidity | 湿度 | % |
| data | pressure | 大气压力 | hPa |
| data | altitude | 海拔高度 | m |
| sys | version | 固件版本（如 HW:1.0.0_SDK:2.0.0） | - |
| sys | runtime | 运行时间 | 秒 |
| sys | eth_mac | 以太网 MAC 地址 | - |
| sys | sta_mac | WiFi MAC 地址 | - |
| net | connmethed | 连接方式（eth=以太网, wifi=无线） | - |
| net | ip | 设备 IP 地址 | - |
| net | dhcp | DHCP 状态（1=启用, 0=静态） | - |
| net | ssid | WiFi SSID | - |
| type | - | 设备型号（如 ST200THPE） | - |
| protocol | mqtt/http/tcpserver/tcpclient | 各协议启用状态（1=启用） | - |
| compensate | t/h/p_compensate | 当前补偿值 | °C/%/hPa |
| set | mqtt/tcp/http_timed_report | 各协议定时上报状态 | - |
| set | mqtt/tcp/http_interval_time | 上报间隔 | 秒 |

**用户意图 → 回复策略：**

| 用户说 | 回复内容 |
|--------|----------|
| "查一下温湿度" | 温度 XX°C，湿度 XX% |
| "气压多少" | 气压 XX hPa |
| "海拔呢" | 海拔 XX m |
| "设备IP是什么" | IP 地址 XXX.XXX.XXX.XXX |
| "设备什么型号" | 型号 ST200THPE |
| "固件版本" | HW:1.0.0_SDK:2.0.0 |
| "设备运行多久了" | 运行时间 Xh Xm |
| "设备详细信息" | 输出全部字段 |

### 2. 查询设备配置 — `customize`

查看设备当前的 MQTT、TCP、HTTP 协议配置参数。

```bash
python3 {{SKILL_DIR}}/st200th_mqtt.py customize --mac <MAC>
python3 {{SKILL_DIR}}/st200th_mqtt.py customize --json
```

**返回数据包含：**

| 分组 | 字段 | 含义 |
|------|------|------|
| mqtt_info | enable, mqtt_server, mqtt_port, client_id, username, password, publish, subcribe, qos, retain, timed_report, interval_time | MQTT 完整配置 |
| tcp_info | enable, tcp_server, tcp_port, timed_report, interval_time | TCP 配置 |
| http_info | enable, http_uri, timed_report, interval_time | HTTP 配置 |
| compensate | t/h/p_compensate | 补偿参数 |

### 3. 设置传感器补偿 — `compensate`

校准传感器读数偏差。**立即生效，无响应返回。**

```bash
# 设置温度补偿 +2°C
python3 {{SKILL_DIR}}/st200th_mqtt.py compensate --mac <MAC> -t 2

# 设置湿度补偿 -5%
python3 {{SKILL_DIR}}/st200th_mqtt.py compensate --mac <MAC> -hu -5

# 设置气压补偿 +10hPa
python3 {{SKILL_DIR}}/st200th_mqtt.py compensate --mac <MAC> -p 10

# 同时设置多个
python3 {{SKILL_DIR}}/st200th_mqtt.py compensate --mac <MAC> -t 1.5 -hu -3 -p 20

# 对所有设备设置
python3 {{SKILL_DIR}}/st200th_mqtt.py compensate --all -t 2
```

**参数范围：**
- `-t`：温度补偿 -20 ~ +20 °C
- `-hu`：湿度补偿 -20 ~ +20 %
- `-p`：气压补偿 -500 ~ +500 hPa

### 4. 重启设备 — `restart`

**立即生效，无响应返回。** 修改协议配置（custom）后需重启才生效。

```bash
python3 {{SKILL_DIR}}/st200th_mqtt.py restart --mac <MAC>
```

### 5. 恢复出厂设置 — `reset`

**立即生效，无响应返回。⚠️ 危险操作，必须让用户确认！**

```bash
python3 {{SKILL_DIR}}/st200th_mqtt.py reset --mac <MAC>
```

执行前应提示用户：
> 恢复出厂设置将清除所有配置（包括 MQTT/TCP/HTTP 设置），确定要继续吗？

### 6. OTA 固件升级 — `ota`

**立即生效，无响应返回。⚠️ 需用户确认！**

```bash
python3 {{SKILL_DIR}}/st200th_mqtt.py ota --mac <MAC> --uri "http://10.0.0.50/likong-iot/module_v1.bin"
```

**限制：**
- URI 仅支持 HTTP（不支持 HTTPS）
- URI 最长 128 字符

### 7. 修改设备协议配置 — `custom`

修改 MQTT/TCP/HTTP 协议参数。**重启后生效。**

```bash
# 修改 MQTT 配置
python3 {{SKILL_DIR}}/st200th_mqtt.py custom --mac <MAC> --protocol mqtt \
  --server "mqtt.example.com" --port 1883 \
  --client-id "mydevice" --username "user" --password "pass" \
  --publish-topic "/my/publish" --subscribe-topic "/my/subscribe" \
  --qos 1 --timed-report 1 --interval 10

# 修改 TCP 配置
python3 {{SKILL_DIR}}/st200th_mqtt.py custom --mac <MAC> --protocol tcp \
  --enable 1 --server "tcp.example.com" --port 8888 \
  --timed-report 1 --interval 5

# 修改 HTTP 配置
python3 {{SKILL_DIR}}/st200th_mqtt.py custom --mac <MAC> --protocol http \
  --enable 1 --http-uri "http://api.example.com" \
  --timed-report 1 --interval 5

# 启用/禁用协议
python3 {{SKILL_DIR}}/st200th_mqtt.py custom --mac <MAC> --protocol tcp --enable 0
```

**注意事项：**
- 修改后需执行 `restart` 才能生效
- HTTP URI 最长 32 字符，不支持 HTTPS
- 定时上报间隔建议 ≥5 秒，最低 2 秒
- client_id、publish、subcribe 不能与其他设备重复

---

## 设备列表管理

```bash
# 添加设备（首次使用）
python3 {{SKILL_DIR}}/st200th_mqtt.py add <MAC> --name "办公室"

# 列出已保存设备
python3 {{SKILL_DIR}}/st200th_mqtt.py list

# 删除设备
python3 {{SKILL_DIR}}/st200th_mqtt.py remove <MAC>
```

---

## 首次使用流程

```
用户: "查一下温湿度"
  ↓
Agent: 执行 list → 无设备
  ↓
Agent: "首次使用，请提供设备的 WiFi MAC 地址（12位十六进制，如 ece334a7e044），
       可在设备管理页面「基本信息」中查看。也可以给设备起个名字，方便后续识别。"
  ↓
用户: "ece334a7e044，就叫办公室吧"
  ↓
Agent: 执行 add ece334a7e044 --name "办公室"
       执行 query
  ↓
Agent: "当前办公室温度 26.9°C，湿度 49.8%。"
```

---

## 错误处理

| 错误 | 原因 | 建议 |
|------|------|------|
| 查询超时 | 设备离线或 MAC 错误 | 确认设备已上电、MAC 正确 |
| MAC 地址格式无效 | 非12位十六进制 | 检查 MAC 格式 |
| 缺少依赖 paho-mqtt | Python 库未安装 | `pip3 install paho-mqtt` |
| MQTT 连接失败 | 网络或凭据问题 | 检查网络连接 |
| 补偿超出范围 | 参数超限 | 温度±20、湿度±20、气压±500 |
| URI 长度超限 | OTA URI > 128字符 | 缩短 URI |
| 存在多个设备 | 未指定 MAC | 使用 --mac 或 --all |
