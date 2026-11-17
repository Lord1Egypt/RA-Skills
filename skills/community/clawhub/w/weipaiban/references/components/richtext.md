# richtext 组件

`<section data-type="richText">` 的 innerHTML 经 `sanitizeRichTextApiHtml` 入库。先满足硬约束，再谈版式。

字号、色、间距由当前 format 的设计方案决定；本页只定义富文本能力与硬约束。

format 可以进一步收窄本组件。`layered-scroll` 与 `parallax-scroll` 当前都禁止独立 richText；其中的多段、加粗和混色文字只能使用本文末尾的 SVG `<foreignObject>` 写法。

## 硬约束

- 纯内联 `style`。禁止 `class` / `id`、`<style>`、外部样式、JavaScript。
- 用 `<section>` 代替 `<div>`（`div` 会被改写成 `section`）。
- **禁用标签**：`script/iframe/object/embed/style/link/title/meta/head/body`、`form/input/button`、`table/tr/td/th/...`、`video/audio`、`svg/canvas/math/foreignobject`。
- **禁用属性**：`id`、任何 `on*`。
- **禁用样式**：`position`、`float`。分栏用 `display:inline-block`，不要 flex/grid。
- **危险协议会剥离**：`src` / `href` 不能是 `javascript:` / `data:` / `vbscript:` / `file:` / `about:`。图片必须是 https CDN，不能 base64。
- 推荐标签：`section`、`p`、`span`、`strong`/`b`、`em`/`i`、`u`、`a`、`img`、`h1`–`h6`、`ul`/`ol`/`li`、`br`、`hr`、`blockquote`。

## 可用样式

`color`、`background` / `background-color`、`background-image`（https 或 CSS 渐变）、`linear-gradient()` / `radial-gradient()`、`border` / `border-radius`、`padding` / `margin`、`font-size` / `font-weight` / `line-height` / `letter-spacing`、`text-align`、`display:inline-block`、`box-shadow`、`width` / `max-width`、`overflow`、`text-decoration`。

## 图片

```html
<img
  src="{manifest.src}"
  style="display:block;width:100%;max-width:100%;border-radius:{主题圆角}px;"
/>
```

- `src` 原样用配图清单里的 CDN（含 `x-oss-process`），不要改成 `_large`、不要 strip process。
- 一图一意：图下紧跟图注，通常 12px，全篇统一居中或左齐。
- 圆角与卡片同一套，见主题。
- 章节主图要插画感（贴纸、点题短文案、几何留白）时，不要在这里堆 `<img>`，改用 [image-svg.md](image-svg.md)。

## 左右栏（对照流）

画布宽 390，左右边距 8–10px，内容宽约 370。两个 `inline-block` 的 `width` + `margin` **合计 ≤ 96%**。

推荐：`width:46%;margin-right:4%;` + `width:50%;`，或上下堆叠（更稳）。胶囊/标签必须写死 `width` 或 `max-width`，不能靠文字撑。不要把像素宽和百分比混在同一行里相加。

## 自查

- 无 `<!--`、无 `class`/`id`、无 `position`/`float`、无 `table`/`svg`/`script`。
- 块内第一层承担左右页边距；字号、行距和段距服从当前 format 的设计方案。

## 画布内 `foreignObject`

SVG 中的多段、加粗或混色文字使用 `<foreignObject>`，内部只放纯内联 HTML：

```html
<foreignObject x="24" y="40" width="342" height="120">
  <section style="font-size:15px;line-height:1.7;color:#333333;">
    <p style="margin:0;font-weight:700;">标题</p>
    <p style="margin:8px 0 0;">正文内容。</p>
  </section>
</foreignObject>
```

- 使用 `<section>`，不要用 `<div>`。
- 只排文字，不在内部放图片、SVG、脚本、表格或定位布局。
- `font-size`、`line-height`、`color` 与 `text-align` 写在内部节点；外层负责 `x/y/width/height`。
- 粗标题必须用 `foreignObject + font-weight`；SVG `<text>` 的 `font-weight` 不生效。
