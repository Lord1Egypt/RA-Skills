# 三层视差滑动 `layered-scroll`

一个中间固定内容层悬在滚动视口之上；视口内部由背景图专用层、前景内容层和背景内容层组成。三层随同一个 scroller 滑动，通过透明内容、遮挡和显露形成连续情境。这里的“视差”指层叠阅读体验，不承诺不同滚动速度。

本页定义该 format 的设计规则、任务数据和 HTML 壳。制作时仍须遵守 [共享方言硬约束](../dialect.md)；只读取本页白名单内、作品实际使用的 [组件文档](../components/)。

## 适用与禁用

适合：地标巡礼、路线叙事、空间探索、产品拆解、时间推进，以及需要固定视觉锚点与多层情境共同讲故事的主题。

不适合：连续长文、信息密集型说明、没有透明前后景关系的主题。

## 体验骨架

```text
作品根层（宽 390，overflow hidden）
├── middleFixed：中间固定内容层，overlay，悬在滚动视口之上
└── scroll：纵向 scroller，viewportHeight 默认 620
    ├── backgroundImage：背景图专用层，overlay-back
    ├── foregroundContent：前景内容层，overlay-front
    └── backgroundContent：背景内容层，普通流式 section，提供滚动高度
```

- `middleFixed`：固定视觉锚点，可放透明主体、标题或小型控制；不放 clickPopup，内容应克制，不得大面积阻断滑动。
- `backgroundImage`：不使用 SVG 包裹，直接纵向排列多个宽 390 的 `<image>`。只用一张可循环背景，再重复引用同一个 CDN URL，直到图片显示高度之和不小于 `backgroundContent` 的内容高度。
- `foregroundContent`：位于滚动内容前方，优先承载 clickPopup 等交互，以及透明人物、框景、装饰和情境元素；可只覆盖首屏，也可用长画布贯穿多屏。
- `backgroundContent`：正常文档流，是主要叙事层并决定可滚动长度；内容不能靠不透明满幅底色持续盖住背景图层。

默认 `viewportHeight=620`、`canvasHeight=600`。它们是可调整的设计值，不是解析器常量；修改时必须同步 `design.json`、scroller 的 `height`、中间固定画布和所有按首屏对齐的前景画布；背景图片高度则按原图比例及背景内容总高度独立计算。

## 当前组件白名单

`middleFixed`、`foregroundContent` 和 `backgroundContent` 当前只能使用以下块级组件：

- `svg`：普通画布；`<text>`、`<foreignObject>` 和 `<g data-type="animationGroup">` 只能写在 SVG 内。
- `clickPopup`：必须使用 `<svg data-type="clickPopup">`，不是 section。
- `slideshow`：使用 `<section data-type="slideshow">`；图注另写相邻 SVG。

明确禁用独立 `<section data-type="richText">`、`<details>` 和 `<section data-type="clickSwitch">`。后续只有在 format 文档和示例同步扩展后才能新增块级组件。

`backgroundImage` 不走上述白名单：它本身是 overlay section，直接子节点只能是 `<image>`，不能有 SVG、编组、文字、图形、动画或交互。

## 设计规则

### 先设计四层关系

先画出首屏和至少两个滚动节点的遮挡关系，再写正文：

- 固定层给读者一个始终可见的坐标，例如月相、罗盘、人物局部或章节标记。
- 背景图层建立统一世界；同一张无缝长背景首尾连续重复，覆盖整段滚动内容。
- 前景内容层从边缘或局部经过，制造“从景物后面走过”的感觉。
- 背景内容层利用透明画布、留白和局部色块推进剧情，让底景在关键位置重新显露。

若移除 `middleFixed` 与 `foregroundContent` 后体验几乎不变，说明层级没有参与叙事，应重新设计。

### 内容与交互

- 每屏只有一个视觉焦点；背景内容层承担开场、推进、高潮、收口和 AI 声明。
- 标题、正文与混色文字使用 SVG 内的 `<text>` 或 `<foreignObject>`；不得用独立 richText 补正文。
- clickPopup 默认放在 `foregroundContent`，让热点、图片按钮和弹层成为明确的前景交互；不要放在 `middleFixed`。若交互前已有 600px 开场，先在前景 overlay 放同高透明 SVG，再放 clickPopup；同时在 `backgroundContent` 的相同位置放与 clickPopup 同高的透明 spacer，为 scroller 撑高并保持纵向对齐。
- slideshow 属于连续叙事，默认放 `backgroundContent`。前景层必须只让实际图片按钮与弹层接管点击，透明区域继续让出滑动。
- 可点击面点前必须有可见 hint；核心信息不只藏在弹窗内。
- 一件作品通常使用 1–3 种交互或动效机制，不为凑组件而添加。
- AI 声明必须是 `backgroundContent` 的最后一个 SVG，固定文案“文章部分内容由AI辅助设计和制作”。

