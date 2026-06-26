---
name: web-novel-master
description: |
  爆款网文创作助手。基于 Claude Code 的智能网文写作系统，支持都市爽文/玄幻修仙/穿越重生/甜宠言情。章章有爽点，名场面驱动，让读者追更停不下来。
---

<div align="center">

# Web Novel Master

### 爆款网文创作利器 · 让 AI 帮你写出会火的书

[![Version](https://img.shields.io/badge/version-v1.0-blue.svg)](https://github.com/tinylion1024/web-novel-master)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CLAUDE](https://img.shields.io/badge/Power%20By-Claude%20Code-orange.svg)](https://claude.com/claude-code)
[![Stars](https://img.shields.io/github/stars/tinylion1024/web-novel-master?style=social)](https://github.com/tinylion1024/web-novel-master)

![封面](./assets/web-novel-master-cover.jpg)

</div>

---

## Table of Contents

- [为什么需要 Web Novel Master？](#为什么需要-web-novel-master)
- [核心亮点](#核心亮点)
- [支持的文风与赛道](#支持的文风与赛道)
- [三种创作模式](#三种创作模式)
- [爆款网文四法则](#爆款网文四法则)
- [黄金套路速查](#黄金套路速查)
- [26 位网文大神文风参考](#26-位网文大神文风参考)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [输出示例](#输出示例)
- [谁在用 Web Novel Master](#谁在用-web-novel-master)
- [如何贡献](#如何贡献)
- [世界观设定](#世界观设定)

---

## 为什么需要 Web Novel Master？

写网文难吗？难。**90% 的新手死在前三章**——节奏拖沓、爽点缺失、人设崩塌。

写网文易吗？易。只要你懂：**爆款网文是可以被设计出来的。**

> 每章 2000-3000 字，章章有爽点，名场面驱动，金句记忆 —— 这些都有方法论。

Web Novel Master 把 **26 位顶流网文作者的写作套路**、**爆款四法则**、**套路模板库**、**完整世界观体系**全部结构化，嵌入 AI 写作流程，让 AI 帮你写出专业级别的网文。

---

## 核心亮点

| | |
|---|---|
| 🤖 **AI 驱动** | 基于 Claude Code，调用顶级大模型辅助创作 |
| 📚 **26 位作者文风库** | 内置天蚕土豆、辰东、猫腻、桐华等顶流风格分析 |
| 🎯 **三模式并行** | [Fast（快速动笔）](#三种创作模式) / [Professional（质量优先）](#三种创作模式) / [Industrial（团队流水线）](#三种创作模式) |
| 🏆 **爆款方法论** | [爽点驱动 + 情绪节奏 + 金句设计 + 名场面规划](#爆款网文四法则) |
| 📖 **套路模板库** | [退婚流/系统流/重生流/马甲文等经典套路](#黄金套路速查) |
| 🔧 **模块化设计** | 可整套使用，也可单独引用某个模块 |

---

## 支持的文风与赛道

内置 **4 大男频赛道 + 7 大女频赛道**，覆盖主流网文全类型：

### 👨 男频（Male-Oriented）

| 赛道 | 风格特点 | 代表大神 |
|------|---------|---------|
| **Xianxia Passion 热血玄幻** | 爽文向、升级快、打脸爽、退婚流 | [天蚕土豆](./references/Soul/01_Male-Oriented/Xianxia_Passion/)、[辰东](./references/Soul/01_Male-Oriented/Xianxia_Passion/)、[风凌天下](./references/Soul/01_Male-Oriented/Xianxia_Passion/)、[逆苍天](./references/Soul/01_Male-Oriented/Xianxia_Passion/) |
| **Xianxia Mortal 仙侠凡人流** | 写实向、设定严谨、节奏慢、智斗流 | [忘语](./references/Soul/01_Male-Oriented/Xianxia_Mortal/)、[耳根](./references/Soul/01_Male-Oriented/Xianxia_Mortal/)、[梦入神机](./references/Soul/01_Male-Oriented/Xianxia_Mortal/) |
| **Urban Hot 都市热销** | 都市异能、高武流、电竞、游戏异界 | [老鹰吃小鸡](./references/Soul/01_Male-Oriented/Urban_Hot/)、[会说话的肘子](./references/Soul/01_Male-Oriented/Urban_Hot/)、[打眼](./references/Soul/01_Male-Oriented/Urban_Hot/)、[柳下挥](./references/Soul/01_Male-Oriented/Urban_Hot/) |
| **Historical Politics 历史权谋** | 宫斗宅斗、穿越历史、朝堂政治 | [猫腻](./references/Soul/01_Male-Oriented/Historical_Politics/)、[愤怒的香蕉](./references/Soul/01_Male-Oriented/Historical_Politics/)、[孑与2](./references/Soul/01_Male-Oriented/Historical_Politics/) |

### 👩 女频（Female-Oriented）

| 赛道 | 风格特点 | 代表大神 |
|------|---------|---------|
| **Ancient Romance 古言穿越** | 仙侠虐恋、古言权谋、三生三世 | [桐华](./references/Soul/02_Female-Oriented/Ancient_Romance/)、[天下归元](./references/Soul/02_Female-Oriented/Ancient_Romance/)、[希行](./references/Soul/02_Female-Oriented/Ancient_Romance/) |
| **Modern Strong-F 现言女强** | 马甲、团宠、总裁、电竞甜文 | [一路烦花](./references/Soul/02_Female-Oriented/Modern_Strong_F/)、[叶非夜](./references/Soul/02_Female-Oriented/Modern_Strong_F/) |
| **Farmlife-Intrigue 种田经商** | 穿越宅斗、发家致富、养成系 | [吱吱](./references/Soul/02_Female-Oriented/Farmlife_Intrigue/) |
| **Rebirth Revenge 重生复仇** | 打脸虐渣、马甲、复仇逆袭 | [苏闲佞](./references/Soul/02_Female-Oriented/Rebirth_Revenge/)、[重生爆款文风参考](./references/Soul/02_Female-Oriented/Rebirth_Revenge/) |
| **Chase Wife 虐恋追妻** | 追妻火葬场、强取豪夺、霸道男主 | [虐恋追妻文风](./references/Soul/02_Female-Oriented/Chase_Wife/)、[强取豪夺文风](./references/Soul/02_Female-Oriented/Chase_Wife/) |
| **Sweet Romance 甜宠治愈** | 高甜、治愈系、姨母笑、无虐 | [高甜宠溺文风](./references/Soul/02_Female-Oriented/Sweet_Romance/)、[治愈系甜宠](./references/Soul/02_Female-Oriented/Sweet_Romance/) |
| **Mary Sue 万能女主** | 全能人设、万人迷、人生赢家 | [万能女主文风](./references/Soul/02_Female-Oriented/Mary_Sue/)、[爽感玛丽苏](./references/Soul/02_Female-Oriented/Mary_Sue/) |

> 💡 每个赛道均内置 **2-4 位代表作者的文风分析**，涵盖金句风格、爽点设计、经典模板、避坑提示，创作时可随时调用。

---

## 三种创作模式

### ⚡ Fast 快速模式（5 Phase）— 30 分钟开写

```
想法 → 确认 → 起草 → 润色 → 校验
```

想立刻动笔？选这个。5 步搞定第一章，2 小时搞定一个开头。

| Phase | 文件 |
|-------|------|
| 0 | [Fast0_Initialization.md](./references/Flow/Fast/Fast0_Initialization.md) |
| 1 | [Fast1_Idea_Clarify.md](./references/Flow/Fast/Fast1_Idea_Clarify.md) |
| 2 | [Fast2_Quick_Draft.md](./references/Flow/Fast/Fast2_Quick_Draft.md) |
| 3 | [Fast3_Simple_Polish.md](./references/Flow/Fast/Fast3_Simple_Polish.md) |
| 4 | [Fast4_Final_Validation.md](./references/Flow/Fast/Fast4_Final_Validation.md) |

### 💻 Professional 专业模式（8 Phase）— 系统化写作

```
初始化 → 核心定位 → 世界人设 → 大纲规划 → 正文撰写 → 润色节奏 → 钩子包装 → 校验发布
```

认真写作、追求质量？选这个。8 步覆盖从构思到发布的完整流程。

| Phase | 文件 |
|-------|------|
| 0 | [Pro0_Initialization.md](./references/Flow/Pro/Pro0_Initialization.md) |
| 1 | [Pro1_Core_Clarify.md](./references/Flow/Pro/Pro1_Core_Clarify.md) |
| 2 | [Pro2_World_Character_Setup.md](./references/Flow/Pro/Pro2_World_Character_Setup.md) |
| 3 | [Pro3_Outline_Planning.md](./references/Flow/Pro/Pro3_Outline_Planning.md) |
| 4 | [Pro4_Full_Draft_Writing.md](./references/Flow/Pro/Pro4_Full_Draft_Writing.md) |
| 5 | [Pro5_Polish_Pacing.md](./references/Flow/Pro/Pro5_Polish_Pacing.md) |
| 6 | [Pro6_Hook_Packaging.md](./references/Flow/Pro/Pro6_Hook_Packaging.md) |
| 7 | [Pro7_Validation_Release.md](./references/Flow/Pro/Pro7_Validation_Release.md) |

### 🏭 Industrial 工业模式（10 Phase）— 团队流水线

```
项目初始化 → 市场调研 → 核心定位 → 世界规则 → 人物标准化 → 模块化大纲 → 团队写作 → 统一润色 → QC校验 → 发布运营
```

长篇连载、团队协作？选这个。10 步工业流水线，支持多人分工、质量管控。

| Phase | 文件 |
|-------|------|
| 0 | [Ind0_Project_Initialize.md](./references/Flow/Ind/Ind0_Project_Initialize.md) |
| 1 | [Ind1_Market_Research.md](./references/Flow/Ind/Ind1_Market_Research.md) |
| 2 | [Ind2_Core_Positioning.md](./references/Flow/Ind/Ind2_Core_Positioning.md) |
| 3 | [Ind3_World_Rule_Setup.md](./references/Flow/Ind/Ind3_World_Rule_Setup.md) |
| 4 | [Ind4_Character_Standard.md](./references/Flow/Ind/Ind4_Character_Standard.md) |
| 5 | [Ind5_Modular_Outline.md](./references/Flow/Ind/Ind5_Modular_Outline.md) |
| 6 | [Ind6_Team_Writing.md](./references/Flow/Ind/Ind6_Team_Writing.md) |
| 7 | [Ind7_Unified_Polish.md](./references/Flow/Ind/Ind7_Unified_Polish.md) |
| 8 | [Ind8_QC_Validation.md](./references/Flow/Ind/Ind8_QC_Validation.md) |
| 9 | [Ind9_Release_Operation.md](./references/Flow/Ind/Ind9_Release_Operation.md) |

---

## 爆款网文四法则

> 这是网文与普通小说的本质区别。不懂这四条，写出来的东西没人看。

| 法则 | 说明 | 实践 |
|------|------|------|
| 🔥 **爽点驱动** | 读者追更，是为了「爽」 | 每章必须有一个让读者拍案的瞬间 |
| 🌊 **情绪波动** | 有憋有放，张弛有度 | 虐 3 章必须爽 1 章，情绪不憋死 |
| 💎 **金句记忆** | 让读者想截图 | 每章至少一句让读者忍不住截图的金句 |
| 🎬 **名场面** | 每 3-5 章一个记忆点 | 打脸/装逼/甜宠/燃点，名场面要够名 |

更多写作方法论：

- [开篇公式](./references/Plot/Opening-Formula.md) — 如何写出抓人的第一段
- [爽点设计指南](./references/Plot/Excitement-Point-Guide.md) — 爽点的类型与密度设计
- [情绪节奏指南](./references/Plot/Emotional-Rhythm-Guide.md) — 憋爽比例与情绪曲线
- [名场面设计指南](./references/Plot/Famous-Scenes-Guide.md) — 打脸/装逼/甜宠/燃点的设计方法

---

## 黄金套路速查

```
退婚流    ▸ 废物开局 → 当众羞辱 → 意外觉醒 → 碾压打脸
系统流    ▸ 濒死/危机 → 系统激活 → 任务奖励 → 飞速变强
重生流    ▸ 死亡/失败 → 重生节点 → 先知优势 → 复仇清算
装逼流    ▸ 低调隐藏 → 被逼无奈 → 展露实力 → 全场震惊
马甲文    ▸ 多重身份 → 故意隐藏 → 逐层掉马 → 爽感炸裂
追妻火葬场 ▸ 前期虐女 → 心死离开 → 追妻追到 → 跪榴莲
```

更多套路模板：

- [套路大全](./references/Plot/Trope-Catalog.md) — 10+ 经典套路完整拆解
- [名场面模板库](./references/Plot/Scene-Template-Library.md) — 打脸/装逼/甜宠/燃点模板
- [悬念设置技巧](./references/Plot/Hook-Techniques.md) — 13 种钩子技法

---

## 26 位网文大神文风参考

内置作者风格分析，创作时可随时调用：

**男频顶流** — [男频文风库](./references/Soul/01_Male-Oriented/)
- 天蚕土豆（退婚流、爽点节奏）
- 辰东（宏大叙事、诸天万界）
- 忘语（凡人流、严谨设定）
- 耳根（虐心、意志流）
- 猫腻（权谋、文笔华丽）
- 老鹰吃小鸡（日更 3 万、高武流）

**女频顶流** — [女频文风库](./references/Soul/02_Female-Oriented/)
- 桐华（虐恋情深、三生三世）
- 天下归元（大女主、女强男强）
- 一路烦花（马甲、团宠）
- 叶非夜（甜宠、总裁）
- 希行（重生复仇、宅斗）
- 吱吱（种田经商、穿越宅斗）

---

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/tinylion1024/web-novel-master.git

# 放入 Claude Code skills 目录
cp -r web-novel-master ~/.claude/skills/

# 重启 Claude Code，输入 /skill web-novel-master 启动
```

### 2. 选择模式

启动后，AI 会引导你选择模式：

```
📌 请选择创作模式：
  [1] ⚡ Fast - 快速动笔（5步，30分钟开始写）
  [2] 💻 Professional - 质量优先（8步，系统化写作）
  [3] 🏭 Industrial - 团队流水线（10步，长篇连载）
```

### 3. 开始创作

以 Professional 模式为例：

```
📌 Phase 1: 核心定位
请告诉我：你想写什么类型的网文？
  - 都市爽文 / 玄幻修仙 / 穿越重生 / 甜宠言情 / 其他

AI 会追问：主角是谁？金手指是什么？爽点设计？...
帮你把模糊的想法变成完整的人物设定和情节规划。
```

---

## 项目结构

```
web-novel-master/
├── SKILL.md                          # Skill 入口
├── README.md                          # 本文档
├── references/
│   ├── Flow/                         # 三模式流程定义
│   │   ├── Fast/                     # [Fast 模式（5 Phase）](#三种创作模式)
│   │   ├── Pro/                      # [Professional 模式（8 Phase）](#三种创作模式)
│   │   └── Ind/                      # [Industrial 模式（10 Phase）](#三种创作模式)
│   ├── Plot/                         # [剧情/爽点/钩子](#爆款网文四法则)
│   │   ├── Opening-Formula.md         # 开篇公式
│   │   ├── Excitement-Point-Guide.md # 爽点设计指南
│   │   ├── Famous-Scenes-Guide.md    # 名场面设计
│   │   ├── Trope-Catalog.md          # 套路大全
│   │   ├── Scene-Template-Library.md # 名场面模板库
│   │   ├── Hook-Techniques.md        # 悬念设置技巧
│   │   └── Plot-Structures.md        # 情节结构模板
│   ├── Soul/                         # [26 位作者文风库](#26-位网文大神文风参考)
│   │   ├── 01_Male-Oriented/         # [男频大神风格](#支持的文风与赛道)
│   │   └── 02_Female-Oriented/       # [女频大神风格](#支持的文风与赛道)
│   ├── Role/                         # [人设/金手指](#爆款网文四法则)
│   │   ├── Golden-Finger-Design.md   # 金手指设计
│   │   ├── Character-Template.md      # 人物档案模板
│   │   └── Character-Building.md     # 人物塑造指南
│   ├── Materials/                    # [素材/描写技巧](#快速开始)
│   │   ├── Content-Expansion.md      # 内容扩充技巧
│   │   └── Dialogue-Writing.md       # 对话写作规范
│   ├── Guides/                       # [写作教程/模板](#快速开始)
│   │   ├── Chapter-Writing-Guide.md # 章节写作指南
│   │   └── Chapter-Template.md       # 章节模板
│   ├── World/                        # [世界观设定](#世界观设定)
│   │   ├── Power-Systems/           # 力量体系（修仙/武侠/异能/科幻）
│   │   ├── Factions/               # 势力设定（宗门/企业/家族）
│   │   ├── Rules/                  # 世界规则（魔法/系统/社会）
│   │   └── Geography/              # 地理设定（大陆/城市）
│   ├── Data/                         # 市场数据（待填充）
│   └── Check/                        # 自检清单（待填充）
└── scripts/
    └── check_chapter_wordcount.py     # 字数校验脚本
```

**80+ 参考文件**，覆盖网文创作的全部环节。

---

## 输出示例

使用 Web Novel Master 创作的小说项目结构：

```
2024-06-01-都市异能王者/
├── 00-大纲.md                         # 完整故事大纲
├── 01-人物档案.md                     # 主角/女主/反派/配角档案
├── 02-名场面时间轴.md                 # 20+ 名场面规划
├── 03-伏笔系统.md                     # 埋的坑和回收计划
├── 04-章节详细规划.md                 # 每章核心事件
├── chapters/
│   ├── 第01章.md                     # 2000-3000字/章
│   ├── 第02章.md
│   └── ...
└── QC校验报告.md                      # 质量评分 & 修复建议
```

---

## 谁在用 Web Novel Master？

- **网文爱好者** — 第一次写小说，不知道怎么开头
- **兼职作者** — 想提升写作效率，保持稳定更新
- **全职作者** — 系统化创作流程，减少卡文概率
- **工作室/团队** — 流水线生产，多人分工协作
- **AI 写作探索者** — 研究如何用 AI 辅助创意写作

---

## 如何贡献

欢迎提交 Issue 和 Pull Request！

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 补充参考素材（作者文风、套路模板）
- 🔧 优化现有流程文件
- ⭐ Star 支持一下

---

## License

MIT License - 永久开源，可自由使用、修改、商业化。

---

## 世界观设定

> 完整的世界观是爆款网文的骨架。Web Novel Master 内置了四大体系的世界观模板，涵盖玄幻仙侠、都市异能、武侠江湖、科幻星际等主流题材。

### 力量体系

| 体系 | 内容 | 适用题材 |
|------|------|---------|
| [修仙力量体系](./references/World/Power-Systems/Cultivation.md) | 境界9级、丹药资源、战斗体系、升级节奏 | 玄幻仙侠 |
| [武侠力量体系](./references/World/Power-Systems/Martial-Arts.md) | 武功境界、门派江湖、秘籍传承 | 武侠小说 |
| [现代异能体系](./references/World/Power-Systems/Modern-Ability.md) | 异能分类、等级划分、都市异能设定 | 都市异能 |
| [科幻科技体系](./references/World/Power-Systems/Sci-Fi-Tech.md) | 文明等级、星际势力、机甲战斗 | 科幻小说 |

### 势力设定

| 体系 | 内容 | 适用题材 |
|------|------|---------|
| [宗门势力](./references/World/Factions/Sects.md) | 宗门等级5级、资源争夺、传承体系 | 玄幻仙侠 |
| [企业势力](./references/World/Factions/Corporations.md) | 企业等级、商战异能、职场模板 | 都市商战 |
| [家族势力](./references/World/Factions/Families.md) | 嫡庶之争、继承权、豪门恩怨 | 都市豪门 |

### 世界规则

| 体系 | 内容 | 适用题材 |
|------|------|---------|
| [魔法规则](./references/World/Rules/Magic-Rules.md) | 魔法等级、元素融合、施法体系 | 西幻异世 |
| [系统规则](./references/World/Rules/System-Rules.md) | 系统类型8种、任务/商城/合成 | 系统流 |
| [社会规则](./references/World/Rules/Social-Rules.md) | 社会阶层、货币体系、势力关系 | 所有题材 |

### 地理设定

| 体系 | 内容 | 适用题材 |
|------|------|---------|
| [大陆设定](./references/World/Geography/Continents.md) | 五域格局、禁地秘境、势力分布 | 玄幻仙侠 |
| [城市设定](./references/World/Geography/Cities.md) | 城市分级、功能区域、打脸场景 | 都市小说 |

**12 个世界观文件**，覆盖所有主流网文题材。

---

<div align="center">

**如果这个项目对你有帮助，请点个 ⭐ Star**

---

## 关注我们

<p>获取更多AI实战干货</p>

<p>关注微信公众号、关注小红书，一起交流学习。</p>

<table>
<tr>
<td align="center">
<img src="./assets/wechat-QR-code.jpg" width="200" alt="微信公众号"/>
<br/>
<strong>微信公众号</strong>
</td>
<td align="center">
<img src="./assets/xhs-QR-code.jpg" width="200" alt="小红书"/>
<br/>
<strong>小红书</strong>
</td>
</tr>
</table>

</div>
