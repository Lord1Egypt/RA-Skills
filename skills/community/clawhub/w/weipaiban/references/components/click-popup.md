# 点击弹窗（clickPopup）

画布 `frame as: clickPopup`。**不是** section。底图在弹窗组外面；每个 `clickPopupGroup` 对应一个热点，包含打开按钮、关闭按钮和弹层内容。

适合在一张场景图上探索多个细节。数量与位置服从当前 format。`layered-scroll` 中默认把整个 clickPopup 放进 `foregroundContent`，并在 `backgroundContent` 放同高透明占位画布负责撑高与对齐；不要把交互主体埋在背景内容层。`parallax-scroll` 只放在内容层或近景，不放进背景容器和远景。`coloring-scroll` 只放在滑动层，不放进上色板。它是会员功能：未订阅可预览，导出需订阅，成品摘要必须标明。

## 写法

```html
<svg
  data-type="clickPopup"
  width="390"
  height="520"
  data-name="05 弹窗"
  data-effect="zoom"
  data-button-effect="blink"
>
  <g data-role="base" data-name="底图">
    <image
      href="{scene}"
      x="0"
      y="0"
      width="390"
      height="520"
      data-fit="cover"
    ></image>
    <text x="24" y="24" width="342" height="24" fill="#FAF8F2" font-size="14">
      点击热点看细节 ›
    </text>
  </g>
  <g data-type="clickPopupGroup" data-name="热点-左">
    <image
      data-role="open"
      href="{openBtn}"
      x="48"
      y="220"
      width="72"
      height="72"
    ></image>
    <image
      data-role="close"
      href="{closeBtn}"
      x="170"
      y="36"
      width="50"
      height="50"
    ></image>
    <g data-role="content" data-name="左卡">
      <rect x="24" y="80" width="342" height="360" rx="16" fill="#2C3330" />
      <image
        href="{detail}"
        x="40"
        y="96"
        width="310"
        height="200"
        data-fit="cover"
      ></image>
      <foreignObject x="40" y="308" width="310" height="112">
        <section style="color:#FAF8F2;font-size:14px;line-height:1.7;">
          <p style="margin:0;font-weight:700;">这一处</p>
          <p style="margin:8px 0 0;">点开才看见的说明。</p>
        </section>
      </foreignObject>
    </g>
  </g>
  <g data-type="clickPopupGroup" data-name="热点-右">
    <image
      data-role="open"
      href="{openBtn}"
      x="270"
      y="300"
      width="72"
      height="72"
    ></image>
    <image
      data-role="close"
      href="{closeBtn}"
      x="170"
      y="36"
      width="50"
      height="50"
    ></image>
    <g data-role="content">
      <image
        href="{detail2}"
        x="0"
        y="0"
        width="390"
        height="520"
        data-fit="contain"
      ></image>
    </g>
  </g>
</svg>
```

`<image>` 必须成对闭合。不要写成 `<section data-type="clickPopup">`（400）。

## 结构

```text
svg clickPopup
├── g data-role=base          底图（始终可见；可多元素）
└── g data-type=clickPopupGroup  × N
    ├── image data-role=open
    ├── image data-role=close
    └── g data-role=content     优先组：图 + 文；也可整幅 image
```

转换器按 `data-role`（或 `data-uid`）打编辑器 uid，不靠 HTML 顺序认角色。`groups[frame]` 先写各组、再写底图。

## 属性

| 节点 / 属性           | 规则                                                                                    |
| --------------------- | --------------------------------------------------------------------------------------- |
| `data-type`（svg）    | 必须 `clickPopup`                                                                       |
| `width` / `height`    | 宽 **390**；高必填。竖 520 / 方 390 / 横 220                                            |
| `data-effect`         | `zoom`（默认）/ `slide` / `slideZoom` / `none`                                          |
| `data-button-effect`  | `blink`（默认）/ `none`                                                                 |
| 底图                  | 至少 1 个非 popup 子节点。推荐一块 `g data-role="base"`                                 |
| popup 组              | **1–6**（转换器）；技能一篇 **2–4**（单组也合法，示例用 2）                             |
| `data-role="open"`    | **必须 `<image>`**。优先写自定义透明图片的 `href`；不允许用 text 代替                   |
| `data-role="close"`   | **必须 `<image>`**。可用默认图，也可写自定义透明图片 `href`                             |
| `data-role="content"` | `<g>`（推荐）或 `<image>`。组内：`image` / `rect` / `text` / `foreignObject` / 普通 `g` |

每组恰好 1 个 open、1 个 close、1 个 content。组内禁止 `animationGroup`、禁止再套 `clickPopupGroup`。

默认图片按钮（未准备自定义素材时使用）：

- open `https://svg-cdn.creatby.com/87703fa265d63e51ace59bba88e0dfc1815254e0.png`
- close `https://svg-cdn.creatby.com/28498232ef90fc3f5a5e24097dd6c99469022319.png`

open 按钮默认从素材池的透明装饰里选一张：在 `asset-request.json` 单列，`role=transparent`、`cropMode=contain`。没有透明图时该槽位占位。多个热点可以复用同一张。按钮图不要带小字，语义由清楚的图形轮廓表达，点前说明由底图层的 hint 承担。

open 的可见尺寸建议 64–88px，点击热区不得小于 44×44px；close 建议 44–56px。各 open 对准画面上不同主体，不要叠在同一点。hint 写在底图层，字号至少 14px，并有足够对比的底或描边；不要写进 popup group。

本块 **不计** 辅助动画组配额。配图从同一素材池选 1 张场景底图，每组再选 1 张细节；不够就复用。

## 和别的块的分工

|                               | 用                                 |
| ----------------------------- | ---------------------------------- |
| 图上多热点、点开看细节/图文卡 | **本组件**                         |
| 整块两面互切                  | [click-switch.md](click-switch.md) |
| 入场点缀                      | 普通 `<svg>` + 动画组              |
