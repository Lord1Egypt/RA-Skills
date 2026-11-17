# 横向滑动展现

流式层上的一块 **可左右滑动的宽画布**，上面可以再叠一层固定内容。映射为编辑器里的垂直外壳 + 顶层叠加（`uid: foregroundContainer`）+ 横向滑动层（`as: scroller`）+ `maxWidth: "none"` 的画布。

一篇可以有多块，用来把同一套浏览节奏重复到几个章节。也可以和轮播、点击切换、点击弹窗出现在同一篇里。插在 01 或 04。不要放 08 / 09 / AI 声明。没有横向浏览的理由就不要加。

这不是自动切页的轮播，也不是 `weipaiban-creator` 的纵向三层视差或 3D 视差。

## 写法

前层盖在视口上，滑动时不动。后层去掉 `data-elevated`，垫在滑动内容后面。不需要固定层时，删掉整个 `overlay`。

```html
<section data-name="04 横向滑动">
  <section data-type="overlay" data-elevated="true">
    <svg width="390" height="600" data-name="固定层">
      <rect x="24" y="24" width="120" height="32" rx="16" fill="#4A5D52"></rect>
      <text x="24" y="28" width="120" height="24" fill="#FAF8F2" font-size="13" data-align="center">左右滑动</text>
    </svg>
  </section>
  <section data-type="scroller" data-scroll-direction="horizontal" height="600">
    <svg data-max-width="none" width="1140" height="600" data-name="横向画布">
      <image href="{left}" x="0" y="0" width="560" height="600" data-fit="cover"></image>
      <image href="{right}" x="580" y="0" width="560" height="600" data-fit="cover"></image>
      <text x="24" y="536" width="320" height="28" fill="#FAF8F2" font-size="16">从湖面滑到街巷</text>
    </svg>
  </section>
</section>
<section data-type="richText" data-name="04 图注">
  <section style="padding:8px 10px 16px;text-align:center;">
    <p style="margin:0;font-size:12px;color:#888888;line-height:1.5;">图：左右滑动，看完这一段路</p>
  </section>
</section>
```

`<image>` 必须成对闭合。色与圆角只来自当前主题。图注写在下一块 richtext。

外壳必须包住叠加层和滑动层。叠加层若直接挂在作品根上，前层会盖住后面的节拍。有叠加层时，它必须写在滑动层前面。

## 两层怎么选

| 层 | 写法 | 适合 |
| --- | --- | --- |
| 前层 | `data-elevated="true"` | 标题、相框、印章、导视。滑动时留在视口上 |
| 后层 | 不写 `data-elevated` | 底纹、远景。滑动内容从上面掠过 |
| 不要固定层 | 不写 `overlay` | 整段都在画布里滑 |

叠加层里恰好一块 `<svg width="390">`，高度等于滑动视口。不要在这层写 `data-max-width`。叠加层的手势会穿透，滑动落在下面的滑动层上。

## 宽画布

滑动层恰好一个直接子节点：`<svg data-max-width="none">`。内部沿用普通画布方言：`image`、`text`、`rect`、`foreignObject`、`g`、动画组。坐标可以超过 390。

画布会按子元素包围盒回写宽高。内容从 `x=0`、`y=0` 起排，`svg` 的 `width` 写成内容右缘（最大的 `x + width`）。要在末尾留白，放一块透明 `rect` 把右缘撑出去。

| 属性 | 规则 |
| --- | --- |
| 外壳 `data-name` | 图层名，标清插在哪一拍 |
| `overlay` | 0 或 1 块，有则在滑动层之前 |
| `data-elevated` | `true` 前层；不写为后层 |
| 固定层 `svg` | `width="390"`，`height` 等于视口 |
| `data-scroll-direction` | 必须 `horizontal` |
| `height`（滑动层） | 视口高。默认 **600**，允许 480–680 |
| `data-max-width` | 宽画布必须 `none`。其它位置写了会 400 |
| 宽画布 `width` | 内容右缘。必须 **> 390** 且 **≤ 1560**（约 1.6–4 屏） |
| 宽画布 `height` | 等于滑动视口，避免被裁切 |

`overlay` 和 `scroller` 只按这一页的外壳来写。辅助画布里面仍然不能写这两个标签。

## 配图

固定层和宽画布里的每张图，在 `asset-request.json` 里各一条，`role=scene`，`usedBy` 指向对应 `data-name`。宽画布上的横幅按画布占位像素从素材池挑比例接近的场景图。见 [assets.md](../assets.md)。

## 和别的块的分工

| | 用 |
| --- | --- |
| 左右滑着看一条自由画布 | **本组件** |
| 自动切页的同尺寸图集 | [slideshow.md](slideshow.md) |
| 一张图 + 图注 | richtext `<img>` |
| 章节主图要插画感 | [image-svg.md](image-svg.md) |
| 两面互切 | [click-switch.md](click-switch.md) |
| 图上多热点弹层 | [click-popup.md](click-popup.md) |

宽画布里的动画组按 [animation-group.md](animation-group.md) 写。

## 禁止

- 在外壳外单独写 `overlay` 或 `scroller`
- 宽画布宽度 ≤ 390 或 > 1560，或高度和视口不一致
- 滑动层里放第二块画布、richtext、轮播、切换或弹窗
- 固定层用宽画布，或宽画布漏写 `data-max-width="none"`
- 用多张 390 宽画布横排冒充这块
- 08 / 09 / AI 声明上加横向滑动
