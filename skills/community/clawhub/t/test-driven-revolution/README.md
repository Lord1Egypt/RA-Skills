# Test-Driven Revolution - 快速开始

**5 分钟上手测试驱动的 AI 自动进化系统**

---

## ⚠️ 重要：何时使用 TDR

### ✅ 用 TDR

- "用 TDR 创建一个 HTTP 服务器"
- "启动 TDR，做个邮件自动回复系统"
- "用 TDR 开发完整的 CRUD 接口"

### ❌ 不用 TDR（直接执行）

- "创建一个频道" → 直接 message 工具
- "给张三发邮件" → 直接邮件工具
- "查天气" → 直接 weather 工具

**原则：TDR 是工具，不是默认行为。用户主动说"用 TDR"时才触发。**

---

## 🔄 完整工作流

```
Planner (协调模型) → Reviewer (高级模型) → Executor (默认模型) → Auditor (高级模型) → 下一轮
```

**角色说明：**
- **Planner（规划师）**：检测任务，触发审阅
- **Reviewer（审阅员）**：决策下一步指令
- **Executor（执行员）**：执行指令，生成代码
- **Auditor（审核员）**：审核执行结果

**实现示例：** 主 Agent/高级模型/审计 Agent/协调模型（可替换为任意 agent）

**角色说明：**
- **主 Agent**：检测任务，触发审阅（协调模型）
- **高级模型**：决策下一步指令（付费）
- **审计 Agent**：执行指令（协调模型）
- **Auditor**：审核执行结果是否达标（协调模型）

---

## 🚀 快速开始

### 0. 自动规划任务（推荐）⭐

```bash
# Step 1: 生成规划 Prompt
node scripts/auto-plan.js "创建一个 HTTP 服务器，监听 3000 端口"

# Step 2: 复制 Prompt 到高级模型会话

# Step 3: 保存返回的 JSON

# Step 4: 创建任务
node scripts/auto-plan.js --create plan-result.json
```

**固定使用高级模型拆解任务，确保规划质量。**

### 1. 配置 Cron（一次性）

```bash
# 主 Agent 心跳 - 每 5 分钟
openclaw cron add \
  --name "tdr-main-heartbeat" \
  --schedule "*/5 * * * *" \
  --agent main \
  --message "cd <workspace>/skills/test-driven-revolution && node scripts/heartbeat-coordinator.js"

# 审计 Agent 心跳 - 每 5 分钟（错开 2 分钟）
openclaw cron add \
  --name "tdr-auditor-heartbeat" \
  --schedule "2,7,12,17,22,27,32,37,42,47,52,57 * * * *" \
  --agent auditor \
  --message "cd <workspace>/skills/test-driven-revolution && node scripts/auditor-heartbeat.js"
```

### 2. 创建第一个任务

```bash
cd <workspace>/skills/test-driven-revolution

cat > tasks/task-001.json << 'EOF'
{
  "task_id": "task-001",
  "title": "我的第一个 TDR 任务",
  "description": "创建一个输出 Hello World 的脚本",
  "status": "pending",
  "depends_on": [],
  "current_subtask": 0,
  "current_iteration": 0,
  "max_iterations": 3,
  "subtasks": [
    "创建脚本文件",
    "创建测试文件",
    "运行测试确保通过"
  ],
  "reference_files": [],
  "history": []
}
EOF
```

### 3. 触发主 Agent 心跳

```bash
# 手动触发（Cron 会自动运行）
node scripts/heartbeat-coordinator.js
```

### 4. 触发审阅

```bash
# 输出审阅 Prompt
node scripts/trigger-review.js task-001

# 复制输出的 Prompt，在主 Agent 会话中用高级模型发送
# 保存返回的 JSON 到 review-result.json
```

### 5. 应用审阅结果

```bash
# 从文件应用
node scripts/apply-review.js task-001 --file review-result.json

# 或从 stdin
cat review-result.json | node scripts/apply-review.js task-001 --stdin
```

### 6. 运行审计 Agent 心跳

```bash
node scripts/auditor-heartbeat.js
```

### 7. 查看进度

```bash
# 任务状态
cat tasks/task-001.json | jq '.status, .current_subtask'

# 事件日志
tail -f logs/events.log | jq
```

---

## 📋 常用命令

### 任务管理

```bash
# 列出所有任务
ls tasks/*.json | xargs -I {} node -e "const t=JSON.parse(require('fs').readFileSync('{}')); console.log(t.task_id, t.status)"

# 查看任务详情
cat tasks/task-001.json | jq

# 查看任务历史
cat tasks/task-001.json | jq '.history'
```

### 锁管理

```bash
# 获取锁
bash scripts/atomic-lock.sh acquire task-001

# 检查锁
bash scripts/atomic-lock.sh check task-001

# 释放锁
bash scripts/atomic-lock.sh release task-001

# 强制解锁（死锁）
bash scripts/force-unlock.sh task-001 --note "死锁超时"
```

### 安全扫描

```bash
# 扫描任务
node scripts/security-scan.js tasks/task-001.json

# 扫描指令
echo "rm -rf /" | node scripts/security-scan.js --stdin
```

### 事件日志

```bash
# 查看某任务事件
grep '"task_id":"task-001"' logs/events.log | jq

# 最新 20 条
tail -20 logs/events.log | jq

# 统计状态
grep '"event":"status_changed"' logs/events.log | jq -r '.to' | sort | uniq -c
```

### Blocked 恢复

```bash
# 恢复任务
bash scripts/unblock-task.sh task-001 --note "已修复"

# 带验证
bash scripts/unblock-task.sh task-001 --note "已修复" --verify
```

---

## 🐛 故障排查

### 任务卡住不动

```bash
# 1. 检查锁
bash scripts/atomic-lock.sh check task-001

# 2. 强制解锁
bash scripts/force-unlock.sh task-001 --note "死锁恢复"

# 3. 手动触发心跳
node scripts/heartbeat-coordinator.js
```

### 安全扫描失败

```bash
# 1. 查看扫描结果
node scripts/security-scan.js tasks/task-001.json

# 2. 如果是误报，手动标记
node -e "
const task = JSON.parse(require('fs').readFileSync('tasks/task-001.json'));
task.security_override = true;
task.security_override_reason = '误报，已人工审查';
fs.writeFileSync('tasks/task-001.json', JSON.stringify(task, null, 2));
"

# 3. 重新触发
node scripts/heartbeat-coordinator.js
```

### 执行失败

```bash
# 1. 查看错误
cat tasks/task-001.json | jq '.history[-1]'

# 2. 恢复任务
bash scripts/unblock-task.sh task-001 --note "修复执行错误"

# 3. 重新执行
node scripts/auditor-heartbeat.js
```

---

## 📖 完整文档

- **SKILL.md** - 完整技能说明
- **DESIGN.md** - 系统架构设计（在 `<workspace>/evolution/`）
- **FIXES_SUMMARY.md** - P0/P1 修复总结

---

**最后更新：** 2026-03-28  
**维护者：** OpenClaw Community
