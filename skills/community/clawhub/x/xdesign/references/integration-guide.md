# 融合集成指南（Integration Guide）

> **适用版本**：x-design v1.x（fused with html-ppt-skill v0.1+）
> **目标读者**：使用本 skill 的 Agent 开发者 & 维护者
> **目的**：解释 XDesign + html-ppt-skill 融合的架构、路由、适配层

## 1. 为什么融合

| 维度 | XDesign 原本 | html-ppt-skill | 融合后 |
|---|---|---|---|
| 核心定位 | 通用设计工作流引擎 | 演示文稿工作室 | 通用设计 + PPT 一体 |
| 视觉能力 | 设计系统提取、品牌色、58 个 DESIGN.md | 36 主题 + 31 布局 + 47 动效 | 全部保留 |
| 输出形态 | React+Babel 单页 HTML | 纯静态 HTML+CSS+JS | 全部保留 |
| 演讲者支持 | ❌ | ✅ 4 卡片 + 提词器 + 计时器 | ✅ |
| 设计系统 | ✅ 58 品牌 | ❌ | ✅ 58 品牌 |
| 多环境兼容 | ✅（CDN + 静态） | ✅（零构建） | ✅ |

**结论**：XDesign 的设计系统提取能力是 html-ppt-skill 缺的；html-ppt-skill 的完整 deck 模板和演讲者模式是 XDesign 缺的。**双向融合 = 1+1>2**。

## 2. 目录结构

```
XDesign/                          ← <skill-base>
├── SKILL.md                      ← 入口 + Intent Router + Mode 1/2/3
├── README.md                     ← 用户面向
├── LICENSE
├── assets/
│   └── design-md/                ← 58 个品牌 DESIGN.md（XDesign 原生）
│       ├── stripe/DESIGN.md
│       ├── linear.app/DESIGN.md
│       └── ... 共 58 个
├── references/                   ← 文档（XDesign 原生 + 新增）
│   ├── design-system-catalog.md
│   ├── technical-specs.md
│   ├── workflow-guide.md
│   ├── integration-guide.md      ← 本文件
│   └── deck-studio-catalog.md    ← deck-studio 速查
├── evals/
│   └── eval-plan.json
└── deck-studio/                  ← 【新】子模块（html-ppt-skill 完整克隆）
    ├── SKILL.md
    ├── README.md / README.zh-CN.md
    ├── LICENSE
    ├── assets/
    │   ├── base.css              ← 设计令牌 + 布局原语
    │   ├── fonts.css             ← webfont imports
    │   ├── runtime.js            ← 键盘 + 演讲者 + 主题循环
    │   ├── themes/               ← 19 个主题 CSS
    │   └── animations/           ← animations.css + 20 个 FX
    ├── references/               ← 6 篇详细文档
    ├── templates/
    │   ├── deck.html             ← 最小 6 页 starter
    │   ├── theme-showcase.html   ← 36 主题展示
    │   ├── layout-showcase.html  ← 31 布局展示
    │   ├── animation-showcase.html
    │   ├── full-decks-index.html
    │   ├── full-decks/           ← 15 个 full-deck 模板
    │   └── single-page/          ← 28 个 single-page 布局
    └── scripts/
        ├── new-deck.sh
        └── render.sh             ← headless Chrome → PNG
```

## 3. 三模式路由表

