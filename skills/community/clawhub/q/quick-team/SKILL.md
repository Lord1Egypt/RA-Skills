---
name: quick-team
description: 用自然语言快速创建 AI 团队成员的目录结构和配置文件。自动生成 SOUL/IDENTITY/TOOLS 等模板，引导完成 openclaw.json 配置。
metadata:
  openclaw:
    requires:
      bins: []
    install: []
    permissions:
      - action: "修改 ~/.qclaw/openclaw.json（agents.list 追加成员）"
        risk: "修改运行时配置，影响 agent spawn 行为"
        mitigation: "修改前展示完整 diff，用户确认后再写入"
      - action: "设置 agents.defaults.subagents.allowAgents"
        risk: "扩大子代理 spawn 权限（星号通配符允许 spawn 任意 agent）"
        mitigation: "默认建议最小白名单（仅新成员 ID），不推荐通配符"
      - action: "重启 OpenClaw Gateway"
        risk: "中断当前所有会话和正在运行的任务"
        mitigation: "仅在用户确认后执行，提醒正在运行的任务会中断"
---

> ⚠️ **权限提醒**：本 skill 会修改 `openclaw.json` 和重启 Gateway。所有配置变更会先展示 diff 供用户确认，不会静默写入。

# Quick Team —— 快速创建团队成员

> **触发：** 用户说「创建一个成员」「帮我新建一个角色」「添加团队成员」「搞个新agent」等。
>
> **核心理念：** 一个主控，零门槛，三分钟一支团队。

---

## 零、快速开始

```
用户：帮我创建一个负责校对审核的成员，叫火眼
Agent：
    [执行创建流程 → 3分钟完成]
    ✅ 团队新成员：火眼
    workspace: ~/.qclaw/workspace-agent-ba01c6a8/huoyan/
    SOUL.md / IDENTITY.md / TOOLS.md / HEARTBEAT.md / MEMORY.md 已创建
```

---

## 一、创建流程（6步）

### 步骤1：确认需求

让用户明确回答以下问题（缺一不可）：

| 问题 | 示例 | 作用 |
|------|------|------|
| **角色名称** | "火眼"、"小策" | 决定目录名和 Agent ID |
| **核心职责** | "校对审核"、"策略分析" | 决定 SOUL.md 的职责描述 |
| **性格风格** | "毒舌"、"温和"、"专业冷静" | 决定语气和人设 |
| **禁止做的事** | "不横向联系"、"不自作主张" | 决定禁止事项 |
| **汇报方式** | "任务完成后直接汇报" | 决定汇报规则 |

**如果用户说不清楚：** 主动给选项，让用户选，不要停下来等。

---

### 步骤2：生成 Agent ID

**规则：** 用中文拼音首字母，不能重复。

| 名称 | ID |
|------|-----|
| 火眼 | huoyan |
| 小策 | xiaoce |
| 小编 | xiaobian |
| 小创 | xiaochuang |

**如果重复：** 自动加数字后缀，如 `xiaoce-2`

---

### 步骤3：创建文件结构

在主控 workspace 下创建子代理目录：

```
workspace/
├── huoyan/
│   ├── SOUL.md        ← 必须：人格定义
│   ├── IDENTITY.md    ← 必须：身份标识
│   ├── TOOLS.md       ← 必须：工具备忘
│   ├── HEARTBEAT.md   ← 必须：心跳配置
│   └── MEMORY.md      ← 必须：长期记忆
```

**必须文件说明：**

| 文件 | 必须 | 用途 |
|------|------|------|
| SOUL.md | ✅ | 角色定位 + 职责 + 禁止事项 + 汇报规则 |
| IDENTITY.md | ✅ | 名称/Emoji/氛围描述 |
| TOOLS.md | ✅ | 常用工具备忘 |
| HEARTBEAT.md | ✅ | 周期性任务配置 |
| MEMORY.md | ✅ | 长期记忆文件 |

**辅助文件说明：**
| 文件 | 必须 | 用途 |
|------|------|------|
| AGENTS.md | ✅ | 主控才有，记录所有成员配置 |
| USER.md | ⚠️ | 主控才需要，子代理一般不需要 |
| BOOTSTRAP.md | ❌ | 仅首次启动用，创建成员时不需要 |

---

### 步骤4：填充模板

从 `templates/` 目录复制对应模板，根据用户需求填写内容。

**重点：SOUL.md 必须包含以下章节（不可删减）：**

