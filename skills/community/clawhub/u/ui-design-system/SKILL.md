---
name: ui-design-system
version: 1.0.0
description: "UI 视觉设计系统——配色主题（10预设+自定义生成）+ 美学变体（soft/minimalist/brutalist）+ 协同选择流程"
tags: [creative, frontend, visual, file-based, memory-based]
triggers:
  - 配色主题
  - UI风格
  - 设计系统
  - theme
  - aesthetic
  - 视觉风格
---

# UI Design System v1.0.0

UI 视觉设计系统：**配色（用什么颜色）→ 美学（用什么语言）→ 协同（怎么组合）**。

> 来源：theme-factory v1.0.0（配色主题）+ ui-styles v1.0.0（美学变体）

---

## Part 1: 配色主题

### 1.1 预设主题（10套）

| # | Theme | Vibe | Best For |
|---|-------|------|----------|
| 1 | Ocean Depths | Professional, calming maritime | Corporate, financial, consulting |
| 2 | Sunset Boulevard | Warm, vibrant energy | Creative pitches, marketing, events |
| 3 | Forest Canopy | Natural, grounded earth tones | Environmental, sustainability, wellness |
| 4 | Modern Minimalist | Clean, contemporary grayscale | Tech, architecture, design showcases |
| 5 | Golden Hour | Rich, warm autumnal | Hospitality, lifestyle, artisan brands |
| 6 | Arctic Frost | Cool, crisp precision | Healthcare, technology, clean tech |
| 7 | Desert Rose | Soft, sophisticated dusty tones | Fashion, beauty, interior design |
| 8 | Tech Innovation | Bold, high-contrast modern | Startups, software launches, AI/ML |
| 9 | Botanical Garden | Fresh, organic vibrancy | Food, garden, natural products |
| 10 | Midnight Galaxy | Dramatic, cosmic depth | Entertainment, gaming, luxury brands |

主题定义文件在 `themes/` 目录，每个文件包含：Color Palette（4色）+ Typography（标题/正文字体）+ Best Used For。

### 1.2 自定义主题生成

当预设不匹配时，按此流程生成：

1. **收集输入** — 品牌、受众、情绪、场景
2. **选择调色板** — 4色组合：
   - 深色锚点（背景/文字）
   - 主强调色（CTA/重点）
   - 辅助色（支撑元素）
   - 浅色/中性色（背景/留白）
3. **配对字体** — 标题（有个性）+ 正文（可读性强）
4. **验证对比度** — 确保 WCAG AA 合规
5. **命名主题** — 描述视觉感受的名字
6. **文档化** — 按标准格式写入主题文件

**调色板和谐规则**：
- Complementary（互补）：色轮对面，高对比
- Analogous（类似）：色轮相邻，和谐
- Triadic（三角）：三等分，活力平衡
- Split-complementary（分裂互补）：基础色+互补色两侧，通用

### 1.3 对比度规范

| 组合 | 最低比率 | WCAG 级别 |
|------|----------|-----------|
| 正文文字 on 背景 | 4.5:1 | AA |
| 大文字(18px+) on 背景 | 3:1 | AA |
| UI组件 / 边框 | 3:1 | AA |
| 增强可读性 | 7:1 | AAA |

### 1.4 应用到不同产物

**Slides/文档**：
- 封面：深色背景 + 浅色文字
- 章节标题：强调色 + 标题字体
- 正文：正文字体 + 浅色背景
- 图表/表格：用强调色和辅助色区分数据系列

**HTML / Landing Pages**：
```css
:root {
  --theme-primary: #hex;
  --theme-accent: #hex;
  --theme-secondary: #hex;
  --theme-bg: #hex;
  --theme-font-heading: "Font", sans-serif;
  --theme-font-body: "Font", sans-serif;
}
```

---

## Part 2: 美学变体

> 当视觉方向已确定时，加载对应变体。每个变体是完整的设计系统，含排版、配色、动效和组件规则。

### 2.1 变体选择指南

