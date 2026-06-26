<div align="center">

**中文** · [![English](https://img.shields.io/badge/English-README.en.md-111827?style=flat-square)](./README.en.md)

# token-efficient-task-router

#### 一个面向智能体的低消耗任务路由与执行控制 Skill

[![Version](https://img.shields.io/badge/version-v0.6.8-2563EB?style=for-the-badge)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/License-MIT-0F766E?style=for-the-badge)](./LICENSE)
[![Modes](https://img.shields.io/badge/Modes-Ask%20%7C%20Plan%20%7C%20Craft%20%7C%20Expert-7C3AED?style=for-the-badge)](./SKILL.md)
[![Token](https://img.shields.io/badge/Token-Efficient-F59E0B?style=for-the-badge)](./GUIDE.md)

![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Supported-2563EB?style=flat-square)
![iMA Copilot](https://img.shields.io/badge/iMA_Copilot-Supported-0F766E?style=flat-square)
![CodeBuddy](https://img.shields.io/badge/CodeBuddy-Supported-7C3AED?style=flat-square)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Supported-E11D48?style=flat-square)

</div>

它不是一个业务 Skill，而是一个“控制型 Skill”。

它的作用是让智能体在真正开始消耗 token、展开长篇输出、读取大量上下文、修改文件或进入高风险操作之前，先判断任务是否明确、是否复杂、是否值得继续深挖，然后再决定该怎么做。

---

## 这是什么

`token-efficient-task-router` 的定位是：

- Token 成本控制器
- 任务模式路由器
- 执行前安全闸门
- 智能体 ROI 管理器

它会帮助智能体先做这些判断：

- 任务是否足够明确
- 当前任务更适合诊断、规划、直接执行还是建议专家介入
- 是否需要用户确认
- 是否只需要样本、下一步结论或分阶段推进，而不是一上来全量完成

## 它解决什么问题

很多智能体在真实工作里会出现同一类低效问题：

- 还没确认需求，就先读很多材料
- 还没确认范围，就先输出很长的内容
- 还没确认文件边界，就先动文件
- 还没判断是否值得，就先全量执行

这个 Skill 的目标不是让智能体更保守，而是让智能体更划算、更稳、更接近用户的真实需求。

## 适合什么场景

当你遇到下面这些任务时，这个 Skill 很有价值：

- 用户需求有些模糊，不适合直接执行
- 任务可能涉及文件、文件夹、项目结构或知识库
- 用户希望减少试错、降低 token 消耗
- 任务可能需要在 Ask、Plan、Craft、Expert 之间做判断
- 任务存在重构、批量处理、长文输出、知识库整理等高成本路径

## 不适合什么场景

这个 Skill 不应该拖慢本来就很简单的任务。

通常不需要重型路由流程的任务包括：

- 一句话润色
- 简短翻译
- 单条命令解释
- 很短的模板生成
- 明确、低风险、一次即可完成的小任务

## 核心能力

### 1. 四种模式路由

- `Ask Mode`：诊断、解释、风险分析、下一步建议
- `Plan Mode`：先规划范围，再等待确认
- `Craft Mode`：明确小任务的快速交付
- `Expert Mode`：在继续试错不划算时建议专家视角介入

### 2. 交互式任务路由确认

当任务模糊、范围大、可能高成本或可能涉及文件时，它不会默认替用户拍板，而是先让用户确认：

- 复杂度
- 工作模式
- 输出详细度

### 3. 渐进式推进

默认优先：

`判断 -> 样本 -> 分阶段 -> 全量`

而不是一上来就“全部做完”。

### 4. 文件安全闸门

未经确认，不鼓励：

- 覆盖核心文件
- 删除文件
- 批量重命名
- 批量移动
- 改动部署配置
- 改动数据库
- 大面积未确认重写

### 5. Token 预算控制

支持四种预算模式：

- `Micro`
- `Standard`
- `Deep`
- `Artifact`

## 平台适配

### WorkBuddy

更偏向保守文件处理，优先只读分析、范围确认和样本批次。

### iMA Copilot

更偏向缩小知识范围，优先最相关材料、短结论和分组输出，而不是默认长篇报告。

### CodeBuddy

更偏向限制读代码范围、修改范围和测试范围，避免扫全仓和大面积重构。

## 示例提示词

```text
请判断这个任务应该进入 Ask、Plan、Craft 还是 Expert 模式。
```

```text
请先用 Plan Mode 规划，不要直接修改文件。
```

```text
这是一个明确的小任务，请直接用 Craft Mode 给结果。
```

```text
这个报错先用 Ask Mode 诊断，不要改代码。
```

```text
请用最省 token 的方式回答，只给我下一步。
```

## 安装方式

### 文件夹方式

将 `token-efficient-task-router/` 目录放入支持 Skill 的本地目录、工作目录或上传目录即可。

### 压缩包方式

当前可发布产物：

- `token-efficient-task-router-v0.6.8.zip`
- `token-efficient-task-router-v0.6.8.skill`

本地测试仍保留最新别名：

- `token-efficient-task-router.zip`
- `token-efficient-task-router.skill`

### Codex 本地安装

如需在 Codex 本地长期复用，可放入：

```text
~/.codex/skills/token-efficient-task-router
```

安装后建议重启一次应用，使新 Skill 稳定生效。

### WorkBuddy 安装

WorkBuddy 官方文档提供的是“技能市场导入本地技能包”的方式。推荐步骤：

1. 在 WorkBuddy 中打开“技能市场”
2. 点击“添加技能”或“上传技能”
3. 选择本地技能包文件，推荐使用 `token-efficient-task-router-v0.6.8.zip`
4. 导入完成后，在已安装技能列表中确认该 Skill 已启用

更稳妥的使用建议：

- 只在当前任务需要时启用这个 Skill
- 如果你准备上传到 SkillHub，建议使用专门给 SkillHub 的精简 zip 包

### CodeBuddy 安装

CodeBuddy 官方文档支持两类目录：

1. 用户级 Skills：`~/.codebuddy/skills/`
2. 项目级 Skills：`.codebuddy/skills/`

推荐两种安装方式：

#### 方式 1：用户级安装

把整个 `token-efficient-task-router/` 文件夹复制到：

```text
~/.codebuddy/skills/token-efficient-task-router
```

#### 方式 2：项目级安装

如果你希望只在某个项目里使用，把整个文件夹复制到：

```text
<project-root>/.codebuddy/skills/token-efficient-task-router
```

安装后可以在 CodeBuddy 里使用 `/skills` 查看是否已加载。

### QClaw 安装

QClaw 的公开资料说明它接入了 ClawHub 和 GitHub Skills 生态，并支持从 ClawHub 一键安装技能包。

因此更推荐的安装方式是：

#### 方式 1：通过 ClawHub / 技能市场安装

如果你的 QClaw 版本带有 Skills 市场或 ClawHub 入口，优先直接通过市场安装。

#### 方式 2：通过 GitHub 技能仓库导入

如果你的 QClaw 版本支持从 GitHub 技能生态读取技能，可以使用当前 Skill 仓库或发布包进行导入。

#### 方式 3：按 OpenClaw 兼容目录手动安装

由于 QClaw 基于 OpenClaw 生态构建，如果你的环境支持手动技能目录，也可以按 OpenClaw 兼容方式放入：

```text
~/.openclaw/skills/token-efficient-task-router
```

或当前工作区：

```text
<workspace>/skills/token-efficient-task-router
```

如果你走的是手动目录方式，建议重启 QClaw 或开启新会话，让技能重新加载。

## 仓库结构

```text
token-efficient-task-router/
├── .gitignore
├── SKILL.md
├── LICENSE
├── README.md
├── README.en.md
├── GUIDE.md
├── GUIDE.en.md
├── VERSION
├── CHANGELOG.md
├── references/
├── templates/
├── examples/
├── tests/
└── scripts/
```

## 公开文档

- [README.md](./README.md)：中文首页说明
- [README.en.md](./README.en.md)：英文首页说明
- [GUIDE.md](./GUIDE.md)：中文对外行为说明
- [GUIDE.en.md](./GUIDE.en.md)：英文对外行为说明
- [CHANGELOG.md](./CHANGELOG.md)：版本演进记录
- [LICENSE](./LICENSE)：开源许可

## 版本与授权

- 当前版本：`v0.6.8`
- 许可证：`MIT`

---

更多英文说明请查看 [README.en.md](./README.en.md)。
