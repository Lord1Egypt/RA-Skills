# XDesign

> Design Workflow Engine — 将想法到可交付物的全流程压缩为对话。
> 你不是在用"画图工具"，你是在驱动一个 **产品经理 + 初级设计师 + 前端开发** 的合体。
> v1.x 已融合 [html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) → 内置 **deck-studio/** 子模块（18 主题 + 31 布局 + 47 动效 + 演讲者模式）。

---

## 它是什么

XDesign 是一个 AI 驱动的设计流程引擎。它不是一个模板工具，不是 Figma 替代品，而是解决从 **"想法" → "可展示成果"** 这段最痛苦过程的完整工作流。

**核心能力：**
- 🎨 **视觉设计** — 通过 HTML 生成原型、演示文稿、落地页、动画、UI 设计
- 🧠 **设计系统提取** — 从品牌资料自动提取颜色/字体/组件规范
- 📐 **线框图 → 高保真** — 渐进式设计流程，先确认结构再打磨视觉
- 🎛️ **实时调参** — Tweaks 面板让用户在设计中即时调整参数
- 📤 **多格式导出** — PPTX、PDF、独立 HTML、Canva、React 组件代码
- 🌍 **多语言支持** — CJK、RTL、欧洲语言的本地化设计指导
- 💡 **设计解释** — 不仅做设计，还能解释设计逻辑，充当设计导师
- 🎤 **演讲者模式（fused）** — 4 卡片可拖拽的 presenter 视图（当前页/下页/提词器/计时器）

---

## 三模式路由

XDesign 内部有 **3 种工作模式**，按用户意图自动分发：

| 触发词 | 模式 | 走哪条路 |
|---|---|---|
| 做一份 PPT、slides、keynote、演讲、pitch deck、带逐字稿 | **Mode 1: Presentation / Deck** | `deck-studio/` 子模块（18 主题 + 31 布局 + 5 full-deck 模板） |
| 设计 APP、原型、dashboard、落地页、组件、UI Kit | **Mode 2: Visual Design / Prototype** | 原 XDesign 流程（Design System → Wireframe → Hi-Fi + React+Babel） |
| 动效视频、时间轴动画、motion design | **Mode 3: Animation / Video** | 原 XDesign `animations.jsx` 路径 |

> ⚠️ 默认走 Mode 1 的前提：用户说"做一份 deck / PPT / slides"；不明确时询问用户。

详见 [references/integration-guide.md](./references/integration-guide.md) 和 [references/deck-studio-catalog.md](./references/deck-studio-catalog.md)。

---

## 支持的项目类型

| 类型 | 说明 | 输出 | 模式 |
|---|---|---|---|
| **Pitch Deck / 演讲 PPT** | 演示文稿/幻灯片（带演讲稿、主题循环、键盘导航） | HTML（自包含、CDN-only） | Mode 1 |
| **小红书图文** | 7 格 bento 网格或全幅 hero + Ken Burns | HTML | Mode 1 |
| **Interactive Prototype** | 可交互的产品/UI 原型 | HTML | Mode 2 |
| **Landing Page** | 落地页/营销页面 | HTML | Mode 2 |
| **Design System** | 品牌设计系统/UI Kit | DESIGN.md + 组件示例 | Mode 2 |
| **Animated Video** | 时间轴动画/动效设计 | HTML | Mode 3 |
| **Wireframe** | 低保真线框图/故事板 | HTML | Mode 2 |

---

## 快速开始

### 1. 写一个结构化的 Prompt

**不要这样写：**
> 做个APP界面

**要这样写：**
```
做一个 B2B SaaS 后台
目标用户：运营人员，非技术背景
使用场景：日常数据监控 + 客户管理
核心功能：
- 数据看板（实时指标）
- 客户列表（筛选+操作）
- 任务分配
页面结构：
- Dashboard（首页）
- Customer List
- Customer Detail
设计风格：简洁冷静，专业可信
参考：
- Stripe Dashboard
- Linear
输出：
1. Wireframe（低保真）
2. 3种 Dashboard 布局方案
```

### 2. 正确的设计流程

```
品牌资料上传 → 设计系统提取 → Wireframe（低保真）→ 确认布局 → 高保真设计 → 导出
```

**关键原则：**
1. **Design System First** — 先建立视觉基础（颜色/字体/组件），再做页面
2. **Wireframe Before Hi-Fi** — 先确认布局和信息层级，再升级视觉
3. **多版本生成** — 不要"再改一下"，而是一次给 3 种不同方案

### 3. 三种迭代方式

| 方式 | 适合场景 | 示例 |
|---|---|---|
| 💬 对话修改 | 方向性调整 | "按钮太重，轻一点" |
| 🖊️ 画布批注 | 具体元素修改 | 点击元素 → "改成卡片布局" |
| 🎛️ 滑杆调整 | 参数微调 | 间距/颜色/字号 |

---

## 技术架构

### 总体结构

- **Mode 2/3**（原 XDesign）：React 18.3.1 + Babel 7.29.0（固定版本，含 integrity hash），单 HTML 文件内嵌 React 组件
- **Mode 1**（deck-studio 子模块）：纯静态 HTML/CSS/JS，**零构建**，CDN webfont，所有主题/布局/动画即拷即用
- **双模式统一**：都输出单文件 HTML 或自包含目录，都可在 Trae IDE / Claude.ai artifacts / 任意浏览器 / GitHub Pages / `file://` 打开

### Mode 1 资源（deck-studio/）

- **18 个主题** — 极简（minimal-white, japanese-minimal）/ 商务（corporate-clean, pitch-deck-vc）/ 暗色（dracula, catppuccin-mocha, gruvbox-dark）/ 强调（bauhaus, memphis-pop, cyberpunk-neon）/ 工程（blueprint, engineering-whiteprint）
- **31 个单页布局** — 封面/目录/章节分隔、bullets/双列/三列、stat-highlight/KPI/表格/Chart.js 4 种图、代码/diff/终端、流程/架构/思维导图/时间轴/甘特/路线图、hero/grid/CTA/Thanks
- **5 个完整 deck 模板** — product-launch / pitch-deck / tech-sharing / weekly-report / course-module（每个都是目录结构，带 scoped CSS）
- **47 个动效** — 27 个 CSS 命名入场动画（fade-up / rise-in / zoom-pop / path-draw / parallax-tilt...）+ 20 个 canvas FX（粒子/烟花/矩阵雨/神经网络/知识图谱/星座...）
- **演讲者模式** — S 键弹出 4 卡片：当前页 + 下一页 + 提词器 + 计时器

### Mode 2/3 资源（原 XDesign）

| 组件 | 用途 |
|---|---|
| `deck_stage.js` | 幻灯片演示（自动缩放/键盘导航/讲稿/打印） |
| `design_canvas.jsx` | 并排展示多个静态方案 |
| `ios_frame.jsx` / `android_frame.jsx` / `macos_window.jsx` / `browser_window.jsx` | 各种设备/窗口外壳 |
| `animations.jsx` | 时间轴动画（Stage + Sprite + Easing） |
| 58 个品牌 DESIGN.md | Stripe / Linear / Notion / Figma / Vercel / Apple / Tesla ... 直接拿现成设计系统 |

### 导出能力

| 格式 | 说明 | 模式 |
|---|---|---|
| **Standalone HTML** | 单文件自包含，离线可用 | Mode 1 + 2 |
| **PPTX (editable)** | 原生文本/形状，可在 PowerPoint 编辑 | Mode 2 |
| **PPTX (screenshots)** | 逐页截图，像素级精确 | Mode 1 + 2 |
| **PDF** | 浏览器打印导出 | Mode 1 + 2 |
| **PNG (per slide)** | `deck-studio/scripts/render.sh` 走 headless Chrome | Mode 1 |
| **Canva** | 导出为可编辑的 Canva 设计 | Mode 2 |
| **React Code** | 转为可开发的 React 组件 | Mode 2 |

---

## 内置 Sub-Skills

通过 `invoke_skill` 按需加载：

| 技能 | 触发场景 | 模式 |
|---|---|---|
| **Make a deck（fused）** | HTML 幻灯片演示 + 主题循环 + 演讲者模式 | Mode 1 |
| Animated video | 时间轴动效设计 | Mode 3 |
| Interactive prototype | 可交互的产品原型 | Mode 2 |
| Make tweakable | 添加设计内调参控件 | Mode 2 |
| Frontend design | 品牌系统外的美学方向 | Mode 2 |
| Wireframe | 线框图/故事板 | Mode 2 |
| Create design system | 创建设计系统/UI Kit | Mode 2 |
| Export as PPTX | 导出 PowerPoint | Mode 2 |
| Save as PDF | 导出 PDF | Mode 1 + 2 |
| Save as standalone HTML | 导出独立 HTML | Mode 1 + 2 |
| Send to Canva | 导出到 Canva | Mode 2 |
| Handoff to Claude Code | 开发者交接包 | Mode 2 |

---

## 多语言支持

XDesign 内置多语言设计指导：

- **CJK 文字**：行高 1.6-1.8，专用字体栈（思源黑体/苹方/游哥特等）
- **RTL 语言**：`dir="rtl"`，镜像布局
- **文本膨胀率**：英→中 ~60-80%，英→德 ~130%，英→日 ~80-100%
- **本地化**：`Intl` API 格式化，`lang` 属性，文本变量化

---

## 高手技巧

### 项目命名 = 隐形上下文
- ❌ "project1" → 生成结果平庸
- ✅ "AI招聘Agent平台" → 后续设计更稳定一致

### 参考输入比 Prompt 更重要
可以喂入：网站链接、Figma 导出、PPT、代码仓库、手绘草图、品牌素材。给它 Stripe/Notion/Linear 的截图，直接生成同级别 UI。

### 让它解释设计逻辑
问"为什么这样布局？"会输出完整的设计思考：信息层级、布局逻辑、色彩选择、交互原理、权衡取舍。相当于白嫖设计导师。

### 设计 → 代码一体化
说"把这个转成 React 组件"，直接从设计稿进入开发流程。

### 做 PPT 时点出"演讲者模式"
说 "我要去给团队讲 xxx" → 自动用 `deck-studio/templates/full-decks/tech-sharing/` 模板，每页生成 150-300 字逐字稿，按 S 键弹 4 卡片 presenter 视图。

### 做 PPT 时先定主题
明确主题能省 3 轮迭代。模糊就给 2-3 候选：
- 投资人 pitch → `pitch-deck-vc` / `corporate-clean` / `bauhaus`
- 技术分享 → `catppuccin-mocha` / `dracula` / `blueprint`
- 小红书 → `xiaohongshu-white`（**注意：本仓库当前未下载，需先 `ls deck-studio/assets/themes/` 确认**）
- 学术报告 → `academic-paper` / `editorial-serif`

---

## 常见坑

| 坑 | 后果 | 解决方案 |
|---|---|---|
| Prompt 太短 | 输出平庸 | 用结构化模板 |
| 没喂数据 | 永远"通用设计" | 先上传品牌资料 |
| 一上来追求精致 | 陷入无限微调 | 先 Wireframe 再 Hi-Fi |
| 当 Figma 替代 | 定位错误 | 这是前期+结构设计工具 |
| 跳过设计系统 | 每页风格不统一 | 先建 Design System |
| **PPT 触发词识别错** | 走 React+Babel 写了 50 行 deck | SKILL.md 入口路由 → 严格按"PPT/slides/deck"分到 Mode 1 |
| **混用两套 design token** | 主题/组件颜色不统一 | deck-studio 用 `var(--text-1)`，DESIGN.md 用自己的 token，二选一 |

---

## 文件结构

```
XDesign/
├── SKILL.md                          # 核心技能（Intent Router + Mode 1/2/3）
├── README.md                         # 本文件
├── LICENSE
├── assets/
│   └── design-md/                    # 58 个品牌 DESIGN.md
│       ├── stripe/
│       ├── linear.app/
│       └── ... 共 58 个
├── references/
│   ├── design-system-catalog.md      # 58 品牌索引
│   ├── technical-specs.md            # 技术规范
│   ├── workflow-guide.md             # 高手玩法
│   ├── integration-guide.md          # 【新】融合架构 + 路由表 + 适配层
│   └── deck-studio-catalog.md        # 【新】deck-studio 资源速查
├── evals/
│   └── eval-plan.json
└── deck-studio/                      # 【新】子模块（html-ppt-skill 完整克隆）
    ├── SKILL.md
    ├── README.md / README.zh-CN.md
    ├── LICENSE
    ├── assets/
    │   ├── base.css                  # 设计令牌 + 布局原语
    │   ├── fonts.css                 # webfont imports
    │   ├── runtime.js                # 键盘 + 演讲者 + 主题循环
    │   ├── themes/                   # 18 个主题 CSS
    │   └── animations/               # animations.css + 20 个 FX
    ├── references/                   # themes.md / layouts.md / animations.md / full-decks.md / authoring-guide.md / presenter-mode.md
    ├── templates/
    │   ├── deck.html                 # 最小 6 页 starter
    │   ├── theme-showcase.html       # 主题展示
    │   ├── layout-showcase.html      # 31 布局展示
    │   ├── animation-showcase.html
    │   ├── full-decks-index.html
    │   ├── full-decks/               # 5 个 full-deck 模板
    │   └── single-page/              # 31 个单页布局
    └── scripts/
        ├── new-deck.sh
        └── render.sh                 # headless Chrome → PNG
```

---