### 背景长图

背景槽按 [assets.md](../assets.md) 取 `orientation=background` 的那一张。选中之后：

- 只保留一个背景 assetId。`tileHeight = round(390 × height / width)`，宽高用素材接口的返回值。
- `repeatCount = ceil(backgroundContentHeight / tileHeight)`；`repeatCount × tileHeight` 必须大于等于背景内容层的实际总高度。背景内容高度变化后必须重新计算。
- 每个重复 `<image>` 都写 `width="390"`、`height="{tileHeight}"` 和同一个 `href`；必须显式写成 `<image ...></image>`，不能用会吞并后续兄弟节点的 HTML 自闭合写法 `<image ... />`。按 HTML 顺序自然纵向堆叠，不写 `x` / `y`，不加间距、圆角、透明度或动效。

### 其它图片

- `middleFixed`、`foregroundContent` 和 `backgroundContent` 中用于叠景的人物、道具、框景用 `role=transparent`。
- clickPopup 的 open 默认使用 64–88px 的透明图片按钮，并在素材清单单列；不要用小字号 text 充当热点按钮。hint 是按钮之外的点前说明，字号至少 14px。
- 要压字的图片在槽位上留出对应净空，选图时避开主体正中被字挡住的那张。
- 同一情境的连续图片优先复用同一张场景图。

### 色彩与深色模式

全篇只走一条色彩路线。正文与局部色块避免纯黑、纯白和写死白底；详细约束见 [微信深色模式](../wechat-dark-color.md)。纵深主要来自图片、透明度、尺度与遮挡，不靠堆装饰。

## `design.json` 契约

顶层 `format` 固定为 `layered-scroll`，`shell` 使用嵌套结构：

```json
{
  "format": "layered-scroll",
  "shell": {
    "viewportHeight": 620,
    "canvasHeight": 600,
    "middleFixed": {
      "id": "middleFixed",
      "role": "overlay-fixed",
      "purpose": "固定视觉锚点"
    },
    "scroll": {
      "id": "scroll",
      "role": "scroller",
      "layers": [
        {
          "id": "backgroundImage",
          "role": "overlay-background-image",
          "purpose": "可循环长背景",
          "assetId": "background-tile",
          "tileHeight": 1170,
          "repeatCount": 2,
          "totalHeight": 2340
        },
        {
          "id": "foregroundContent",
          "role": "overlay-foreground-content",
          "purpose": "透明前景与框景"
        },
        {
          "id": "backgroundContent",
          "role": "flow-background-content",
          "purpose": "主要剧情与滚动高度",
          "contentHeight": 1972
        }
      ]
    }
  }
}
```

每个 `blocks[]` 必须包含 `id`、`kind`、`layer`、`name`、`height` 与可执行的 `layout`。`layer` 只能是 `middleFixed`、`backgroundImage`、`foregroundContent` 或 `backgroundContent`。

- 内容层的 `kind` 只能是 `svg`、`clickPopup`、`slideshow`；animationGroup 记录在所属 SVG 的 `features` 中，不单独成块。
- `backgroundImage` 对应一个 `kind="imageStack"` 的结构记录，包含唯一 `assetId`、按原图比例计算的 `tileHeight`、`repeatCount` 与 `totalHeight`；它不算内容组件。
- `backgroundContent.contentHeight` 必须等于其直接子块高度之和；`backgroundImage.totalHeight >= backgroundContent.contentHeight`。
- 前景 clickPopup 必须有 `placement.y` 或前置透明 SVG 标明纵向位置；`backgroundContent` 中对应一个同高 `kind="svg"` 的透明 spacer，保证内容高度和交互位置一致。
- 可点块必须写 `hint`；图片引用稳定 `assetId`。
- `placement` 用于叠加层道具，形如 `{ "x": 150, "y": 16, "width": 220, "height": 220 }`。
- `layout` 写坐标、透明关系、图片处理和遮挡意图，不写无法执行的气氛形容词。
- 最后一块为 `ai-credit`，`layer="backgroundContent"`、`kind="svg"`。

完整数据形状见 [`examples/formats/layered-scroll/design.json`](../../examples/formats/layered-scroll/design.json)。

