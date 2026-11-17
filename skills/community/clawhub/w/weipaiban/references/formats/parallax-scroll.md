# 3D视差多层滑动 `parallax-scroll`

一个背景容器铺在视差容器后面。视差容器里的远景、内容层和近景随同一次纵向滑动以不同速度错开；近景可以再加一个轻微立体转角。速度差来自编辑器视差容器的 `translateZ`，转角来自近景的 `rotate3d`。不要手写 `perspective`、`preserve-3d`、缩放补偿或内层滚动轨道，这些由导出器生成。

本页定义该 format 的设计规则、任务数据和 HTML 壳。制作时仍须遵守 [共享方言硬约束](../dialect.md)；只读取本页白名单内、作品实际使用的 [组件文档](../components/)。

## 适用与禁用

适合：纵深空间、路线推进、产品分层拆解，以及需要远的慢、近的快、近处还有一点立体面的主题。

不适合：连续长文、信息密集说明、不需要速度差的叠层阅读。后一种用 `layered-scroll`。

## 体验骨架

```text
作品根层（宽 390）
├── background：顶层叠加背景容器，写在视差容器前面
└── parallax：纵向视差容器，viewportHeight 默认 700
    ├── far：远景，translateZ < 0，不写 rotate3d，滑得更慢
    ├── content：内容层，translateZ = 0，恰好一层，不写 rotate3d
    └── near：近景，translateZ > 0，可写轻微 rotate3d，滑得更快
```

- `background`：纯色画布或一张背景图。高度不小于内容层画布高度之和。不放文字、按钮和第二张图，不接点击。
- `far`：慢层。透明景物和远处装饰，画布矮于内容层。
- `content`：基准速度，也是主要叙事层。开场、推进、高潮、收口和 AI 声明都在这里。画布高度之和必须大于另外每一层。
- `near`：快层，可以有轻微转角。元素少，留出中间，不要铺满挡住滑动。更近的一层用更大的正 `translateZ`，转角幅度仍然受同一上限约束。

默认 `viewportHeight=700`。它是可调整的设计值；修改时同步 `design.json` 和 parallax 的 `height`。`perspective` 固定为 `1`，不要在 HTML 里写 `data-perspective`。

深度用下面这组小数，不要写成几十或几百：

| 职责             | `data-translate-z` | `data-rotate3d` |
| ---------------- | ------------------ | --------------- |
| 远景             | `-0.2`             | 不写            |
| 内容             | `0`                | 不写            |
| 近景             | `0.18`             | 可写            |
| 更近一层（可选） | `0.25`             | 可写            |

层数默认 3，最多 5。每层一个不同的深度。至少一层 `translateZ > 0` 的近景带上下面任一转角，作品才有立体面。

可照抄的近景转角（单位是度，绝对值不超过 `0.08`）：

- 绕竖轴轻侧：`0.1 -1 0 0.036`
- 浅混合倾斜：`-0.6 0.3 0.7 0.032`

`perspective` 为 1 时，普通 CSS 里的 `8deg` 会把层转进相机后面。这里的 `0.03`～`0.06` 已经是可见的轻微立体，不要自行加大。

## 当前组件白名单

`far`、`content`、`near` 当前只能使用以下块级组件：

- `svg`：普通画布。`<text>`、`<foreignObject>` 和 `<g data-type="animationGroup">` 只能写在 SVG 内。
- `clickPopup`：必须使用 `<svg data-type="clickPopup">`。只放在内容层或近景；按钮写 `pointer-events="visible"`。
- `slideshow`：使用 `<section data-type="slideshow">`，放在内容层。图注另写相邻 SVG。

明确禁用独立 `<section data-type="richText">`、`<details>` 和 `<section data-type="clickSwitch">`。深度层里也不要再套 `overlay`、`scroller` 或另一个 `parallax`。

`background` 不走上述白名单：它是 overlay，里面只放一块纯色 SVG，或一张 `<image>`（可以包在 SVG 里，也可以是该层唯一的直接 image）。

## 设计规则

### 先定四层关系

