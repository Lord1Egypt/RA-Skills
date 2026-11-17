# 点击切换（clickSwitch）

流式层上的 **两面互切**。映射为 `as: clickSwitch`。两层都是 **SVG 画布**，才能叠图、hint 胶囊、轻 autoplay。不要用 richtext 两张静图冒充。

一篇可以有多块，也可以和点击弹窗、轮播、横向滑动出现在同一篇里。插在 04（对照流）或 05。不要放 08 / 09 / AI 声明。

## 写法

```html
<section data-type="clickSwitch" data-name="05 对照" data-effect="fade" data-duration="0.5">
  <section data-state="before">
    <svg width="390" height="520" data-name="改造前">
      <image href="{before}" x="0" y="0" width="390" height="520" data-fit="cover"></image>
      <rect x="24" y="460" width="342" height="36" rx="18" fill="#4A5D52" />
      <text x="24" y="466" width="342" height="24" fill="#FAF8F2" font-size="13" data-align="center">
        改造前 · 点击看之后 ›
      </text>
    </svg>
  </section>
  <section data-state="after">
    <svg width="390" height="560" data-name="改造后">
      <image href="{after}" x="0" y="0" width="390" height="560" data-fit="cover"></image>
      <rect x="24" y="500" width="342" height="36" rx="18" fill="#4A5D52" />
      <text x="24" y="506" width="342" height="24" fill="#FAF8F2" font-size="13" data-align="center">
        改造后 · 点击看之前 ›
      </text>
    </svg>
  </section>
</section>
```

`<image>` 必须成对闭合。色与圆角只来自当前主题。

## 属性

| 属性 | 规则 |
| --- | --- |
| `data-type` | 必须 `clickSwitch` |
| `data-state` | 两层必须 `before` / `after` |
| `data-effect` | 只准 **`fade`** |
| `data-trigger` | 只准 `click`（或缺省） |
| `data-duration` | 秒，缺省 `0.5` |
| `data-name` | 图层名，标清插在哪一拍 |

## 层内容

- 每层 **恰好 1 个** `<svg width="390">`。after 可以更高。
- svg 内：`image` / `rect` / `text` / `foreignObject` / 普通 `g`。入场用 **autoplay 动画组**；hint 写在组外、点前可见。
- **不要** 在层内再放点击 appear 组（和切换抢手势）。
- **不要** 层内嵌套 clickSwitch / details / 轮播 / 弹窗 / richText。

两侧都要有「点击看… ›」。对照流的 Before/After 优先用本组件。配图从同一 tag 的素材池里选两张能对照着看的场景图。只有用户点名了生图技能时，才按该技能做同机位的前后图。

## 和别的块的分工

| | 用 |
| --- | --- |
| 两面互切、日夜、真假、改造前后 | **本组件** |
| 图上多个热点弹层 | [click-popup.md](click-popup.md) |
| 3 张以上同框连看 | [slideshow.md](slideshow.md) |
| 左右滑一条自由画布 | [horizontal-scroll.md](horizontal-scroll.md) |
| 入场点缀 | 矮 `<svg>` + 动画组 |