## HTML 壳语法

根 section 先写中间固定层，再写 scroller。scroller 的三个直接子层必须按背景图、前景内容、背景内容的顺序书写：

```html
<section data-name="作品标题" data-background="#F7F7F7">
  <section data-type="overlay" data-elevated="true" data-name="中间固定内容层">
    <svg width="390" height="600" data-name="固定内容画布">...</svg>
  </section>
  <section
    data-type="scroller"
    data-scroll-direction="vertical"
    height="620"
    data-name="滑动长图内容层"
  >
    <section data-type="overlay" data-elevated="false" data-name="背景图专用层">
      <image
        href="{background-tile}"
        width="390"
        height="1170"
        data-fit="contain"
      ></image>
      <image
        href="{background-tile}"
        width="390"
        height="1170"
        data-fit="contain"
      ></image>
    </section>
    <section data-type="overlay" data-elevated="true" data-name="前景内容层">
      <svg width="390" height="600" data-name="前景内容画布">...</svg>
      <svg data-type="clickPopup" width="390" height="520" data-name="场景探索">
        ...
      </svg>
    </section>
    <section data-name="背景内容层">
      <svg width="390" height="600" data-name="开场">...</svg>
      <svg width="390" height="520" data-name="场景探索占位">
        <rect
          x="0"
          y="0"
          width="390"
          height="520"
          fill="#F7F7F7"
          opacity="0"
        ></rect>
      </svg>
      <section data-type="slideshow" height="520" data-name="沿途图集">
        ...
      </section>
      <svg width="390" height="40" data-name="AI声明">...</svg>
    </section>
  </section>
</section>
```

### 叠加层

- 根下 `middleFixed` 与 scroller 内 `foregroundContent` 使用 `data-elevated="true"`；`backgroundImage` 使用 `false`。
- 背景图专用层的直接 image 按顺序纵向排列。所有 image 的 `href` 相同，总显示高度必须覆盖背景内容层；不使用 SVG 包裹。
- overlay 默认不接管指针。需要交互时，只在实际按钮或画布上开启可点击能力，不得用透明大画布覆盖 scroller。
- `foregroundContent` 的画布高度按实际叙事决定：只影响首屏时用 `canvasHeight`，贯穿全文时可与背景内容总高度一致。
- 前景 clickPopup 前面的透明 SVG 与背景内容中的块一一对应，使弹窗滚动到预定位置；背景内容的同高 spacer 不放文字、图片、交互或不透明底。

### scroller 与背景内容

- scroller 固定 `data-scroll-direction="vertical"`，`height` 等于 `shell.viewportHeight`。
- 背景内容层使用普通 `<section>`，由其中 SVG、前景交互的同高 spacer 与 slideshow 的高度累加形成滚动长度。
- 背景图与前景 overlay 自身高度为 0，不参与 scroller 的内容高度计算；背景图的直接 image 通过 overflow 覆盖滚动区，背景内容普通 section 才负责撑高。
- AI 声明是背景内容普通 section 的最后一个直接子节点。

组件细节只按实际使用读取：

- [SVG 画布](../components/svg.md)
- [点击弹窗](../components/click-popup.md)
- [轮播](../components/slideshow.md)
- [动画组](../components/animation-group.md)
- [SVG 内富文本](../components/richtext.md#画布内-foreignobject)

## 发布前质量闸门

- 根层恰有中间固定 overlay 与 scroller 两个直接子层；scroller 内三层顺序正确。
- 默认视口 620、首屏画布 600；如有调整，design 与 HTML 所有关联尺寸一致。
- 背景图专用层没有 SVG；直接子节点全部是指向同一 CDN URL 的 image，纵向总高度不小于背景内容高度，且没有点击能力。
- 这张背景来自素材池里 `orientation=background` 的图；池里没有时该槽位是占位图，摘要里写明。
- clickPopup 位于前景内容层，open 使用清楚可见的图片按钮；前景与固定层没有大面积拦截滑动，所有可点面点前有 hint。
- 背景内容层确实提供滚动高度，并以透明内容或局部色块持续露出底景。
- 没有独立 richText、details 或 clickSwitch；文字和 foreignObject 都位于 SVG 内。
- manifest URL 原样使用；失败素材已明确回退并在摘要披露。
- AI 声明位于背景内容层末尾；总元素 ≤300、HTML ≤512KB。

完整 HTML 见 [`examples/formats/layered-scroll/work.html`](../../examples/formats/layered-scroll/work.html)。示例只说明契约与语法，不复制其题材、配色或构图。
