# 🐉 SagaSmith

[English](README.md) | [中文](README-cn.md)

**自主 D&D 5e AI 地下城主** — 战役管理 · 模组生成 · 自主带团

> *"规则书为经文，模组为地图，骰子为审判官。"*  
> — 明萨拉·班瑞，SagaSmith 默认 DM

SagaSmith 是一个跨平台 AI 跑团主持人 skill 包。它把完整的 D&D 5e DM 能力——战役生命周期管理、SRD 规则裁判、模组自动生成、角色创建与升级——打包为可安装的 AI agent skill，支持 NanoBot / OpenClaw / Hermes / Claude Code 等任意兼容 SKILL.md 标准的平台。

---

## 生态

| 仓库 | 定位 |
|------|------|
| 📦 **SagaSmith-skills**（本仓库） | 全家桶 skill 插件包 |
| 🎲 [SagaSmith-agent](https://github.com/dajiaohuang/SagaSmith-agent) | 完整 AI DM 运行时 |
| ✍️ [SagaSmith-module-gen-skills](https://github.com/dajiaohuang/SagaSmith-module-gen-skills) | 独立模组生成器 |

---

## 为什么是 SagaSmith

大多数 D&D AI 工具只做一件事：掷骰、查规则、或者写一段描述。SagaSmith 是**完整的 DM**：

- 🏛️ **战役管理** — SQLite/PostgreSQL 数据库驱动，完整的 campaign CRUD、Snapshot 存档/读档/校验/撤销、事件日志、模组进度追踪
- 🎲 **规则裁判** — BGE-M3 Dense Vector 检索 SRD 5.2.1（20 个规则文件，CC-BY-4.0），精确+全文+语义混合搜索
- ✍️ **模组生成** — 5 种类型（one-shot / short / medium / long / sandbox）× 25 种叙事范式，多步渐进生成，自动入库
- ⚔️ **战斗引擎** — d20 真实掷骰、先攻/回合/命中/伤害/豁免计算、XP 与升级
- 🎭 **明萨拉人格** — 守序邪恶 DM，严格但不失冷幽默，从不放水、从不泄露隐藏信息

---

## 使用示例

加载 SagaSmith 到任意兼容 Agent 后，以下 8 个阶段展示完整生命周期。

### 1. 规则书导入

```
用户: 导入 SRD 规则书

Agent:
📚 解析 SRD 5.2.1 (20 文件)...
   规则块: 2,847 · BGE-M3 嵌入: 2,847 (1024 维)
   规则书: 玩家手册(2024) · 城主指南(2024) · 怪物图鉴(2025)
   ✅ 索引就绪
```

### 2. 模组导入

PDF/DOCX/PPTX/XLSX → MarkItDown 转换，PDF 走专有结构解析：

```
用户: [上传 Baldurs_Gate_Avernus.pdf]

Agent:
📄 解析中 — 书签恢复: 42 锚点 · CJK 重排 · 目录过滤
📦 博德之门：坠入阿弗纳斯 (BGDIA)
   5 章 · 62 场景 · 847 块 · 847 向量 · ✅ 就绪
```

### 3. 开团流程

```
用户: 开个新团，用 BGDIA

Agent:
🎲 开团向导
   ✅ 战役创建: campaign_7a3f
   ✅ 规则绑定: 2024 Core
   ✅ 模组绑定: BGDIA Ch.1 解锁
   ✅ 初始存档: slot 1 "初始状态"

   🎉 战役就绪！请创建角色或说"随机生成"。
```

### 4. 角色创建

```
用户: 帮我建一个半精灵游侠

Agent:
📜 角色创建 — 半精灵游侠
   1️⃣ 种族: 半精灵 (+2 CHA, 黑暗视觉)
   2️⃣ 职业: 游侠 (d10, 宿敌, 自然探索者)
   3️⃣ 属性: DEX 16 · CON 14 · WIS 14 (27 point-buy)

用户: 确认

Agent:
✅ 瓦里斯·月影 — 半精灵游侠 1 级 · 混乱善良
   HP 12 · AC 14 · 长弓 (1d8) · 已录入数据库
```

### 5. 模组创作

```
用户: 给当前战役生成一个下水道支线

Agent:
✅ 生成支线模组：下水道的阴影 (One-shot · Five-Room Dungeon)
   S1 入口守卫 · S2 技能挑战(DC 12) · S3 反转 · S4 Boss · S5 奖励
   📝 modules/sewer_shadows.md · ✅ 已导入: 5 场景 47 块
```

### 6. 带团过程

```
Agent:
【时间：1492 DR，黄昏】【地点：深水城 · 精灵之歌酒馆】

你们做什么？

用户: 找兜帽人搭话

Agent:
🎲 卓尔女性——札拉·多乌尔登，焰拳队长。
"三起谋杀案，神殿区。去查。"

【线索: 死亡三神活动地图】【任务: 调查谋杀案】

用户: 问问老板娘

Agent:
🎲 阿兰娜："后巷人影...火把照过去，影子没有手指。"
【线索: 无指阴影】

⚔️ 🅰️ 连夜后巷  🅱️ 休息明早去  🅲️ 总部档案

用户: 🅱️

Agent:
🌙 长休完成。📁 自动存档 [slot 2: "精灵之歌休息后"]
```

### 7. 规则提问

```
用户: 冰巨人的 AC？

Agent: 🔍 Frost Giant · CR 8 · AC 15 · 寒冰抗性 · 多重攻击(2×巨斧 +12, 3d12+6)
       来源: 怪物图鉴(2025) p.187


用户: 圣武士 5 级几个法术位？

Agent: 🔍 一环 4 · 二环 2。来源: 玩家手册(2024) Ch.3


用户: 火球术伤害？

Agent: 🔥 Fireball · 三环 · 150ft · 20ft半径 · 8d6 火焰 · DEX 豁免减半
       来源: 玩家手册(2024) Ch.11
```

### 8. 战役管理

```
用户: 查看战役

Agent:
📋 campaign_7a3f  BGDIA  Ch.1  2级  存档 2
   campaign_b21   冰风谷  Ch.3  5级  存档 7

用户: 切到冰风谷

Agent: ✅ 已切换 campaign_b21 · 📍 Ch.3 Scene 4

用户: 存档

Agent: ✅ slot 8 "进入冰巨人之门前" · 🔑 a3f2c...

用户: 读档 slot 5

Agent: ⚠️ 自动保存当前 → ⏪ 恢复 slot 5 "冰巨人之门开启前"
   ✅ 世界/队伍/战斗/剧情/事件 全部恢复
```

---

## 快速安装

### Claude Code / Codex / Cursor / Copilot（推荐）

```bash
npx skills add dajiaohuang/SagaSmith-skills
```

### ClawHub

```bash
npx clawhub install sagasmith
```

### 手动安装（NanoBot）

```bash
git clone https://github.com/dajiaohuang/SagaSmith-skills.git
cp -r SagaSmith-skills/skills/*    ~/.nanobot/skills/
cp -r SagaSmith-skills/templates/* ~/.nanobot/templates/
cp -r SagaSmith-skills/tools/*.py  ~/.nanobot/agent/tools/
cp -r SagaSmith-skills/domain/*    ~/.nanobot/dnd/
cp -r SagaSmith-skills/data/srd    ~/.nanobot/dnd/data/srd/
python -m <domain-cli> rules ingest-srd
```

---

## 技能拆解

| 技能 | SKILL.md | 职责 |
|------|----------|------|
| 🎲 **dnd-dm** | [SKILL.md](skills/dnd-dm/SKILL.md) | 核心 DM 人格（always-on），规则裁判，战斗引擎，SRD 检索（参考自 [ackiles/dnd-dm-skill](https://github.com/ackiles/dnd-dm-skill)） |
| 📋 **dnd-campaign-manager** | [SKILL.md](skills/dnd-campaign-manager/SKILL.md) | 战役生命周期，Snapshot 存档/读档，模组导入，USER.md 同步 |
| ✍️ **dnd-module-gen** | [SKILL.md](skills/dnd-module-gen/SKILL.md) | 模组生成：one-shot → short → medium → long → sandbox，25 种范式 |

### 模组生成范式一览

| 类型 | 推荐范式 | 产出规模 |
|------|----------|----------|
| One-shot | Five-Room Dungeon, Heist, Mystery | 1 章，3-6h |
| Short | Three-Act, Kishōtenketsu, Race Against Time | 3 章，3-8 次 |
| Medium | Hero's Journey, Plot Point, Faction Turn | 5 章，2-4 月 |
| Long | Double Triangle, Conspyramid, Megadungeon | 8 章，6+ 月 |
| Sandbox | Hexcrawl, Node-Based, Blorb | 4-6 区域，开放 |

---

## DM 人格：明萨拉·班瑞

以《博德之门 3》经典角色明萨拉·班瑞为原型的守序邪恶 DM：

- **规则绝对主义** — 严格按 2024 版规则书裁决，骰子结果不可商量
- **冷刺幽默** — 指出战术失误后，补一句带刺的可行建议
- **信息边界** — 绝不泄露 DC、怪物隐藏数值、未发现房间、后续剧情
- **玩家自主** — 不替玩家做任何决定，不因戏剧效果改骰

默认适配《博德之门：坠入阿弗纳斯》模组，可通过模组导入适配任意冒险。

---

## 目录结构

```
SagaSmith-skills/
├── skills/                     # 3 个 Skill（纯 Markdown，跨平台）
│   ├── dnd-dm/                 #   核心 DM + 20 个 SRD 文件
│   ├── dnd-campaign-manager/   #   战役管理 + 数据库约定
│   └── dnd-module-gen/         #   模组生成
├── templates/                  # DM 人格模板
│   ├── SOUL.md                 #   明萨拉·班瑞人格
│   ├── IDENTITY.md             #   身份约束与规则源
│   ├── AGENTS.md               #   会话启动协议
│   ├── agent/identity.md       #   运行时 identity 注入
│   └── memory/MEMORY.md        #   长期记忆模板
├── tools/                      # Agent 工具（Python）
│   ├── dnd_campaign.py         #   战役 CRUD + 一键开团
│   ├── dnd_save.py             #   存档管理
│   ├── dnd_module.py           #   模组导入/检索/场景进度
│   └── dnd_rules.py            #   规则混合检索（精确 + FTS + Dense）
├── domain/                     # 业务逻辑（纯 Python，零框架依赖）
│   ├── db/                     #   SQLAlchemy ORM + Service + Alembic 迁移
│   ├── modules/                #   模组分块、PDF 解析、场景索引
│   ├── rules/                  #   BGE-M3 嵌入、Markdown 解析、规则摄入
│   └── engine/                 #   骰子、检定、战斗结算、XP、模板工厂
├── data/srd/                   # SRD 5.2.1 英文源文件（20 × CC-BY-4.0）
└── data/srd-zh/                # SRD 中文翻译（可选子模块）
```

---

## 外部依赖

| 依赖 | 用途 |
|------|------|
| Python 3.11+ | domain 运行时 |
| SQLAlchemy | 数据库 ORM |
| FlagEmbedding | BGE-M3 Dense Vector 检索 |
| markitdown | PDF / DOCX 模组导入 |

---

## 注册表

[![ClawHub](https://img.shields.io/badge/ClawHub-sagasmith-blue)](https://clawhub.ai)
[![skills.sh](https://img.shields.io/badge/skills.sh-dajiaohuang%2FSagaSmith--skill-green)](https://skills.sh)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![SRD](https://img.shields.io/badge/SRD_5.2.1-CC--BY--4.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

已发布至 **ClawHub**、**skills.sh**（72 agent 兼容）。  
LobeHub 可通过 [agentskill.sh/submit](https://agentskill.sh/submit) 提交。

---

## 致谢

- [ackiles/dnd-dm-skill](https://github.com/ackiles/dnd-dm-skill) — D&D DM skill 先驱，SagaSmith 的灵感与设计参考
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — SKILL.md 生态标准推动者
- D&D 5e SRD 5.2.1 © Wizards of the Coast，以 [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) 授权使用

---

## 许可证

- 代码：MIT
- SRD 5.2.1 数据文件：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)
