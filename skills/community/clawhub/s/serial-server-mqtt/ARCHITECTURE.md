# SP501LW Skill 架构说明

## 核心设计原则：配置与操作分离

### 问题背景

在 mqtt.md 中明确说明：
- 当发送配置消息到设备时，设备会：
  1. 解析配置
  2. 写入 NVS（非易失存储）
  3. 发送 ACK 回复
  4. **延迟约 500ms 后执行 esp_restart()（重启）**

这意味着**所有配置操作都会导致设备重启 5-30 秒**。

### 关键限制

重启期间，设备**离线**，**无法接收任何指令**。

❌ **错误做法**：
```bash
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "设备"  # 设备开始重启
python3 sp501lw_mqtt.py send --id "设备" --data "fffff"  # ❌ 此时设备离线，失败
```

✅ **正确做法**：
```bash
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "设备"  # 设备开始重启
sleep 30  # 等待重启完成
python3 sp501lw_mqtt.py send --id "设备" --data "fffff"  # ✅ 设备已在线，成功
```

---

## Skill 中的两类操作

### 第一类：配置操作（会重启）

这些操作会修改设备 NVS 配置，导致设备重启：

| 命令 | 作用 | 重启 |
|------|------|------|
| `set-mode` | 切换工作模式 | ✅ 重启 5-30 秒 |
| `set-poll-time` | 设置轮询周期 | ✅ 重启 5-30 秒 |
| `add-modbus` | 添加 Modbus 轮询项 | ✅ 重启 5-30 秒 |
| `edit-modbus` | 编辑 Modbus 轮询项 | ✅ 重启 5-30 秒 |
| `remove-modbus` | 删除 Modbus 轮询项 | ✅ 重启 5-30 秒 |
| `set-mqtt` | 修改 MQTT 配置 | ✅ 重启 5-30 秒 |
| `set-serial` | 修改串口参数 | ✅ 重启 5-30 秒 |
| `set-network` | 修改网络参数 | ✅ 重启 5-30 秒 |
| `enable-modbus` | 启用轮询项 | ✅ 重启 5-30 秒 |
| `disable-modbus` | 禁用轮询项 | ✅ 重启 5-30 秒 |

**特点**：
- 返回消息中会明确说明"设备将重启"
- 每次重启需要等待 5-30 秒
- 不能连续发送配置指令（会等待设备重启）

### 第二类：操作命令（不会重启）

这些操作不修改配置，不会导致重启，可以立即执行：

| 命令 | 作用 | 重启 |
|------|------|------|
| `send` | 发送串口数据 | ❌ 不重启 |
| `listen` | 监听设备数据 | ❌ 不重启 |
| `receive` | 单次接收 | ❌ 不重启 |
| `info` | 查询设备信息 | ❌ 不重启 |
| `sys` | 查询系统信息 | ❌ 不重启 |
| `mode-info` | 查询模式信息 | ❌ 不重启 |
| `mqtt-info` | 查询 MQTT 配置 | ❌ 不重启 |
| `net-info` | 查询网络信息 | ❌ 不重启 |
| `serial-info` | 查询串口配置 | ❌ 不重启 |

**特点**：
- 不修改 NVS，只查询或发送数据
- 不会导致设备重启
- 可以连续执行多个命令

---

## 典型使用场景

### 场景 1：AI 进入 mqtt_tcp 透传模式并发送数据

```bash
# 配置阶段（会重启）
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "测试设备"
# 返回：工作模式已切换为: mqtt_tcp，设备将在 5-30 秒内重启

# 等待阶段（CRITICAL！必须等待）
sleep 30

# 操作阶段（不会重启，可以连续执行）
python3 sp501lw_mqtt.py send --id "测试设备" --data "fffff" --format text
python3 sp501lw_mqtt.py listen --id "测试设备" --format hex
```

### 场景 2：AI 配置多个 Modbus 轮询项

```bash
# 第一个配置（会重启）
python3 sp501lw_mqtt.py add-modbus --id "测试设备" \
  --slave-addr 1 --function-code 3 \
  --register-addr 0 --register-num 2 \
  --interval 5000 --timeout 1000 \
  --data-format Float
# 返回：Modbus 轮询项已添加，设备将在 5-30 秒内重启

# 等待第一个配置生效
sleep 30

# 第二个配置（又会重启）
python3 sp501lw_mqtt.py add-modbus --id "测试设备" \
  --slave-addr 2 --function-code 3 \
  --register-addr 0 --register-num 2 \
  --interval 10000 --timeout 1000 \
  --data-format Unsigned
# 返回：Modbus 轮询项已添加，设备将在 5-30 秒内重启

# 等待第二个配置生效
sleep 30

# 现在可以监听采集数据（不会重启）
python3 sp501lw_mqtt.py listen --id "测试设备"
```

### 场景 3：修改网络配置然后继续操作

```bash
# 配置阶段
python3 sp501lw_mqtt.py set-network --id "测试设备" \
  --mode wifi --ssid "MyWiFi" --password "pass123"
# 返回：网络配置已更新，设备将重启

# 等待重启
sleep 30

# 验证设备已上线（不会重启）
python3 sp501lw_mqtt.py info --id "测试设备"

# 然后继续其他操作（不会重启）
python3 sp501lw_mqtt.py send --id "测试设备" --data "test" --format text
```

---

## AI 使用指南

### 对 AI 的建议

1. **识别操作类型**：
   - 如果返回消息包含"设备将重启"，说明这是配置操作
   - 需要立即执行 `sleep 30`

2. **等待时间**：
   - 保守估计：总是等待 30 秒
   - 较激进：如果连续执行多个配置，可以在最后一个后再等

3. **错误处理**：
   - 如果操作超时，检查是否还在重启
   - 等待足够时间后重试

### 代码实现示例

```python
def configure_and_send(device_id, config_cmd, wait_time=30, send_cmd=None):
    """配置然后发送的完整流程"""
    
    # 步骤 1：执行配置
    print(f"[1] 执行配置: {config_cmd}")
    execute_command(config_cmd)
    
    # 步骤 2：检查返回消息，确认会重启
    if "设备将重启" in response:
        print(f"[2] 设备重启中...等待 {wait_time} 秒")
        time.sleep(wait_time)
    
    # 步骤 3：执行操作命令
    if send_cmd:
        print(f"[3] 执行操作: {send_cmd}")
        execute_command(send_cmd)
```

---

## 关键要点总结

| 项目 | 说明 |
|------|------|
| **配置操作** | 会修改 NVS，导致设备重启 5-30 秒 |
| **操作命令** | 不修改配置，立即执行，可连续使用 |
| **等待时间** | 保守推荐 30 秒，以确保重启完成 |
| **错误原因** | 通常是配置后没有等待，设备还在重启 |
| **判断标准** | 看返回消息是否包含"设备将重启"字样 |

---

## 变更记录

- v1.0.0：初始版本
  - 明确分离配置与操作
  - 所有配置操作返回消息都标记重启
  - 提供完整的等待建议
