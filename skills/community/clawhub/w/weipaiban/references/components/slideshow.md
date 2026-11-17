# 轮播（slideshow）

format 容器中的 **图集**，映射为编辑器 `type: slideshow`。它自动播放，不是点击切换。

建议 **3–6** 张且同尺寸。不要用于 AI 声明，不要用轮播代替单图；只有 2 张时优先用对照或点击切换。

详细属性只看本页。

## 写法

```html
<section
  data-type="slideshow"
  data-name="04 图集"
  data-effect="fade"
  height="520"
>
  <img src="{manifest.src}" data-title="月下湖面" />
  <img src="{manifest.src}" data-title="灯笼街巷" />
  <img src="{manifest.src}" data-title="团圆饭桌" />
</section>
<section data-type="richText" data-name="04 图注">
  <section style="padding:8px 10px 16px;text-align:center;">
    <p style="margin:0;font-size:12px;color:#888888;line-height:1.5;">
      图：同一轮月亮，三种看见的方式
    </p>
  </section>
</section>
```

`src` 原样用配图清单（含 `x-oss-process`）。子节点只用 `<img>`，不要写 SVG 的 `<image />`（HTML 会吞掉后面的标签）。通常图注写在下一块 richText，轮播本身不叠字；`layered-scroll` 与 `parallax-scroll` 禁止独立 richText，图注必须改用相邻 SVG 的 `<text>` 或 `<foreignObject>`。

## 属性

| 属性                 | 规则                                                                            |
| -------------------- | ------------------------------------------------------------------------------- |
| `data-type`          | 必须 `slideshow`                                                                |
| `height`             | 视口高，必填。竖图 `3:4` → **520**（默认）；方图 `1:1` → 390；横图 `16:9` → 220 |
| `width`              | 不写。写了必须 `390`                                                            |
| `data-name`          | 图层名，标清插在哪一拍                                                          |
| `data-effect`        | 只准下表 5 个。缺省 `fade`                                                      |
| `data-duration`      | 切页时长（秒），缺省 `2`                                                        |
| `data-delay`         | 开播延迟（秒），缺省 `1`                                                        |
| `data-end`           | `indefinite`（默认）或 `click`                                                  |
| `data-reverse`       | `true` 时反向。默认不写                                                         |
| `data-fit`           | 根上缺省 `cover`；单张可覆盖                                                    |
| `data-corner-radius` | 满幅默认 0；需要圆角时服从当前设计方案                                          |
| `data-title`（每张） | 编辑器图层名，读者看不见                                                        |

转换器还接受 `<image href>` 和另外 14 种效果名；本技能不要用。

## 效果（只这 5 个）

| `data-effect` | 适用                       |
| ------------- | -------------------------- |
| `fade`        | **默认**。图集、节气、品牌 |
| `basic`       | 产品多角度                 |
| `kenBurns`    | 摄影 / 散文，慢看          |
| `vertical`    | 竖构图连看                 |
| `cover`       | 步骤、前后轻微差异         |

不要写百叶窗、翻书、扇形、钟摆、九宫格等。

## 配图

每张 slide 在 `asset-request.json` 里一条，`usedBy` 指向这块 `data-name`。全部同一 `cropMode`（默认 `cover`），`width/height` 用视口像素（如 390×520）。从素材池按相近比例选取，不够就复用。

## 和别的块的分工

|                     | 用                                                                        |
| ------------------- | ------------------------------------------------------------------------- |
| 一张图 + 图注       | 普通 format 用 richText；`layered-scroll` 与 `parallax-scroll` 用相邻 SVG |
| 章节主图要插画感    | [image-svg.md](image-svg.md)                                              |
| 3 张以上同框连看    | **本组件**                                                                |
| 入场动效 / 图上压字 | 矮 `<svg>` + 动画组                                                       |
| 两面互切            | [click-switch.md](click-switch.md)                                        |
| 图上多热点弹层      | [click-popup.md](click-popup.md)                                          |

轮播计 1 个元素，**不占**「至多 2 块带动画组的画布」配额。不要写进 `<svg>` 里。

## 禁止

- 一篇超过 1 块，或 3 张以下 / 6 张以上
- 各 slide 比例不一致
- 子节点放 `svg` / `section` / 文字
- 在轮播上叠 `foreignObject` 或幻想 `title` 会显示
- 在 AI 声明中使用轮播
