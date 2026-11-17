# 流式 HTML 方言（每轮必读）

提交给 `POST/PUT /api/v1/vectors/svg`。违反即 400。

默认写流式 richtext。章节主图要插画感时用图文 SVG（普通 `<svg>`，见 [image-svg.md](components/image-svg.md)）。需要动效或叠层时，在同级插入辅助 `<svg>`。图集用 `<section data-type="slideshow">`。左右滑动的自由画布用 [horizontal-scroll.md](components/horizontal-scroll.md) 的外壳（可选 `overlay` + 横向 `scroller` + `data-max-width="none"`）。两面互切用 `<section data-type="clickSwitch">`（层内是 svg）。图上多热点用 `<svg data-type="clickPopup">`。不要写 `<details>`。`overlay` / `scroller` 只出现在横向滑动外壳里。轮播、横向滑动、点击切换、点击弹窗一篇里不限块数，也可以混用。

## 骨架

```html
<section data-name="月下团圆" data-background="#FAF8F2">
  <section data-type="richText" data-name="01 版首">
    <section style="padding:16px 10px;">…</section>
  </section>
  <svg width="390" height="160" data-name="01 入场点缀">…</svg>
  <section data-type="richText" data-name="02 钩子">
    <section style="padding:16px 10px;">…</section>
  </section>
</section>
```

| 标签 | 映射 | 要点 |
| --- | --- | --- |
| 根 `<section>` | 作品 section | `data-name`；`data-background` 用主题纸色，不要 `#FFFFFF` / `#000` |
| `<section data-type="richText">` | 流式富文本 | innerHTML 即正文，见 [richtext.md](components/richtext.md) |
| `<section data-type="slideshow">` | 轮播图集 | 子节点仅 `<img>`。见 [slideshow.md](components/slideshow.md) |
| 横向滑动外壳 | 横向滑动展现 | 垂直 section 内：可选 `overlay`，然后唯一的横向 `scroller`，其内唯一宽画布。见 [horizontal-scroll.md](components/horizontal-scroll.md) |
| `<section data-type="clickSwitch">` | 点击切换 | 恰好 2 层 svg。见 [click-switch.md](components/click-switch.md) |
| `<svg data-type="clickPopup">` | 点击弹窗 | frame；底图 + 多组热点。见 [click-popup.md](components/click-popup.md) |
| `<svg width="390">` | 画布 | 辅助点缀见 [svg.md](components/svg.md)；章节插画式配图见 [image-svg.md](components/image-svg.md) |

- 根必须是普通 `<section>`。技能自己写根。
- 一个节拍一块 richtext；画布、图文 SVG、轮播、横向滑动或点击交互插在相关节拍旁，不要把整节改成画布。图文 SVG / 轮播 / 横向滑动的图注仍用下一块 richtext。
- `<svg data-type="clickPopup">` 按 [click-popup.md](components/click-popup.md) 写，不要当成辅助画布。
- 块间距写在块内 padding/margin（根 autoLayout spacing 为 0）。
- 画布里的 `text` / `rect` / `image` / `foreignObject` / `g` **必须在 `<svg>` 内**，直接放进 section 会 400。
- 整段 ≤ 512KB、元素 ≤ 300（画布内每个子元素都计数）。
- **禁止** `<!-- 注释 -->`。流式块内禁 `class` / `id` / `<style>` / JS。

示例：`examples/chapter-flow.html`、`examples/image-svg-beat.html`、`examples/motion-beat.html`、`examples/slideshow-beat.html`、`examples/horizontal-scroll-beat.html`、`examples/click-switch-beat.html`、`examples/click-popup-beat.html`。
