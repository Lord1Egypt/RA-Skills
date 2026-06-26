---
name: flink-conn-kafka
description: Kafka 连接管理子技能，用于管理 Kafka 实例、接入点配置、消息消费调试等。Use this skill when the user wants to add/remove/update a Kafka instance, manage a Kafka endpoint, or consume/debug messages from a concrete Kafka topic/instance. Always trigger only when the request contains a Kafka-connection intent + a concrete object/action.
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

# Kafka 连接管理子技能

用于管理 Kafka 实例、接入点配置、消息消费调试等功能。

---

## 通用约定（必读）

本技能的基础约定与只读约定统一收敛在：

- `../../../COMMON.md`
- `../../../COMMON_READONLY.md`

本技能当前按只读层管理，用于 Kafka 连接信息查询和消息消费调试；若后续扩展为真实配置变更，再切回 mutation 约定。

---

## 🎯 核心功能

### 1. Kafka Instance 管理

#### 1.1 新增或更新 Kafka Instance

**命令格式**：
```bash
volc_flink conn kafka instance add [--name NAME] [--topic TOPIC] [--group-id GROUP_ID]
```

**参数说明**：
- `--name`：Kafka Instance 名称（不传则交互输入）
- `--topic`：Instance 级默认 Topic（不传则交互输入）
- `--group-id`：Instance 级默认 Group ID（不传则交互输入）

**示例**：
```bash
# 交互式添加
volc_flink conn kafka instance add

# 命令行参数添加
volc_flink conn kafka instance add --name my-kafka --topic my-topic --group-id my-consumer-group
```

---

#### 1.2 删除 Kafka Instance

**命令格式**：
```bash
volc_flink conn kafka instance rm --name NAME
```

**参数说明**：
- `--name`：要删除的 Kafka Instance 名称

**示例**：
```bash
volc_flink conn kafka instance rm --name my-kafka
```

---

### 2. Kafka Endpoint 管理

#### 2.1 列出 Kafka Endpoint

**命令格式**：
```bash
volc_flink conn kafka endpoint list [--instance INSTANCE]
```

**参数说明**：
- `--instance`：仅列出指定 Kafka Instance 的 endpoints（可选）

**示例**：
```bash
# 列出所有 Endpoint
volc_flink conn kafka endpoint list

# 列出指定 Instance 的 Endpoint
volc_flink conn kafka endpoint list --instance my-kafka
```

---

#### 2.2 查看 Kafka Endpoint 详情

**命令格式**：
```bash
volc_flink conn kafka endpoint detail --instance INSTANCE --name NAME
```

**参数说明**：
- `--instance`：Kafka Instance 名称
- `--name`：Kafka Endpoint 名称

**示例**：
```bash
volc_flink conn kafka endpoint detail --instance my-kafka --name my-endpoint
```

---

#### 2.3 为 Kafka Instance 增加接入点

**命令格式**：
```bash
volc_flink conn kafka endpoint add --instance INSTANCE [--name NAME] [--bootstrap-servers BOOTSTRAP_SERVERS] [--security-protocol SECURITY_PROTOCOL] [--sasl-mechanism SASL_MECHANISM] [--username USERNAME] [--password PASSWORD] [--set-default]
```

**参数说明**：
- `--instance`：Kafka Instance 名称（必填）
- `--name`：Kafka Endpoint 名称（不传则交互输入）
- `--bootstrap-servers`：bootstrap servers（不传则交互输入）
- `--security-protocol`：协议，默认 PLAINTEXT
- `--sasl-mechanism`：SASL 机制，默认不设置
- `--username`：用户名，默认不设置
- `--password`：密码，默认不设置
- `--set-default`：将该 endpoint 设为默认

**安全协议选项**：
- `PLAINTEXT`：无加密（默认）
- `SASL_PLAINTEXT`：SASL 认证，无加密
- `SSL`：SSL 加密
- `SASL_SSL`：SASL 认证 + SSL 加密

**SASL 机制选项**：
- `PLAIN`：普通用户名密码认证
- `SCRAM-SHA-256`：SCRAM SHA-256 认证
- `SCRAM-SHA-512`：SCRAM SHA-512 认证

