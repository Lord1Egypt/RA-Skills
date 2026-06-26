# 🧬 灵魂存档 Soul Archive

> *"每一次对话都是灵魂的切片。切片够多，就能拼出完整的你。"*

[English](README.md) · **中文** · MIT License

---

数字人格持久化系统 + 主动智能体记忆引擎。可作为 [Claude Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/getting-started) / WorkBuddy Skill / 通用 Python 工具使用。

通过日常 AI 对话**沉淀你的数字灵魂副本**；同时给 AI 自己一份**主动的长期记忆**，让它别再重复同样的错误。

![灵魂存档主图](docs/zh/screenshot_header.png)

## 设计原则

- 🔒 **本地优先** —— 数据存在 `~/.agent-commons/skills_data/soul-archive/`，永不上传
- 📂 **可读可改** —— 全部明文 JSON，随时打开编辑
- 🤖 **主动伴随** —— AI 在对话中自动沉淀与召回
- 🎯 **单用户极简** —— 一个用户，一台电脑，一份灵魂

## 它采集什么

| 维度 | 内容 |
|---|---|
| 👤 **身份** | 名字 / 年龄 / 职业 / 所在地 / 生活习惯 / 数字身份 |
| 💫 **性格** | MBTI / 大五人格 / 特质 / 价值观 / 决策风格 |
| 🗣️ **语言风格** | 口头禅 / 句式 / 用词 / 幽默 / 语气词 / 类比 |
| 🧠 **知识与观点** | 关注的话题、立场、信奉的方法论框架（如"第一性原理"） |
| 📝 **记忆** | 情景记忆 + 12 种情绪触发 |
| ⚙️ **工作偏好** | 工具 / 技术栈 / 硬规则 / 输出偏好 |
| 🎯 **理想抱负** | 长期目标 / 在做的项目 / 想学的技能 / 认知盲区 |

最终成果：一个**数字灵魂副本** + 一份**任意 AI agent 都能加载的人格上下文层**。

## 六大模式

| 模式 | 做什么 | 触发 |
|---|---|---|
| 🔍 **灵魂沉淀** | 从对话中提取人格信息 | "灵魂沉淀" / 对话结束自动 |
| 💬 **灵魂对话** | 构建角色扮演 prompt，让 AI 以你的身份说话 | "灵魂对话" |
| 📊 **灵魂报告** | 生成交互式 HTML 人格画像 | "灵魂报告" |
| 🎯 **上下文注入** | 输出 ≤800 token 的人格摘要供 agent 加载 | 会话开始 |
| 🤖 **智能体记忆** | 召回相关模式 / 失败预警 / 蒸馏新模式 | 任务开始 |
| 🔄 **AI 自我改进** | 反思、自我批评、从纠正中学习 | 任务完成 / 用户纠正 |

## 快速开始

```bash
git clone https://github.com/dqsjqian/soul-archive.git
cd soul-archive

# 1. 初始化
python3 scripts/soul.py init

# 2. 查看状态
python3 scripts/soul.py status

# 3. 在 AI 对话开始时注入人格摘要
python3 scripts/soul.py context

# 4. 任务执行前查相关模式
python3 scripts/soul.py recall --task "我现在要做的事"

# 5. 生成 HTML 报告
python3 scripts/soul.py report --output ~/soul-report.html
```

> **依赖**：仅需 Python 3.10+，零第三方依赖。

## 架构

```
{SKILL_DIR}/                  ← Skill 引擎
<soul_dir>/  ← 你的灵魂数据（由 scripts/soul_paths.py 解析，详见 SKILL.md）
```

引擎是 Skill；数据放在用户主目录，所以同机器上任何 IDE / AI 工具 / Workspace 都能访问同一份灵魂。

```
<soul_dir>/
├── profile.json
├── config.json
├── identity/{basic_info,personality}.json
├── memory/
│   ├── episodic/YYYY-MM-DD.jsonl
│   ├── semantic/{topics,knowledge}.json
│   └── emotional/patterns.json
├── style/{language,communication}.json
├── workflow/preferences.json
├── aspirations.json
├── agent/{patterns.json,episodes/,corrections.jsonl,reflections.jsonl,distill_log.jsonl}
└── soul_changelog.jsonl
```

## 隐私

- 数据在 `~/.agent-commons/skills_data/soul-archive/`，明文 JSON，**永不上传**。
- 数据目录的 `.gitignore` 拦截误提交。
- Soul Chat 在本地构建 prompt；是否被外部 LLM 看到，取决于**你**用的 agent / 平台。
- 默认敏感话题（健康、财务、亲密关系）需用户确认。
- `config.json` 提供每个维度的开关——不想采的可关闭。

详见 [PRIVACY.md](PRIVACY.md)。

## 截图

### 身份卡

![身份](docs/zh/screenshot_identity.png)

### 语言指纹

![语言](docs/zh/screenshot_language.png)

### 话题与观点

![话题](docs/zh/screenshot_topics.png)

## License

MIT —— 灵魂存档是你的，代码和数据都是。
