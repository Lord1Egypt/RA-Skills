---
name: team-sessions
description: 主控发号施令、成员各司其职的团队沟通流程规范。零横向沟通，workspace 隔离，sessions_spawn 标准流程。
metadata:
  openclaw:
    requires:
      bins: []
    install: []
    permissions:
      - 修改 ~/.qclaw/openclaw.json（允许 spawn subagent，这是 OpenClaw 标准配置，不是危险操作）
      - 执行 openclaw gateway restart
---

# Team Sessions

> **触发：** 派任务给团队成员、协调子代理、管理多会话通信。
>
> **核心理念：** 一个主控，多成员，零横向沟通。

---

## 一、Sessions Spawn 三要素

```javascript
sessions_spawn({
  agentId: "成员ID",          // 控制读谁的 SOUL.md（人格身份）
  cwd: "成员workspace路径",   // 控制子代理 workspace 根目录（隔离）
  task: "任务内容...",        // 要做的事
  mode: "run" | "session"     // run=一次完成，session=持久会话
})
```

### 关键理解

| 参数 | 作用 | 不设的后果 |
|------|------|-----------|
| `agentId` | 激活成员身份 | 子代理不知道自己是谁 |
| `cwd` | 隔离 workspace | 读到父代理的 SOUL.md，人格混乱 |
| `task` | 传递任务 | 子代理无事可做 |

### Workspace 隔离原理

```
父代理 workspace/
├── SOUL.md          ← 父代理的人格
├── 任务文件.md
└── 成员A/           ← 成员A的独立 workspace
    ├── SOUL.md      ← 成员A的人格
    └── 产出文件.md
└── 成员B/
    ├── SOUL.md      ← 成员B的人格
    └── ...
```

**必须设 `cwd` 指向成员子目录**，否则所有子代理都读父代理的 SOUL.md。

---

## 二、配置步骤

### Step 1：创建成员 workspace

为每个成员创建独立目录：

```bash
mkdir -p ~/.qclaw/workspace-main/{member-a,member-b,member-c}
```

### Step 2：写入成员 SOUL.md

每个成员的 workspace 下放自己的 SOUL.md：

```bash
# member-a/SOUL.md
echo "你是成员A，负责..." > ~/.qclaw/workspace-main/member-a/SOUL.md

# member-b/SOUL.md  
echo "你是成员B，负责..." > ~/.qclaw/workspace-main/member-b/SOUL.md
```

### Step 3：配置 openclaw.json

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "allowAgents": ["*"]
      }
    },
    "list": {
      "member-a": {
        "agentId": "member-a",
        "workspace": "~/.qclaw/workspace-main/member-a"
      },
      "member-b": {
        "agentId": "member-b", 
        "workspace": "~/.qclaw/workspace-main/member-b"
      }
    }
  }
}
```

> ⚠️ **关于 `allowAgents: ["*"]`**：这是 OpenClaw 的标准配置，允许主控 spawn 子代理。`["*"]` 表示允许所有 agentId，不等于"所有 agent 都有权限"——子代理的权限仍由主控控制。如果你的部署已有其他 agent，可以只列出需要的 agentId（如 `["member-a","member-b"]`）。

### Step 4：重启 Gateway

```bash
openclaw gateway restart
```

---

## 三、标准派任务流程

### 判断任务类型

| 情况 | 方式 | 说明 |
|------|------|------|
| 一次性任务 | `sessions_spawn` + `mode="run"` | 执行完自动结束 |
| 多轮对话 | `sessions_spawn` + `mode="session"` | 保持会话，后续用 `sessions_send` |
| 已有会话 | `sessions_send` | 往已有会话发消息 |

### 构造任务包

每个任务必须包含：

```
【任务编号】T001
【执行者】成员A
【背景】...
【任务内容】...
【交付物】写什么文件、输出什么格式
【禁止】不要做什么
```

### 派任务示例

```javascript
sessions_spawn({
  agentId: "member-a",
  cwd: "/Users/you/.qclaw/workspace-main/member-a",
  task: `【任务 T001】请执行以下任务...

背景：用户需要一份市场调研报告

任务：分析竞品A、B、C的定价策略

交付物：写入 ~/workspace-main/member-a/output.md，包含：
- 竞品列表
- 定价对比表
- 结论建议

禁止：
- 不输出摘要，直接写正文
- 不使用 Markdown 标题（#）
`,
  mode: "run",
  runTimeoutSeconds: 120
})
```

### 等待结果

派完任务后：

```javascript
// 让出控制权，等待子代理完成
sessions_yield()
```

子代理完成后，系统会自动唤醒主代理，此时：

1. 读子代理 workspace 的产出文件
2. 检查是否达标
3. 决定下一步（通过/打回/换人）

---

## 四、沟通铁律

### 1. 零横向沟通

- 成员之间不互相 @、不互相回复
- 所有信息汇总到主代理
- 主代理统一调度

### 2. 汇报格式

```
【任务 T001 完成】
交付物：~/workspace/member-a/output.md
耗时：45秒
状态：✅ 完成
```

### 3. 失败处理三规则

| 次数 | 处理 |
|------|------|
| 第1次失败 | 重派，内容不变 |
| 第2次失败 | 换人，或将内容内嵌进任务 |
| 第3次失败 | 上报用户 |

### 4. 主代理不执行

- 遇到任何需要"做"的事情，第一反应是"派给谁"
- 不自己写代码、不改文件、不执行脚本

---

## 五、常见错误

### Forbidden Error

```
Error: sessions_spawn forbidden
```

**原因：** `openclaw.json` 没设 `allowAgents: ["*"]`

**解法：** 修改配置 → 重启 gateway

### 读到父代理 SOUL.md

**症状：** 子代理用错人格（语气/能力不对）

**原因：** 没设 `cwd` 或 workspace 目录不存在

**解法：** 确认 `cwd` 指向正确，且目录下有对应 SOUL.md

### 子代理空跑

**症状：** 返回空结果或只返回"任务完成"

**原因：**
1. 任务太大 → 拆小
2. 能力不够 → 预写脚本让他执行
3. 描述不清 → 极简 prompt（做什么/输出什么/禁止什么）

---

## 六、最佳实践

1. **预写脚本**：复杂任务先写 Python 脚本，让子代理只执行 `python3 xxx.py`
2. **任务编号**：每个任务带编号，方便追踪
3. **超时设置**：`runTimeoutSeconds` 根据任务复杂度调整（默认30s，复杂任务设120s）
4. **产物规范**：子代理产出统一放自己 workspace，主代理去读取
5. **备份机制**：重要操作前自动备份现有配置
