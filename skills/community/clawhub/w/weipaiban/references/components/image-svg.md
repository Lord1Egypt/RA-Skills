# 图文 SVG

一块 **390 宽的图文画布**。仍是普通 `<svg>`（不要写 `data-type`），入库后是 `frame`。内部由主体图、几何留白、点题短文案和少量透明装饰组成。

普通场景画布见 [svg.md](svg.md)，3 张以上连看见 [slideshow.md](slideshow.md)。色、圆角和层级服从当前 format 的设计方案。

只在图像与文字确实需要共同构图时使用；同一场景不要既放普通图片又放重复的图文 SVG。不要用于 AI 声明。

## 写法

```html
<svg width="390" height="380" data-overflow="visible" data-name="04-1 图文">
  <rect
    x="248"
    y="20"
    width="128"
    height="128"
    rx="64"
    fill="#ECFDF5"
    opacity="0.85"
  />
  <rect
    x="28"
    y="52"
    width="300"
    height="220"
    rx="16"
    fill="#D1FAE5"
    opacity="0.45"
  />
  <image
    href="{main}"
    x="48"
    y="36"
    width="294"
    height="220"
    data-fit="cover"
    data-corner-radius="16"
  ></image>
  <rect x="48" y="292" width="28" height="1" fill="#059669" />
  <text
    x="84"
    y="280"
    width="200"
    height="24"
    fill="#059669"
    font-size="16"
    font-family="serif"
    letter-spacing="4"
  >
    先称一次
  </text>
  <image
    href="{sticker-a}"
    x="16"
    y="24"
    width="56"
    height="56"
    data-fit="contain"
  >
    <animate
      data-preset="漂浮"
      data-trigger="load"
      data-duration="2.6"
      data-repeat="indefinite"
    />
  </image>
  <image
    href="{sticker-b}"
    x="318"
    y="220"
    width="64"
    height="64"
    data-fit="contain"
  >
    <animate
      data-preset="钟摆"
      data-trigger="load"
      data-delay="0.4"
      data-duration="2.8"
      data-repeat="indefinite"
    />
  </image>
</svg>
<section data-type="richText" data-name="04-1 图注">
  <section style="padding:8px 10px 16px;text-align:center;">
    <p style="margin:0;font-size:12px;color:#888888;line-height:1.5;">
      图：放学后的称重，只做这一件事
    </p>
  </section>
</section>
```

`<image>` 必须成对闭合。`href` 原样用配图清单（含 `x-oss-process`）。图注写在 **下一块 richtext**，不要把长句写进画布。

## 属性

| 属性              | 规则                                                                                      |
| ----------------- | ----------------------------------------------------------------------------------------- |
| `width`           | **必须 390**                                                                              |
| `height`          | 声明多少就是多少。建议 **300–460**。不要做成 520+ 整屏场景，也不要矮成辅助点缀（120–280） |
| `data-overflow`   | 写 **`visible`**，贴纸可探出边缘                                                          |
| `data-name`       | 图层名，标清插在哪一拍，建议 `{节拍} 图文`                                                |
| `data-background` | 默认不写，透出作品纸色                                                                    |

层叠：HTML **后写的叠在上面**。几何底先写，主图，再字，贴纸最后。

每块子元素（含 rect / image / text / g）建议 **≤ 18**。

## 三种构图（每块只选一种）

### 单图留白

主图约 294–342 宽，左右边距 ≥ 24，上下留白 ≥ 28。贴纸落**对角两角**（不要四角塞满）。短文案在图下或图侧留白里，不压死主图焦点。上表即此式。

### 双图错落

两张主图不同 `x/y`、尺寸略差，允许轻微叠压。叠压处用主题浅底 `rect` 隔开，不要让两张照片糊成一块。第二张可更大圆角或改圆形。**只允许两张主图**，不要三图拼贴。

```html
<svg width="390" height="420" data-overflow="visible" data-name="04-2 图文">
  <rect
    x="24"
    y="72"
    width="168"
    height="210"
    rx="80"
    fill="#ECFDF5"
    opacity="0.5"
  />
  <image
    href="{main-a}"
    x="36"
    y="36"
    width="200"
    height="260"
    data-fit="cover"
    data-corner-radius="16"
  ></image>
  <image
    href="{main-b}"
    x="176"
    y="96"
    width="168"
    height="210"
    data-fit="cover"
    data-corner-radius="105"
  ></image>
  <text
    x="36"
    y="328"
    width="220"
    height="28"
    fill="#059669"
    font-size="16"
    font-family="serif"
    letter-spacing="3"
  >
    只留明天
  </text>
  <image
    href="{sticker}"
    x="318"
    y="28"
    width="56"
    height="56"
    data-fit="contain"
  >
    <animate
      data-preset="呼吸"
      data-trigger="load"
      data-duration="2.4"
      data-repeat="indefinite"
    />
  </image>
</svg>
```

