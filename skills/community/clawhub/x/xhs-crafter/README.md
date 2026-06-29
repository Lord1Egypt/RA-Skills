# xhs-crafter

将 Markdown 文章排版为 3:4 比例的精美图片卡片 + 压缩文字稿，用于微信公众号/小红书贴图发布。

[![版本](https://img.shields.io/badge/version-7.1.1-blue)](https://github.com/EdwardWason/xhs-crafter)
[![许可证](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-xhs--crafter-orange)](https://clawhub.ai/EdwardWason/xhs-crafter)

## 功能

- **MD → 图片卡片**：自动将 Markdown 文章拆分排版为多张 1080x1440 (3:4) HTML 页面，截图为 PNG
- **双风格系统**：Editorial Magazine（杂志风，衬线+暖纸底）和 Swiss International（瑞士网格风，无衬线+白底）
- **11 品类适配**：商业/科技/职场/旅行/教程/影视/游戏/美食/彩妆/穿搭/家居/健身/情感/推荐，自动路由风格+主题+版式
- **10 套主题色**：Ink Classic / Indigo Porcelain / Forest Ink / Kraft Paper / Dune / Midnight Ink / IKB Blue / Lemon Yellow / Lemon Green / Safety Orange
- **28 种布局模板**：M01-M16（Editorial）+ S01-S12（Swiss）
- **三层背景架构**：paper→wash→grain，氛围强度按页面角色分级（strong/medium/subtle）
- **三层节奏系统**：明暗交替 + 氛围强弱 + 版式多样性
- **密度铁律**：活跃构图 >= 78% 画布高度，确保信息密度
- **字号速查表**：15级字号体系直接嵌入SKILL.md，确保跨会话一致性
- **自动验证**：7项validate.js检查（溢出/footer碰撞/最小字号/密度等）
- **文字压缩**：保留原话引言+场景描述，压缩至 <= 1000 字
- **双通道交付**：本地文件夹 + 飞书云盘同步

## 快速开始

```bash
npx clawhub@latest install EdwardWason/xhs-crafter
```

## 使用方法

在 TRAE / Claude Code / OpenClaw 中，直接提供 MD 文件路径即可触发：

```
请用 xhs-crafter 对这篇文章排版：/path/to/article.md
```

5 步全自动工作流，用户只需给 MD，直接出文件夹：

1. **Intake** — 识别内容品类（自动推断）
2. **Content Plan** — 内容规划（压缩阶梯+页面角色+节奏规划）
3. **Compose** — 组装 HTML（双风格+10 主题+28 布局）
4. **Validate** — 自检（密度+图片+节奏+风格）
5. **Screenshot & Deliver** — 截图交付（本地文件夹+飞书云盘）

## 文件结构

```
xhs-crafter/
├── SKILL.md                              # 技能主文件（入口，含字号速查表）
├── assets/
│   ├── template-editorial-card.html      # Editorial 种子模板
│   ├── template-swiss-card.html          # Swiss 种子模板
│   ├── screenshot.js                     # Puppeteer 截图脚本
│   └── validate.js                       # 7项自动验证脚本
└── references/
    ├── style-system.md                   # Editorial vs Swiss 身份测试+反模式
    ├── category-cookbook.md              # 11 品类路由表
    ├── content-planning.md               # 压缩阶梯+页面角色+钩子模式
    ├── portrait-fill.md                  # 3:4 密度规则+三层节奏系统
    ├── image-overlay.md                  # 文字压图规则
    ├── background-systems.md             # 三层背景架构+氛围强度分级
    ├── theme-presets.md                  # 10 套主题色 CSS 变量
    ├── components.md                     # 字体/字号/间距规范（权威来源）
    ├── layout-recipes.md                 # 28 种布局模板
    ├── screenshot-treatment.md           # 截图装裱规范
    ├── image-sources.md                  # 图库 API 接入+AI生图验证
    └── workflow.md                       # 工作流详细参考
```

## 品类适配

| 品类 | 风格 | 主题 |
|------|------|------|
| 商业/科技分析 | Editorial | Indigo Porcelain |
| 职场/干货 | Swiss | IKB Blue |
| 旅行/生活方式 | Editorial | Kraft Paper |
| 教程/工具 | Swiss | IKB Blue |
| 影视/读书 | Editorial | Ink Classic |
| 游戏 | Editorial (dark) | Midnight Ink |
| 美食 | Editorial | Kraft Paper |
| 彩妆 | Editorial | Dune |
| 穿搭 | Editorial | Indigo Porcelain |
| 家居 | Editorial | Forest Ink |
| 健身/情感/推荐 | Swiss | Safety Orange |

## 文档

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 技能主文件，5 步工作流+字号速查表+密度铁律+节奏铁律 |
| [references/style-system.md](references/style-system.md) | Editorial vs Swiss 视觉锚点+身份测试 |
| [references/components.md](references/components.md) | 字体/字号/间距规范（唯一权威来源） |
| [references/layout-recipes.md](references/layout-recipes.md) | 28 种布局模板详细说明 |
| [references/theme-presets.md](references/theme-presets.md) | 10 套主题色 CSS 变量定义 |
| [references/category-cookbook.md](references/category-cookbook.md) | 11 品类风格/主题/版式映射 |
| [references/background-systems.md](references/background-systems.md) | 三层背景架构+氛围强度分级 |
| [references/portrait-fill.md](references/portrait-fill.md) | 3:4 密度规则+三层节奏系统 |
| [references/image-sources.md](references/image-sources.md) | 图库接入+AI生图验证规则 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录 |

License: MIT-0

---

# xhs-crafter

Convert Markdown articles into beautifully designed 3:4 ratio image cards + compressed text drafts for WeChat Official Account / Xiaohongshu (Little Red Book) image-post publishing.

[![version](https://img.shields.io/badge/version-7.1.1-blue)](https://github.com/EdwardWason/xhs-crafter)
[![license](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-xhs--crafter-orange)](https://clawhub.ai/EdwardWason/xhs-crafter)

## Features

- **MD → Image Cards**: Automatically split and layout Markdown articles into multiple 1080x1440 (3:4) HTML pages, screenshot as PNG
- **Dual Style System**: Editorial Magazine (serif + warm paper) and Swiss International (sans-serif + white + single accent)
- **11 Category Routing**: Business/Tech/Career/Travel/Tutorial/Film/Gaming/Food/Makeup/Fashion/Home/Fitness/Emotion/Recommendation — auto-route style + theme + layout
- **10 Theme Presets**: Ink Classic / Indigo Porcelain / Forest Ink / Kraft Paper / Dune / Midnight Ink / IKB Blue / Lemon Yellow / Lemon Green / Safety Orange
- **28 Layout Templates**: M01-M16 (Editorial) + S01-S12 (Swiss)
- **Three-Layer Background**: paper→wash→grain, atmosphere intensity graded by page role (strong/medium/subtle)
- **Three-Layer Rhythm System**: Light/dark alternation + atmosphere intensity + layout diversity
- **Density Rules**: Active composition >= 78% canvas height, ensuring information density
- **Font Size Cheat Sheet**: 15-level type scale embedded in SKILL.md for cross-session consistency
- **Auto Validation**: 7-rule validate.js (overflow/footer collision/min font/density etc.)
- **Text Compression**: Preserve original quotes + scene descriptions, compress to <= 1000 characters
- **Dual Delivery**: Local folder + Feishu cloud drive sync

## Quick Start

```bash
npx clawhub@latest install EdwardWason/xhs-crafter
```

## Usage

In TRAE / Claude Code / OpenClaw, simply provide an MD file path to trigger:

```
Please use xhs-crafter to layout this article: /path/to/article.md
```

5-step fully automated workflow — just give MD, get output folder:

1. **Intake** — Identify content category (auto-inferred)
2. **Content Plan** — Content planning (compression ladder + page roles + rhythm planning)
3. **Compose** — Assemble HTML (dual style + 10 themes + 28 layouts)
4. **Validate** — Self-check (density + images + rhythm + style)
5. **Screenshot & Deliver** — Screenshot delivery (local folder + Feishu cloud drive)

## File Structure

```
xhs-crafter/
├── SKILL.md                              # Main skill file (entry point, with font size cheat sheet)
├── assets/
│   ├── template-editorial-card.html      # Editorial seed template
│   ├── template-swiss-card.html          # Swiss seed template
│   ├── screenshot.js                     # Puppeteer screenshot script
│   └── validate.js                       # 7-rule auto validation script
└── references/
    ├── style-system.md                   # Editorial vs Swiss identity test + anti-patterns
    ├── category-cookbook.md              # 11-category routing table
    ├── content-planning.md               # Compression ladder + page roles + hook patterns
    ├── portrait-fill.md                  # 3:4 density rules + three-layer rhythm system
    ├── image-overlay.md                  # Text-on-image rules
    ├── background-systems.md             # Three-layer background + atmosphere intensity
    ├── theme-presets.md                  # 10 theme CSS variable definitions
    ├── components.md                     # Font/size/spacing spec (authoritative source)
    ├── layout-recipes.md                 # 28 layout template details
    ├── screenshot-treatment.md           # Screenshot framing spec
    ├── image-sources.md                  # Image API integration + AI image verification
    └── workflow.md                       # Workflow detailed reference
```

## Category Mapping

| Category | Style | Theme |
|----------|-------|-------|
| Business/Tech Analysis | Editorial | Indigo Porcelain |
| Career/Productivity | Swiss | IKB Blue |
| Travel/Lifestyle | Editorial | Kraft Paper |
| Tutorial/Tools | Swiss | IKB Blue |
| Film/Books | Editorial | Ink Classic |
| Gaming | Editorial (dark) | Midnight Ink |
| Food | Editorial | Kraft Paper |
| Makeup | Editorial | Dune |
| Fashion | Editorial | Indigo Porcelain |
| Home | Editorial | Forest Ink |
| Fitness/Emotion/Recommendation | Swiss | Safety Orange |

## Documentation

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Main skill file, 5-step workflow + font size cheat sheet + density rules + rhythm rules |
| [references/style-system.md](references/style-system.md) | Editorial vs Swiss visual anchors + identity test |
| [references/components.md](references/components.md) | Font/size/spacing spec (authoritative source) |
| [references/layout-recipes.md](references/layout-recipes.md) | 28 layout template details |
| [references/theme-presets.md](references/theme-presets.md) | 10 theme CSS variable definitions |
| [references/category-cookbook.md](references/category-cookbook.md) | 11-category style/theme/layout mapping |
| [references/background-systems.md](references/background-systems.md) | Three-layer background + atmosphere intensity |
| [references/portrait-fill.md](references/portrait-fill.md) | 3:4 density rules + three-layer rhythm system |
| [references/image-sources.md](references/image-sources.md) | Image API integration + AI image verification |
| [CHANGELOG.md](CHANGELOG.md) | Version change log |

License: MIT-0
