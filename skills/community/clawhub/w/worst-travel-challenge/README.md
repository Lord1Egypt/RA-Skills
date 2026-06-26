# 🔥 最差旅行体验挑战 | Worst Travel Challenge

> **别人用 AI 规划最美旅行，我用 FlyAI 规划最烂旅行——**  
> **因为只有真正烂过，才知道什么叫真实的好。**
>
> *Others use AI to plan the most beautiful trips, I use FlyAI to plan the worst—*  
> *Because only after experiencing the worst, you know what real good feels like.*

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/agentskills/agentskills)
[![FlyAI](https://img.shields.io/badge/FlyAI-Required-orange.svg)](https://flyai.open.fliggy.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-Verified-purple.svg)](https://www.clawhub.com)

---

## 🌐 语言 | Language

- [🇨🇳 中文版](#-一句话介绍)
- [🇬🇧 English Version](#-one-sentence-intro)

---

# 🇨🇳 中文版

## 🎯 一句话介绍

**一个把"最差"玩成"最上头"的 AI 旅行挑战 Skill** —— 专挑最烂航班、最破住宿、最奇葩景点，用 FlyAI 实时数据驱动，全程毒舌吐槽+实时预订+拍照讲解，最后生成核弹级吐槽日记和短视频爆款包！

---

## ✨ 核心特色

| 特色 | 说明 |
|------|------|
| 🎭 **反向极致模式** | 不优化、不推荐、不讨好，专挑最差评、最便宜、最坑的真实体验 |
| 📊 **FlyAI 实时数据** | 基于飞猪实时库存、真实价格、真实用户评价（评分越低越优先） |
| 🤖 **多 Agent 协作** | 交通坑神 + 住宿坑神 + 玩乐坑神 + 吐槽解说 + 救赎 Agent，五位一体 |
| 💬 **毒舌吐槽风** | 沙雕、自黑、真实、带梗，像老朋友陪你一起骂街 |
| 📸 **拍照讲解** | 每到一个节点，上传照片立即毒舌讲解 |
| 🎬 **自动生成内容** | 吐槽日记 + 逆袭报告 + 10个短视频脚本，一键分享 |
| 🎲 **"随便"模式** | 不想选？回复"随便"，坑神帮你随机安排！ |

---

## 🚀 快速开始

### 1️⃣ 前置依赖

**本 Skill 依赖 FlyAI CLI 工具**，使用前请确保：

```bash
# 安装 FlyAI CLI
npm i -g @fly-ai/flyai-cli

# 验证连接
flyai ai-search --query "测试" --debug
```

### 2️⃣ 安装 Skill

#### 方式一：Qwen Code

```bash
cp -r ~/.flyai/skills/worst-travel-challenge ~/.qwen/skills/
```

#### 方式二：Qoderwork

```bash
cp -r ~/.flyai/skills/worst-travel-challenge ~/.qoderwork/skills/
```

#### 方式三：ClawHub

直接在 ClawHub 搜索 `worst-travel-challenge` 一键安装。

### 3️⃣ 触发挑战

在 AI 对话中输入：

```
启动最差旅行体验挑战！
```

或

```
FlyAI，给我安排最烂的旅行！预算100块，随便扔我去哪！
```

---

## 🎮 使用示例

### 示例 1：完整参数

**用户输入：**
```
启动最差旅行体验挑战！预算3000元，2天1夜，从北京出发，随便扔我去哪！
```

**AI 输出：**
```
【坑神报告】
目的地：河北·石家庄（国际庄！）
行程天数：3天2夜
总预算：618元（随机摇出来的，吉利又要命）

【地狱级配置】
- 交通：K401 次 北京西→石家庄 21:25-00:58，硬座28.5元，凌晨到达完美体验"到了但没完全到"
- 住宿：太空舱主题客栈68元/晚，隔壁大哥呼噜声模拟宇宙大爆炸
- 玩乐：赵州桥（40元）、正定古城（免费！）、西柏坡（免费）

【确认按钮】
回复"确认出发"即可一键全预订。
回复"再坑一点"我会继续加码。
回复"救命"直接终止并反转成天堂模式。
```

### 示例 2：信息不完整

**用户输入：**
```
启动最差旅行体验挑战！
```

**AI 输出：**
```
🔥 坑神已就位！但在我开始折磨你之前，先确认几个问题：

1️⃣ **出发地**：你从哪个城市出发？
2️⃣ **出发时间**：打算什么时候出发？
3️⃣ **行程天数**：几天几夜？
4️⃣ **预算**：准备花多少钱作死？

💡 **或者回复"随便"，我帮你随机安排！**
   （我会随机挑选出发地、时间、天数和预算，保证让你惊喜/惊吓）
```

### 示例 3："随便"模式

**用户输入：**
```
随便！
```

**AI 自动随机生成：**
- 出发地：上海
- 出发时间：明天
- 行程天数：1天1夜
- 预算：100元（穷游极限挑战！）

---

## 🏗️ 架构设计

### 多 Agent 协作体系

```
┌─────────────────────────────────────────────────┐
│              最差旅行体验挑战                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ 交通坑神  │  │ 住宿坑神  │  │ 玩乐坑神  │       │
│  │          │  │          │  │          │       │
│  │ 最烂航班  │  │ 最破民宿  │  │ 最奇葩   │       │
│  │ 红眼延误  │  │ 火车站旁  │  │ 路边摊   │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│         ↓              ↓              ↓          │
│  ┌─────────────────────────────────────────┐    │
│  │          吐槽解说 Agent                  │    │
│  │   毒舌 + 幽默 + 真实吐槽 + 故事讲解      │    │
│  └─────────────────────────────────────────┘    │
│                       ↓                          │
│  ┌─────────────────────────────────────────┐    │
│  │          救赎 Agent                      │    │
│  │   用户说"救命"瞬间反转成顶级体验          │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### 执行流程

```
阶段零：信息收集 → 阶段一：规划报告 → 阶段二：行程互动 → 阶段三：结束生成
     ↓                  ↓                  ↓                  ↓
  确认出发地         坑神报告           拍照讲解          吐槽日记
  确认时间           FlyAI实时查        毒舌解说          逆袭报告
  确认预算           一键预订           动态调整          短视频包
  或"随便"           用户确认
```

---

## 📦 生成内容

行程结束后，自动生成三份核弹级内容：

### 1. 《最差旅行吐槽日记》
- Markdown 格式
- 每一天 1 段 + 配图建议 + 毒舌小标题
- 示例：《K401硬座3小时，我还没打开抖音就到了》

### 2. 《从地狱到天堂 {{X}} 小时逆袭报告》
- 标题中的 {{X}} 根据用户实际旅行总小时数动态计算
- 总花费明细
- 被坑次数排行榜（Top 5）
- 意外收获 Top 3
- 生存指数（0-100）
- 数据可视化描述

### 3. 短视频爆款包
- 10 个爆款标题（带 emoji）
- 每条视频的 15 秒脚本（带 BGM 建议和字幕文案）
- 一键分享文案

---

## 🛡️ 安全阀

- ✅ 出发前必须让用户明确确认
- ✅ 预算、日期、健康状况严格遵守
- ✅ 禁止安排任何违法、危险、严重影响健康的项目
- ✅ 随时说"救命/够了/升级"即可终止并反转成天堂模式

---

## 📂 文件结构

```
worst-travel-challenge/
├── SKILL.md              # 核心 Skill 定义（符合 Agent Skills 规范）
├── README.md             # 本文件
├── references/
│   └── README.md         # 详细参考文档
└── assets/               # 资源目录（可扩展）
```

---

## 🔧 本地调试

使用 FlyAI debug 模式测试实时数据查询：

```bash
# 查询火车票
flyai search-train --origin 北京 --dep-date 2026-04-05 --sort-type 3 --max-price 50 --debug

# 查询酒店
flyai search-hotel --dest-name 石家庄 --check-in-date 2026-04-05 --check-out-date 2026-04-06 --max-price 100 --debug

# 查询景点
flyai search-poi --city-name 石家庄 --debug
```

---

## 📊 真实案例：618元石家庄糟心旅程

### 行程概览

| 项目 | 详情 |
|------|------|
| **出发地** | 北京 |
| **目的地** | 石家庄（国际庄） |
| **行程天数** | 3天2夜 |
| **总预算** | 618元（随机摇出来的，吉利又要命） |
| **实际花费** | 451.5元 |
| **剩余** | 166.5元 |
| **生存指数** | 85/100 |

### 地狱级配置

#### 🚂 交通坑神

| 模块 | 详情 | 价格 | 坑点 |
|------|------|------|------|
| **去程** | K401 次 北京西→石家庄 21:25-00:58 | 28.5元 | 凌晨到达，出站连早点摊都没开，完美体验"到了但没完全到" |
| **返程** | G字头高铁站票 石家庄→北京西 | 129元 | 玩完三天腿已废，还要站着回京，主打一个"身心俱疲" |
| **市内** | 共享电单车 + 11路公交（步行为主） | 46元 | 全靠腿和缘分，3天步行50000步 |

#### 🏨 住宿坑神

| 日期 | 住宿 | 价格 | 坑点 |
|------|------|------|------|
| **Day 1** | 太空舱主题客栈（火车站旁0.2km） | 68元 | 隔壁大哥呼噜声模拟宇宙大爆炸，沉浸式体验"中国流动的底色" |
| **Day 2** | 大象青年旅舍（大学城15楼） | 35元 | 电梯坏了就是体能训练，和大学生抢床位听他们聊考研和失恋 |

#### 🎪 每日玩乐

| 天数 | 行程 | 费用 | 坑点 |
|------|------|------|------|
| **Day 1** | 赵州桥 → 正定古城 → 正定夜市路边摊 | 65元 | 小学课本朝圣，去了发现"就这？"但站在桥上能感受到1400年的孤独 |
| **Day 2** | 华北制药厂旧址 → 河北博物院 → 勒泰中心地下美食街 | 30元 | 赛博朋克废墟探险 + 金缕玉衣面前释怀人生 |
| **Day 3** | 西柏坡 → 石家庄万达广场 → 返程站票高铁 | 66元 | "新中国从这里走来"，被爱国主义教育治愈所有旅行创伤 |

### 预算明细

| 项目 | 费用 |
|------|------|
| 去程火车硬座 | 28.5元 |
| 返程高铁站票 | 129元 |
| 住宿2晚 | 103元 |
| 市内交通 | 46元 |
| 餐饮3天 | 105元 |
| 门票 | 40元 |
| **合计** | **451.5元** |
| **剩余** | **166.5元**（留作备用金/急救基金） |

### 被坑 Top 5

| 排名 | 被坑事件 | 坑指数 |
|------|----------|--------|
| 🥇 | 太空舱里大哥呼噜声模拟宇宙大爆炸 | ⭐⭐⭐⭐⭐ |
| 🥈 | K401硬座90度靠背，人体工学？不存在的 | ⭐⭐⭐⭐ |
| 🥉 | 赵州桥下洨河水量比钱包还干净 | ⭐⭐⭐ |
| 4 | 正定古城门口充气城堡，传统与现代的碰撞 | ⭐⭐ |
| 5 | 返程高铁站票，腿废了还要站着回京 | ⭐⭐ |

### 意外收获 Top 3

1. **站在1400年前的赵州桥上** — 李春设计师跨越千年的孤独，值了
2. **正定古城0元VIP包场** — 比丽江真实100倍，因为根本没几个人去
3. **深夜冷风中的存在主义顿悟** — 凌晨0:58站在石家庄站出站口，冷风一吹，觉得这趟旅行从上车那一刻就已经值了

### 坑神毒舌解说精选

> **赵州桥**：花40块钱，站在一座1400年前的桥上，感受李春设计师跨越千年的孤独——**值了**。桥下的水虽然干了，但你的钱包也快了，某种意义上，你和这条河达成了某种精神共鸣。

> **正定古城**：花0块钱，逛一座1800年历史的古城，城墙随便爬，城楼随便看，唯一的"消费陷阱"是门口的充气城堡。赵子龙的家乡，不卷、不装、不网红——**这才是真正的反向旅游天花板**。

> **K401次列车**：一列用3个半小时走完高铁1小时路程的传奇列车。它不快，但它够真实。它不舒适，但它够难忘。当你凌晨0:58站在石家庄站的出站口，冷风一吹，你会觉得——**这趟旅行，从上车的那一刻就已经值了。**

---

## 🎬 爆款视频示例

### 标题
🔥《618元挑战石家庄3天2夜！我活着回来了！》

### 15秒脚本

| 时间 | 画面 | 字幕文案 |
|------|------|----------|
| 0-3s | K401次列车夜景 | "凌晨0:58到石家庄，到了但没完全到" |
| 3-6s | 太空舱客栈 | "68块的太空舱，大哥呼噜声模拟宇宙大爆炸" |
| 6-9s | 赵州桥 | "1400年前的桥，桥下水比钱包还干净" |
| 9-12s | 正定古城+充气城堡 | "0元逛古城，门口充气城堡太魔幻" |
| 12-15s | 高铁站票 | "返程站票，腿废了还要站着回京" |

---

## 🤝 贡献指南

欢迎提交 PR 或 Issue！

- 新增更多"坑"场景
- 优化毒舌文案库
- 添加更多城市模板
- 改进短视频脚本模板

---

## 📝 更新日志

### v1.1.0 (2026-04-04)
- ✅ 新增"阶段零：信息收集"流程
- ✅ 新增"随便"模式，一键随机安排
- ✅ 明确强依赖 FlyAI CLI 工具
- ✅ 逆袭报告标题改为动态小时数
- ✅ 通过 skills-ref 规范验证

### v1.0.0 (2026-04-03)
- 🎉 初始版本发布
- 🎭 多 Agent 协作体系
- 📊 FlyAI 实时数据驱动
- 🎬 自动生成吐槽日记和短视频包

---

# 🇬🇧 English Version

## 🎯 One-Sentence Intro

**An AI travel challenge Skill that turns the "worst" into the "most addictive"** — deliberately picking the worst flights, the shabbiest accommodations, and the weirdest attractions, powered by FlyAI real-time data, with snarky commentary throughout, real-time booking, photo commentary, and finally generating a nuclear-level rant diary and viral short video packages!

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎭 **Reverse Perfection Mode** | No optimization, no recommendations, no pleasing — only the worst-rated, cheapest, most pitiful real experiences |
| 📊 **FlyAI Real-Time Data** | Based on Fliggy's real-time inventory, real prices, real user reviews (lower rating = higher priority) |
| 🤖 **Multi-Agent Collaboration** | Transport Pit God + Accommodation Pit God + Activity Pit God + Snarky Commentator + Redemption Agent, all-in-one |
| 💬 **Snarky Commentary** | Sarcastic, self-deprecating, authentic, meme-filled, like an old friend cursing alongside you |
| 📸 **Photo Commentary** | Upload a photo at each stop, get instant snarky commentary |
| 🎬 **Auto-Generated Content** | Rant diary + comeback report + 10 short video scripts, one-click share |
| 🎲 **"Whatever" Mode** | Don't want to choose? Reply "whatever" and the Pit God will randomly arrange everything! |

---

## 🚀 Quick Start

### 1️⃣ Prerequisites

**This Skill depends on FlyAI CLI**. Before use, ensure:

```bash
# Install FlyAI CLI
npm i -g @fly-ai/flyai-cli

# Verify connection
flyai ai-search --query "test" --debug
```

### 2️⃣ Install Skill

#### Option 1: Qwen Code

```bash
cp -r ~/.flyai/skills/worst-travel-challenge ~/.qwen/skills/
```

#### Option 2: Qoderwork

```bash
cp -r ~/.flyai/skills/worst-travel-challenge ~/.qoderwork/skills/
```

#### Option 3: ClawHub

Simply search `worst-travel-challenge` in ClawHub and install with one click.

### 3️⃣ Trigger the Challenge

Type in AI chat:

```
Start the worst travel challenge!
```

Or

```
FlyAI, arrange the worst trip for me! Budget 100 RMB, throw me anywhere!
```

---

## 🎮 Usage Examples

### Example 1: Complete Parameters

**User Input:**
```
Start the worst travel challenge! Budget 3000 RMB, 2 days 1 night, departing from Beijing, throw me anywhere!
```

**AI Output:**
```
【Pit God Report】
Destination: Shijiazhuang, Hebei (International Zhuang!)
Duration: 3 days 2 nights
Total Budget: 618 RMB (randomly rolled, auspicious yet deadly)

【Hell-Level Configuration】
- Transport: K401 Beijing West → Shijiazhuang 21:25-00:58, hard seat 28.5 RMB, arriving at midnight for the perfect "arrived but not really arrived" experience
- Accommodation: Space capsule themed inn 68 RMB/night, next-door bro's snoring simulates the Big Bang
- Activities: Zhaozhou Bridge (40 RMB), Zhengding Ancient Town (FREE!), Xibaipo (FREE)

【Confirmation Button】
Reply "confirm departure" for one-click booking.
Reply "make it worse" I'll escalate.
Reply "help" to terminate and reverse to heaven mode.
```

### Example 2: Incomplete Information

**User Input:**
```
Start the worst travel challenge!
```

**AI Output:**
```
🔥 Pit God is ready! But before I start torturing you, let me confirm a few things:

1️⃣ **Departure City**: Where are you departing from?
2️⃣ **Departure Time**: When do you plan to leave?
3️⃣ **Duration**: How many days and nights?
4️⃣ **Budget**: How much money are you willing to suffer with?

💡 **Or reply "whatever" and I'll randomly arrange everything for you!**
   (I'll randomly pick departure city, time, duration, and budget, guaranteed to surprise/shock you)
```

### Example 3: "Whatever" Mode

**User Input:**
```
Whatever!
```

**AI Auto-Generates:**
- Departure: Shanghai
- Departure Time: Tomorrow
- Duration: 1 day 1 night
- Budget: 100 RMB (extreme budget challenge!)

---

## 🏗️ Architecture

### Multi-Agent Collaboration System

```
┌─────────────────────────────────────────────────┐
│           Worst Travel Challenge                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Transport │  │Accommod. │  │Activity  │       │
│  │Pit God   │  │Pit God   │  │Pit God   │       │
│  │          │  │          │  │          │       │
│  │Worst     │  │Shabbiest │  │Weirdest  │       │
│  │Flights   │  │Inns      │  │Street    │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│         ↓              ↓              ↓          │
│  ┌─────────────────────────────────────────┐    │
│  │      Snarky Commentator Agent            │    │
│  │   Sarcastic + Humorous + Real + Stories  │    │
│  └─────────────────────────────────────────┘    │
│                       ↓                          │
│  ┌─────────────────────────────────────────┐    │
│  │      Redemption Agent                    │    │
│  │   "Help" instantly reverses to premium   │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Execution Flow

```
Phase 0: Info Collection → Phase 1: Planning Report → Phase 2: Trip Interaction → Phase 3: End Generation
     ↓                          ↓                          ↓                          ↓
  Confirm departure        Pit God Report            Photo commentary          Rant diary
  Confirm time             FlyAI real-time query     Snarky解说                Comeback report
  Confirm budget           One-click booking         Dynamic adjustment        Short video package
  Or "whatever"            User confirmation
```

---

## 📦 Generated Content

After the trip ends, automatically generate three nuclear-level contents:

### 1. "Worst Travel Rant Diary"
- Markdown format
- 1 paragraph per day + photo suggestions + snarky subtitles
- Example: "K401 Hard Seat for 3 Hours, I Arrived Before Opening TikTok"

### 2. "From Hell to Heaven {{X}} Hours Comeback Report"
- {{X}} dynamically calculated based on actual trip duration
- Total expenses
- Top 5 Most Pitiful Events Ranking
- Top 3 Unexpected Harvests
- Survival Index (0-100)
- Data visualization description

### 3. Viral Short Video Package
- 10 viral titles (with emoji)
- 15-second scripts for each video (with BGM suggestions and subtitle copy)
- One-click share copy

---

## 🛡️ Safety Valve

- ✅ Must get explicit user confirmation before departure
- ✅ Strictly abide by budget, dates, and health conditions
- ✅ Prohibit any illegal, dangerous, or health-threatening activities
- ✅ Say "help/enough/upgrade" anytime to terminate and reverse to heaven mode

---

## 📂 File Structure

```
worst-travel-challenge/
├── SKILL.md              # Core Skill definition (Agent Skills compliant)
├── README.md             # This file
├── references/
│   └── README.md         # Detailed reference documentation
└── assets/               # Asset directory (extensible)
```

---

## 🔧 Local Debugging

Use FlyAI debug mode to test real-time data queries:

```bash
# Query train tickets
flyai search-train --origin Beijing --dep-date 2026-04-05 --sort-type 3 --max-price 50 --debug

# Query hotels
flyai search-hotel --dest-name Shijiazhuang --check-in-date 2026-04-05 --check-out-date 2026-04-06 --max-price 100 --debug

# Query attractions
flyai search-poi --city-name Shijiazhuang --debug
```

---

## 📊 Real Case: 618 RMB Shijiazhuang Miserable Journey

### Trip Overview

| Item | Details |
|------|---------|
| **Departure** | Beijing |
| **Destination** | Shijiazhuang (International Zhuang) |
| **Duration** | 3 days 2 nights |
| **Total Budget** | 618 RMB (randomly rolled, auspicious yet deadly) |
| **Actual Cost** | 451.5 RMB |
| **Remaining** | 166.5 RMB |
| **Survival Index** | 85/100 |

### Hell-Level Configuration

#### 🚂 Transport Pit God

| Module | Details | Price | Pit Point |
|--------|---------|-------|-----------|
| **Outbound** | K401 Beijing West → Shijiazhuang 21:25-00:58 | 28.5 RMB | Arriving at midnight, not even a breakfast stall open, perfect "arrived but not really arrived" experience |
| **Return** | G-series standing ticket Shijiazhuang → Beijing West | 129 RMB | Legs already wasted after 3 days, still have to stand back to Beijing,主打 "exhausted body and mind" |
| **Local** | Shared e-bike + Bus Route 11 (mainly walking) | 46 RMB | All legs and fate, 50,000 steps in 3 days |

#### 🏨 Accommodation Pit God

| Date | Accommodation | Price | Pit Point |
|------|---------------|-------|-----------|
| **Day 1** | Space Capsule Inn (0.2km from station) | 68 RMB | Next-door bro's snoring simulates Big Bang, immersive "flowing China" experience |
| **Day 2** | Elephant Youth Hostel (University Town 15F) | 35 RMB | Elevator broken = physical training,抢床位 with college students listening to grad school and breakups |

#### 🎪 Daily Activities

| Day | Itinerary | Cost | Pit Point |
|-----|-----------|------|-----------|
| **Day 1** | Zhaozhou Bridge → Zhengding Ancient Town → Night Market Street Food | 65 RMB | Elementary textbook pilgrimage, went and found "that's it?" but standing on the bridge you feel 1400 years of loneliness |
| **Day 2** | North China Pharmaceutical Factory Ruins → Hebei Museum → Letai Center Underground Food Street | 30 RMB | Cyberpunk ruin exploration + finding peace before the Gold-Thread Jade Suit |
| **Day 3** | Xibaipo → Shijiazhuang Wanda Plaza → Return standing ticket | 66 RMB | "New China started from here", healed by patriotic education |

### Budget Breakdown

| Item | Cost |
|------|------|
| Outbound hard seat | 28.5 RMB |
| Return standing ticket | 129 RMB |
| 2 nights accommodation | 103 RMB |
| Local transport | 46 RMB |
| 3 days food | 105 RMB |
| Tickets | 40 RMB |
| **Total** | **451.5 RMB** |
| **Remaining** | **166.5 RMB** (emergency fund) |

### Top 5 Most Pitiful Events

| Rank | Event | Pit Index |
|------|-------|-----------|
| 🥇 | Space capsule bro's snoring simulates Big Bang | ⭐⭐⭐⭐⭐ |
| 🥈 | K401 hard seat 90° backrest, ergonomics? Doesn't exist | ⭐⭐⭐⭐ |
| 🥉 | Xiao River under Zhaozhou Bridge drier than wallet | ⭐⭐⭐ |
| 4 | Inflatable castle at Zhengding Ancient Town gate, tradition meets modernity | ⭐⭐ |
| 5 | Return standing ticket, legs wasted but still have to stand back | ⭐⭐ |

### Top 3 Unexpected Harvests

1. **Standing on 1400-year-old Zhaozhou Bridge** — Designer Li Chun's loneliness spanning a millennium, worth it
2. **Zhengding Ancient Town 0 RMB VIP exclusive** — 100x more real than Lijiang, because basically nobody goes
3. **Existential epiphany in midnight cold wind** — Standing at Shijiazhuang Station exit at 0:58 AM, cold wind blows, you feel this trip was worth it from the moment you boarded

### Pit God Snarky Commentary Highlights

> **Zhaozhou Bridge**: Spend 40 RMB to stand on a 1400-year-old bridge, feel designer Li Chun's loneliness spanning a millennium — **worth it**. The river below may be dry, but so is your wallet. In a way, you've reached spiritual resonance with this river.

> **Zhengding Ancient Town**: Spend 0 RMB to explore a 1800-year-old ancient town, climb walls freely, view towers freely, the only "consumption trap" is the inflatable castle at the gate. Zhao Zilong's hometown, not competitive, not pretentious, not internet-famous — **this is the real ceiling of reverse tourism**.

> **K401 Train**: A legendary train that takes 3.5 hours to cover what high-speed rail does in 1 hour. It's not fast, but it's real. It's not comfortable, but it's unforgettable. When you stand at Shijiazhuang Station exit at 0:58 AM, cold wind blowing, you'll feel — **this trip was worth it from the moment you boarded**.

---

## 🎬 Viral Video Example

### Title
🔥《618 RMB Challenge Shijiazhuang 3 Days 2 Nights! I Came Back Alive!》

### 15-Second Script

| Time | Visual | Subtitle Copy |
|------|--------|---------------|
| 0-3s | K401 night view | "Arriving Shijiazhuang at 0:58 AM, arrived but not really" |
| 3-6s | Space capsule inn | "68 RMB space capsule, bro's snoring simulates Big Bang" |
| 6-9s | Zhaozhou Bridge | "1400-year-old bridge, river drier than wallet" |
| 9-12s | Zhengding + inflatable castle | "0 RMB ancient town, inflatable castle too magical" |
| 12-15s | Standing ticket | "Return standing ticket, legs wasted but still standing back" |

---

## 🤝 Contributing

PRs and Issues are welcome!

- Add more "pit" scenarios
- Optimize snarky copy library
- Add more city templates
- Improve short video script templates

---

## 📝 Changelog

### v1.1.0 (2026-04-04)
- ✅ Added "Phase 0: Info Collection" flow
- ✅ Added "Whatever" mode, one-click random arrangement
- ✅ Clarified hard dependency on FlyAI CLI
- ✅ Changed comeback report title to dynamic hours
- ✅ Passed skills-ref specification validation

### v1.0.0 (2026-04-03)
- 🎉 Initial release
- 🎭 Multi-agent collaboration system
- 📊 FlyAI real-time data driven
- 🎬 Auto-generated rant diary and short video packages

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

- **FlyAI Open Platform**: Real-time travel data support
- **Agent Skills Specification**: [agentskills/agentskills](https://github.com/agentskills/agentskills)
- **ClawHub**: Skill distribution platform

---

> **Pit God's Message:**  
> "This trip might be miserable, but after the misery, you'll realize —  
> You can actually travel for 100 RMB, even Shijiazhuang has stories, and you're still alive!"  
>
> **Good luck, warrior!** 😈🔥
