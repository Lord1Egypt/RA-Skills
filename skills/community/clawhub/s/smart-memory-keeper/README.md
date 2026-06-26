# 🐰 smart memory-keeper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.5.0-blue)](https://github.com/porkapple/memory-keeper/releases)
[![Author](https://img.shields.io/badge/author-爱兔%20aitu-orange)](https://github.com/porkapple)

---

你有没有这种经历——

跟 Openclaw 聊了两个小时，终于把它"调教好了"：它懂你的项目、懂你的习惯、懂你想要什么。

然后因为某个任务卡住了，你手滑按了 `/new`。

它又变成什么都不知道的陌生人了。

**memory-keeper 解决的就是这个问题。**

它不需要额外的服务器、不需要数据库、不消耗你额外的 token——它只是教会 AI 把重要的事写下来，下次见面时第一件事就去读这些笔记。

就像一个有随手记笔记习惯的助手，和一个什么都靠脑子记的助手，时间长了差距会越来越大。

---

## ⚠️ 安装前须知

安装 memory-keeper 后，需要**手动**完成一次初始化配置：

- 在 `AGENTS.md` 里追加 session 启动时的记忆加载规则
- 在 `HEARTBEAT.md` 里追加每日日记检查任务

这是 memory-keeper 工作的原理——它通过修改你的 Agent 启动配置，让 AI 每次 session 开始时自动读取记忆文件。**所有修改内容在 SKILL.md 中完整列出，安装前可以逐行审查。没有任何隐藏操作，也不需要任何额外凭证。**

如果你不希望修改全局配置，可以只手动复制 `SKILL.md` 中的相关规则，选择性地应用。

---

## 📦 安装

### 方式一：通过 OpenClaw Skill 安装（推荐）

```bash
openclaw skills install smart-memory-keeper
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/porkapple/memory-keeper.git ~/.openclaw/workspace/skills/memory-keeper
```

安装后，按照 `SKILL.md` 中"安装后配置"章节的说明，完成 `AGENTS.md` 和 `HEARTBEAT.md` 的配置（必做一次）。

---

## 🧠 三层记忆结构

| 层级 | 文件 | 内容 | 加载时机 |
|------|------|------|----------|
| 🔥 热层 | `memory/tasks.md` | 进行中的任务状态 | 每次 session 启动 |
| 🌡️ 温层 | `memory/YYYY-MM-DD.md` | 最近 7 天的日记 | 每次 session 启动 |
| 🧊 冷层 | `MEMORY.md` | 项目索引 | 提到具体项目时 |

---

## ✨ 核心特性

- **工作状态恢复**：`tasks.md` 记录"做到哪一步"和"下一步干什么"，新 session 秒接上下文
- **每日日记**：按主题归类，只写有价值的内容；包含"已验证的方法"和"待关注风险"两个关键章节
- **记忆三段式**：经验教训必须写「规则 + 为什么 + 触发场景」，知道原因才能判断边界情况
- **记对，也记错**：不只记纠正，也记用户认可的方向——只记错误会让 AI 越来越保守
- **Dream 整理**：每 7 天自动整理记忆，修正漂移、合并重复、归档旧日记
- **绝对时间**：所有日期强制用 `YYYY-MM-DD`，禁止"下周"、"明天"等相对表达

---

## 📁 文件结构

安装并初始化后，工作目录结构如下：

```
~/.openclaw/workspace/
├── MEMORY.md                    # 项目索引（冷层）
├── memory/
│   ├── tasks.md                 # 任务状态（热层）
│   ├── dream-state.json         # Dream 整理状态追踪
│   ├── 2026-04-03.md            # 每日日记（温层）
│   ├── 2026-04-02.md
│   └── archive/                 # 30天前的旧日记归档
│       └── 2026-03-01.md
└── skills/
    └── memory-keeper/
        ├── SKILL.md                  # 核心流程与触发规则
        └── references/
            ├── formats.md            # tasks.md / 日记 / MEMORY.md 格式规范
            ├── dream-guide.md        # Dream 整理四阶段详解
            └── install-snippets.md   # AGENTS.md / HEARTBEAT.md 待追加内容
```

---

## 🔄 Dream 整理机制

触发条件：距上次整理超过 **7 天** 且积累了 **3 个工作日 session**。

触发后执行四阶段整理：
1. **定向**：扫描近期任务和日记，明确当前状态
2. **收集**：找出值得长期保留的经验和方法
3. **整合**：写入 MEMORY.md，修正漂移的旧记忆（矛盾时直接重写，不并存）
4. **修剪**：归档 30 天前的日记，MEMORY.md 保持 200 行以内

---

## 📝 License

[MIT License](./LICENSE)

---

## 👤 作者

**爱兔 aitu** - 安兔兔的AI员工

> "记忆不是备忘录，是决策参考。"
