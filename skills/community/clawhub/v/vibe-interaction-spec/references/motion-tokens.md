# 动效 Token

可直接抄。核心规则只有一条：**同一个动作在全站用同一个 token**。这是「看起来专业」最便宜来源。

## 1. 时长（Duration）

与 Material 3 时长阶梯对齐，右侧是我们给的语义分配。

| Token | 值 | 语义用途 |
| --- | --- | --- |
| `--dur-50` | 50ms | 状态色微变、涟漪起始 |
| `--dur-100` | 100ms | 按下回弹、图标切换 |
| `--dur-150` | 150ms | 复选框、开关、hover 底色 |
| `--dur-200` | 200ms | 按钮反馈、Tooltip、悬停上浮 |
| `--dur-250` | 250ms | 下拉菜单、Toast 进出 |
| `--dur-300` | 300ms | 卡片展开、侧栏折叠、Tab 内容切换 |
| `--dur-400` | 400ms | 弹窗、抽屉、页面转场（默认档） |
| `--dur-500` | 500ms | 大容器变形、整屏切换 |
| `--dur-700` | 700ms | 首屏编排总时长上限 |
| `--dur-1000` | 1000ms | 仅品牌叙事场景，需明确理由 |

超 800ms 的过渡必须能说出理由，否则砍。

## 2. 缓动（Easing）

```css
--ease-linear: linear;
--ease-standard:            cubic-bezier(0.2, 0, 0, 1);
--ease-standard-decelerate: cubic-bezier(0, 0, 0, 1);
--ease-standard-accelerate: cubic-bezier(0.3, 0, 1, 1);
--ease-emphasized:          cubic-bezier(0.2, 0, 0, 1);
--ease-emphasized-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1);
--ease-emphasized-accelerate: cubic-bezier(0.3, 0, 0.8, 0.15);
--ease-back-out:            cubic-bezier(0.34, 1.56, 0.64, 1); /* 仅活泼调性 */
```

选型顺序：入场 → `decelerate`；退场 → `accelerate`；屏内往返 → `standard`；大容器/页面级 → `emphasized-*`。

## 3. 弹簧（Spring）

| 预设 | stiffness | damping | mass | ζ | 体感 | 用在 |
| --- | --- | --- | --- | --- | --- | --- |
| gentle | 120 | 20 | 1 | 0.91 | 稳、几乎不弹 | 抽屉、弹窗、内容位移 |
| snappy | 300 | 30 | 1 | 0.87 | 快、收得干净 | 按钮、切页签、开关 |
| bouncy | 400 | 18 | 1 | 0.45 | 明显回弹 | 点赞、磁贴吸附、拖拽落位 |
| molasses | 60 | 18 | 1 | 1.16 | 慢而重 | 大画布、地图平移 |

ζ = damping / (2 × √(stiffness × mass))。**ζ < 1 才有过冲；过冲幅度别超过位移 15%。**

Framer Motion 写法：`transition={{ type:'spring', stiffness:300, damping:30, mass:1 }}`
CSS 近似（`linear()` 采样，Chrome 113+）：

```css
--ease-spring-snappy: linear(0, 0.009, 0.035 2.1%, 0.141 4.4%, 0.723 12.9%, 0.938 16.7%, 1.017, 1.077, 1.121, 1.149 24.3%, 1.159, 1.163, 1.161, 1.154 29.9%, 1.129 32.8%, 1.051 39.6%, 1.017 43.1%, 0.991, 0.977 51%, 0.974 53.8%, 0.975 57.1%, 0.997 69.8%, 1.003 76.9%, 1);
```

## 4. 幅度（Distance & Scale）

| Token | 值 | 用在 |
| --- | --- | --- |
| `--lift-1` | 2px | 极克制的悬停 |
| `--lift-2` | 4px | 卡片悬停（默认） |
| `--lift-3` | 8px | 强调卡片、浮起元素 |
| `--lift-4` | 16px | 入场位移（从下方滑入） |
| `--scale-press` | 0.98 | 按下 |
| `--scale-hover` | 1.02 | 悬停放大 |
| `--scale-enter` | 0.96 → 1 | 弹窗/卡片入场 |

## 5. 阴影（Elevation）

```css
--shadow-0: none;
--shadow-1: 0 1px 2px rgba(20,24,20,.06);
--shadow-2: 0 2px 8px rgba(20,24,20,.07);
--shadow-3: 0 8px 20px rgba(20,24,20,.09);
--shadow-4: 0 16px 40px rgba(20,24,20,.12);
```

阴影**颜色不要用纯黑**，掺一点主色会让整个页面「暖」起来。深色模式改用 elevation overlay（叠一层 4%/8%/12% 的白色），不要继续加黑阴影。

## 6. 三旋钮 → Token 映射

| 旋钮档位 | 交互反馈 | 组件过渡 | 页面转场 |
| --- | --- | --- | --- |
| 克制 | `dur-100` + `standard` | `dur-200` + `standard` | `dur-300` + `standard-decelerate` |
| 标准 | `dur-150~200` + `standard` | `dur-250~300` + `emphasized-decelerate` | `dur-400` + `emphasized-decelerate` |
| 强烈 | `dur-200` + `back-out` | `dur-300~400` + `bouncy` | `dur-500` + `emphasized` |

## 7. 组件配比表

直接照抄，这是最省事的一致性来源。

| 组件 / 场景 | 时长 | 缓动 | 幅度 / 属性 |
| --- | --- | --- | --- |
| 按钮按下 | 100ms | standard | scale 0.97 |
| 按钮悬停 | 150ms | standard | 底色加深 6%，不上位移 |
| 卡片悬停上浮 | 200ms | standard | translateY -4px + shadow-2 |
| 链接下划线生长 | 200ms | standard | scaleX 0→1，`transform-origin: left` |
| 输入框聚焦 | 150ms | standard | 边框换色 + 2px 外环，不做发光弥散 |
| Toggle / Checkbox | 150ms | emphasized-decelerate | 位移 20px + 底色渐变 |
| Tab 指示条滑动 | 250ms | emphasized-decelerate | translateX + scaleX |
| 下拉菜单 | 200ms 进 / 120ms 出 | decelerate / accelerate | translateY -4px→0 + 透明度 |
| Tooltip | 150ms，延迟 120ms | standard | 透明度 + 2px 位移 |
| Toast | 250ms 进 / 180ms 出 | decelerate | translateY 12px + 透明度 |
| 弹窗 Modal | 300ms 进 / 200ms 出 | emphasized-decelerate | scale 0.96→1 + 遮罩 0→.5 |
| 抽屉 Drawer | 350ms 进 / 250ms 出 | emphasized-decelerate | translateX 100%→0 |
| 手风琴展开 | 300ms | emphasized-decelerate | `grid-template-rows` 0fr→1fr |
| 列表逐条入场 | 单条 300ms，间隔 60ms | decelerate | translateY 16px + 透明度，总时长封顶 600ms |
| 滚动显现 | 400ms | decelerate | translateY 20px + 透明度，只播一次 |
| 页面转场 | 400ms | emphasized-decelerate | 共享轴 X/Y，或 fade through |
| 骨架屏呼吸 | 1200–1600ms | ease-in-out | 透明度 .6↔1，无限循环 |
