# Autonomous Agent 模式

> **⚠️ 重要变更**：废弃 tmux 伪 agent → 使用 sessions_spawn 真正的 autonomous agent

## 之前方案的问题

**tmux + 遥控**（伪 agent）：
- ❌ 我需要主动检查 → 发现卡住 → 手动干预
- ❌ Claude Code 本身不是 autonomous（会暂停等批准）
- ❌ 依赖外部循环监控

## 新方案：sessions_spawn

**真正 autonomous**：
- ✅ 子 agent 自己决策执行
- ✅ 无需我主动监控
- ✅ 完成后自动通知

## 配置步骤（一次性）

### 步骤1：配置 Gateway 支持子 Agent

编辑 `~/.openclaw/openclaw.json`，在 `agents.list` 中添加 `main` agent 的子 agent 权限：

```json
{
  "agents": {
    "list": [{
      "id": "main",
      "subagents": {
        "allowAgents": ["dev-agent", "research-agent", "test-agent"]
      }
    }]
  }
}
```

或使用 Gateway tool：
```javascript
gateway({
  action: "config.patch",
  raw: {
    agents: {
      list: [{
        id: "main",
        subagents: {
          allowAgents: ["dev-agent", "research-agent", "test-agent"]
        }
      }]
    }
  }
})
```

### 步骤2：验证配置

```javascript
agents_list()
// 应该看到 allowAgents 中的 agent IDs

sessions_spawn({
  task: "测试任务",
  agentId: "dev-agent",
  runTimeoutSeconds: 60
})
// 返回 status: "accepted" 表示成功
```

## 使用方式

### 创建开发任务

```javascript
sessions_spawn({
  task: `
    开发 AI-First 长租公寓系统

    ## 🚨 强制规则

    **角色定位**：你是流程驱动器（driver），不是代码实现者

    **绝对禁止**：
    - ❌ 使用 \`write\` 工具写代码文件（src/**/*.py, tests/**/*.py）
    - ❌ 跳过 /speckit.* 命令
    - ❌ 直接实现代码

    **必须执行**：
    - ✅ 通过 \`sdd-driver.sh\` 脚本操作 Claude Code
    - ✅ 监控脚本输出，判断意外情况
    - ✅ 尝试自动修复可恢复错误
    - ✅ 仅在无法修复或需要补充上下文时通知人工

    ## 标准流程

    使用驱动脚本执行：

    \`\`\`bash
    # 1. 初始化项目（如需要）
    cd ~/openclaw/workspace/projects/ai-apartment
    specify init . --here --ai claude --force --no-git

    # 2. 启动 Claude Code 会话
    ~/.openclaw/skills/sdd-dev-workflow/scripts/sdd-driver.sh \
      start dev-session . acceptEdits

    # 3. 逐个执行阶段
    ~/.openclaw/skills/sdd-dev-workflow/scripts/sdd-driver.sh \
      run dev-session constitution "创建项目宪法" 300

    ~/.openclaw/skills/sdd-dev-workflow/scripts/sdd-driver.sh \
      run dev-session specify "定义功能规范" 300

    # ... 继续其他阶段

    # 4. 验收测试
    ~/.openclaw/skills/sdd-dev-workflow/scripts/sdd-driver.sh \
      verify .
    \`\`\`

    ## 完成标准

    - ✅ 代码已实现（不是文档）
    - ✅ 测试已通过（至少 1 个核心测试）
    - ✅ 功能可运行（服务能启动）

    ## 🚨 强制验收检查（必须执行）

    \`\`\`bash
    # 1. 语法检查
    python3 -m py_compile backend/app/main.py

    # 2. 核心测试
    cd backend && poetry run pytest tests/test_api/ -v

    # 3. 服务启动验证
    cd backend && timeout 5 poetry run uvicorn app.main:app || true
    \`\`\`

    ## 核心原则

    **可运行 > 完整性**

    禁止：
    - ❌ 配置未使用的外部服务
    - ❌ 生成空测试文件
    - ❌ 只写代码不验证

    ## 工作目录

    /path/to/workspace/projects/your-project
  `,
  agentId: "dev-agent",
  runTimeoutSeconds: 7200,  // 2小时超时
  cleanup: "keep"  // 保留 session 供后续查看
})
```

### agentId 规范

- `dev-agent`：开发任务（SDD 工作流）
- `research-agent`：深度研究任务
- `test-agent`：测试任务

**优点**：
- ✅ 真正 autonomous（自己决策执行）
- ✅ 可移植（skill 包含配置说明）
- ✅ 其他 OpenClaw 实例安装 skill 后即可使用

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `forbidden` | agent ID 未配置 | 添加到 `allowAgents` 列表 |
| `timeout` | 任务超时 | 增加 `runTimeoutSeconds` |
| `agent not found` | agent ID 不存在 | 检查 `agents_list()` |

### 错误示例

```javascript
// 错误：agent 未配置
{
  "error": "forbidden",
  "message": "Agent 'dev-agent' not in allowAgents list"
}

// 解决：配置 Gateway
gateway({
  action: "config.patch",
  raw: {
    agents: {
      list: [{
        id: "main",
        subagents: {
          allowAgents: ["dev-agent", "research-agent", "test-agent"]
        }
      }]
    }
  }
})
```

## 监控子 Agent 进度

### 方式1：查看 session 列表

```javascript
sessions_list({ kinds: ["isolated"] })
// 查找 agentId 对应的 session
```

### 方式2：读取项目进度文件

```bash
# 查看进度
cat projects/your-project/.task-context/progress.json

# 查看检查点
cat projects/your-project/.task-context/checkpoint.md
```

### 方式3：Heartbeat 自动监控

Heartbeat 会自动检查所有 in_progress 任务的进度，发现异常时通知。
