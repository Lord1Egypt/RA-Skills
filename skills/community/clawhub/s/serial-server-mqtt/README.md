# SP501LW 串口网关 MQTT 管理技能 V1.0

通过 MQTT 协议完全控制立控 SP501LW 串口网关，支持**串口透传**和 **Modbus RTU 数据采集**两种核心模式。

## 快速开始

### 1. 安装依赖

```bash
pip3 install paho-mqtt>=2.0.0
```

### 2. 首次使用

```bash
# 注册设备
python3 sp501lw_mqtt.py add \
  --id "我的网关" \
  --cmd-topic "/public/a1b2c3d4e5f6/publish" \
  --data-topic "/public/a1b2c3d4e5f6/subscribe"

# 列出设备
python3 sp501lw_mqtt.py list
```

### 3. 使用模式

#### 模式 A：串口透传（mqtt_tcp）- AI 当作串口

```bash
# 切换模式
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "我的网关"

# 监听数据
python3 sp501lw_mqtt.py listen --id "我的网关"

# 发送命令（另一个终端）
python3 sp501lw_mqtt.py send --id "我的网关" --data "AT+RST" --format text
```

#### 模式 B：数据采集（modbus_rtu）- AI 当作采集器

```bash
# 切换模式
python3 sp501lw_mqtt.py set-mode modbus_rtu --id "我的网关"

# 添加采集任务
python3 sp501lw_mqtt.py add-modbus --id "我的网关" \
  --slave-addr 1 \
  --function-code 3 \
  --register-addr 0 \
  --register-num 2 \
  --interval 5000 \
  --timeout 1000 \
  --data-format Float

# 监听采集数据
python3 sp501lw_mqtt.py listen --id "我的网关"
```

## 完整文档

详见 [SKILL.md](SKILL.md)

## 示例

- [mqtt_tcp 模式示例](examples/mqtt_tcp_example.sh)
- [modbus_rtu 模式示例](examples/modbus_rtu_example.sh)
- [自定义 Broker 示例](examples/custom_broker.sh)

## 核心概念

- **`--id`**：设备标识（用户定义，不绑定 MAC）
- **`--cmd-topic`**：命令主题（发送命令的地方）= mqtt_pub_topic
- **`--data-topic`**：数据主题（接收数据的地方）= mqtt_sub_topic
- **mqtt_tcp**：原始串口透传，AI 像操作串口一样操作设备
- **modbus_rtu**：Modbus RTU 采集器，AI 配置轮询项，设备自动采集上报

## 支持的功能

✅ 设备管理（add/list/remove/update）  
✅ 工作模式切换（mqtt_tcp/modbus_tcp/modbus_rtu）  
✅ 串口透传（send/receive/listen）  
✅ Modbus 配置（add/edit/remove/enable/disable/import/export）  
✅ 设备配置（MQTT/串口/网络/OTA）  
✅ 参数查询（info/sys/mode-info/mqtt-info 等）  

## 快速参考

### 设备管理
```bash
python3 sp501lw_mqtt.py add --id <ID> --cmd-topic <TOPIC> --data-topic <TOPIC>
python3 sp501lw_mqtt.py list
python3 sp501lw_mqtt.py remove --id <ID>
python3 sp501lw_mqtt.py update --id <ID> [选项...]
```

### 核心功能
```bash
python3 sp501lw_mqtt.py set-mode [mqtt_tcp|modbus_tcp|modbus_rtu] --id <ID>
python3 sp501lw_mqtt.py send --id <ID> --data <DATA> --format [text|hex]
python3 sp501lw_mqtt.py listen --id <ID> [--format text|hex]
python3 sp501lw_mqtt.py add-modbus --id <ID> [参数...]
```

### 配置
```bash
python3 sp501lw_mqtt.py set-mqtt --id <ID> [参数...]
python3 sp501lw_mqtt.py set-serial --id <ID> [参数...]
python3 sp501lw_mqtt.py set-network --id <ID> [参数...]
```

### 查询
```bash
python3 sp501lw_mqtt.py info --id <ID>
python3 sp501lw_mqtt.py mode-info --id <ID>
python3 sp501lw_mqtt.py mqtt-info --id <ID>
```

## 获取帮助

```bash
python3 sp501lw_mqtt.py --help
python3 sp501lw_mqtt.py <命令> --help
```