先画出首屏和至少两个滚动位置上，背景、远景、内容和近景谁露出来，再写正文。

- 背景给整段滑动一个连续的底。纯色用本篇色板；图片则是一张铺满背景画布的图。
- 远景从边缘经过，移动更慢，让内容像从它前面走过。
- 内容层承担阅读。去掉近景和远景之后，故事仍然完整。
- 近景只在局部出现，并带轻微转角，读起来比内容更靠近屏幕。

若远景、近景和背景换成同一张不透明满幅图之后体验几乎不变，说明深度没有参与叙事，应重新设计。

### 内容与交互

- 每屏一个视觉焦点。标题、正文和混色文字使用 SVG 内的 `<text>` 或 `<foreignObject>`。
- clickPopup 的 open 使用 64–88px 的透明图片按钮，hint 是按钮之外的点前说明，字号至少 14px。核心信息不只藏在弹窗里。
- 前景点击面不要用大透明画布盖住滑动。层本身不接指针，只有按钮打开 `pointer-events="visible"`。
- 一件作品通常使用 1–3 种交互或动效机制。
- AI 声明必须是内容层的最后一个 SVG，固定文案“文章部分内容由AI辅助设计和制作”。
- 视差容器是会员功能：未订阅可预览，导出需订阅。成品摘要必须标明。

### 背景与其它图片

- 纯色背景写一个满幅 `<rect>`，颜色来自色板，避开纯黑和纯白，不进图片槽。
- 要图片背景时按 [assets.md](../assets.md) 取一张。可循环长底只用 `orientation=background` 的那张。
- 远景和近景的景物用 `role=transparent`。
- 背景画布高度 ≥ 内容层画布高度之和。内容层高于远景，也高于每一层近景。

### 色彩与深色模式

全篇只走一条色彩路线。正文与局部色块避免纯黑、纯白和写死白底；详细约束见 [微信深色模式](../wechat-dark-color.md)。纵深来自速度差、转角、透明和遮挡。

## `design.json` 契约

顶层 `format` 固定为 `parallax-scroll`：

```json
{
  "format": "parallax-scroll",
  "shell": {
    "viewportHeight": 700,
    "perspective": 1,
    "scrollDirection": "vertical",
    "background": {
      "id": "background",
      "role": "overlay-background",
      "kind": "solid",
      "purpose": "整段滑动的底色",
      "height": 840
    },
    "layers": [
      {
        "id": "far",
        "role": "far",
        "translateZ": -0.2,
        "purpose": "慢速远景",
        "contentHeight": 600
      },
      {
        "id": "content",
        "role": "content",
        "translateZ": 0,
        "purpose": "主要叙事",
        "contentHeight": 840
      },
      {
        "id": "near",
        "role": "near",
        "translateZ": 0.18,
        "rotate3d": "0.1 -1 0 0.036",
        "purpose": "快速近景与轻微转角",
        "contentHeight": 500
      }
    ]
  }
}
```

`background.kind` 为 `solid` 或 `image`。`image` 时写 `assetId`。`layers[].role` 只能是 `far`、`content`、`near`。`content` 恰好一层，且不得带 `rotate3d`。`far` 的 `translateZ` 小于 0，不得带 `rotate3d`。`near` 的 `translateZ` 大于 0；写了 `rotate3d` 时角度绝对值不超过 0.08。

每个 `blocks[]` 必须包含 `id`、`kind`、`layer`、`name`、`height` 与可执行的 `layout`。`layer` 只能是 `background`、`far`、`content`、`near`。

- 深度层的 `kind` 只能是 `svg`、`clickPopup`、`slideshow`。animationGroup 记在所属 SVG 的 `features` 里。
- `background` 对应一个 `kind` 为 `solid` 或 `image` 的结构记录，不算内容组件。
- 某一层的 `contentHeight` 等于该层直接子块高度之和。
- `content.contentHeight` 大于其他每个深度层的 `contentHeight`，并且 `background.height >= content.contentHeight`。
- 可点块必须写 `hint`。图片引用稳定 `assetId`。
- 最后一块为 `ai-credit`，`layer="content"`、`kind="svg"`。

