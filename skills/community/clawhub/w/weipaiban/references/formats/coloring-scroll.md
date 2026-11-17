# 滑动上色 `coloring-scroll`

一块上色板固定在视口里，垫在纵向滑动层后面。滑动层里要上色的区域保持透明。内容从下往上穿过色板时，镂空先对着下半的纸色，再进入上半的附色，读起来像在上色。

本页定义该 format 的设计规则、任务数据和 HTML 壳。制作时仍须遵守 [共享方言硬约束](../dialect.md)。滑动层里实际用到哪个组件，再读对应的 [组件文档](../components/)。

## 适用与禁用

适合：填色、线稿上色、滚动显色，以及颜色本身要参与叙事的主题。

不适合：连续长文、没有镂空关系的满幅插画、需要远近速度差的纵深。后一种用 `parallax-scroll`。要固定锚点和多层同速叠读时用 `layered-scroll`。

## 体验骨架

```text
作品根层（宽 390，背景色 = 纸色）
├── plate：顶层叠加(后层)，固定上色板，不占滚动高度
└── scroll：纵向 scroller，viewportHeight 默认 600
    └── 竖向流动内容，总高大于视口；镂空区域露出后面的色板
```

- `plate`：只有一块上色板。上半是要附上的颜色，下半与滑动内容的纸色相同，中间一条过渡分割。不放文字、按钮和第二张图，不接点击。
- `scroll`：主要叙事层，也决定可滚动长度。要上色的地方留空或使用透明通道；不透明的纸底、文字和控件盖住色板。

默认 `viewportHeight=600`。它是可调整的设计值；修改时同步 `design.json` 和 scroller 的 `height`。色板显示高度不小于视口，顶对齐，不随内容滚动。过渡分割落在视口中下段，让未上色和已上色同时留在屏幕里。

上色方向固定：

| 位置 | 颜色                     | 镂空经过时       |
| ---- | ------------------------ | ---------------- |
| 上半 | 附色                     | 显出要涂上的颜色 |
| 过渡 | 附色与纸色之间的一条分割 | 颜色在这里出现   |
| 下半 | 与纸底相同               | 看起来还没上色   |

内容向上移动，镂空先经过下半，再进入上半。

## 滑动层可以放什么

滑动层沿用方言里 scroller 已能解析的流式子树，不另设窄白名单：

- `svg`：普通画布。`<text>`、`<foreignObject>` 和 `<g data-type="animationGroup">` 写在 SVG 内。
- 直接 `<image>`：镂空长图或其它流式图片。
- `slideshow`、`clickPopup`、`details`、`clickSwitch`、`richText`。

色板层不走这份清单：它里面只有一张上色板图，或一块表示同一色板的 SVG。

两层都不要再嵌 `overlay`、`scroller` 或 `parallax`。

## 设计规则

### 先定色板和镂空

先画出首屏和至少两个滚动位置：哪些镂空还停在纸色带，哪些已经进入附色带。再写正文。

- 纸底、色板下半、根层 `data-background` 使用同一个色值。
- 附色与纸色都要能在深色模式下成立，避开纯黑和纯白。详细约束见 [微信深色模式](../wechat-dark-color.md)。
- 去掉镂空之后如果画面几乎不变，说明上色没有参与叙事，应重新设计。

### 镂空

- 位图镂空只用素材池里 `transparent=true` 的图，`contain`。没有则改用 SVG 留空。用户自己的不透明图才走 `rembg`。
- SVG 只画不该变色的形状，留空就是镂空。整幅不透明底再盖一层透明矩形，挖不出洞。
- 文字放在纸色形状上，不靠镂空上色。
- 独立 richText 若自带不透明底，会把色板挡死；正文优先放进 SVG。

### 内容与交互

- 滑动内容总高必须大于视口。
- 滑动层和其中的画布不要写不透明 `data-background`。
- clickPopup、details、clickSwitch、slideshow 可以放在滑动层。可点面点前要有可见 hint；不用大透明画布盖住滑动。clickPopup 的 open 使用 64–88px 的透明图片按钮，hint 字号至少 14px。使用 clickPopup 时，成品摘要标明未订阅可预览、导出需订阅。
- slideshow 的图注写在相邻 SVG。一件作品通常使用 1–3 种交互或动效机制。
- AI 声明必须是滑动层的最后一个 SVG，固定文案“文章部分内容由AI辅助设计和制作”。声明本身铺在纸色上。

### 上色板

- 纯色硬边或两三级色阶：写一块 SVG。先铺满纸色，再在上半盖附色。过渡的 y 落在视口中下段。不要写 `<path>` 或 `<mask>`，解析器会丢掉它们。
- 波浪、笔触、晕边：从素材池的场景图里选一张，作为色板层的直接 `<image>`。宽 390，高等于 `round(390 × 原图高 / 原图宽)`，且不小于视口。`data-fit="contain"`。这张图不循环，也不使用 `orientation=background`。池里没有场景图时改回纯色 SVG。
- 用户已提供上色板时直接上传使用。

