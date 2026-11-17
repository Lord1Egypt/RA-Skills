# 动画组

画布里的编排容器。**只能写在 `<svg>` 内**，不能当 section 子节点，不能嵌套。preset 名单见 [effect-presets.md](effect-presets.md)。

默认用于 autoplay 入场、循环氛围或一次点击揭示。数量服从当前 format 的元素预算；点前可见的 hint 写在组外。

图文 SVG 的贴纸循环（`漂浮` / `呼吸` / `钟摆`）直接挂在 `<image>` 上，**不必**进组，也 **不占**「至多 2 块带动画组的画布」配额。见 [image-svg.md](image-svg.md)。

```html
<svg width="390" height="160" data-name="01 入场点缀">
  <g data-type="animationGroup" data-mode="autoplay" data-name="色条入场">
    <rect
      x="175"
      y="24"
      width="40"
      height="1"
      fill="#4A5D52"
      opacity="0"
      data-editor-visible="true"
    >
      <animate data-preset="渐现" data-trigger="load" data-duration="0.5" />
    </rect>
    <foreignObject x="40" y="48" width="310" height="40">
      <section
        style="font-size:18px;font-weight:700;color:#4A5D52;text-align:center;letter-spacing:1px;"
      >
        月下团圆
      </section>
      <animate
        data-preset="上浮渐现"
        data-trigger="load"
        data-delay="0.4"
        data-duration="0.55"
      />
    </foreignObject>
  </g>
</svg>
```

## 属性

| 属性           | 值                                      | 默认        |
| -------------- | --------------------------------------- | ----------- |
| `data-mode`    | `appear` / `disappear` / `autoplay`     | `appear`    |
| `data-trigger` | `pointerUp` / `pointerDown` / `load`    | `pointerUp` |
| `data-order`   | `down` 正向从上到下 / `up` 反向从下到上 | `down`      |

`autoplay` 时触发强制为 `load`，**不要写 `data-order`**（没有执行顺序）。

**组内 `<animate data-trigger>` 必须与组相同**（点击组用 `pointerUp`，自动组用 `load`）。写错则时间轴是空的。出现/消失组里仍可另挂 `data-trigger="load"` 的自动层。

## opacity

- **`load` 且从透明入场**（渐现、上浮渐现、左滑渐现、弹入、盖章）：元素写 `opacity="0"` 和 `data-editor-visible="true"`。
- **组触发的点击入场/出场**：不要写 opacity 0（wrapper 负责）。
- **循环氛围**（漂浮、呼吸）：不要写 0，否则一直看不见。

## 执行顺序

`autoplay` 先后只看 `data-delay`：按画面从上到下写 HTML，delay 递增。

`appear` / `disappear` 默认 `data-order="down"` 从上到下（后写的更靠上、更先播）。需要从下到上、底先字后、或竖排从上往下依次出现，写 `data-order="up"`。不要倒着写 HTML，也不要倒着排 delay 来换方向。

delay 跟**播放顺序**对齐：先播的 `data-delay="0"`，下一拍 ≈ 上一拍 delay+duration（可重叠 0.05–0.1s）。不要所有层 delay=0、duration 全相同。`down` 时后写 delay 更小；`up` 时先写 delay 更小。

```html
<svg width="390" height="200" data-name="04 金句点睛">
  <rect x="40" y="8" width="88" height="28" rx="2" fill="#4A5D52" />
  <text x="48" y="12" width="72" height="20" fill="#FAF8F2" font-size="12">
    点开看 ›
  </text>
  <g
    data-type="animationGroup"
    data-mode="appear"
    data-trigger="pointerUp"
    data-order="up"
    data-name="金句出现"
  >
    <rect x="40" y="52" width="310" height="120" rx="2" fill="#F4F1E8">
      <animate
        data-preset="上浮渐现"
        data-trigger="pointerUp"
        data-delay="0"
        data-duration="0.5"
      />
    </rect>
    <foreignObject x="56" y="76" width="278" height="80">
      <section
        style="font-size:16px;font-weight:700;color:#4A5D52;text-align:center;line-height:1.75;"
      >
        月亮不会等人。
      </section>
      <animate
        data-preset="渐现"
        data-trigger="pointerUp"
        data-delay="0.4"
        data-duration="0.4"
      />
    </foreignObject>
  </g>
</svg>
```

一个节拍一个子节点：图+标签包进普通 `<g>`，animate 挂在这个 `g` 上。

## 点击组

hint 胶囊（圆角 `rect` + 一句「点开看 ›」）写在动画组**外面**，点前必须看见。无 hint 就补一句。热区是整组范围。

## 禁止

- 再套一层 `animationGroup`
- 组内用 width/height 类 preset（见 effect-presets）
- 在 AI 声明上加组
