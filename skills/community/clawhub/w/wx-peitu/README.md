# wx-peitu · 公众号长文配图生成器

![GitHub stars](https://img.shields.io/github/stars/EdwardWason/wx-peitu?style=flat-square)
![License](https://img.shields.io/github/license/EdwardWason/wx-peitu?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![WeChat](https://img.shields.io/badge/WeChat-Illustration-07C160?style=flat-square)
![ClawHub](https://img.shields.io/badge/ClawHub-wx--peitu-FF6B35?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square)

一个适配 TRAE / Claude Code 等 Agent 环境的公众号配图技能，用于从 MD 长文生成**公众号配图 PNG 包**，自动同步到**飞书云盘**。

内置两套视觉系统，共用一份配图工作流：
- **电子杂志风（Editorial）**。衬线体 + 暖纸底 + 水墨氛围，适合深度观察、人文文化、人物访谈、读书笔记。
- **瑞士国际主义（Swiss）**。无衬线 + 灰白底 + 单一 accent + 极致字号对比，适合科技产品、数据研究、职场干货、教程指南。

> 核心交付物是 **PNG 图片**，不是代码。HTML 只是中间产物，Puppeteer 截图后直接出图。

## 30 秒开始

```bash
clawhub install wx-peitu
```

也可以直接把这段话发给有 shell 权限的 AI Agent：

```text
帮我安装 wx-peitu。请把 https://github.com/EdwardWason/wx-peitu 克隆到 ~/.claude/skills/wx-peitu，安装完成后检查 SKILL.md 和 references/ 是否存在。
```

安装后直接对 Agent 说：

```text
帮这篇文章做一套公众号配图
```

也可以试这些请求：

```text
大师推荐，直接来
帮这篇科技文章做一套瑞士风配图，IKB 蓝
这篇文章做5张配图，电子杂志风
第3张颜色太深，帮我调一下
```

## 效果

- 🎨 **双视觉系统**：Editorial 做氛围与叙事，Swiss 做事实与结构，两套共用同一份工作流
- 📐 **5 个画板尺寸**：封面 900×383、正文 640×auto、金句 640×640、分隔 640×200、封底 900×383
- 🧩 **20 种配图类型**：封面/封底/金句图/数据图/逻辑链/流程管道/版本线/判断卡/认知纠偏/宣言卡/案例卡等
- 🏗 **10 种版式骨架**：流程图/决策树/漏斗图/VS 对战/路径图/条形图/网格卡片/时间线/照片叠加/文字块，禁止连续 3 张同版式
- 🎯 **4-Purpose 框架**：每张配图标注 purpose（attention/readability/memorability/conversion），驱动设计参数
- 🖼 **3 大图库接入**：Pexels / Unsplash / Wallhaven，用户图片始终优先
- ✅ **密度门控**：3 维 15 分评分，≥9 分及格，8 类 48 条反模式 + AI 去污染
- 📱 **飞书云盘同步**：截图后自动上传飞书云盘，手机端直接下载发布
- 🔧 **微调模式**：只改指定配图，不重新生成全部

## 适合 / 不适合

**✅ 合适**：公众号长文配图 / 文章封面封底 / 数据可视化卡片 / 金句图 / 逻辑流程图 / 知识卡片 / 对比图 / 漏斗图

**❌ 不合适**：全文排版（用 md2wechat）/ 视频动效 / 纯图片修图 / 追星粉丝向 / 纯促销硬广 / 超过 15 张配图的文章

## 10 个品类自动检测

| 品类 | 检测信号 | 默认风格 | 默认色板 |
|------|---------|---------|---------|
| 深度观察 / 商业洞察 | "IPO"/"估值"/"财报" | Swiss | IKB Blue |
| 科技 / 产品 | "AI"/"发布"/"功能" | Swiss | IKB Blue / Safety Orange |
| 人文 / 文化 | "历史"/"文学"/"艺术" | Editorial | 牛皮纸 / 森林墨 |
| 职场 / 干货 | "方法"/"步骤"/"清单" | Swiss | Lemon Green |
| 旅行 / 生活 | "旅行"/"城市"/"美食" | Editorial | 暖色 earth |
| 读书 / 笔记 | "书评"/"阅读"/"摘录" | Editorial | 墨水经典 |
| 人物 / 访谈 | "专访"/"对话"/"人物" | Editorial | 沙丘 / 森林墨 |
| 数据 / 研究 | "研究"/"报告"/"统计" | Swiss | IKB Blue |
| 观点 / 评论 | "我认为"/"其实"/"真相" | Editorial | 墨水经典 |
| 教程 / 指南 | "教程"/"指南"/"如何" | Swiss | Lemon Green |

## 常见使用场景

| 任务 | 推荐方式 |
|------|---------|
| 长文章 → 公众号配图 | 抽核心观点，Editorial 走叙事节奏，Swiss 走数据拆条 |
| 科技产品测评 | Swiss + IKB 蓝，漏斗图 / VS 对战 / 流程图 |
| 深度商业分析 | Swiss + IKB 蓝，数据图 + KPI 大字报 |
| 人文观察 / 人物故事 | Editorial + 墨水经典，金句图 + 照片叠加封面 |
| 数据报告 | Swiss + IKB 蓝，条形图 / 网格卡片 |
| 教程 / 方法论 | Swiss + Lemon Green，流程图 / 决策树 |

## 为什么是 HTML → Puppeteer → PNG

- **Agent 友好**：HTML + CSS 是文本，Agent 能直接写、读、改、验证
- **版式精确**：CSS Grid + 严格字号 / 留白 / 网格，远超 Markdown 排版能力
- **图源开放**：可以接 Unsplash / Pexels / Wallhaven 等任意网络资源
- **交付简单**：PNG 直接发，不需要部署、不需要导出工具
- **手机可达**：飞书云盘同步后，手机打开飞书 App 即可下载发布

## 使用流程

Skill 本身是结构化工作流，Agent 会按 6 步走：

1. **Step A 解析** — 从文章提取 20 种可视化单元，标注 Purpose（attention/readability/memorability/conversion）
2. **Step B 方案** — 展示配图方案（emoji + 一句话描述），密度评分内部计算，用户确认
3. **Step C 风格** — 3 个问题定风格 + 品类自动检测 + 视觉节奏规划，"大师推荐"可跳过
4. **Step D 生成 HTML** — 每张配图独立 HTML 文件（内联 CSS + `<img>` 标签 + 固定尺寸），版式多样性检查
5. **Step E 使用指南** — 文章章节 ↔ 配图映射 + 快速修改指令
6. **Step F 截图交付** — Puppeteer → PNG → 桌面文件夹 → 飞书云盘同步

详细说明见 [`SKILL.md`](./SKILL.md)。深度细节去看对应 `references/*.md`。

## 主题色预设

### Editorial 5 套

| 主题 | 色调 | 适合场景 |
|------|------|---------|
| 🖋 **墨水经典 Ink Classic** | `#141413` / `#f5f4ed` | 通用默认、商业话题、不知道选啥时最稳 |
| 🌿 **森林墨 Forest Ink** | `#1a2e1f` / `#f5f1e8` | 自然、可持续、非虚构 |
| 🍂 **牛皮纸 Kraft Paper** | `#2a1e13` / `#eedfc7` | 怀旧、人文、阅读、文学 |
| 🌙 **沙丘 Dune** | `#1f1a14` / `#f0e6d2` | 艺术、设计、创意、时尚 |
| 🏺 **莫兰迪 Morandi** | `#3D3529` / `#F5F0E8` | 优雅、克制、生活方式 |

### Swiss 4 套

| 主题 | 锚点色 | 适合场景 |
|------|--------|---------|
| 🔵 **克莱因蓝 IKB** | `#002FA7` | 通用默认、商业发布、AI 产品、方法论 |
| 🟡 **柠檬黄 Lemon** | `#FFD500` | 年轻、运动、零售、消费品 |
| 🟢 **柠檬绿 Lemon Green** | `#C5E803` | 生态、健康、Z 世代、绿色品牌 |
| 🟠 **安全橙 Safety Orange** | `#FF6B35` | 警示、新闻、工业、活力主题 |

## 触发方式

装好后，Agent 会自动发现并调用这个 skill。触发关键词：

- "公众号配图" / "文章配图" / "长文配图" / "公众号排版" → Multi-Illustration Mode
- "大师推荐" / "你定" / "直接来" → Master Mode（全自动）
- "第 N 张颜色太深" / "第 N 张换个版式" → 微调模式（Tweak Mode）

## 安装

### 方式一：ClawHub 安装（推荐）

```bash
clawhub install wx-peitu
```

### 方式二：一行命令安装

```bash
npx skills add https://github.com/EdwardWason/wx-peitu --skill wx-peitu
```

### 方式三：手动命令行

```bash
git clone https://github.com/EdwardWason/wx-peitu.git ~/.claude/skills/wx-peitu
```

## 目录结构

```
wx-peitu/
├── SKILL.md                    ← Skill 主文件：6 步工作流 + 规则
├── README.md                   ← 本文件
├── LICENSE                     ← MIT-0
├── CHANGELOG.md                ← 版本变更记录
├── .gitignore
├── .claude-plugin/
│   └── plugin.json             ← Claude Code 插件元数据
└── references/
    ├── workflow.md             ← 6 步工作流 + 微调模式 + 截图交付 + 云盘同步
    ├── design-system.md        ← 双风格 + 字号阶梯 + 色板 + 品牌 DNA
    ├── quality-gates.md        ← 密度评分 + 48 条反模式 + AI 去污染
    └── assets.md               ← 图库接入 + 图表系统 + HTML 模板骨架
```

## 核心设计原则

1. **克制优于喊话** — 品牌色 ≤ 5% 面积，单一 accent 原则，信息流里克制反而最显眼
2. **结构优于装饰** — 字号 + 字体对比 + 网格留白撑起信息层级，不靠阴影和卡片
3. **版式优于自由** — 10 种版式骨架先选后改，不要发明不存在的页面
4. **越大越轻** — 44px+ 标题 weight ≤ 400，小字才用重字重，这是"高级感"的核心
5. **温度优于冷感** — 所有灰色必须暖调（R ≈ G > B），禁止冷蓝灰，禁止纯白背景
6. **内容驱动数量** — 配图数量由内容分析决定，不强制固定数量
7. **图片优先用户的** — 用户自有图片始终优先于图库，不重复追问
8. **密度门控不可协商** — 每张配图独立过密度评分（≥9/15），不过就不生成

## 视觉参考

- *The Economist* / *Monocle* / *Kinfolk* 的版式与字距
- Massimo Vignelli / Helvetica Forever / 瑞士国际主义网格系统
- 小红书 / 公众号信息流里"克制反而吃香"的内容样本
- 歸藏的图文卡片实践与"做杂志，不做网页"方法论

## 字号阶梯

### WeChat Card Type Scale（640px 画布）

| Role | Size | Weight | 说明 |
|------|------|--------|------|
| Display / Hero | 36-44px | 300-400 | 自信，不压迫 |
| Section Title | 24-32px | 400-500 | 层级锚点 |
| Body | 14-16px | 400-500 | 手机舒适阅读 |
| Captions / Meta | 10-12px | 500-600 | 小字重字重 |
| Data Numbers | 28-36px | 300-400 | 数据卡片，大于正文小于标题 |

### Cover Type Scale（900×383 封面/封底）

| Role | Size | Weight | 说明 |
|------|------|--------|------|
| Cover Title | 44-52px | 300-400 | 缩略图 1 秒可读 |
| Cover Subtitle | 15-18px | 400 | 辅助信息 |
| Cover Meta | 11-13px | 500 | 来源 / 作者 / 日期 |

## FAQ

**可以批量出图吗？**
可以。一篇文章通常生成 5-10 张配图，screenshot.js 一键全部截图到桌面文件夹。

**为什么封面/封底必须有照片背景？**
纯色封面在信息流里无法让读者停止滑动。Hero 页面的任务是"停止滑动"，照片背景 + 文字叠加是最有效的方式。

**为什么不允许自定义颜色？**
这个 Skill 的核心价值是稳定产出。自由选色会破坏整体风格，只允许从预设色板里挑。

**怎么同步到手机？**
截图后自动上传飞书云盘。手机打开飞书 App → 云盘 → 找到对应文件夹 → 下载图片 → 发布。

**怎么修改某一张配图？**
直接说"第 N 张颜色太深"或"第 N 张换个版式"，进入微调模式，只重新生成目标配图。

**支持英文图文吗？**
支持。字体系统同时覆盖中英文，版式骨架未做语言绑定。

## 贡献

Bug、排版问题、新版式需求 — 欢迎开 Issue 或 PR。

## License

MIT-0 © 2026 [EdwardWason](https://github.com/EdwardWason)

本项目采用 **MIT-0** 协议，可自由使用、修改、分发，无需署名。