## `design.json` 契约

顶层 `format` 固定为 `coloring-scroll`：

```json
{
  "format": "coloring-scroll",
  "shell": {
    "viewportHeight": 600,
    "scrollDirection": "vertical",
    "paperColor": "#1F3A28",
    "paintColor": "#E6B325",
    "plate": {
      "id": "plate",
      "role": "overlay-back",
      "kind": "svg",
      "purpose": "固定上色板",
      "height": 700,
      "splitY": 420
    },
    "scroll": {
      "id": "scroll",
      "role": "scroller",
      "purpose": "镂空内容向上穿过色带",
      "contentHeight": 1140
    }
  }
}
```

`plate.kind` 为 `svg` 或 `image`。`image` 时写 `assetId`，过渡在图片里，不写 `splitY`。`svg` 时 `splitY` 是附色矩形的高度，且 `0 < splitY < viewportHeight`。`plate.height >= viewportHeight`。`scroll.contentHeight` 等于滑动层直接子块高度之和，并且大于 `viewportHeight`。

每个 `blocks[]` 必须包含 `id`、`kind`、`layer`、`name`、`height` 与可执行的 `layout`。`layer` 只能是 `plate` 或 `scroll`。

- `plate` 恰好一块。`kind` 为 `svg` 或 `image`。
- `scroll` 的 `kind` 可以是 `svg`、`image`、`slideshow`、`clickPopup`、`details`、`clickSwitch`、`richText`。animationGroup 记在所属 SVG 的 `features` 里。
- 可点块必须写 `hint`。图片引用稳定 `assetId`。
- 最后一块为 `ai-credit`，`layer="scroll"`、`kind="svg"`。

完整数据形状见 [`examples/formats/coloring-scroll/design.json`](../../examples/formats/coloring-scroll/design.json)。

## HTML 壳语法

根 section 先写后层上色板，再写纵向 scroller。色板用图时：

```html
<section data-name="作品标题" data-background="#1F3A28">
  <section data-type="overlay" data-name="顶层叠加(后层)">
    <image href="{plate}" width="390" height="700" data-fit="contain"></image>
  </section>
  <section
    data-type="scroller"
    data-scroll-direction="vertical"
    height="600"
    data-name="滑动层"
  >
    <image href="{hollow}" width="390" height="1180" data-fit="contain"></image>
    <svg width="390" height="40" data-name="AI声明">...</svg>
  </section>
</section>
```

纯色硬边把色板换成一块 SVG。纸色矩形先写，附色矩形后写，附色才叠在上半：

```html
<section data-type="overlay" data-name="顶层叠加(后层)">
  <svg width="390" height="700" data-name="上色板">
    <rect x="0" y="0" width="390" height="700" fill="#1F3A28"></rect>
    <rect x="0" y="0" width="390" height="420" fill="#E6B325"></rect>
  </svg>
</section>
```

### 上色板

- 使用 `<section data-type="overlay">`，不写 `data-elevated`，或显式写 `data-elevated="false"`。它是 scroller 的前一个兄弟节点。
- 这一层高度为 0，不占滚动长度。图片或画布从中溢出来，铺在滑动层后面。
- 不要写 `pointer-events="visible"`，也不要写 `data-translate-z` 或 `data-rotate3d`。

### 滑动层

- `data-type="scroller"`、`data-scroll-direction="vertical"`，`height` 等于 `shell.viewportHeight`。
- 直接子节点的高度相加形成滚动长度。直接 image 与 SVG 都可以，按书写顺序纵向排列。
- 镂空长图必须显式写成 `<image ...></image>`。
- AI 声明是滑动层的最后一个直接子节点。

组件细节只按实际使用读取：

- [SVG 画布](../components/svg.md)
- [点击弹窗](../components/click-popup.md)
- [轮播](../components/slideshow.md)
- [动画组](../components/animation-group.md)
- [SVG 内富文本](../components/richtext.md#画布内-foreignobject)

## 发布前质量闸门

- 根层恰有后层 overlay 与纵向 scroller 两个直接子层，色板在前。
- 色板 `elevated` 为 false，高度为 0，不接点击。显示高度不小于视口。
- 上半是附色，下半与滑动内容纸色、根层背景是同一个色值。过渡落在视口内。
- 滑动内容总高大于视口。要上色的区域是透明镂空，滑动层没有整屏不透明底。
- 色板里没有文字、按钮或第二张图。两层都没有再嵌 overlay、scroller 或 parallax。
- 可点面点前有 hint。clickPopup 若出现，只在滑动层，并在成品摘要标明会员导出。
- manifest URL 原样使用。AI 声明位于滑动层末尾。总元素 ≤300、HTML ≤512KB。

完整 HTML 见 [`examples/formats/coloring-scroll/work.html`](../../examples/formats/coloring-scroll/work.html)。示例用 SVG 硬边色板说明契约，不复制其题材、配色或构图。波浪过渡仍按上面的直接 image 壳制作。
