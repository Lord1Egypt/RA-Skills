# 通用骨架与排版规范

## 通用 HTML 布局骨架

生成 HTML 时使用此骨架，替换 `[STYLE]` 为上方对应风格的 CSS，`[CONTENT]` 为处理后的内容：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>长图</title>
    <style>
    /* === 重置 === */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    ul, ol { padding-left: 1.5em; }
    img { max-width: 100%; }

    /* === 风格样式（从上方复制对应风格） === */
    [STYLE]
    </style>
</head>
<body>
    <div class="container">
        [CONTENT]
    </div>
</body>
</html>
```

---

## 通用排版规范

- **宽度**：容器最大 560px，留两侧 padding（24-40px）
- **行高**：正文 1.7-1.9，标题 1.2-1.4
- **字号层级**：大标题 1.8-2.2em → 小标题 1.1-1.2em → 正文 1em → 辅助 0.8em
- **换行保护**：所有正文和标题加 `word-break: keep-all; overflow-wrap: break-word`，防止中文在标点或奇怪位置断行
- **图片缩放**：不使用外部图片；图标用 CSS 形状或 inline SVG data URI 替代（**不使用 emoji**）
- **输出路径**：PNG 统一存放至输出目录（默认 `./output`，可用环境变量 `T2EI_OUTPUT_DIR` 覆盖）
- **截图高度**：`export_image.js` 自动测量 `.container` 真实高度并精确裁剪，无需手动控制

---

## 开源CSS工具库参考

> 以下工具已验证可在 Puppeteer 无头环境使用（inline / data URI 方式，不依赖 CDN）。

### 1. Hero Patterns（SVG 背景纹理库）
- **地址**：https://heropatterns.com/
- **用法**：将生成的 `background-image: url("data:image/svg+xml,...")` 直接内联到 CSS，零外部依赖
- **适合风格**：报纸风（细点阵纹）、水墨风（云纹）、蒸汽朋克（六边形铆钉铺地）、赛博风（蜂窝网格）
- **注意**：选好颜色和不透明度后复制 CSS code，不要用 `<img>` 方式引入

### 2. MagicPattern CSS Backgrounds（纯 CSS 渐变纹理）
- **地址**：https://www.magicpattern.design/tools/css-backgrounds
- **用法**：生成器产出纯 CSS `background-image: repeating-linear-gradient(...)` 代码，直接复制使用
- **适合场景**：快速生成斜纹、方格、点阵、波浪等背景纹理，不需要 SVG
- **适合风格**：极简风（微噪点）、Cowork 风（点阵）、Bloomberg 风（扫描线）

### 3. Glassmorphism CSS（毛玻璃效果）
- **核心属性**：`backdrop-filter: blur(10-15px)` + `background: rgba(255,255,255,0.1-0.25)` + `border: 1px solid rgba(255,255,255,0.2)`
- **浏览器支持**：Chrome 76+、Safari 9+、Firefox 103+（Puppeteer Chrome 146 完全支持）
- **适合场景**：用于赛博风 `.glass-card`（已使用）、Apple风卡片（已使用）；可做第9种"Aurora毛玻璃风"
- **注意**：需要有背景内容才能看到 blur 效果；纯色背景下无效果

### 4. CSS Shapes / clip-path 技术（纯CSS绘制复杂图形）
- **参考**：MDN clip-path docs、CyberTechUI（Dev.to 2026-01）
- **核心技术**：`clip-path: polygon(...)` 36点路径绘制齿轮；`conic-gradient` 绘制仪表盘刻度；`radial-gradient` 模拟金属质感
- **已用于**：蒸汽朋克风的齿轮、压力表、铆钉（完整示例见风格8）
- **扩展方向**：复杂星形、六边形卡片、斜角切口效果（`.card { clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 0 100%) }`）

### ⚠️ 不适用的框架（禁止使用）
以下框架依赖 CDN 外部资源，Puppeteer 无头环境无法加载，**不要引入**：
- NES.css、XP.css、98.css、RPGUI — 依赖 CDN 字体/图片
- Bootstrap、Tailwind CDN 版 — 外部样式表
