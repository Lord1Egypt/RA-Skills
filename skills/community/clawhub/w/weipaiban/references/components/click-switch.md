# 点击切换（clickSwitch）

format 容器中的 **两面互切**，映射为 `as: clickSwitch`。两层优先使用 SVG 画布，以便保持同构、叠图、hint 和轻量 autoplay。

适合前后、日夜、真假和改造对照。数量与放置位置服从当前 format；不要用于 AI 声明。

## 写法

```html
<section
  data-type="clickSwitch"
  data-name="05 对照"
  data-effect="fade"
  data-duration="0.5"
>
  <section data-state="before">
    <svg width="390" height="520" data-name="改造前">
      <image
        href="{before}"
        x="0"
        y="0"
        width="390"
        height="520"
        data-fit="cover"
      ></image>
      <rect x="24" y="460" width="342" height="36" rx="18" fill="#4A5D52" />
      <text
        x="24"
        y="466"
        width="342"
        height="24"
        fill="#FAF8F2"
        font-size="13"
        data-align="center"
      >
        改造前 · 点击看之后 ›
      </text>
    </svg>
  </section>
  <section data-state="after">
    <svg width="390" height="560" data-name="改造后">
      <image
        href="{after}"
        x="0"
        y="0"
        width="390"
        height="560"
        data-fit="cover"
      ></image>
      <rect x="24" y="500" width="342" height="36" rx="18" fill="#4A5D52" />
      <text
        x="24"
        y="506"
        width="342"
        height="24"
        fill="#FAF8F2"
        font-size="13"
        data-align="center"
      >
        改造后 · 点击看之前 ›
      </text>
    </svg>
  </section>
</section>
```

`<image>` 必须成对闭合。色与圆角服从当前设计方案。

## 属性

| 属性            | 规则                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------ |
| `data-type`     | 必须 `clickSwitch`                                                                                     |
| `data-state`    | 两层必须 `before` / `after`                                                                            |
| `data-effect`   | `fade`（默认）/ `retractExpand` / `retractExpandFree` / `opacityExpandFree` / `opacitySingleLayerFree` |
| `data-trigger`  | `click`（默认）/ `touchstart` / `load`                                                                 |
| `data-duration` | 秒，缺省 `0.5`                                                                                         |
| `data-delay`    | 秒，缺省 `0.5`                                                                                         |
| `data-easing`   | 缺省 `ease-out`                                                                                        |
| `data-name`     | 图层名，标清插在哪一拍                                                                                 |

## 层内容

- 根必须恰好两个直接子层。优先写 `<section data-state="before|after">`；都不写 state 时按书写顺序识别。
- 每层可以是一块 SVG，也可以是包含多块 SVG、richText、details 或嵌套 clickSwitch 的完整流式子树；总嵌套深度不超过 5。
- 两侧应保持视觉同构并都有“点击看… ›”hint。入场优先用 autoplay 动画组；避免再放会抢同一手势的点击 appear 组。
- `fade` 最稳妥；其它效果属于会员能力或特殊展开形态，使用前在成品摘要标明。

两侧都要有「点击看… ›」。对照流的 Before/After 优先用本组件。前后两面从素材池选两张场景图，不够就复用同一张。

## 和别的块的分工

|                                | 用                               |
| ------------------------------ | -------------------------------- |
| 两面互切、日夜、真假、改造前后 | **本组件**                       |
| 图上多个热点弹层               | [click-popup.md](click-popup.md) |
| 3 张以上同框连看               | [slideshow.md](slideshow.md)     |
| 入场点缀                       | 矮 `<svg>` + 动画组              |
