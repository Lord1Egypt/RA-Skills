# SVG 画布组件

任意 format 容器中的一块 **390 宽画布**（`frame`）。需要绝对定位、叠层或动画时使用。图像与短文案的组合可参考 [image-svg.md](image-svg.md)，动画编排见 [animation-group.md](animation-group.md)。色、圆角和布局服从当前 format 的设计方案。

画布子标签包括：`rect`、`circle`、`line`、`image`、`text`、`foreignObject`、`g`、`g data-type="animationGroup"`。不要在 SVG 内写 `details` / `overlay` / `scroller` / `slideshow`。

普通 `<svg>` 可以是短点缀，也可以是场景画布；高度由 format 与设计稿决定。`<svg data-type="clickPopup">` 是独立交互，见 [click-popup.md](click-popup.md)。点击切换的层内 SVG 见 [click-switch.md](click-switch.md)。

## 画布

```html
<svg width="390" height="200" data-name="01 入场点缀">…</svg>
```

| 属性                 | 规则                                                   |
| -------------------- | ------------------------------------------------------ |
| `width`              | **必须 390**                                           |
| `height`             | 声明多少就是多少；必须与设计稿及所在 format 的层级一致 |
| `data-name`          | 图层名，标清插在哪一拍                                 |
| `data-background`    | 可选纯色；缺省透明，露出作品底                         |
| `data-overflow`      | 图文 SVG 写 `visible`；矮点缀默认不写                  |
| `data-corner-radius` | 画布圆角，默认 0                                       |
| `data-auto-expand`   | `true` 时高度按内容延展；默认 `false`                  |

层叠：HTML **后写的叠在上面**。底 `rect` 先写，字/图后写。

坐标系：子元素 `x/y` 相对画布左上。文字左缘约 8–10（与页边距齐）。

## 子元素

### `rect`

色块、分割短线、卡片底、hint 胶囊。支持 `fill`、`stroke`、`stroke-width`、`stroke-dasharray`、`rx`。只支持纯色矩形；圆形用 `rx` 大于等于短边一半近似。

### `circle` / `line`

- `<circle cx="80" cy="80" r="28" fill="#8A2B2B" />` 转换为等边圆角矩形；支持 `fill`、`stroke`、`stroke-width`。
- `<line x1="24" y1="40" x2="366" y2="40" stroke="#8A2B2B" stroke-width="2" />` 转换为带旋转的细矩形。
- 二者都可挂动效。复杂 path 与描边动画仍不支持。

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

普通编组。`transform="translate(x,y)"` 优先于 `data-x` / `data-y`。支持 `x/y/width/height`、`opacity`、`data-rotation`、`data-name`。图标+标签包进一个 `g` 再挂 animate；嵌套最深 5 层。

无 `data-type` 的 `g` 不是动画组。

## 通用几何属性

所有可见画布元素可使用：

| 属性                  | 含义                                         |
| --------------------- | -------------------------------------------- |
| `x` / `y`             | 相对画布或所在编组的左上角坐标               |
| `width` / `height`    | 元素盒子；`image` 必填                       |
| `opacity`             | 0–1                                          |
| `data-editor-visible` | 元素透明时仅在编辑画布显示，不改变预览与发布 |
| `data-rotation`       | 顺时针旋转角度                               |
| `data-name`           | 编辑器图层名                                 |

`text` 还支持 `font-family`、`font-size`、`letter-spacing`、`data-line-height`、`data-align` 与 `data-valign`。字体只使用 `sans-serif`、`serif`、`monospace`；文本框不会自动撑高。

## 原生 SMIL

优先使用 [preset](effect-presets.md)。需要自定义关键帧时可写：

- `<animate attributeName="opacity|width|height" values="..." />`
- `<animateTransform type="scale|rotate|translate|skewX|skewY" values="..." />`

时序可使用 `data-trigger`、`data-delay`、`data-duration`、`data-repeat`，或等价的 `begin`、`dur`、`repeatCount`。`values` 用分号分隔关键帧，`keyTimes` 数量必须与之相同。

同一元素下、同 trigger 与同时序的多条 SMIL 会合并为组合动效，但同一效果不能重复同一通道。禁止 `<animateMotion>` 和 `stroke-dashoffset`；`animate` 的其它 `attributeName`、`animateTransform` 的其它 `type` 都会导致 400。

```html
<rect x="24" y="40" width="342" height="88" fill="#8A2B2B" rx="12">
  <animateTransform
    type="scale"
    values="1;1.04;1"
    dur="1.8"
    repeatCount="indefinite"
  />
  <animate
    attributeName="opacity"
    values="0.9;1;0.9"
    dur="1.8"
    repeatCount="indefinite"
  />
</rect>
```

## 和 richtext 的分工

下表适用于允许独立 richText 的 format；`layered-scroll` 与 `parallax-scroll` 的文字与图注一律放在 SVG 的 `<text>` 或 `<foreignObject>` 中。

|                              | `data-type="richText"` | 普通画布             | 图文 SVG                      |
| ---------------------------- | ---------------------- | -------------------- | ----------------------------- |
| 长段、清单、图+图注          | 是                     | 否                   | 图注仍用下一块 richtext       |
| 图上压字、色条入场、轻点揭示 | 否                     | 是                   | 否                            |
| 章节主图 + 贴纸 + 点题字     | `<img>`（无装饰）      | 否                   | 是                            |
| 图片标签                     | `<img src>`            | `<image href>`       | `<image href>`                |
| 动效                         | 无效                   | 动画组 / `<animate>` | 贴纸循环 `漂浮`/`呼吸`/`钟摆` |
