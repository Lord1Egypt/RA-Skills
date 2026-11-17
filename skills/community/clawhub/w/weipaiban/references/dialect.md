# 作品 HTML 方言硬约束速查（/api/v1/vectors/svg · 每轮必读）

本页只定义所有 format 共享的解析硬约束；format 文档可以进一步收窄可用组件。作品壳与层级读已选择的 format 文档；
具体标签再按需读 [components](components/)；动效名单见
[components/effect-presets.md](components/effect-presets.md)。
**先满足硬约束再谈美观，违反即 400。**

## 两套坐标系（不要混用）

- **流式层**：`<section>` / `<details>` / `<section data-type="clickSwitch">` 上下排列；section 内也可直接放 `<image>` 作为流式图片。
- **画布层**：`<svg>` 内部绝对定位——`<text>` / `<foreignObject>` / `<image>` / `<rect>` / `<circle>` / `<line>` / `<g>` / `<animate>`。
  这些画布标签通常**必须写在 `<svg>` 里**；唯一例外是 section 下的直接 `<image>`，用于纵向流式图片堆叠。

## 会直接 400 的硬约束

- 根必须是 `<section>` / `<details>` / `<svg>`（单个 svg 会自动包一层作品 section）。
- **最多 300 元素**（含包装层）；**编组最深 5 层**；**流式嵌套最深 5 层**；整段 **≤ 512KB**。
- `<svg>` **`width` 固定 390**；**`height` 精确沿用声明值**（需自动撑高写 `data-auto-expand="true"`）。
- `<image>` **三件套必填**：`href`（站内 CDN `svg-cdn.creatby.com`，或另给 `data-asset-name`）+ `width` + `height`。禁 `javascript:`/`data:`/`//` 地址。
- **动效白名单外即 400**：禁 `<animateMotion>`、`stroke-dashoffset`；preset 见 [components/effect-presets.md](components/effect-presets.md)（54 个，**不是** frame 的 24 个）。
- `<details>` **必须有 `<summary>`**，且 summary 后至少一层内容。
- `clickSwitch` **必须恰好 2 层**（before / after）。
- `animationGroup` **只能在 `<svg>` 内**，禁止嵌套、禁止作为 section 子节点。
- `slideshow` **必须 2–12 张** `<img>` / `<image>`，且声明 `height`。
- `clickPopup` 必须是 `<svg data-type="clickPopup">`（不是 section）；至少 1 个 `clickPopupGroup` + 外部底图；每组 `open`/`close` 为 `<image>`，`content` 为 `<g>` 或 `<image>`。
- `parallax` 只支持纵向。直接子节点必须是普通 `<section>` 深度层，且每层至少一个流式子节点。`data-translate-z` 必须 `< 1`。`data-rotate3d` 写成 `x y z deg`，只允许出现在 `data-translate-z > 0` 的层上，角度绝对值 ≤ 0.08。层内禁止再嵌 `parallax`、`scroller`、`overlay`。

- `quiz` 必须恰好有 questions / before / after 三个 390 宽画布；每题至少两个选项、恰好一个正确项；点击区域不重叠；结果含 0 分兜底。完整语法见 [quiz](formats/quiz.md)。
- `choiceExpand` 恰好四块画布：左右封面宽 195 且同高，左右展开宽 390 且同高，展开高度不小于封面高度。每张封面一个 `expandTrigger`，每张展开稿一个 `collapseTrigger`。四选一、六选一是 2 或 3 个这种 section 竖向叠放。完整语法见 [choice-expand](formats/choice-expand.md)。

`scene-transition` 复用 overlay、等高 SVG 和画布“高度归零”动效，不新增 `data-type="sceneTransition"`。归零动效是 SVG 的直接子节点，不放进动画组；完整结构见 [场景转场](formats/scene-transition.md)。

## 流式标签