| 用户说... | 加载变体 |
|-----------|----------|
| "premium", "luxury", "calm", "expensive", "Apple-y", "soft" | `soft.md` |
| "minimalist", "clean", "Linear-style", "Notion-like", "editorial product" | `minimalist.md` |
| "brutalist", "industrial", "Swiss", "mechanical", "raw", "tactical" | `brutalist.md` |

### 2.2 Soft（高端视觉设计）
- **Vibe**: $150k agency build, haptic depth, cinematic spatial rhythm
- **Typography**: Geist, Clash Display, PP Editorial New, Plus Jakarta Sans
- **Color**: Deep OLED black or warm creams, muted sage, deep espresso
- **Motion**: Spring physics, custom cubic-bezier, magnetic hover
- **Signature**: "Double-Bezel" nested card architecture

### 2.3 Minimalist（高级实用主义）
- **Vibe**: Notion/Linear, warm monochrome, typographic contrast
- **Typography**: SF Pro Display, Geist Sans, Lyon Text, Newsreader
- **Color**: Pure white or warm bone (#F7F6F3), ultra-light gray borders
- **Motion**: Invisible — present but never distracting, 600ms fade-up
- **Signature**: Flat bento grids with 1px #EAEAEA borders

### 2.4 Brutalist（工业战术风格）
- **Vibe**: Swiss typographic print meets military terminal
- **Typography**: Neue Haas Grotesk (Black), JetBrains Mono, Archivo Black
- **Color**: Matte unbleached paper (#F4F4F0) OR deactivated CRT (#0A0A0A), aviation red accent
- **Motion**: None — static, mechanical precision
- **Signature**: Zero border-radius, visible compartmentalization, ASCII framing

### 2.5 变体规则

1. **每个项目只选一种变体** — 不要混合美学
2. **写代码前先读完整变体文件** — `references/soft.md` / `minimalist.md` / `brutalist.md`
3. **遵守所有禁令** — 每个变体有绝对负面约束
4. **使用变体推荐字体** — 不要用默认字体替代
5. **应用动效规则** — 每个变体有特定的动效强度

---

## Part 3: 协同选择流程

```
用户需求 → 判断美学方向
  ├─ 方向明确 → 加载对应变体（Part 2）→ 在变体内选择/生成配色（Part 1）
  └─ 方向模糊 → 先选配色主题（Part 1）→ 根据主题气质匹配变体（Part 2）
```

**选择矩阵**：

| 场景 | 推荐变体 | 推荐主题 |
|------|----------|----------|
| 企业官网/后台 | Minimalist | Modern Minimalist / Arctic Frost |
| 品牌营销页 | Soft | Golden Hour / Desert Rose |
| 技术产品发布 | Brutalist / Minimalist | Tech Innovation |
| 电商/消费品 | Soft | Sunset Boulevard / Botanical Garden |
| 娱乐/游戏 | Brutalist | Midnight Galaxy |

### 与 frontend-design 的关系

- `frontend-design` 负责 Brief Inference、Three Dials、通用设计原则
- 本 skill 在美学方向确定后提供具体执行规范
- 变体规则覆盖通用默认值

---

## 文件结构

```
ui-design-system/
├── SKILL.md                          # 本文档
├── themes/                           # 10套预设主题
│   ├── ocean-depths.md
│   ├── sunset-boulevard.md
│   ├── forest-canopy.md
│   ├── modern-minimalist.md
│   ├── golden-hour.md
│   ├── arctic-frost.md
│   ├── desert-rose.md
│   ├── tech-innovation.md
│   ├── botanical-garden.md
│   └── midnight-galaxy.md
└── references/                       # 美学变体详细规范
    ├── soft.md
    ├── minimalist.md
    └── brutalist.md
```

---

## NEVER Do

- 未经确认就应用主题 — 始终让用户明确选择
- 混合不同主题的颜色 — 每个主题是 cohesive unit
- 忽视对比度比率 — 可读性优先于美学
- 用强调色做大段文字 — 强调色只用于 emphasis
- 跳过字体配对 — 标题和正文字体必须互补
- 硬编码主题值 — 使用 CSS variables 便于切换
- 混合美学变体 — 一个项目只用一种变体

---

*Version 1.0.0 — 合并自 theme-factory v1.0.0 + ui-styles v1.0.0*
