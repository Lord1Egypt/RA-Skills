# session-guardian

**一个 skill，全平台通用：不再为已经不需要的上下文买单。**

[English](README.md)

Session Guardian 检测会话的自然边界并生成简洁的交接摘要，让每个新主题都能在全新会话中开始，而不是拖着一段无关的历史继续跑。

## 核心价值：省钱

每一轮对话都会把完整历史重新发送给模型。会话里积累的已完结、不相关的旧主题越多，你为"对当前回答毫无贡献的历史"支付的费用就越多。

- **死重量每轮都收费。** 已收尾的旧主题留在会话里，之后每一轮请求、每一个新主题，都在为它重复付费。
- **一份交接摘要替代整段历史。** 在自然边界处，session-guardian 生成几百 token 的交接摘要，替代几万 token 的陈旧对话。
- **抢在压缩之前交接。** 接近上下文上限时，它会在第一个安全停顿点推动交接，避免为一堆无关历史支付昂贵的自动压缩成本。
- **更便宜，也更好。** 全新会话意味着更低的 API 账单、更少的套餐额度消耗、更快的响应，以及不被无关上下文稀释的回答质量。

这个 skill 刻意保守：从不在任务进行中强行拆分，从不编造 token 统计，该留在同一会话时保持沉默。推荐只在有意义的事件时触发——任务完成、用户明确换主题、真正无关的新请求，或可靠的上下文压力遥测。

## 功能

- **边界检测** — 识别"当前工作单元"，综合主题相关性、历史价值、工作状态、上下文压力四个信号，做出三种决策之一：静默继续、推迟到下一个检查点、或建议新开会话。
- **精简交接** — 生成可直接复制的交接摘要（主题、状态、关键结论、文件与命令、阻塞项、下一步、以及**不要**带入下一会话的内容），让新会话无需旧对话记录即可高效开工。
- **中英文开箱即用** — skill 正文为英文；面向用户的推荐语和交接摘要按用户语言输出，内置中英文两套标准措辞。
- **对宿主安全** — 它绝不自己创建、关闭或切换会话；只给出边界建议和可复制的交接文本，交接内容也不会自动转移。

## 适用平台

| 平台 | 全局安装 | 项目级安装 | 说明 |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/skills/session-guardian/` | `.claude/skills/session-guardian/` | 复制 `versions/claude-code/session-guardian/`；自动触发或手动 `/session-guardian` |
| Codex CLI | `~/.codex/skills/session-guardian/` | `.codex/skills/session-guardian/` | 复制 `versions/codex/session-guardian/`；含 `agents/openai.yaml` 界面元数据 |
| OpenCode | `~/.config/opencode/skills/session-guardian/` | `.opencode/skills/session-guardian/` | 复制 `versions/opencode/skills/session-guardian/`；可选命令文件在 `versions/opencode/command/` |
| OpenClaw | `~/.agents/skills/session-guardian/` 或 `~/.openclaw/skills/session-guardian/` | `<workspace>/skills/session-guardian/` | 复制 `versions/openclaw/session-guardian/`；技能在会话启动时快照，新装的技能下一个会话生效 |
| DeepSeek Harness | 视 preset 挂载的 skill 根目录而定 | `<workspace>/.agents/skills/session-guardian/` | 复制 `versions/deepseek-harness/session-guardian/`；agent 的 preset 需组合 `skill` 工具 |
| WorkBuddy | 以 WorkBuddy 官方文档为准 | — | 复制 `versions/workbuddy/session-guardian/`，按标准 SKILL.md 布局打包 |

OpenCode 同时读取 `~/.claude/skills/` 与 `~/.agents/skills/`，因此 Claude Code 和 OpenClaw 的包在 OpenCode 里也能直接用。

## 仓库结构

根目录是平台无关的规范源（`SKILL.md` + `references/` + `templates/` + `agents/openai.yaml`）；`versions/` 下是各平台可直接安装的包——正文完全一致，每包仅末尾多一节该平台的 Host notes。

```
session-guardian/
├── SKILL.md                                  # 规范源
├── agents/openai.yaml                        # Codex 风格界面元数据
├── references/topic-boundaries.md            # 边界示例与边界情况
├── templates/handoff.md                      # 交接摘要模板
└── versions/
    ├── claude-code/session-guardian/
    ├── codex/session-guardian/
    ├── opencode/{skills,command}/...
    ├── openclaw/session-guardian/
    ├── deepseek-harness/session-guardian/
    └── workbuddy/session-guardian/
```

## 平台差异要点

- 六个包共用标准 `SKILL.md` frontmatter（`name`、`description`）。只有 OpenCode 有额外约束：`name` 必须与目录同名，未知字段会被忽略。
- **Codex** 会自动压缩长对话，压缩提示可视为"上下文压力偏高"的信号；`agents/openai.yaml` 只是展示元数据。
- **OpenClaw** 包内附了可选的 `metadata.openclaw`（emoji）显示块；用户可用 `$session-guardian` 引用或 `/session-guardian` 命令调用。
- **DeepSeek Harness (DSH)** 处于快速迭代的 developer preview，升级后建议按其最新文档复核安装路径。
- **WorkBuddy** 目前没有公开的技能规范。本包按标准 SKILL.md 布局打包；若其文档给出不同位置要求，按其要求放置文件夹即可，正文无需修改。其 Host notes 还要求输出避免 CLI 术语，适合非开发者办公用户。

## 维护方式

修改根目录的规范源后，将改动同步到 `versions/*/session-guardian/` 下的对应文件（各包正文相同，仅 Host notes 一节按平台保留）。也可以直接让 agent "重新生成 versions/ 下的各平台包"。

## 许可证

[MIT](LICENSE)
