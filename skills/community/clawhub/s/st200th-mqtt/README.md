# ST200TH 温湿度变送器 Skill

用于 Claude Code / OpenClaw 等 AI Agent 的 IoT 技能包，通过 MQTT 协议全功能管理立控 ST200TH 温湿度变送器。

## 功能概览

| 功能 | 命令 | 说明 |
|------|------|------|
| 查询传感器数据 | `query` | 温度、湿度、气压、海拔 |
| 查询设备信息 | `query` | IP、型号、固件版本、运行时间、MAC |
| 查看设备配置 | `customize` | MQTT/TCP/HTTP 完整配置 |
| 修改协议配置 | `custom` | 修改 MQTT/TCP/HTTP 参数（重启生效） |
| 传感器补偿校准 | `compensate` | 温度/湿度/气压偏差补偿（立即生效） |
| 重启设备 | `restart` | 立即重启 |
| 恢复出厂设置 | `reset` | 清除所有配置 |
| OTA 固件升级 | `ota` | HTTP 远程升级 |
| 设备列表管理 | `add/remove/list` | 记住 MAC，后续免输入 |

## 安装

### 通过 ClawHub

```bash
npx clawhub@latest install st200th-mqtt
```

### 手动安装

```bash
pip3 install "paho-mqtt>=2.0.0"
```

## 快速上手

```bash
# 1. 添加设备
python3 st200th_mqtt.py add ece334a7e044 --name "办公室"

# 2. 查询温湿度
python3 st200th_mqtt.py query

# 3. 查看设备配置
python3 st200th_mqtt.py customize

# 4. 设置温度补偿 +2°C
python3 st200th_mqtt.py compensate -t 2

# 5. 修改 MQTT 定时上报间隔为 10 秒
python3 st200th_mqtt.py custom --protocol mqtt --timed-report 1 --interval 10

# 6. 重启设备使配置生效
python3 st200th_mqtt.py restart
```

## 命令详解

### 查询传感器数据

```bash
python3 st200th_mqtt.py query                    # 默认设备
python3 st200th_mqtt.py query --mac ece334a7e044  # 指定设备
python3 st200th_mqtt.py query --all               # 所有设备
python3 st200th_mqtt.py query --all --json        # JSON 输出
```

输出示例：
```
== 办公室 (ece334a7e044) ==
  设备型号: ST200THPE
[传感器数据]
  温度: 26.95 °C
  湿度: 49.78 %
  气压: 948.38 hPa
  海拔: 554.68 m
[网络信息]
  连接方式: 以太网
  IP 地址:  192.168.31.213
[系统信息]
  固件版本:  HW:1.0.0_SDK:2.0.0
  运行时间:  0h1m30s（90秒）
  以太网MAC: E8:6B:EA:C2:32:8F
  WiFi MAC:  E8:6B:EA:C2:32:8C
[协议状态]
  MQTT:       启用
  HTTP:       启用
  TCP Server: 未启用
  TCP Client: 未启用
```

### 传感器补偿

```bash
python3 st200th_mqtt.py compensate -t 2 -hu -5 -p 10  # 温度+2 湿度-5 气压+10
python3 st200th_mqtt.py compensate --all -t 1          # 所有设备温度+1
```

范围：温度 ±20°C，湿度 ±20%，气压 ±500hPa

### 修改协议配置

```bash
# MQTT
python3 st200th_mqtt.py custom --protocol mqtt --server "mqtt.example.com" --port 1883

# TCP
python3 st200th_mqtt.py custom --protocol tcp --enable 1 --server "tcp.example.com" --port 8888

# HTTP（URI 最长32字符，不支持 HTTPS）
python3 st200th_mqtt.py custom --protocol http --enable 1 --http-uri "http://api.example.com"
```

修改后需 `restart` 生效。

### OTA 升级

```bash
python3 st200th_mqtt.py ota --uri "http://10.0.0.50/likong-iot/module_v1.bin"
```

仅支持 HTTP，URI 最长 128 字符。

## 发布到 ClawHub

```bash
clawhub login
clawhub publish . --slug st200th-mqtt --name "ST200TH 温湿度变送器" \
  --version 1.0.0 --tags "iot,mqtt,temperature,humidity,sensor,likong"
```

## 协议文档

https://docv2.likong-iot.com/products/transmitters/ST200TH/mqtt