完整数据形状见 [`examples/formats/parallax-scroll/design.json`](../../examples/formats/parallax-scroll/design.json)。

## HTML 壳语法

根 section 先写背景容器，再写视差容器。视差容器的直接子层按远景、内容、近景书写：

```html
<section data-name="作品标题" data-background="#F4EFE6">
  <section data-type="overlay" data-elevated="true" data-name="背景容器">
    <svg width="390" height="840" data-name="背景画布">
      <rect x="0" y="0" width="390" height="840" fill="#F4EFE6"></rect>
    </svg>
  </section>
  <section
    data-type="parallax"
    height="700"
    data-scroll-direction="vertical"
    data-name="视差容器"
  >
    <section data-name="远景" data-translate-z="-0.2">
      <svg width="390" height="600" data-name="远景画布">...</svg>
    </section>
    <section data-name="内容" data-translate-z="0">
      <svg width="390" height="800" data-name="开场">...</svg>
      <svg width="390" height="40" data-name="AI声明">...</svg>
    </section>
    <section
      data-name="近景"
      data-translate-z="0.18"
      data-rotate3d="0.1 -1 0 0.036"
    >
      <svg width="390" height="500" data-name="近景画布">...</svg>
    </section>
  </section>
</section>
```

图片背景把纯色 `rect` 换成一张图，仍然只放在背景容器里：

```html
<section data-type="overlay" data-elevated="true" data-name="背景容器">
  <svg width="390" height="840" data-name="背景画布">
    <image
      href="{background}"
      x="0"
      y="0"
      width="390"
      height="840"
      data-fit="cover"
    ></image>
  </svg>
</section>
```

### 背景容器

- 使用 `data-type="overlay"` 和 `data-elevated="true"`，作为视差容器的前一个兄弟节点。
- 它的高度为 0，不占滚动长度；画布从中溢出来铺在透明内容后面。视差容器写在它后面，滚动层盖在背景之上。
- 不要在这一层写 `data-translate-z` 或 `data-rotate3d`。

### 深度层

- 每个直接子节点都是不带 `data-type` 的 `<section>`，并写 `data-translate-z`。
- 远景和内容层不要写 `data-rotate3d`。近景的 `data-rotate3d` 是四个数 `x y z deg`。
- 不要写 `data-perspective`、`data-perspective-origin`、`data-overflow`。滚动方向只写 `vertical`。
- 层内 SVG 的 `width` 固定 390。同一层里多块满宽 SVG 会纵向排开。
- AI 声明是内容层的最后一个直接子节点。

组件细节只按实际使用读取：

- [SVG 画布](../components/svg.md)
- [点击弹窗](../components/click-popup.md)
- [轮播](../components/slideshow.md)
- [动画组](../components/animation-group.md)
- [SVG 内富文本](../components/richtext.md#画布内-foreignobject)

## 发布前质量闸门

- 根层恰有背景 overlay 与 parallax 两个直接子层，背景在前。
- parallax 为纵向，视口高与 `shell.viewportHeight` 一致；HTML 没有写 `perspective`。
- 恰好一个 `translateZ=0` 的内容层，其画布高度之和大于其他深度层，且不超过背景画布高度。
- 远景和内容层没有非零 `rotate3d`。至少一层近景的转角绝对值在 0.08 度以内。
- 背景容器没有文字和点击。近景没有大面积挡住滑动。
- clickPopup 只在内容层或近景，open 是可见图片按钮，点前有 hint。
- 没有独立 richText、details、clickSwitch，也没有层内的 overlay、scroller 或第二个 parallax。
- manifest URL 原样使用。AI 声明位于内容层末尾。总元素 ≤300、HTML ≤512KB。
- 成品摘要标明视差容器需要订阅后才能导出。

完整 HTML 见 [`examples/formats/parallax-scroll/work.html`](../../examples/formats/parallax-scroll/work.html)。示例只说明契约与语法，不复制其题材、配色或构图。
