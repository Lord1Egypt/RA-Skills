# WOOP Daily — AI Skill

> 你是否想早睡，却每晚刷手机停不下来？
> 你是否定了目标，却一拖再拖迟迟没有开始？
> 你是否想养成一个习惯，坚持了三天就放弃了？
>
> **这个 skill 可以帮助你。** 每天 5 分钟，基于 20 余年科学研究，把愿望真正变成行动。
>
> 不是一个 todo list 工具，是一次有节奏的真实对话。设计哲学借鉴自 Anthropic 官方 skills、Headspace/Noom 的 onboarding 心理学，以及疗愈聊天机器人的对话研究。

[![AgentSkills Compatible](https://img.shields.io/badge/AgentSkills-compatible-4A90D9?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyek0xMCAxN2wtNS01IDEuNDEtMS40MUwxMCAxNC4xN2w3LjU5LTcuNTlMMTkgOGwtOSA5eiIvPjwvc3ZnPg==)](https://agentskills.io)

**支持的 AI 工具：** Claude Code · Claude.ai · Gemini CLI · GitHub Copilot · VS Code · Cursor · OpenAI Codex · Roo Code · OpenHands · 以及所有支持 [AgentSkills 开放标准](https://agentskills.io)的工具

---

## 什么是 WOOP？

WOOP（Wish · Outcome · Obstacle · Plan）是纽约大学心理学教授 Gabriele Oettingen 开发的**心智对比**方法，结合了两项经过大量实验验证的技术：

- **Mental Contrasting（心智对比）**：先鲜活想象最好结果，再诚实面对内在障碍。这个"对比"动作激发真实的行动必要感，而非普通的正向思考。
- **Implementation Intentions（执行意图）**：用"如果-那么"格式制定计划，让大脑预演应对障碍，行动趋于自动化。

**研究数据：**
- 运动量提升 2 倍（vs. 单纯信息组，持续 4 个月）
- 学习时间 4.3h vs 1.5h（vs. 普通目标设定，住院医生 RCT）
- 有效领域：减重、戒烟、学业、人际、疼痛管理、习惯养成

## 支持的命令

| 命令 | 功能 |
|------|------|
| `/woop-daily` | 交互式选择模式，开始练习 |
| `/woop-daily today` | 今日 5 分钟 WOOP |
| `/woop-daily week` | 本周目标 WOOP |
| `/woop-daily habit` | 习惯养成 WOOP |
| `/woop-daily review` | 先回顾上次，再做新练习 |
| `/woop-daily reminder` | 设置每日定时提醒（基于 OpenClaw cron） |
| `/woop-daily story` | 通过寓言理解 WOOP 为什么有用（适合"我不太相信"的时候） |
| `/woop-daily today 早睡` | 携带愿望直接开始，跳过第一步提问 |

AI 也会根据上下文**自动触发**（无需输入 `/`），当你说"我想推进某事"、"帮我设定目标"、"做个 WOOP"时。

## 安装

### 方式一：ClawHub（推荐，一行）

```bash
clawhub install woop-daily
```

### 方式二：Claude Code（命令行）

```bash
git clone https://github.com/ReffWu/woop-daily.git ~/.claude/skills/woop-daily
```

### 方式二：Gemini CLI

```bash
mkdir -p ~/.gemini/skills/woop-daily && \
curl -o ~/.gemini/skills/woop-daily/SKILL.md \
  https://raw.githubusercontent.com/ReffWu/woop-daily/main/SKILL.md
```

### 方式三：其他 AgentSkills 兼容工具

将 `SKILL.md` 和 `references/` 目录放入该工具的 skills 目录即可。具体路径参见各工具文档：
- [Cursor](https://cursor.com/docs/context/skills)
- [GitHub Copilot](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [OpenAI Codex](https://developers.openai.com/codex/skills/)
- [Roo Code](https://docs.roocode.com/features/skills)
- [OpenHands](https://docs.openhands.dev/overview/skills)

### 方式四：项目级安装（仅当前项目可用）

```bash
mkdir -p .claude/skills/woop-daily/references
cp SKILL.md .claude/skills/woop-daily/
cp references/science.md .claude/skills/woop-daily/references/
```

## 使用示例

```
你：/woop-daily today

Claude：好，开始今日 WOOP 练习。你今天最想实现的一件事是什么？

你：把那篇文章的初稿写完

Claude：如果你完成了这篇初稿，最好的结果会是什么？试着想象完成那一刻——
        你会看到什么，感受到什么？

你：感觉终于卸下了一块石头，可以轻松地去做别的事

Claude：很好。现在，把那个轻松的感觉放一放，转过来看看自己的内心——
        你内心里，什么可能会阻止你今天动笔？

你：我总是会想"还没准备好"，一直拖着不开始

Claude：好，现在给这个障碍制定一个计划：如果你又冒出"还没准备好"的念头，
        你会怎么做？

你：如果我又觉得"没准备好"，那么我就先只写开头的一段，不管质量

Claude：很好。今天的 WOOP：
        愿望「把文章初稿写完」
        如果「觉得没准备好」
        你会「先只写开头一段」
        加油！
```

## Skill 设计原则

### 心理学层面（基于原始研究）
- **Obstacle 必须是内在的**：外部环境很难控制，内心障碍才能真正面对和计划
- **Outcome 用感官想象**：不是列清单，而是调动感受——心智对比起作用的关键
- **期望值感知**：信心低时 WOOP 帮你明智放弃，而不是硬撑
- **一次只做一个**：聚焦比多多益善有效

### 对话设计层面（v2.0+ 重塑）
- **Listen first, then guide**：每次 substantive share 之后先简短承认，再问下一个问题
- **Earned empathy**：先承认用户的挣扎（包括外部障碍），再温和拉回到框架
- **Read entry energy**：散乱型、专注型、好奇型、情绪型、回归型、质疑型——6 种状态 6 种开场
- **Sit with silence**：用户说"不知道"时，不要急推
- **Mark the close**：仪式化收尾（"你装了一个心理回路"），不要用日志记录作为结尾
- **Don't sell**：永不吹"科学验证"。工作本身就是证据
- **Narrative over explanation**：用户问"为什么有用"时，讲寓言不讲科学。故事传递理解的形状，理论传递事实的颗粒

## 文件结构

```
woop-daily/
├── SKILL.md                              # 主文件 / 流程地图
├── CHANGELOG.md                          # 标准变更日志
└── references/
    ├── conversation-craft.md             # 对话艺术：节奏、承认、9 种特殊情况
    ├── parable-fog-river.md              # 寓言《会造桥的少年》+ MCII 拆解
    ├── science.md                        # 心理机制：MCII = Oettingen + Gollwitzer
    └── skill-design-principles.md        # 通用经验：构建任何对话型 skill 的最佳实践
```

`SKILL.md` 是入口（地图）。三份 reference 是灵魂层——尤其 `conversation-craft.md` 决定了对话的真正品质（何时倾听、何时承认、何时沉默、8 种特殊情况的处理）。

`skill-design-principles.md` 是从 Anthropic 官方 skills、Garry Tan、Zara Zhang、高转化 onboarding 设计、疗愈聊天机器人研究中沉淀的通用经验，可被任何对话型 skill 复用。

## 理论基础

| 概念 | 描述 |
|------|------|
| Mental Contrasting | Oettingen (2000)，三种思维模式：Indulging / Dwelling / Mental Contrasting |
| Implementation Intentions | Gollwitzer (1999)，If-Then 计划的神经科学基础 |
| MCII | Mental Contrasting + Implementation Intentions，两者结合效果最优 |
| Expectancy Moderation | 期望值调节效果，低期望时帮助明智放弃 |

## 参考文献

- Oettingen, G. (2014). *Rethinking Positive Thinking: Inside the New Science of Motivation.* Current/Penguin.
- Oettingen, G., & Gollwitzer, P. M. (2010). Strategies of setting and implementing goals. In J. E. Maddux & J. P. Tangney (Eds.), *Social psychological foundations of clinical psychology.*
- Frontiers in Psychology (2021). A Meta-Analysis of the Effects of Mental Contrasting With Implementation Intentions on Goal Attainment.
- [woopmylife.org](https://woopmylife.org) — Official WOOP practice resource

## License

MIT
