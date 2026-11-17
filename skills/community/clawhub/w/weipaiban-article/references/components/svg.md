# SVG 画布组件

流式层上的一块 **390 宽画布**（`frame`）。只在需要叠层或动画时插入，默认仍用 [richtext.md](richtext.md)。**章节插画式配图**（主图 + 贴纸 + 点题字）走 [image-svg.md](image-svg.md)，不要写成矮点缀。动画组见 [animation-group.md](animation-group.md)。色与圆角只来自当前主题，见 [visual-system.md](../visual-system.md)。

本步只写这些子标签：`rect`、`image`、`text`、`foreignObject`、`g`、`g data-type="animationGroup"`。不要写 `details` / `overlay` / `scroller` / `slideshow`（轮播是流式块）。横向滑动的宽画布见 [horizontal-scroll.md](horizontal-scroll.md)，不要把 `overlay` 或 `scroller` 写进 `<svg>`。

普通 `<svg>` 是点缀（高 120–280），`width` 必须 390。图文 SVG 也是普通 `<svg>`，但更高（300–460），角色不同。`<svg data-type="clickPopup">` 见 [click-popup.md](click-popup.md)，不要当辅助画布写。点击切换的层内 svg 见 [click-switch.md](click-switch.md)。

## 画布

```html
<svg width="390" height="200" data-name="01 入场点缀">
  …
</svg>
```

| 属性 | 规则 |
| --- | --- |
| `width` | **必须 390** |
| `height` | 声明多少就是多少。辅助画布宜矮（120–280），不要做成整屏场景 |
| `data-name` | 图层名，标清插在哪一拍 |
| `data-background` | 可选纯色；缺省透明，露出作品底 |
| `data-overflow` | 图文 SVG 写 `visible`；矮点缀默认不写 |

层叠：HTML **后写的叠在上面**。底 `rect` 先写，字/图后写。

坐标系：子元素 `x/y` 相对画布左上。文字左缘约 8–10（与页边距齐）。

## 子元素

### `rect`

色块、分割短线、卡片底、hint 胶囊。`fill` 用主题色；`rx` 用主题卡片圆角。

### `image`

三件套必填：`href`（站内 CDN，含 `x-oss-process`）+ `width` + `height`。`data-fit`：`cover` 或 `contain`。圆角用 `data-corner-radius`（圆形 ≥ 短边一半）。不要用 `<img>`。必须成对闭合。

### `text`

单行标题、hint、印章。**不解析 `font-weight`，字重恒 400。** `fill` 用主题正文/主色，不要 `#000`。

### `foreignObject`

画布上的**多段/加粗/混色文字**。内部纯内联 HTML，用 `<section>` 不用 `<div>`。

- **只排文字**，不放图、不用渐变/阴影/边框当装饰（那些用外面的 `rect`）。
- 粗标题必须走这里，不要用 `<text>` 冒充加粗。
- 禁用标签与流式 richtext 相同（`script`/`table`/`svg`/`img`/`position`/`float`）。

### `g`

普通编组。`transform="translate(x,y)"` 或 `data-x` / `data-y`。图标+标签包进一个 `g` 再挂 animate。

无 `data-type` 的 `g` 不是动画组。

## 和流式 richtext 的分工

| | 流式 `data-type="richText"` | 辅助画布 | 图文 SVG |
| --- | --- | --- | --- |
| 长段、清单、图+图注 | 是 | 否 | 图注仍用下一块 richtext |
| 图上压字、色条入场、轻点揭示 | 否 | 是 | 否 |
| 章节主图 + 贴纸 + 点题字 | `<img>`（无装饰） | 否 | 是 |
| 图片标签 | `<img src>` | `<image href>` | `<image href>` |
| 动效 | 无效 | 动画组 / `<animate>` | 贴纸循环 `漂浮`/`呼吸`/`钟摆` |
