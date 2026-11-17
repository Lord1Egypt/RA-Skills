# richtext 组件

`<section data-type="richText">` 的 innerHTML 经 `sanitizeRichTextApiHtml` 入库。先满足硬约束，再谈版式。

字号、色、间距的配额在 [visual-system.md](../visual-system.md)；本页只谈**一块富文本能写什么**。

## 硬约束

- 纯内联 `style`。禁止 `class` / `id`、`<style>`、外部样式、JavaScript。
- 用 `<section>` 代替 `<div>`（`div` 会被改写成 `section`）。
- **禁用标签**：`script/iframe/object/embed/style/link/title/meta/head/body`、`form/input/button`、`table/tr/td/th/...`、`video/audio`、`svg/canvas/math/foreignobject`。
- **禁用属性**：`id`、任何 `on*`。
- **禁用样式**：`position`、`float`。分栏用 `display:flex`（`align-items`、`gap`、`flex` 可用）。`display:inline-block` 只用于单行小标签。不要 `display:grid`。
- **危险协议会剥离**：`src` / `href` 不能是 `javascript:` / `data:` / `vbscript:` / `file:` / `about:`。图片必须是 https CDN，不能 base64。
- 推荐标签：`section`、`p`、`span`、`strong`/`b`、`em`/`i`、`u`、`a`、`img`、`h1`–`h6`、`ul`/`ol`/`li`、`br`、`hr`、`blockquote`。

## 可用样式

`color`、`background` / `background-color`、`background-image`（https 或 CSS 渐变）、`linear-gradient()` / `radial-gradient()`、`border` / `border-radius`、`padding` / `margin`、`font-size` / `font-weight` / `line-height` / `letter-spacing`、`text-align`、`display:flex`、`display:inline-block`、`box-shadow`、`width` / `max-width`、`overflow`、`text-decoration`。

## 图片

```html
<img src="{manifest.src}" style="display:block;width:100%;max-width:100%;border-radius:{主题圆角}px;" />
```

- `src` 原样用配图清单里的 CDN（含 `x-oss-process`），不要改成 `_large`、不要 strip process。
- 一图一意：图下紧跟图注，12px、`#888`–`#999`，全篇统一居中或左齐（见当前主题）。
- 圆角与卡片同一套，见主题。
- 章节主图要插画感（贴纸、点题短文案、几何留白）时，不要在这里堆 `<img>`，改用 [image-svg.md](image-svg.md)。

## 左右栏（对照流）

画布宽 390，左右边距 8–10px，内容宽约 370。分栏用 flex，不要用两个 `inline-block` 百分比硬拼。

```html
<section style="display:flex;align-items:stretch;gap:12px;">
  <section style="flex:1;min-width:0;">左栏</section>
  <section style="flex:1;min-width:0;">右栏</section>
</section>
```

胶囊/标签写死 `width` 或 `max-width`，不能靠文字撑。窄处挤不下时改成上下堆叠。

## 自查

- 无 `<!--`、无 `class`/`id`、无 `position`/`float`、无 `table`/`svg`/`script`。
- 块内第一层承担左右页边距；字号/行距/段距对照 [visual-system.md](../visual-system.md)。
