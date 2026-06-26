---
name: writing-agent-creator
description: |
  Generate writing agent configurations for OpenClaw. Use when the user wants to:
  (1) Create specialized writing agents (tech, marketing, academic, business, creative)
  (2) Add custom agent templates (persisted, won't be overwritten)
  (3) Generate sub-agent spawn instructions
  (4) List available agent templates
  IMPORTANT: This skill GENERATES configs - it does NOT modify user's existing files.
  User custom templates are saved to ~/.openclaw/workspace/agent-templates/
metadata:
  openclaw:
    emoji: "✍️"
    user-invocable: true
---

# Writing Agent Creator

Create customized writing agents with persistent user templates.

## Template System

### 📁 User Templates (Highest Priority)
```
~/.openclaw/workspace/agent-templates/
```
- ✅ **Persistent** - Never overwritten by skill updates
- ✅ **Highest priority** - Override system templates with same ID
- ✅ **User full control** - Create, edit, delete anytime
- ✅ **Auto-detected** - Skill automatically finds and loads them

### 📁 System Templates (Fallback)
```
~/.openclaw/workspace/skills/writing-agent-creator/references/agent-registry.md
```
- Built-in templates
- Updated with skill updates
- Cannot be modified by user directly
- User can override by creating user template with same ID

### Template Resolution Order

1. Check user templates first (`~/.openclaw/workspace/agent-templates/`)
2. If not found, check system templates
3. If user template has same ID as system template → **user wins**

## Commands

### List Templates
```
/writing-agent-creator list
```
Shows all available templates (system + user)

### Create Agent
```
/writing-agent-creator create
```
Interactive flow to select and generate agent config

### Add Custom Template
```
/writing-agent-creator add
```
Add your own template, saved to user-templates/

### Remove Template
```
/writing-agent-creator remove <id>
```
Remove user template (cannot remove system templates)

## Workflow

### 1. List Available Templates

```
请选择你需要的 Agent（可多选）：

【系统模板 - 不可删除】
[1] 🔧 科技写作
[2] 📢 营销文案
...

【用户模板 - 可自定义】
[12] 🆕 用户自定义模板1
[13] 🆕 用户自定义模板2
...

输入编号，或输入 'add' 添加新模板：
```

### 2. Select and Configure

- User selects template IDs
- Skill gathers requirements
- Generates configuration

### 3. Choose Output Format

**A) SOUL.md 片段** → Copy-paste into existing SOUL.md
**B) Sub-agent 指令** → Ready-to-use spawn commands
**C) 保存为用户模板** → Add to user-templates/ for reuse

## Adding Custom Templates

### Method 1: Interactive

```
用户: /writing-agent-creator add

助手: 创建自定义模板：

1. 模板名称：如"产品经理"
2. 表情符号：如 📦
3. 触发词：如 [产品] [PRD]
4. 用途描述
5. 风格要点
6. 系统提示词

请提供以上信息：
```

### Method 2: Direct File

Create file: `~/.openclaw/workspace/agent-templates/<id>.md`

```yaml
---
id: product-manager
name: 产品经理
emoji: 📦
trigger: [产品, PRD, 需求]
description: PRD文档、需求分析、产品规划
use_cases:
  - PRD 文档
  - 需求分析
  - 产品路线图
style:
  tone: 专业、结构化、数据驱动
  key_points:
    - 用户价值明确
    - 数据支撑决策
    - 可执行性强
prompt_template: |
  你是一名资深产品经理。

  ## 工作原则
  1. 用户价值 - 每个功能都要回答"用户价值是什么"
  2. 数据驱动 - 用数据支撑决策
  3. 可执行性 - 输出可落地的方案

  ## 输出格式
  - PRD 标准结构
  - 优先级明确
  - 验收标准清晰
---
```

## Template Priority

When same ID exists:
1. **User template wins** - allows overriding system templates
2. User can effectively "customize" system templates by creating same ID

## Output Formats

### A. SOUL.md 片段

```markdown
## 🔧 科技写作模式

[配置内容]

使用：[技术] 写一篇教程
```

User copies to their SOUL.md

### B. Sub-agent 指令

```
sessions_spawn(
  task: """你是科技写作专家...""",
  model: "zai/glm-4.7-flash",
  mode: "session"
)
```

### C. 保存为用户模板

Auto-saves to `~/.openclaw/workspace/agent-templates/<id>.md`

## File Structure

```
~/.openclaw/
├── workspace/
│   ├── SOUL.md              # 用户主 Agent 人格
│   └── agent-templates/     # 用户自定义模板（持久化）
│       ├── product-manager.md
│       ├── data-analyst.md
│       └── ...
└── skills/
    └── writing-agent-creator/
        ├── SKILL.md
        └── references/
            └── agent-registry.md  # 系统模板
```

## Example Session

```
用户: 帮我创建一个数据分析 Agent

助手: [检测到可能是自定义需求]

是否要创建为可复用的模板？

[Y] 是，保存为用户模板
[N] 否，只生成一次性配置

用户: Y

助手: 请提供：
1. 模板名称：数据分析
2. 触发词：[数据] [分析]
3. 用途：SQL查询、数据分析报告
4. 风格：精确、可视化、业务导向

用户: [提供信息]

助手: ✅ 已创建用户模板：数据分析
保存位置：~/.openclaw/workspace/agent-templates/data-analyst.md

生成 Sub-agent 指令：
sessions_spawn(
  task: """你是数据分析专家...""",
  model: "zai/glm-4.7-flash"
)
```

## Notes

- User templates persist across skill updates
- System templates may change with skill updates
- User can override system templates with same ID
- Templates are markdown files, easy to edit manually