| 用户触发 | 模式 | 入口 | 输出 |
|---|---|---|---|
| "做一份 PPT" | Mode 1 | `deck-studio/templates/deck.html` 或 `templates/full-decks/<name>/` | 单文件 HTML 或多文件目录 |
| "做 slides" | Mode 1 | 同上 | 同上 |
| "我要去讲 xxx" | Mode 1 | `deck-studio/templates/full-decks/presenter-mode-reveal/` | 多文件目录 |
| "带逐字稿" | Mode 1 | 同上 | 同上 |
| "pitch deck" | Mode 1 | `deck-studio/templates/full-decks/pitch-deck/` | 多文件目录 |
| "小红书图文" | Mode 1 | `deck-studio/templates/single-page/image-grid.html` | 单文件 HTML |
| "设计一个 APP" | Mode 2 | XDesign 原生 `deck_stage.js` 或 `design_canvas.jsx` | 单文件 HTML（React+Babel） |
| "做 dashboard" | Mode 2 | 同上 | 同上 |
| "做一个 landing page" | Mode 2 | 同上 | 同上 |
| "做设计系统" | Mode 2 | `assets/design-md/<brand>/DESIGN.md` | DESIGN.md + 组件示例 |
| "动效视频" | Mode 3 | XDesign `animations.jsx` | 单文件 HTML（time-based） |
| "时间轴动画" | Mode 3 | 同上 | 同上 |

## 4. 适配层（Adapter Layer）

### 4.1 路径适配

XDesign 的 `references/` 引用 `assets/`，但 deck-studio 把资源放在自己的 `deck-studio/assets/`。**绝对不要在 XDesign 的根目录里复制 assets**——双份资源会导致主题/动画版本不一致。

```html
<!-- 错误：在 XDesign 根目录放主题 -->
<link rel="stylesheet" href="assets/themes/aurora.css">

<!-- 正确：从 deck-studio 子目录引用 -->
<link rel="stylesheet" href="deck-studio/assets/themes/aurora.css">
```

### 4.2 主题命名映射

deck-studio 的 36 个主题全部在 `deck-studio/assets/themes/` 已下载。包括：academic-paper, arctic-cool, aurora, bauhaus, blueprint, catppuccin-latte, catppuccin-mocha, corporate-clean, cyberpunk-neon, dracula, editorial-serif, engineering-whiteprint, glassmorphism, gruvbox-dark, japanese-minimal, magazine-bold, memphis-pop, midcentury, minimal-white, neo-brutalism, news-broadcast, nord, pitch-deck-vc, rainbow-gradient, retro-tv, rose-pine, sharp-mono, soft-pastel, solarized-light, sunset-warm, swiss-grid, terminal-green, tokyo-night, vaporwave, xiaohongshu-white, y2k-chrome.**

**Agent 可直接按使用场景推荐，无需再检查磁盘。**

### 4.3 启动模板选择

| 场景 | full-deck 模板 | 备选 |
|---|---|---|
| 产品发布会 | `templates/full-decks/product-launch/` | `deck.html` |
| 投资人 pitch | `templates/full-decks/pitch-deck/` | `deck.html` |
| 技术分享（带提词器）| `templates/full-decks/tech-sharing/` | `templates/full-decks/presenter-mode-reveal/` |
| 周报 | `templates/full-decks/weekly-report/` | `deck.html` |
| 课程模块 | `templates/full-decks/course-module/` | `deck.html` |
| 小红书图文 | `templates/single-page/image-grid.html` | `templates/single-page/image-hero.html` |
| 演讲（有提词器）| `templates/full-decks/presenter-mode-reveal/` | 无替代 |

### 4.4 多环境兼容层

deck-studio 的资源是 CDN-friendly 的：

```html
<!-- 任意环境下都能跑 -->
<link rel="stylesheet" href="deck-studio/assets/base.css">
<link rel="stylesheet" id="theme-link" href="deck-studio/assets/themes/aurora.css">
<script src="deck-studio/assets/runtime.js"></script>
```

**无构建步骤**：
- 无 `npm install` / 无 webpack / 无 vite
- webfont 走 `fonts.css` 的 CDN 引用（Google Fonts）
- 动画走 `animations.css` 命名样式 + `data-anim` 属性

**运行环境**：
- ✅ Trae IDE artifact 模式（Claude Code）
- ✅ Claude.ai artifacts
- ✅ 任意浏览器（`open index.html`）
- ✅ GitHub Pages（路径相对）
- ✅ 本地 `file://` 协议
- ⚠️ 注意 `runtime.js` 用 `postMessage`，需要父窗口或单窗口模式

## 5. 反模式（Anti-patterns）

### ❌ 错误 1：XDesign 的 deck 路径被绕过