**示例**：
```bash
# 交互式添加
volc_flink conn kafka endpoint add --instance my-kafka

# PLAINTEXT 协议（无认证）
volc_flink conn kafka endpoint add --instance my-kafka --name my-endpoint --bootstrap-servers kafka:9092 --set-default

# SASL_PLAINTEXT 协议
volc_flink conn kafka endpoint add --instance my-kafka --name my-sasl-endpoint --bootstrap-servers kafka:9092 --security-protocol SASL_PLAINTEXT --sasl-mechanism PLAIN --username myuser --password mypass --set-default

# SASL_SSL 协议
volc_flink conn kafka endpoint add --instance my-kafka --name my-ssl-endpoint --bootstrap-servers kafka:9093 --security-protocol SASL_SSL --sasl-mechanism SCRAM-SHA-256 --username myuser --password mypass --set-default
```

---

#### 2.4 为 Kafka Instance 删除接入点

**命令格式**：
```bash
volc_flink conn kafka endpoint rm --instance INSTANCE --name NAME
```

**参数说明**：
- `--instance`：Kafka Instance 名称
- `--name`：Kafka Endpoint 名称

**示例**：
```bash
volc_flink conn kafka endpoint rm --instance my-kafka --name my-endpoint
```

---

### 3. Kafka 消息操作

#### 3.1 按时间范围消费消息

**命令格式**：
```bash
volc_flink conn kafka messages consume [--partition PARTITION] [--start START] [--end END] [--limit LIMIT] [--instance INSTANCE] [--endpoint ENDPOINT] [--topic TOPIC] [--group-id GROUP_ID] [--poll-timeout POLL_TIMEOUT] [--max-idle-polls MAX_IDLE_POLLS] [--offsets-timeout OFFSETS_TIMEOUT] [--raw]
```

**参数说明**：
- `--partition`：分区号（不传则从所有 partition 消费）
- `--start`：开始时间，如 2024-07-01T00:00:00Z（不传默认最近 3 小时）
- `--end`：结束时间，默认当前时间
- `--limit`：最多返回条数，默认 10
- `--instance`：Kafka Instance 名称（存在多个 instance 时建议显式指定）
- `--endpoint`：Kafka Endpoint 名称（不传则使用 instance 默认 endpoint）
- `--topic`：覆盖默认 Topic
- `--group-id`：覆盖默认 Group ID
- `--poll-timeout`：单次 poll 超时时间（秒），默认 1.0
- `--max-idle-polls`：连续空轮询次数上限，默认 3
- `--offsets-timeout`：按时间查找起始 offset 的超时时间（秒），默认 10
- `--raw`：输出原始 JSON

**时间格式**：
- ISO 8601 格式：`2024-07-01T00:00:00Z`
- 相对时间：`-3h`（最近 3 小时）、`-1d`（最近 1 天）

**示例**：
```bash
# 消费最近 3 小时的消息（默认 10 条）
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic

# 消费指定时间范围的消息
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --start 2024-07-01T00:00:00Z --end 2024-07-02T00:00:00Z --limit 50

# 消费指定分区的消息
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --partition 0 --limit 20

# 输出原始 JSON
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --raw

# 消费更多消息
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --limit 100
```

---

## 快速入门指引

### 完整的首次使用流程

**步骤 1：添加 Kafka Instance**
```bash
# 交互式添加（推荐）
volc_flink conn kafka instance add

# 或使用命令行参数
volc_flink conn kafka instance add --name my-kafka --topic my-topic --group-id my-consumer-group
```

**步骤 2：添加 Kafka Endpoint**
```bash
# PLAINTEXT 协议（无认证）
volc_flink conn kafka endpoint add --instance my-kafka --name my-endpoint --bootstrap-servers kafka:9092 --set-default

# 或 SASL_PLAINTEXT 协议（有认证）
volc_flink conn kafka endpoint add --instance my-kafka --name my-sasl-endpoint --bootstrap-servers kafka:9092 --security-protocol SASL_PLAINTEXT --sasl-mechanism PLAIN --username myuser --password mypass --set-default
```

