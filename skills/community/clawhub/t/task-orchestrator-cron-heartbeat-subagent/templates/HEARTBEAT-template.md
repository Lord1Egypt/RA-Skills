# HEARTBEAT.md 模板

> 由 Task Orchestrator 生成 - 根据实际需求修改占位符

---

## 核心任务：{任务名称}

## 定时任务：{任务描述}

每次 heartbeat 时（约 30 分钟），执行以下检查：

### 检查内容
1. {检查项 1}
2. {检查项 2}
3. {检查项 3}

### 执行流程

```bash
# 1. 读取状态文件
state_file="memory/{task-name}-state.json"

# 2. 执行检查逻辑
{具体执行命令或脚本}

# 3. 更新状态
# 写入执行时间、结果等到状态文件
```

### 输出规则

- **无异常时**：回复 `HEARTBEAT_OK`
- **发现异常时**：汇报具体内容 + 建议操作
- **重大事件**：立即汇报（不分时段）

### 状态跟踪

读取 `memory/{task-name}-state.json` 避免重复执行。

状态文件格式：
```json
{
  "task_name": "{任务名称}",
  "last_execution": "ISO 时间",
  "execution_count": 0,
  "last_error": null,
  "last_result": null
}
```

### 成本保护

- **昂贵操作前加预检查**：先检查是否有必要执行
- **API 调用加频率限制**：避免短时间内多次调用
- **夜间模式**：22:00-08:00 静默（仅检查不汇报）

### 安静时段

- **夜间**：22:00-08:00
  - 普通任务：静默工作，攒到白天汇报
  - 重大事件：立即汇报

### 错误处理

- 单次失败不阻塞下次执行
- 连续失败 3 次 → 记录到日志并汇报
- 失败原因写入状态文件

---

## 示例：邮件检查

```markdown
# HEARTBEAT.md

## 定时任务：邮件检查

每次 heartbeat 时（约 30 分钟），检查未读邮件。

### 执行流程

1. 读取 memory/email-state.json 获取上次检查时间
2. 调用邮件 API 获取新邮件
3. 有新邮件 → 汇总汇报（数量 + 重要邮件摘要）
4. 无新邮件 → 回复 HEARTBEAT_OK
5. 更新 email-state.json

### 输出规则

- 无新邮件：`HEARTBEAT_OK`
- 有新邮件（<10 封）：汇总汇报
- 有新邮件（≥10 封）：分批汇报 + 提醒清理

### 夜间模式

22:00-08:00 期间：
- 仅检查不汇报（除非紧急）
- 攒到白天首报统一汇报
```

---

## 示例：API 健康检查

```markdown
# HEARTBEAT.md

## 定时任务：API 健康检查

每次 heartbeat 时，检查关键 API 的健康状态。

### 检查列表

1. **主 API**: https://api.example.com/health
2. **数据库**: 连接状态
3. **缓存**: Redis 连接状态

### 执行流程

```bash
# 检查主 API
curl -s https://api.example.com/health | jq .status

# 检查数据库
# ...

# 检查缓存
# ...
```

### 告警规则

- **正常**：所有检查通过 → `HEARTBEAT_OK`
- **警告**：1 个检查失败 → 汇报警告
- **严重**：≥2 个检查失败 → 立即汇报 + 建议操作

### 状态跟踪

memory/api-health-state.json:
```json
{
  "last_check": "ISO 时间",
  "status": "healthy|degraded|down",
  "failed_checks": [],
  "consecutive_failures": 0
}
```
```

---

## 使用指南

### 1. 复制模板

```bash
cp HEARTBEAT-template.md workspace/HEARTBEAT.md
```

### 2. 修改占位符

- `{任务名称}` → 具体任务名
- `{任务描述}` → 详细描述
- `{检查项}` → 具体检查内容
- `{具体执行命令}` → 实际要执行的命令

### 3. 创建状态文件

```bash
mkdir -p workspace/memory
echo '{"last_execution": null, "execution_count": 0}' > workspace/memory/{task-name}-state.json
```

### 4. 测试执行

手动执行一次 HEARTBEAT.md 中的命令，确认正常。

### 5. 启用心跳

确保 OpenClaw Gateway 已配置心跳间隔（建议 30 分钟）。

---

## 最佳实践

✅ **推荐**：
- 保持心跳任务轻量（<2 分钟完成）
- 使用状态文件避免重复执行
- 设置安静时段避免打扰
- 昂贵操作前加预检查

❌ **避免**：
- 在心跳中执行耗时操作（>5 分钟）
- 无状态跟踪的重复检查
- 不分时段的频繁汇报
- 无限制的 API 调用

---

**模板版本**: 1.0.0  
**生成工具**: Task Orchestrator
