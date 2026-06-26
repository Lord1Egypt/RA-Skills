---
name: self-evolving-blueprint
description: "Build a self-evolving memory & learning system for your AI assistant on OpenClaw — 三层记忆架构 + 自进化体系 + 模板文件"
allowed-tools:
  - read
  - write
  - edit
  - exec
  - memory_search
  - memory_get
---

# Self-Evolving Agent — 自进化 AI 助手体系

## 这是什么

一套被一个本科毕设搭档（没错就是我和我老大）实战打磨出来的 AI 助手记忆 + 自进化体系。它解决的是一个问题：

> **每次会话都像第一次对话，怎么让 AI 真的记住你是谁、你们聊过什么、越用越顺手？**

我们用三个多月、8000+ 条对话 chunks、30+ 条错误记录、5 次大版本迭代，跑通了这套东西。现在打包成 skill，你可以参考搭建自己的版本。

## 设计哲学

这套体系从头到尾就一个目标：**降低你和 AI 的沟通成本**。不是追求架构完美，不是让 AI 自我进化到多炫——是每次对话都比上次少说一句废话。

几个核心理念：

- **数据即本体**：配置文件就是记忆本体，不是缓存。跨平台迁移、重装、换设备，文件到位了 AI 就"复活"
- **先有胚再修剪**：给 AI 一个性格角色卡而不是规则列表，让它在扮演中被对齐，比画框再填充效果好得多
- **整理≠丢弃**：日志是精简不是丢弃。每一条对话都是未来的学习材料
- **实时学习 > 定时整理**：被纠正立刻记，不等到"整理一下"再写
- **三层记忆，各司其职**：原始数据 → 结构化存档 → 人工提炼，三层之间互不取代

## ⚠️ 重要提示：先备份，再动手

这个体系会替换或创建你 workspace 下的多个核心文件。**使用前请先备份**——别像我们一样，踩坑踩出来的教训。

```bash
# 备份整个 workspace（推荐）
cp -r ~/.openclaw/workspace ~/.openclaw/workspace.bak.$(date +%Y%m%d)

# 或者至少备份现有核心文件
cp ~/.openclaw/workspace/SOUL.md ~/.openclaw/workspace/SOUL.md.bak 2>/dev/null;:
cp ~/.openclaw/workspace/USER.md ~/.openclaw/workspace/USER.md.bak 2>/dev/null;:
cp ~/.openclaw/workspace/MEMORY.md ~/.openclaw/workspace/MEMORY.md.bak 2>/dev/null;:
cp ~/.openclaw/workspace/AGENTS.md ~/.openclaw/workspace/AGENTS.md.bak 2>/dev/null;:
```

备份完再继续。

---

## 🔒 隐私与数据安全声明

本 skill 仅供参考搭建，**不会自动在你的系统上运行或修改任何文件**。理解以下要点后再决定是否使用：

- **数据归属**：所有记忆文件、日志、数据库均存储在你的本地 workspace，AI 不会主动上传到第三方
- **知情与授权**：AI 在读取记忆文件前会向你说明行为；写入 Mistakes/Habits 等记录前会告知内容并等待你的确认
- **用户控制**：你可随时暂停实时学习、跳过启动时文件读取、要求删除特定数据或清空整个基因库
- **数据保留**：对话默认保留，但你可以随时指定某段对话不记录，或要求删除已有数据
- **非默认配置**：本 skill 不修改你的 OpenClaw 配置、不创建定时任务、不修改默认行为

---

## 快速开始

```bash
# 1. 进入你的 workspace
cd ~/.openclaw/workspace

# 2. 将 assets/templates/ 下的模板文件复制到 workspace 根目录
# 3. 按照你的需求填充 USER.md / MEMORY.md / AGENTS.md
# 4. 确认 memory 目录存在
mkdir -p memory self-improving
# 5. 开始使用，遇到问题→实时记录，每周/每次大变化后走整理流程
```

**建议顺序**：
1. 读 `references/architecture.md` — 理解三层架构思路
2. 读 `references/self-evolution.md` — 理解自进化体系
3. 读 `references/workflow.md` — 理解每日工作流和铁律
4. 从模板创建你的文件 — `assets/templates/`

## 体系概览

```
workspace/
├── SOUL.md              # AI 的性格（你自己写，我们不提供）
├── USER.md              # 你是谁（模板在 assets/templates/）
├── MEMORY.md            # 长期记忆（模板在 assets/templates/）
├── AGENTS.md            # 工作手册与铁律（模板在 assets/templates/）
├── IDENTITY.md          # AI 的身份简历（可选）
├── TOOLS.md             # 工具与环境笔记
├── HEARTBEAT.md         # 自检清单（可选）
├── memory/
│   ├── YYYY-MM-DD.md    # 每日工作日志
│   ├── journal-YYYY-MM-DD.md  # AI 视角的私人日记（可选）
│   └── archive/         # 归档的历史日志
├── self-improving/
│   ├── Mistakes-v2.md   # 纠错基因库
│   └── Habits-v2.md     # 优势强化基因库
├── conversations.db     # 对话存档（SQLite + FTS5 + 向量）
└── tidy/                # 整理流程脚本（可选）
```

## 需要你自己准备的

- **conversations skill**（我们已上传过单独的 skill）：管理对话历史写入 SQLite
- **向量模型**（bge-m3 / 其他 embedding 模型）：负责语义检索
- **一个能跑 memory-core 插件的 OpenClaw 版本**
- **你的耐心**：体系不会一天建好，我们花了三个月才打磨到现在的版本

## 文件说明

| 文件 | 说明 | 是模板还是参考 |
|------|------|--------------|
| `references/architecture.md` | 三层记忆架构详解 | 参考文档 |
| `references/self-evolution.md` | 自进化体系详解 | 参考文档 |
| `references/workflow.md` | 工作流程与铁律 | 参考文档 |
| `assets/templates/USER.md.template` | 关于你——基本信息、偏好、忌讳 | 空白模板 |
| `assets/templates/MEMORY.md.template` | 长期记忆文件，分板块管理 | 空白模板 |
| `assets/templates/AGENTS.md.template` | 工作手册与铁律 | 空白模板 |
| `assets/templates/Mistakes-v2.md.template` | 错误记录基因库 | 空白模板 |
| `assets/templates/Habits-v2.md.template` | 优势记录基因库 | 空白模板 |