| 标签                                 | 映射       | 要点                                                                                                                                                                              |
| ------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<section data-type="quiz">`         | 计分答题   | 三画布结构；每题单次单选，选中后叠加反馈；点击提交展开向下匹配的结果。见 [quiz](formats/quiz.md)                                                                                  |
| `<section data-type="choiceExpand">` | 选择其一   | 一行二选一。左右封面同高，左右展开同高。四选一、六选一是多行叠放。见 [choice-expand](formats/choice-expand.md)                                                                    |
| `<section>`                          | section    | 垂直组合画布与交互；`data-name` / `data-background`                                                                                                                               |
| `<svg>`                              | frame      | 一块画布；内部走画布方言；叠加层里可点时写 `pointer-events="visible"`                                                                                                             |
| `<svg data-type="clickPopup">`       | 点击弹窗   | 底图在组外；N 个 `g data-type="clickPopupGroup"`（open/close 图 + content 组）。见 [components/click-popup.md](components/click-popup.md)                                         |
| `<details>` + `<summary>`            | 点击展开   | summary=展开前；其后每个直接子节点=一层展开后；可再嵌套 details                                                                                                                   |
| `<section data-type="clickSwitch">`  | 点击切换   | 恰好 2 子层；`data-state="before"\|"after"` 或书写顺序                                                                                                                            |
| `<section data-type="overlay">`      | 顶层叠加   | `data-elevated="true"` 前层 / 缺省后层；子树与普通 section 相同                                                                                                                   |
| `<section data-type="scroller">`     | 滑动层     | `height` 视口高（默认 600）；`data-scroll-direction`；子树与普通 section 相同。横向滑动的唯一直接子 `<svg>` 可写 `data-max-width="none"` 且 `width` > 390、≤ 1560，此时不缩到 390 |
| `<section data-type="parallax">`     | 3D 视差    | 纵向视口，默认高 700；`perspective` 固定为 1。直接子层用 `data-translate-z`，近景才可写轻微 `data-rotate3d`。见 [formats/parallax-scroll.md](formats/parallax-scroll.md)          |
| `<section data-type="richText">`     | 流式富文本 | innerHTML 为正文（纯内联 HTML）；不再解析为流式子树                                                                                                                               |
| `<section data-type="slideshow">`    | 轮播图集   | 子节点用 `<img src>`（`<image>` 须成对闭合）；2–12 张；`height` 必填。见 [components/slideshow.md](components/slideshow.md)                                                       |
| section 下直接 `<image>...</image>`  | 流式图片   | `href` + `width` + `height` 必填；必须显式闭合；按书写顺序排布，不需要 SVG；用于长背景重复堆叠                                                                                    |
| `<g data-type="animationGroup">`     | 动画组     | **仅画布内**；`data-mode` / `data-trigger` / `data-order`                                                                                                                         |

## 画布标签（`<svg>` 内）

| 标签              | 元素   | 要点                                                                                                                            |
| ----------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- |
| `<text>`          | 文本   | `fill` / `font-size`(16) / `data-align` / `data-valign`；**不解析 `font-weight`，字重恒 400**；宋体要显式 `font-family="serif"` |
| `<foreignObject>` | 富文本 | 见 [components/richtext.md](components/richtext.md)；用 `<section>` 不用 `<div>`；**粗标题只能在这里做**                        |
| `<image>`         | 图片   | 三件套必填；`data-fit`=`contain`\|`cover`\|`fill`                                                                               |
| `<rect>`          | 图形   | `fill` 纯色 / `rx`；圆用 `rx`≥半边长                                                                                            |
| `<circle>`        | 圆形   | `cx` / `cy` / `r`；转换成等边圆角矩形                                                                                           |
| `<line>`          | 线段   | `x1` / `y1` / `x2` / `y2` / `stroke` / `stroke-width`                                                                           |
| `<g>`             | 编组   | `transform="translate(x,y)"` 或 `data-x/data-y`                                                                                 |

**层叠**：SVG 文档靠后 = 叠更上层。背景先写，文字/前景后写。

## 动效 preset

完整 54 个中文名、进出成对、以及**动画组禁用 width/height** 见
[components/effect-presets.md](components/effect-presets.md)。写法：

`<animate data-preset="左滑渐现" data-trigger="load" data-delay="0" data-duration="0.7" />`

组触发动效的 `data-trigger` 须与组相同：点击出现/消失用 `pointerUp`，自动播放用 `load`。不要用缺省的 load 配点击组，否则时间轴是空的。
出现/消失组里仍可另挂 `data-trigger="load"` 的自动播放（与组 `data-mode` 无关）。
**`load` 且从透明开始的入场**（渐现、上浮渐现、左滑渐现、弹入、盖章、放大出现等）：元素必须写 `opacity="0"` 和 `data-editor-visible="true"`，否则播放前会先完整显示再闪一下。组触发的点击入场不要写 opacity 0（套组 wrapper 负责）；漂浮/呼吸/心跳等循环氛围不要写（从可见开始，写 0 会一直看不见）。
autoplay 无执行顺序（不写 `data-order`）。appear/disappear 正向 `down` 从上到下、反向 `up` 从下到上；delay 跟播放顺序对齐，不要倒写 HTML 换方向。duration 不要全相同。

组内推荐：渐现、上浮渐现、左滑渐现、弹入、盖章。循环氛围：漂浮、呼吸、闪烁、钟摆。摇摆是一次性衰减，不要 `indefinite`。

## `<image>` 占位图 URL

| 比例 | URL                                                                                                     |
| ---- | ------------------------------------------------------------------------------------------------------- |
| 2x3  | `https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/2d21226218402d33a1766d175d57de2094df4874.png_large` |
| 3x2  | `https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/93c19eefa547172bee902b6a8b0c7e5c25aa3566.png_large` |
| 3x4  | `https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/e0aaf2ba7d33fad7e0e6bd38278ba5d83af25d39.png_large` |
| 4x3  | `https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/6bfbc9f89541c901b68bb9b2ce6323b75f61dca7.png_large` |
| 9x16 | `https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/b41b901953ab639e3a41360ff72415a0b0b75bef.png_large` |
| 16x9 | `https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/778ff62e975858f9e774c26e530fdff749fd952f.png_large` |
| 21x9 | `https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/f1a3517d3756cc29ae3fb31b743b6de26a7a6fc1.png_large` |
| 1x1  | `https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/019ddbf3a1cfd4f8e48f1c6eec0442dd11f34bdf.png_large` |

## 最小合规骨架

```html
<section data-name="作品" data-background="#f7f3ea">
  <svg width="390" height="120" data-name="标题条">
    <rect x="0" y="34" width="10" height="52" fill="#3b6cff" rx="2" />
    <text x="24" y="48" width="350" height="40" fill="#132038" font-size="28">
      这里是主标题
      <animate data-preset="上浮渐现" data-duration="0.7" />
    </text>
  </svg>
</section>
```