```markdown
# SOUL.md

## 我是谁
{一句话角色定位}

## 我的职责
1. {具体职责1}
2. {具体职责2}
3. {具体职责3}

## 禁止事项
- {明确不做的事}

## 汇报规则
- {汇报格式和要求}

## 铁律
- {不可逾越的红线}
```

---

### 步骤5：配置 openclaw.json

**先展示变更，用户确认后再写入。**

需要修改的内容：

1. 在 `agents.list` 中追加新成员：

```json
{
  "id": "huoyan",
  "name": "火眼",
  "workspace": "/Users/xxx/.qclaw/workspace-agent-主控ID/huoyan"
}
```

2. **关于 `allowAgents`**：如果主控需要 spawn 子代理，需设置 `agents.defaults.subagents.allowAgents`。

**推荐最小白名单**（仅允许需要的成员）：
```json
"allowAgents": ["huoyan"]
```

通配符 `["*"]` 会允许 spawn 任意 agent，存在权限扩大风险，不推荐除非用户明确要求。

**操作流程：**
- 展示完整 diff（新增了什么、改了什么）
- 用户确认后再写入文件
- 如果用户不确认，跳过此步骤，提示用户稍后手动配置

---

### 步骤6：重启 Gateway 并验证

> ⚠️ 重启 Gateway 会中断当前所有会话和正在运行的任务。请用户确认后再执行。

```bash
# 重启前提醒用户
openclaw gateway restart
```

重启后测试激活：

```javascript
sessions_spawn({
  agentId: "huoyan",
  cwd: "/Users/xxx/.qclaw/workspace-agent-主控ID/huoyan",
  mode: "run",
  task: "介绍一下你自己"
})
```

**验证通过的标准：**
- ✅ 回复体现正确的角色人格
- ✅ 没有读错 SOUL.md（比如读成了其他成员的）
- ✅ 文件路径正确

---

## 二、子代理标准目录结构

```
workspace/
├── 主控workspace/
│   ├── SOUL.md
│   ├── IDENTITY.md
│   ├── AGENTS.md          ← 记录所有成员配置
│   ├── MEMORY.md
│   ├── TOOLS.md
│   ├── HEARTBEAT.md
│   │
│   ├── 子代理A/            ← 每个子代理一个独立目录
│   │   ├── SOUL.md
│   │   ├── IDENTITY.md
│   │   ├── TOOLS.md
│   │   ├── HEARTBEAT.md
│   │   └── MEMORY.md
│   │
│   ├── 子代理B/
│   │   └── ...
│   │
│   └── memory/            ← 主控的日常记忆
│       └── YYYY-MM-DD.md
│
└── skills/                ← 主控的 skills
    └── ...
```

---

## 三、模板说明

| 模板文件 | 用途 | 备注 |
|---------|------|------|
| `SOUL.md` | 角色人格定义 | 核心，必须完整填写 |
| `IDENTITY.md` | 身份标识 | 名称/Emoji/氛围 |
| `TOOLS.md` | 工具备忘 | 常用命令和配置 |
| `HEARTBEAT.md` | 周期性任务 | 保持空可节省API |
| `MEMORY.md` | 长期记忆 | 持续积累信息 |

`examples/assistant/` 目录中有完整示例，可参考格式。

---

## 四、常见问题

### Q：用户只给了一个名字怎么办？

**A：** 先根据名字推断角色方向，然后主动给选项：

```
用户：帮我建一个叫小明
Agent：好的，小明大概负责什么方向？
  A. 执行类——完成具体任务（校对、整理、测试）
  B. 审核类——检查、评分、给意见
  C. 创意类——头脑风暴、策划、提案
  D. 其他（请描述）
```

### Q：spawn 后读错了 SOUL.md？

**A：** 检查是否同时传了 `agentId` + `cwd`。两个参数缺一不可。

### Q：新建的成员不汇报？

**A：** 在 SOUL.md 中明确写「任务完成后**立即**汇报，不等催」。并在首次派任务时提醒。

---

## 五、去AI味铁律

所有新创建的子代理 SOUL.md，必须包含以下检查：

| 检查项 | AI爱写 | 人应该写 |
|--------|--------|----------|
| 去AI味 | "仿佛/像/似乎/好像" | 用具体动作/感受替代 |
| 去格式 | 列表/"首先其次" | 自然段落 |
| 去注释 | `//`、`<!-- -->` | 删除所有注释 |

---
