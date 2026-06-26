# ClawFlows Workflow Format Guide | ClawFlows Workflow 格式指南

## Overview | 概述

ClawFlows 是一个多技能自动化流程市场，工作流以 YAML 文件定义，提交到 GitHub Registry 经 PR 审核后上线。

Workflow 与 Skill 的核心区别：
- **Skill**：本地写好，`clawhub publish` 直接发布，即时生效
**Workflow**：本地写好，需 fork registry 提 PR，等审核合并后才上线

---

## Two Formats | 两种格式

Every automation comes in two flavors:  
每个自动化都有两种格式：

| Format | 用途 | Token 消耗 |
|--------|------|-----------|
| **Abstract（能力型）** | 跨平台可移植，描述需要哪些 capabilities | 0 |
| **Lobster-Ready（直接运行型）** | 直接可跑，deterministic shell pipelines | 0 |

---

## File Structure | 目录结构

```
automations/<workflow-name>/
├── automation.yaml    # Workflow 定义
├── metadata.json      # 搜索/展示元数据
└── README.md         # 文档（英中文双语）
```

---

## automation.yaml | Workflow 定义

```yaml
name: my-workflow           # 唯一标识，slug 格式（小写字母、数字、连字符）
description: One-line description  # 一行描述，用于搜索结果
author: your-github-username
version: 1.0.0             # 语义化版本

requires:
  - capability: capability-name  # 所需能力，非具体 skill 名

trigger:
  manual: true               # manual=true 表示手动触发；或 schedule: "0 9 * * *"

config:
  setting_name:
    description: "用户可配置的设置项说明"
    default: default_value
    required: false           # 是否必填

steps:
  - name: step-name          # 步骤名，唯一标识
    capability: capability-name
    method: methodName
    args:
      key: value
    capture: output_var      # 捕获输出，供后续步骤使用
```

### Key Fields | 关键字段

| 字段 | 说明 |
|------|------|
| `name` | URL-safe slug（小写、连字符）|
| `requires[].capability` | 引用 capability，不写具体 skill 名 |
| `trigger.schedule` | Cron 表达式，定时触发 |
| `trigger.manual` | true 表示手动触发 |
| `steps[].capture` | 捕获输出为变量，`${变量名}` 引用 |
| `steps[].condition` | JavaScript 表达式，用于条件判断 |
| `steps[].onFalse` | 条件为 false 时的动作（exit/skip/skip-to:step） |

---

## metadata.json | 元数据

```json
{
  "name": "workflow-name",
  "description": "One-line description of what it does",
  "author": "your-github-username",
  "version": "1.0.0",
  "requires": ["capability-1", "capability-2"],
  "trigger": "schedule",
  "schedule": "0 9 * * *",
  "tags": ["tag1", "tag2", "tag3"]
}
```

---

## README.md | 文档规范

```markdown
# Workflow Name | 工作流名称

Brief description. 简短中文描述。

## What It Does | 功能说明

Detailed explanation of the workflow.

## Requirements | 必要条件

- **capability-name**: Description of what it provides.

## Configuration | 配置项

| Setting | Description | Default |
|---------|-------------|---------|
| `setting` | Description | `default` |

## Example Output | 输出示例

Screenshots, sample notifications, or output examples.

## Author

Created by [Your Name](https://github.com/username)
```

---

## Local Install & Run | 本地安装与运行

安装后路径：`~/.openclaw/workspace/automations/<workflow-name>/`

常用命令：
```bash
clawflows install <workflow-name>     # 从 ClawFlows Registry 安装
clawflows run <workflow-name>          # 运行
clawflows run <workflow-name> --dry-run  # 预览（不实际执行）
clawflows check <workflow-name>         # 检查所需 capabilities
clawflows list                         # 列出已安装的工作流
clawflows logs <workflow-name>          # 查看运行日志
```

---

## Publishing Steps | 提交流程

