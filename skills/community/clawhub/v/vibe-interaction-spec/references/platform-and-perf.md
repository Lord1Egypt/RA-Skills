# 平台与性能

动效「好看但卡」等于负分。这一层是验收线，不是优化项。

## 1. 属性成本三分法

浏览器的渲染流水线：Style → Layout → Paint → Composite。属性落在哪一段，决定它能不能 60fps。

| 成本 | 属性 | 后果 |
| --- | --- | --- |
| **合成（可用）** | `transform`、`opacity` | 只走 GPU 合成，最便宜的动画路径 |
| **绘制（慎用）** | `box-shadow`、`border-radius`、`background`、`color`、`outline`、`filter` | 每帧重绘，区域大就掉帧；小元素可接受 |
| **布局（禁止）** | `width`、`height`、`top`、`left`、`right`、`bottom`、`margin`、`padding`、`border-width`、`font-size`、`line-height`、`flex-basis` | 触发重排，连带整页重算，必卡 |

推论：

- 位移别写 `top`，写 `translate`
- 展开别写 `height`，写 `grid-template-rows: 0fr → 1fr`、`clip-path` 或 `transform: scaleY`
- 阴影别做 hover 过渡（重绘大），改用**叠加一层预先存在的伪元素改透明度**
- `filter: blur()` 与 `backdrop-filter` 极贵，只用在固定尺寸小区域

## 2. API 选型

| 需求 | 用什么 | 为什么 |
| --- | --- | --- |
| 状态间简单切换（hover / focus / active） | CSS `transition` | 零 JS，自动可打断 |
| 声明式关键帧、循环 | CSS `animation` + `@keyframes` | 同上 |
| 需要读当前值、动态目标、播放控制 | Web Animations API `el.animate()` | 有 `pause/reverse/finish`，可读 `currentTime` |
| 跨页/跨视图的元素连续 | View Transitions API | MPA 一行 `@view-transition { navigation: auto }`；SPA 用 `document.startViewTransition()` |
| 滚动绑定 | CSS `animation-timeline` | 合成线程执行，比 JS 顺 |
| 复杂时间线、滚动编排 | GSAP + ScrollTrigger | 原生做不了序列、反向、scrub |
| React 内布局动画与手势 | Framer Motion / Motion One | 自带 layout、drag、spring |

顺序原则：**CSS 能做的不要上 JS，原生 API 能做的不要上库**。库里最容易失控的是 ScrollTrigger 与 layout 补间。

## 3. 首帧入场：`@starting-style`

元素第一次挂载（`<dialog>`、popover、Toast）时，普通 transition 不会触发，因为初始值没有「前一个状态」。用 `@starting-style` 补：

```css
.toast { opacity: 1; transform: translateY(0); transition: opacity .25s, transform .25s; }
@starting-style { .toast { opacity: 0; transform: translateY(12px); } }
```

不再需要 `requestAnimationFrame` 里加 class 那种脏办法。

## 4. FLIP（布局动画的正解）

元素位置变了但不许改布局时：

1. **First**：动画前记录 `getBoundingClientRect()`
2. **Last**：改完 DOM 后立刻再测一次
3. **Invert**：用 `transform: translate(dx, dy) scale(...)` 把元素「拉回」原位
4. **Play**：下一帧移除 transform，让它 transition 回 0

要点：Invert 那一帧必须 `transition: none`，否则会看到闪一下。

## 5. 性能预算

| 指标 | 目标 | 说明 |
| --- | --- | --- |
| 单帧预算 | 16.7ms（60fps）/ 8.3ms（120fps） | 超了就是掉帧，用户能看见 |
| INP | < 200ms（好），> 500ms 差 | 交互到下次绘制的延迟，动效阻塞交互会直接恶化它 |
| CLS | < 0.1 | 动画不能引起布局位移 |
| 长任务 | 单次 < 50ms | 用 Performance 面板看 Long Tasks / LoAF |

## 6. 卡顿根因（按出现频率）

1. 动了布局属性（height / top / margin）
2. `transition: all`——把不相干属性一起过渡，包括布局属性
3. 大面积的 `box-shadow` 或 `backdrop-filter` 在动画
4. 同时动画的元素过多（50+ 个卡片各自 transform 也会挂）
5. 在 `scroll` 事件里同步读 `offsetTop`（布局抖动）
6. `will-change` 到处加，图层爆炸，显存吃满

`will-change` 只给「即将发生」的元素加，且动画结束后移除。**默认不加**，浏览器自己会提升图层。

## 7. 无障碍（硬性）

| 项 | 要求 |
| --- | --- |
| `prefers-reduced-motion: reduce` | 关闭位移/缩放/视差，保留透明度或颜色变化。**不要直接 `animation: none`**，否则反馈信息一起消失 |
| 触发阈值 | 位移 > 40px、视差、缩放 > 1.1 的动画必须响应此偏好 |
| 闪烁 | 每秒不超过 3 次（WCAG 2.3.1，癫痫风险） |
| 自动播放 | 超过 5 秒的循环动效需可暂停（WCAG 2.2.2） |
| 可关闭 | 由交互触发的非必要动效应可关（WCAG 2.3.3，AAA） |
| 焦点 | `:focus-visible` 必须有可见焦点环，且不能只靠颜色 |
| 播报 | Toast / 动态结果用 `aria-live="polite"`；错误用 `role="alert"` |
| 信息冗余 | 动效不能是唯一的信息载体（不能只靠「抖一下」表示错误） |

推荐写法（比 `reduce` 覆盖更严格，默认不动）：

```css
@media (prefers-reduced-motion: no-preference) {
  .card { transition: transform .2s var(--ease-standard); }
}
```

## 8. 移动端

| 问题 | 解法 |
| --- | --- |
| 手机没有 hover，但 CSS 里 `.btn:hover` 会在点按后「粘住」 | 全部包进 `@media (hover: hover) and (pointer: fine)` |
| 触屏需要替代反馈 | `:active` 的 scale 0.98 或底色变化，不要依赖 hover |
| 拖拽与页面滚动冲突 | 容器上加 `touch-action: pan-y` / `none`，配合 Pointer Events |
| 滚动监听掉帧 | `addEventListener('scroll', fn, { passive: true })` |
| 100vh 在移动端地址栏遮挡 | 用 `100dvh` |
| 刘海与手势条 | `env(safe-area-inset-*)` |

## 9. 交付前真机清单

- [ ] 连续快速触发同一交互 10 次，动画不排队、不残留中间态
- [ ] 动画进行中点击其他元素，能立即响应（不被打断锁死）
- [ ] 低端安卓（或 4x CPU 降速）下滚动不抖
- [ ] 键盘 Tab 走一遍，焦点环始终可见
- [ ] 系统开启「减少动态效果」后，信息仍然完整
- [ ] 触屏点按后，悬停样式没有粘住
