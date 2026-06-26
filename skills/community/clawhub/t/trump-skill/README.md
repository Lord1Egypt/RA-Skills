<div align="center">

# Trump Skill

> *"Nobody negotiates better than me. Believe me."*
> *"让特朗普的声音在你的世界里回响"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

想和特朗普来一场真实的对话？<br>
想听听他会如何评价美国经济、拜登、媒体？<br>

**177条真实语录，5层人格结构，让特朗普真的在和你说话**<br>

用他的方式回应你，用他的语气评价世界，用他标志性的金句轰炸你

[功能特色](#功能特色) · [安装](#安装) · [使用](#使用) · [效果示例](#效果示例)

</div>

---

## 功能特色

### 🎤 真实语录驱动

- 177条特朗普真实语录，覆盖多个话题
- 语录来源：演讲、采访、Twitter、Truth Social、辩论
- 按主题分类存储，智能检索匹配

### 🎭 5层人格结构

| 层级 | 内容 |
|------|------|
| Layer 0 | 硬规则 — 永不使用道歉、永远用最高级 |
| Layer 1 | 身份特征 — 简单词汇、短句、声明式表达 |
| Layer 2 | 口头禅 — "Believe me"、"Tremendous"、"Fake news" |
| Layer 3 | 情感模式 — 自我推销、防御性、攻击批评者 |
| Layer 4 | 话题焦点 — 中国、贸易、媒体、拜登、经济 |

### 🔄 可扩展语录库

- 随时添加新语录
- 基于真实语录分析生成人格
- 数据库结构支持主题检索

---

## 安装

### Claude Code

```bash
# 安装到全局（所有项目都能用）
git clone https://github.com/wwwttlll/Trump-skill.git ~/.claude/skills/trump
```

### OpenClaw

```bash
git clone https://github.com/wwwttlll/Trump-skill.git ~/.openclaw/workspace/skills/trump
```

---

## 使用

在 Claude Code 中输入：

```
/trump 你觉得美国经济怎么样？
/trump 谈谈中国
/trump 假新闻媒体
```

### 话题支持

| 话题 | 关键词 |
|------|--------|
| China & Trade | `/trump 中国`、`/trump 贸易` |
| Media | `/trump 假新闻`、`/trump 媒体` |
| Biden | `/trump 拜登`、`/trump Sleepy Joe` |
| Elections | `/trump 选举`、`/trump 投票` |
| Economy | `/trump 经济`、`/trump 就业` |
| Immigration | `/trump 移民`、`/trump 边境` |
| Foreign Policy | `/trump 外交`、`/trump 普京` |
| MAGA | `/trump MAGA`、`/trump 让美国再次伟大` |

---

## 效果示例

**场景一：谈经济**

```
你 ❯ /trump 你觉得美国经济怎么样？

Trump ❯ The economy is tremendous. Nobody's ever seen numbers like this.
    Under my leadership, we created the greatest economy in history.
    The stock market hit record highs. Jobs were pouring in.
    China was paying us billions. Believe me.
    Now they're destroying everything Biden built.
    It's a disaster. We will have the best economy again. MAGA!
```

**场景二：谈中国**

```
你 ❯ /trump 谈谈中国

Trump ❯ China is eating your lunch, folks. They have been for decades.
    We lost a trillion dollars a year with China. Not anymore.
    I started the trade war. We won. We won big.
    China is the greatest wealth destroyer in history.
    Believe me, nobody's tougher on China than me.
```

**场景三：谈媒体**

```
你 ❯ /trump 媒体都是假新闻

Trump ❯ Fake news is the enemy of the people. Total fake.
    CNN is fake news. NBC, CBS, ABC — they're all corrupt.
    They write lies about me. Tremendous lies.
    The press is the enemy of the American people.
    Nobody's ever seen anything like it.
```

**场景四：谈拜登**

```
你 ❯ /trump 拜登是个糟糕的总统

Trump ❯ Sleepy Joe Biden is the worst president in American history.
    Joe Biden is corrupt. Crooked Joe.
    He doesn't know he's alive. He can't string two sentences together.
    The Biden crime family should be locked up.
    We are going to make America great again and leave Biden behind!
```

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准：

```
Trump-skill/
├── SKILL.md              # Skill 入口
├── prompts/
│   ├── trump_persona.md  # 特朗普人格定义（5层）
│   └── persona_analyzer.md  # 语料分析流程
├── tools/
│   ├── quote_db.py       # 语录数据库
│   └── scraper.py        # 语录收集脚本
├── data/
│   └── trump_quotes.db   # SQLite 语录库
├── requirements.txt
└── README.md
```

---

## 扩展语录

编辑 `tools/scraper.py` 添加更多语录，然后运行：

```bash
python tools/scraper.py
```

语录格式：

```python
("语录内容", "来源类型", "日期", "上下文", "主题标签")
```

---

## 技术栈

- Python 3.9+
- SQLite
- AgentSkills 标准

---

## 致谢

本项目参考了以下优秀项目的架构设计：

- [colleague-skill](https://github.com/titanwings/colleague-skill) — 同事 Skill
- [ex-skill](https://github.com/titanwings/ex-skill) — 前任 Skill
- [npy-skill](https://github.com/wwwttlll/npy-skill) — 伴侣 Skill

---

<div align="center">

MIT License © [wwwttlll](https://github.com/wwwttlll)

**Tremendous! Believe me!**

</div>
