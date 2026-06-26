---
name: flink-conn
description: Flink 上下游资源连接管理技能，用于管理 Kafka、数据库等上下游资源连接，包括实例管理、接入点配置、消息消费调试等。Use this skill when the user wants to configure or inspect concrete upstream/downstream connections, such as Kafka instances, endpoints, or sampled message reads. Always trigger only when the request contains a connection intent + a concrete connection object/action.
required_binaries:
  - volc_flink
may_access_config_paths:
  - ~/.volc_flink
  - $VOLC_FLINK_CONFIG_DIR
credentials:
  primary: volc_flink_local_config
  optional_env_vars:
    - VOLCENGINE_ACCESS_KEY
    - VOLCENGINE_SECRET_KEY
    - VOLCENGINE_REGION
---

# Flink 上下游资源连接管理技能

用于管理 Kafka、数据库等上下游资源连接，包括实例管理、接入点配置、消息消费调试等功能。

---

## 通用约定（必读）

本技能的基础约定与只读约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_READONLY.md`

本技能当前按只读层管理，用于连接信息查询、Endpoint 检查和消费调试；若后续扩展为真实配置变更，再切回 mutation 约定。

---

## 🎯 核心功能

### 1. Kafka 连接管理

#### 1.1 Kafka Instance 管理
- 新增或更新 Kafka Instance
- 删除 Kafka Instance
- 列出所有 Kafka Instance

#### 1.2 Kafka Endpoint 管理
- 为 Kafka Instance 增加接入点
- 删除 Kafka Instance 的接入点
- 查看 Kafka Endpoint 详情
- 设置默认 Endpoint

#### 1.3 Kafka 消息操作
- 按时间范围消费消息
- 支持原始 JSON 输出
- 支持指定分区消费
- 支持自定义消费组

---

## 子技能

### Kafka 子技能
详细的 Kafka 连接管理功能请参考子技能：[flink-conn-kafka](./kafka/SKILL.md)

---

## 快速入门

### 首次使用流程

1. **添加 Kafka Instance**
```bash
volc_flink conn kafka instance add --name my-kafka --topic my-topic --group-id my-group
```

2. **添加 Endpoint**
```bash
volc_flink conn kafka endpoint add --instance my-kafka --name my-endpoint --bootstrap-servers kafka:9092 --set-default
```

3. **消费消息**
```bash
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --limit 10
```

---

## 常用命令速查

### Kafka Instance 管理
```bash
# 新增或更新 Kafka Instance
volc_flink conn kafka instance add --name <name> --topic <topic> --group-id <group-id>

# 删除 Kafka Instance
volc_flink conn kafka instance rm --name <name>
```

### Kafka Endpoint 管理
```bash
# 列出 Endpoint
volc_flink conn kafka endpoint list

# 查看 Endpoint 详情
volc_flink conn kafka endpoint detail --instance <instance> --name <name>

# 添加 Endpoint
volc_flink conn kafka endpoint add --instance <instance> --name <name> --bootstrap-servers <servers> --set-default

# 删除 Endpoint
volc_flink conn kafka endpoint rm --instance <instance> --name <name>
```

### Kafka 消息操作
```bash
# 消费消息（最近 3 小时，默认 10 条）
volc_flink conn kafka messages consume --instance <instance> --topic <topic>

# 按时间范围消费
volc_flink conn kafka messages consume --instance <instance> --topic <topic> --start <start-time> --end <end-time> --limit <limit>

# 指定分区消费
volc_flink conn kafka messages consume --instance <instance> --topic <topic> --partition <partition>

# 输出原始 JSON
volc_flink conn kafka messages consume --instance <instance> --topic <topic> --raw
```

---

## 输出格式

### Instance 添加成功
```
# ✅ Kafka Instance 添加成功

## 📋 Instance 信息
- **名称**: [name]
- **默认 Topic**: [topic]
- **默认 Group ID**: [group-id]

## 💡 下一步
1. 添加 Endpoint: `volc_flink conn kafka endpoint add`
2. 消费消息: `volc_flink conn kafka messages consume`
```

### Endpoint 添加成功
```
# ✅ Kafka Endpoint 添加成功

## 📋 Endpoint 信息
- **Instance**: [instance]
- **名称**: [name]
- **Bootstrap Servers**: [servers]
- **安全协议**: [protocol]
- **设为默认**: [是/否]

## 💡 下一步
1. 消费消息: `volc_flink conn kafka messages consume`
```

### 消息消费结果
```
# 📨 Kafka 消息消费结果

## 📋 消费信息
- **Instance**: [instance]
- **Topic**: [topic]
- **时间范围**: [start] - [end]
- **消息数量**: [count]

## 📄 消息列表
[消息内容]
```

---

## 错误处理

### 常见错误及处理

#### 错误 1：Instance 不存在
**错误信息**：`Kafka instance not found`

**处理方式**：
- 提示："指定的 Kafka Instance 不存在"
- 建议：先添加 Instance：`volc_flink conn kafka instance add`
- 或列出可用 Instance：`volc_flink conn kafka instance list`

#### 错误 2：Endpoint 不存在
**错误信息**：`Kafka endpoint not found`

**处理方式**：
- 提示："指定的 Kafka Endpoint 不存在"
- 建议：先添加 Endpoint：`volc_flink conn kafka endpoint add`
- 或列出可用 Endpoint：`volc_flink conn kafka endpoint list`

#### 错误 3：连接失败
**错误信息**：`Failed to connect to Kafka`

**处理方式**：
- 提示："连接 Kafka 失败"
- 检查：Bootstrap Servers 地址是否正确
- 检查：网络连接是否正常
- 检查：安全配置是否正确

#### 错误 4：认证失败
**错误信息**：`Authentication failed`

**处理方式**：
- 提示："Kafka 认证失败"
- 检查：用户名和密码是否正确
- 检查：SASL 机制配置是否正确
- 检查：安全协议配置是否正确

---

## 注意事项

### 重要：安全提示

⚠️ **关于 Kafka 认证信息的安全**：
1. **不要在聊天中直接粘贴密码** - 建议使用交互式输入
2. **妥善保管认证信息** - 不要泄露给他人
3. **使用最小权限原则** - 为 Kafka 用户分配最小必要权限

### 通用注意事项

1. **先添加 Instance**：在添加 Endpoint 前，先确保 Instance 已配置完成
2. **设置默认 Endpoint**：添加 Endpoint 时建议使用 `--set-default` 设置为默认
3. **合理设置时间范围**：消费消息时注意时间范围，避免消费过多消息
4. **使用合适的 Limit**：设置合理的消息数量限制，避免输出过长

---

## 🎯 技能总结

### 核心功能
1. ✅ **Kafka Instance 管理** - 新增、删除、列出 Kafka Instance
2. ✅ **Kafka Endpoint 管理** - 添加、删除、查看 Endpoint，设置默认
3. ✅ **Kafka 消息消费** - 按时间范围消费，支持原始 JSON 输出
4. ✅ **安全认证支持** - 支持 PLAINTEXT、SASL_PLAINTEXT、SASL_SSL 等协议

### 与其他技能的关系
- **这是连接管理技能** - 提供上下游资源连接的基础功能
- **支持其他技能** - 为 SQL 开发、任务调试等提供数据访问能力
- **独立使用** - 也可以单独用于 Kafka 数据调试和查看

这个技能是 Flink 上下游资源连接管理的核心技能！