**步骤 3：消费消息测试**
```bash
# 消费最近 3 小时的消息
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --limit 10
```

---

## 常用场景示例

### 场景 1：快速调试 Kafka 数据

```bash
# 1. 添加 Instance
volc_flink conn kafka instance add --name debug-kafka --topic debug-topic --group-id debug-group

# 2. 添加 Endpoint
volc_flink conn kafka endpoint add --instance debug-kafka --name debug-endpoint --bootstrap-servers kafka:9092 --set-default

# 3. 消费最新消息
volc_flink conn kafka messages consume --instance debug-kafka --topic debug-topic --limit 20
```

### 场景 2：按时间范围排查问题

```bash
# 消费指定时间范围内的消息
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --start 2024-07-01T08:00:00Z --end 2024-07-01T12:00:00Z --limit 100
```

### 场景 3：查看原始 JSON 数据

```bash
# 输出原始 JSON 格式，便于进一步分析
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --raw --limit 5
```

### 场景 4：指定分区消费

```bash
# 只消费分区 0 的消息
volc_flink conn kafka messages consume --instance my-kafka --topic my-topic --partition 0 --limit 20
```

---

## 安全配置指南

### PLAINTEXT（无加密，无认证）
适用于开发环境或内部安全网络。

```bash
volc_flink conn kafka endpoint add --instance my-kafka --name plain-endpoint --bootstrap-servers kafka:9092 --security-protocol PLAINTEXT --set-default
```

### SASL_PLAINTEXT（SASL 认证，无加密）
适用于需要认证但不需要加密的场景。

```bash
volc_flink conn kafka endpoint add --instance my-kafka --name sasl-endpoint --bootstrap-servers kafka:9092 --security-protocol SASL_PLAINTEXT --sasl-mechanism PLAIN --username myuser --password mypass --set-default
```

### SASL_SSL（SASL 认证 + SSL 加密）
适用于生产环境，提供最高安全性。

```bash
volc_flink conn kafka endpoint add --instance my-kafka --name ssl-endpoint --bootstrap-servers kafka:9093 --security-protocol SASL_SSL --sasl-mechanism SCRAM-SHA-256 --username myuser --password mypass --set-default
```

---

## 输出格式

### Instance 添加成功
```
# ✅ Kafka Instance 添加成功

## 📋 Instance 信息
- **名称**: my-kafka
- **默认 Topic**: my-topic
- **默认 Group ID**: my-consumer-group

## 💡 下一步
1. 添加 Endpoint: `volc_flink conn kafka endpoint add`
2. 消费消息: `volc_flink conn kafka messages consume`
```

### Endpoint 添加成功
```
# ✅ Kafka Endpoint 添加成功

## 📋 Endpoint 信息
- **Instance**: my-kafka
- **名称**: my-endpoint
- **Bootstrap Servers**: kafka:9092
- **安全协议**: PLAINTEXT
- **设为默认**: 是

## 💡 下一步
1. 消费消息: `volc_flink conn kafka messages consume`
```

### 消息消费结果
```
# 📨 Kafka 消息消费结果

## 📋 消费信息
- **Instance**: my-kafka
- **Topic**: my-topic
- **时间范围**: 2024-07-01T00:00:00Z - 2024-07-02T00:00:00Z
- **消息数量**: 10

## 📄 消息列表
[消息 1]
[消息 2]
...
```

---

## 错误处理

### 常见错误及处理

#### 错误 1：Instance 不存在
**错误信息**：`Kafka instance not found`

**处理方式**：
- 提示："指定的 Kafka Instance 不存在"
- 建议：先添加 Instance：`volc_flink conn kafka instance add`

#### 错误 2：Endpoint 不存在
**错误信息**：`Kafka endpoint not found`

**处理方式**：
- 提示："指定的 Kafka Endpoint 不存在"
- 建议：先添加 Endpoint：`volc_flink conn kafka endpoint add`

#### 错误 3：连接失败
**错误信息**：`Failed to connect to Kafka`

