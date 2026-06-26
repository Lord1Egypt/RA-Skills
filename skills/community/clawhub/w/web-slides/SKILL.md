---
name: web-pptx-generator
description: 专业单页面HTML PPT生成器。Use when user needs to create beautiful HTML presentations. Supports multiple themes, mobile-friendly, export to PDF. 单页PPT、HTML演示文稿、PPT生成。
version: 2.0.4
license: MIT-0
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: ["node"]
dependencies: "npm install -g @aspect-ratio/preview-renderer"
---

# Web Slides

为用户生成高质量、单文件、可直接运行的 HTML 演示文稿。

核心定位：

- 不依赖任何 API Key
- 与具体模型、厂商、推理服务无关
- 优先使用预制高端主题，而不是临时拼设计
- 以效果好为第一优先级，同时兼顾低 token
- 输出天然兼容桌面演示与移动端浏览

## 何时使用

- 用户要做 PPT、Slides、演示稿、pitch deck、发布会页面、汇报稿
- 用户要 HTML 版本的演示文稿，而不是 `.pptx`
- 用户强调科技风、高级感、精美、商务、路演、发布会、数据报告
- 用户要求生成结果开箱即用、无需接外部服务

## 工作方式

主 `SKILL.md` 只保留路由和生成规则。需要细节时按需读取：

- 运行时说明：`references/runtime.md`
- 主题总览：`references/theme-catalog.md`
- 布局系统：`references/layout-system.md`
- 质量标准：`references/quality-bar.md`
- 输出流程：`references/assembly-workflow.md`
- 内容结构：`references/content-schema.md`
- 单主题细节：`references/themes/*.md`

本 skill 必须保持模型无关：

- 不假设特定模型品牌、版本或厂商能力
- 不依赖 OpenAI、Claude、GPT 等命名能力
- 不把视觉效果建立在某个模型“更会设计”的前提上
- 重点依赖预制主题、布局系统、内容结构和本地脚本

如果需要快速定位主题、场景、布局或直接拿推荐结果，优先运行：

- `node scripts/get-theme-bundle.mjs --list`
- `node scripts/get-theme-bundle.mjs --theme cyber-grid`
- `node scripts/get-theme-bundle.mjs --scene investor-pitch`
- `node scripts/recommend-deck.mjs --scene investor-pitch --density medium`
- `node scripts/scaffold-deck.mjs --scene ai-product-launch --title "你的标题"`
- `node scripts/markdown-to-content.mjs --input examples/investor-pitch.md --output examples/investor-pitch.json --scene investor-pitch --mobile`
- `node scripts/validate-content.mjs examples/investor-pitch.json`
- `node scripts/qa-deck.mjs --content examples/investor-pitch.json`
- `node scripts/smoke-test.mjs`
- `node scripts/generate-slide-html.mjs --scene investor-pitch --title "Investor Pitch" --out dist/investor-pitch.html`
- `node scripts/generate-slide-html.mjs --content examples/investor-pitch.json --out dist/investor-pitch.html`
- `node scripts/render-preview.mjs --input dist/investor-pitch.html --output dist/investor-pitch.png`
- `node scripts/build-preview-gallery.mjs`

## 生成原则

1. 先定场景，再定主题，再定布局，不要先写 HTML。
2. 输出流程必须与具体模型无关，核心质量来自主题系统、布局系统和本地生成脚本。
3. 优先从预制主题中选最合适的一套；不要混搭到破坏统一性。
4. 优先使用布局原型承载内容；不要每页都自由发挥。
5. 任何页面都要同时检查桌面显示和移动端缩放后的可读性。
6. 如果用户没有给风格，默认走高级、正式、科技感或商务感，不走卡通和花哨路线。
7. 如果用户给的是长文或提纲，优先整理为 `references/content-schema.md` 里的 JSON 结构，再生成 HTML。

## 最小决策流程

### Step 1：识别任务类型

从用户输入中提取：

- 场景：汇报 / 路演 / 产品发布 / 技术分享 / 白皮书 / 数据复盘 / 教学培训
- 调性：科技 / 商务 / 极简 / 高端 / 发布会 / 学术 / 创意
- 内容密度：轻 / 中 / 重
- 输出规模：短 deck（6-10 页）/ 标准 deck（10-16 页）/ 长 deck（16-24 页）
- 是否强调移动端浏览

### Step 2：选择主题

优先先跑脚本拿最小推荐结果，再读 `references/theme-catalog.md`。

如果用户要求很明确，再读对应单主题文件：

- `references/themes/cyber-grid.md`
- `references/themes/executive-dark.md`
- `references/themes/executive-light.md`
- `references/themes/glass-future.md`
- `references/themes/data-intelligence.md`
- `references/themes/startup-pitch.md`
- `references/themes/product-launch.md`
- `references/themes/dev-summit.md`
- `references/themes/luxury-black-gold.md`
- `references/themes/editorial-serif.md`
- `references/themes/neo-minimal.md`
- `references/themes/creative-motion.md`

### Step 3：选择布局集

读 `references/layout-system.md`，从以下布局原型中选 6-10 个组合成整套 deck：

- cover
- agenda
- section-break
- insight
- two-column
- metrics
- chart-focus
- timeline
- comparison
- quote
- closing

### Step 4：按质量标准约束输出

读 `references/quality-bar.md`，确保：

- 首屏有高级感
- 页面层级清楚
- 信息密度可控
- 动效克制
- 手机端不崩

### Step 5：组装 HTML

读 `references/assembly-workflow.md`，或直接用生成器脚本先产出单文件 HTML 骨架。

输出要求：

- 单个 HTML 文件
- CSS 内嵌
- JS 尽量精简
- 对移动端友好
- 不依赖任何 API Key

## 输出偏好

默认生成策略：

- 渲染：自定义单文件 HTML 演示运行时
- 主题：从 12 套旗舰主题中选择
- 布局：优先复用固定布局原型
- 动画：轻量、克制、不卡顿
- 色彩：统一，不乱换
- 文案：标题短、重点强、避免大段堆砌

## 不要这样做

- 不要只换配色而没有版式差异
- 不要把“科技风”理解成荧光蓝堆砌
- 不要为了酷炫牺牲可读性
- 不要在每页塞满 8 个以上 bullet
- 不要把网页长文直接切成幻灯片
- 不要为了省 token 放弃视觉完成度

## 成功标准

这项技能的目标不是“能生成 PPT”，而是生成后让用户觉得：

- 一打开就高级
- 可以直接拿去讲
- 不像普通网页排版
- 手机上看也精致
- 比同类技能更稳定、更省 token、更不依赖外部能力