圆形：`data-corner-radius` ≥ 短边一半（上例 168×210 → ≥ 84，写成 105 即可）。

### 画中画

一张主图 + 一张小图嵌在角落或边缘。小图方形（圆角 = 主题卡片圆角）或正圆（边长 72–120，`data-corner-radius` ≥ 半边长）。小图必须完整落在画布内。贴纸仍用透明小物件，**不要用第三张照片冒充贴纸**。

```html
<svg width="390" height="400" data-overflow="visible" data-name="04-3 图文">
  <rect
    x="40"
    y="28"
    width="310"
    height="310"
    rx="16"
    fill="#ECFDF5"
    opacity="0.35"
  />
  <image
    href="{main}"
    x="48"
    y="36"
    width="294"
    height="294"
    data-fit="cover"
    data-corner-radius="16"
  ></image>
  <image
    href="{pip}"
    x="246"
    y="246"
    width="88"
    height="88"
    data-fit="cover"
    data-corner-radius="44"
  ></image>
  <foreignObject x="20" y="48" width="28" height="140">
    <section
      style="font-size:14px;line-height:1.7;color:#059669;letter-spacing:2px;writing-mode:vertical-rl;text-orientation:upright;"
    >
      先看见
    </section>
  </foreignObject>
  <image
    href="{sticker}"
    x="12"
    y="300"
    width="56"
    height="56"
    data-fit="contain"
  >
    <animate
      data-preset="漂浮"
      data-trigger="load"
      data-duration="2.8"
      data-repeat="indefinite"
    />
  </image>
</svg>
```

## 文字

- 点题 **2–8 字**。不要段落，不要图注长句。
- 横排：`<text font-family="serif">` + `letter-spacing`。要加粗才用 `foreignObject`。
- 竖排：`foreignObject` 内 `writing-mode:vertical-rl;text-orientation:upright;`，窄高盒子（宽 24–36）。只在当前视觉方向确实需要时使用。
- 细线：1×24～40 的 `rect`，填主题 `line` 或 `primary`。横排在字侧或字下，竖排在字旁。
- **不要**写 `KaiTi` / `cursive` / 其它自定义 `font-family`（微信不加载）。手写感用 serif + 字距。国风且用户明确要书法时，从素材池的透明装饰里选一张字贴；没有则该槽位占位。

## 贴纸与动效

贴纸 48–72px，1:1，透明，`data-fit="contain"`。每块 **1–3** 张，优先对角。物体完整、无文字。

循环氛围直接挂在贴纸 `<image>` 上，**不必**包 `animationGroup`；仍计入 format 的整体动效预算：

| preset | 用法           |
| ------ | -------------- |
| `漂浮` | 位移，默认首选 |
| `呼吸` | 轻微缩放       |
| `钟摆` | 等幅摆动       |

`data-trigger="load"`，`data-repeat="indefinite"`，duration **2.2–3.2**，多张贴纸错开 `data-delay`。不要写 `opacity="0"`（循环从可见开始）。

- `摇摆` 只播一次，不要 `indefinite`。
- 主图默认静止；最多极轻 `呼吸`，不要整张主图漂浮。
- 不要心跳 / 闪烁 / 弹跳（那是 CTA）。不要 width/height 类 preset。
- 只有额外做点击 appear / 编排入场时才用动画组，见 [animation-group.md](animation-group.md)。

## 配图

每张主图、每张贴纸在 `asset-request.json` 里一条，`usedBy` 指向该 SVG 的 `data-name`。主图 `width/height` 使用真实画布占位像素，`role=scene`。贴纸 `role=transparent`，`cropMode=contain`，`width/height` 通常 48–72。见 [assets.md](../assets.md)。

## 和别的块的分工

|                                  | 用                                              |
| -------------------------------- | ----------------------------------------------- |
| 普通一图一意、无装饰             | richtext `<img>`，见 [richtext.md](richtext.md) |
| 章节主图要插画感 / 贴纸 / 点题字 | **本组件**                                      |
| 3 张以上同框连看                 | [slideshow.md](slideshow.md)                    |
| 矮入场、图上压一句、轻点揭示     | [svg.md](svg.md) + 动画组                       |
| 两面互切                         | [click-switch.md](click-switch.md)              |
| 图上多热点弹层                   | [click-popup.md](click-popup.md)                |

不要写成 `data-type="clickPopup"`。不要把贴纸主图化。

## 禁止

- 同一场景既放 `<img>` 又放内容重复的图文 SVG
- 四角对称贴满、三张以上主图、foreignObject 里放图或装饰边框
- 自定义 `font-family` 名、没有体系的额外颜色、纯黑 `#000` 字
- HTML 注释