1. Fork [github.com/Cluka-399/clawflows-registry](https://github.com/Cluka-399/clawflows-registry)
2. 在 fork 中创建 `automations/<workflow-name>/`
3. 放入 `automation.yaml`、`metadata.json`、`README.md`
4. Commit 并 Push 到 fork
5. 提交 PR 到主仓库
6. 等官方审核合并
7. 合并后 GitHub Actions 自动重建 index，出现在 clawflows.com

---

## Capability Reference | 能力参考

常用 capabilities：
- `database` — 数据存储（SQLite）
- `chart-generation` — 图表生成
- `calendar` — 日历/日程
- `tts` — 文字转语音
- `notification` — 通知推送

Browse all: https://clawflows.com/capabilities/

---

## Naming Rules | 命名规则

- **Slug**：小写字母、数字、连字符（无下划线和空格）
  - ✅ `douyin-manager`
  - ❌ `Douyin_Manager`
- **Display name**：英文在前，中文在后
  - `Douyin Manager | 抖音管理者`
- **Description**：一行，英文为主，中文辅助，控制在 150 字符内

---

## Writing Rules | 写作规范

- **Abstract** 格式引用 capabilities，不写死具体 skill
- **Config** 配置项让用户无需改代码即可自定义
- **Bilingual**：README.md 使用英中文双语
- **去标识化**：README.md 不暴露个人位置、姓名、API 密钥
- **Approval Gates**：关键操作步骤用条件判断暂停，等用户确认

---

## Practical Experience Notes | 实践经验总结

Based on real workflow creation (Bilibili Manager | B站管理者). 基于实际工作流创建经验。

### Do Nots | 避免事项

| Issue | Problem | Solution |
|-------|---------|----------|
| Runtime data in workflow file | Workflow 文件包含日志逻辑 | Runtime data belongs to user workspace, not workflow definition. 日志是运行时数据，存放在用户工作区，不在工作流定义中 |
| Duplicate content | 描述重复（中英各写一遍然后又写一遍）| English and Chinese should complement each other, not repeat. 英文和中文应互补，不是重复 |
| Changelog in workflow | 工作流文件包含更新日志 | Changelog belongs to PR/commit, not workflow file. 更新日志属于 PR/commit，不在工作流文件中 |
| Embed skill logic | 工作流直接嵌入 skill 实现代码 | Workflow declares capabilities, skill provides implementation. 工作流声明 capabilities，skill 提供实现 |
| Local paths in public docs | 文档写死本地路径 | Use relative or generic references. 使用相对路径或通用引用 |

### Name & Description | 名称与描述

```yaml
# Good | 正确
name: bilibili-manager
description: "Check DMs, browse content, auto-reply, heartbeat patrol. | B站管理者：私信管理、内容浏览、自动回复、心跳巡逻。"

# Avoid | 避免
name: morois-bilibili-dm  # Personal name | 个人名称
description: "B站私信管理器"  # Single language only | 只有单语言
```

### Skill Reference | Skill 引用

```yaml
# ===== Skill Reference | Skill 引用 =====
# First check if already installed locally | 先检测本地是否已安装
# If not installed: clawhub install bilibili-messager | 未安装则：clawhub install bilibili-messager
# Operations follow the skill, workflow handles flow control | 具体操作以skill为准，工作流仅负责流程控制
```

### Workflow Structure | 工作流结构

```yaml
# ===== Workflow =====
name: workflow-name
description: "English first | 中文描述"
version: 1.0.0

requires:
  - capability: browser
  - capability: notification

config:
  auto_mode:
    description: "Auto mode: no confirmation needed | 自动模式：无需确认"
    default: false

steps:
  # Stage 1: Preparation | 阶段1：准备
  # Stage 2: Execute core logic | 阶段2：执行核心逻辑
  # Stage 3: Report result | 阶段3：汇报结果
```

### Configuration Design | 配置设计原则

| Principle | Description |
|----------|-------------|
| User intent detection | Parse user input to determine mode (manual/auto/heartbeat) |
| Configurable intervals | Use minutes not seconds for heartbeat (e.g., 30, 60, 120) |
| Clear defaults | Default to safest option (manual mode) |
| Mode introduction | Auto-show mode guide on first run |

### Bilingual Format | 双语格式规范

**Title**: `English Name | 中文名`

**Description**: English sentence first, then Chinese translation. 不要重复内容。
```
Check DMs, browse content, auto-reply, heartbeat patrol. | B站管理者：私信管理、内容浏览、自动回复、心跳巡逻。
```

**Features table**:
```markdown
| Feature | Description | 功能 |
|---------|-------------|------|
| 📬 Check DM List | Get conversation list | 检查私信列表 |
```

**PR Description**:
```markdown
## Workflow Name | 工作流名称

English description first. | 中文描述。

### Features | 功能说明
| Feature | Description | 功能 |
|---------|-------------|------|
```

### Git Commit & PR | Git 提交与 PR

```bash
# Commit message
git commit -m "feat: add workflow-name | 工作流名称"

# PR title
gh pr create --title "feat: workflow-name | 工作流名称"
```

### Publishing Checklist | 发布检查清单

- [ ] Name is URL-safe slug | 名称是 URL 安全的 slug
- [ ] Description is bilingual | 描述是双语的
- [ ] README.md is full bilingual | README.md 是完整双语的
- [ ] No runtime data in workflow file | 工作流文件不包含运行时数据
- [ ] No local paths in public docs | 公开文档不含本地路径
- [ ] No personal names/keys | 无个人名称/密钥
- [ ] Skill reference mentions local-check-first | Skill 引用提到先检测本地
- [ ] Config descriptions are bilingual | 配置描述是双语的
- [ ] YAML syntax validated | YAML 语法已验证