**处理方式**：
- 提示："连接 Kafka 失败"
- 检查：Bootstrap Servers 地址是否正确
- 检查：网络连接是否正常
- 检查：端口是否开放

#### 错误 4：认证失败
**错误信息**：`Authentication failed`

**处理方式**：
- 提示："Kafka 认证失败"
- 检查：用户名和密码是否正确
- 检查：SASL 机制配置是否正确
- 检查：安全协议配置是否正确

#### 错误 5：Topic 不存在
**错误信息**：`Topic not found`

**处理方式**：
- 提示："指定的 Topic 不存在"
- 检查：Topic 名称是否正确
- 确认：Topic 是否已经创建

---

## 注意事项

### 重要：安全提示

⚠️ **关于 Kafka 认证信息的安全**：
1. **不要在聊天中直接粘贴密码** - 建议使用交互式输入
2. **妥善保管认证信息** - 不要泄露给他人
3. **使用最小权限原则** - 为 Kafka 用户分配最小必要权限
4. **定期轮换认证信息** - 提高安全性

### 通用注意事项

1. **先添加 Instance**：在添加 Endpoint 前，先确保 Instance 已配置完成
2. **设置默认 Endpoint**：添加 Endpoint 时建议使用 `--set-default` 设置为默认
3. **合理设置时间范围**：消费消息时注意时间范围，避免消费过多消息
4. **使用合适的 Limit**：设置合理的消息数量限制，避免输出过长
5. **注意时区问题**：时间参数使用 UTC 时间（Z 后缀）
6. **生产环境谨慎操作**：在生产环境消费消息时，注意不要影响正常业务

---

## 📚 常用命令速查

### Instance 管理
```bash
# 添加 Instance（交互式）
volc_flink conn kafka instance add

# 添加 Instance（命令行）
volc_flink conn kafka instance add --name <name> --topic <topic> --group-id <group-id>

# 删除 Instance
volc_flink conn kafka instance rm --name <name>
```

### Endpoint 管理
```bash
# 列出 Endpoint
volc_flink conn kafka endpoint list

# 查看 Endpoint 详情
volc_flink conn kafka endpoint detail --instance <instance> --name <name>

# 添加 Endpoint（PLAINTEXT）
volc_flink conn kafka endpoint add --instance <instance> --name <name> --bootstrap-servers <servers> --set-default

# 添加 Endpoint（SASL_PLAINTEXT）
volc_flink conn kafka endpoint add --instance <instance> --name <name> --bootstrap-servers <servers> --security-protocol SASL_PLAINTEXT --sasl-mechanism PLAIN --username <user> --password <pass> --set-default

# 删除 Endpoint
volc_flink conn kafka endpoint rm --instance <instance> --name <name>
```

### 消息消费
```bash
# 消费最近 3 小时消息（默认 10 条）
volc_flink conn kafka messages consume --instance <instance> --topic <topic>

# 按时间范围消费
volc_flink conn kafka messages consume --instance <instance> --topic <topic> --start <start-time> --end <end-time> --limit <limit>

# 指定分区消费
volc_flink conn kafka messages consume --instance <instance> --topic <topic> --partition <partition>

# 输出原始 JSON
volc_flink conn kafka messages consume --instance <instance> --topic <topic> --raw
```

---

## 🎯 技能总结

### 核心功能
1. ✅ **Kafka Instance 管理** - 新增、删除 Kafka Instance
2. ✅ **Kafka Endpoint 管理** - 添加、删除、查看 Endpoint，支持多种安全协议
3. ✅ **Kafka 消息消费** - 按时间范围消费，支持原始 JSON 输出，指定分区
4. ✅ **安全认证支持** - PLAINTEXT、SASL_PLAINTEXT、SASL_SSL 等多种安全配置
5. ✅ **灵活的参数配置** - 支持自定义消费组、超时时间、轮询次数等

### 使用场景
- ✅ 快速调试 Kafka 数据
- ✅ 按时间范围排查问题
- ✅ 查看原始 JSON 数据
- ✅ 指定分区消费
- ✅ 生产环境数据验证

这个子技能提供了完整的 Kafka 连接管理和消息消费功能！