```html
<!-- 错误：直接用 React+Babel 写演示文稿 -->
<deck-stage>
  <section>...slide 1...</section>
</deck-stage>
<script type="text/babel">...</script>
```
→ 触发词是 "PPT/deck" 时，应该用 `deck-studio/templates/deck.html`，而不是 `deck_stage.js`。

### ❌ 错误 2：把 deck-studio 的主题复制到 XDesign 根目录

```bash
cp -r deck-studio/assets/themes/* assets/themes/  # 错
```
→ 主题更新时会产生双份不一致。

### ❌ 错误 3：在 deck 里写 speaker notes 到 slide 上

```html
<section class="slide">
  <h1>产品发布</h1>
  <p style="font-size: 10px; color: #999">Speaker: 这里可以补充 xxx</p>  <!-- 错 -->
</section>
```
→ Speaker notes 必须进 `<div class="notes">`，由 S 键弹出。

### ❌ 错误 4：混用两套 design token

```css
/* 错 */
.slide { color: #111; }  /* 字面颜色 */
/* 对 */
.slide { color: var(--text-1); }  /* design token */
```

## 6. 维护流程

### 6.1 更新 deck-studio 子模块

当 [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) 仓库更新时：

```bash
# 1. 删除旧的（保留自定义 examples）
rm -rf deck-studio/assets deck-studio/templates deck-studio/references
rm deck-studio/SKILL.md deck-studio/README.md deck-studio/LICENSE
# 2. 重新克隆 / 下载
# （参见 tasks 目录下的 history）
```

### 6.2 添加新主题

```bash
# 1. 创建 CSS 文件
cat > deck-studio/assets/themes/my-theme.css <<'EOF'
:root {
  --bg: #fafafa;
  --text-1: #111;
  --accent: #ff6b6b;
  /* ... 继承 base.css 的全部 token */
}
EOF
# 2. 在 deck-studio/references/themes.md 注册
# 3. 在 XDesign/SKILL.md Mode 1 章节补充
```

### 6.3 添加新 full-deck 模板

```bash
mkdir deck-studio/templates/full-decks/my-deck
# 创建：index.html, style.css, README.md
# 在 deck-studio/references/full-decks.md 注册
# 在 deck-studio/templates/full-decks-index.html 添加 iframe
```

## 7. 验证清单

修改后跑一遍：

- [ ] `ls deck-studio/assets/themes/` — 36 个 CSS 都在
- [ ] `ls deck-studio/templates/full-decks/` — 15 个 full-deck
- [ ] `ls deck-studio/templates/single-page/` — 31 个布局
- [ ] `cat deck-studio/SKILL.md | head -50` — 可读
- [ ] 浏览器打开 `deck-studio/templates/theme-showcase.html` — 主题全部渲染
- [ ] 浏览器打开 `deck-studio/templates/deck.html` — ← → 翻页，T 切主题，S 演讲者模式

## 8. 常见问题

**Q: deck-studio 和 XDesign 的 `assets/` 冲突吗？**
A: 不冲突。`XDesign/assets/` 是 XDesign 原生的 design-md 和组件代码；`XDesign/deck-studio/assets/` 是 html-ppt-skill 的主题和动画。两套独立。

**Q: 一个项目能同时用 XDesign 的 DESIGN.md 配色 + deck-studio 的主题吗？**
A: 可以但**不建议**。两者 design token 命名可能冲突（`--text-1` 在 base.css 里有特定含义，在 DESIGN.md 里可能不同）。优先二选一。

**Q: 输出是单文件 HTML 还是目录？**
A: deck-studio 默认单文件。full-deck 模板因为有 `style.css` 是目录结构。Agent 应输出**自包含** HTML（CDN 引用），不要 inline 大量 CSS。

**Q: 为什么不用 submodule 方式管理 deck-studio？**
A: html-ppt-skill 还在活跃迭代，使用 submodule 容易锁版本；当前采用快照克隆（snapshot clone）方式更稳定。后续如果版本稳定再切到 submodule。
