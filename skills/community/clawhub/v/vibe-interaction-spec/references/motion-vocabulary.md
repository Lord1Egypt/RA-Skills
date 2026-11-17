# 动效专业词汇

用于**解释「为什么这么动」**和做多元素编排。effect-catalog 回答「这个效果叫什么」，这里回答「它属于哪一类、该多快、该怎么接」。

## 1. 动效的四种职能

先确定这个动画在干什么。职能不同，时长预算和缓动完全不同。

| 职能 | 英文 | 在解决什么 | 时长预算 | 缓动倾向 |
| --- | --- | --- | --- | --- |
| 反馈 | Feedback | 确认「收到了」 | 100–200ms | ease-out，快进快出 |
| 状态转移 | Transition | 说明「从 A 变成了 B」 | 200–300ms | ease-in-out 或 standard |
| 空间连续 | Spatial continuity | 说明「我从哪来、到哪去」 | 300–500ms | emphasized decelerate |
| 注意力引导 | Attention | 说「先看这里」 | 300–600ms，且只播一次 | ease-out + 延迟编排 |

**职能错配是廉价的第二大来源**：给一次按钮点击配 600ms 的叙事级动画，用户会觉得卡。

## 2. 迪士尼原则的 UI 子集

12 条里只有 6 条在界面里真正成立，其余是角色动画语汇。

| 原则 | 英文 | 在 UI 里长什么样 |
| --- | --- | --- |
| 缓入缓出 | Slow In / Slow Out | 一切非匀速运动的默认，即 easing |
| 预期 | Anticipation | 下拉前的轻微下压、抽屉开启前的位移预兆 |
| 跟随 | Follow Through | 主体停下后，附属元素（阴影、图标）略滞后收尾 |
| 交叠 | Overlapping Action | 元素不是等前一个结束才开始，而是交叠 60–80% |
| 次要动作 | Secondary Action | 主位移之外，阴影/描边/颜色同步微变 |
| 夸张 | Exaggeration | 按调性放大 1.2–1.5 倍，超过就变廉价 |

## 3. 时序与编排（Timing & Choreography）

| 术语 | 英文 | 取值 / 规则 |
| --- | --- | --- |
| 时长阶梯 | duration scale | 50 / 100 / 150 / 200 / 250 / 300 / 400 / 500 / 700ms，只用阶梯值 |
| 距离相关时长 | distance-scaled duration | 8px 用 200ms，300px 用 400–500ms；**不是线性比例** |
| 逐个延迟 | stagger | 每项 30–80ms；超过 5 项必须封顶总时长（上限 300ms） |
| 交叠 | overlap | 下一段在前一段进行到 60–80% 时开始 |
| 停留 | hold | 关键帧之间留 1–2 帧静止，避免「一直在动」的噪感 |
| 预延迟 | delay | 悬停提示 100–150ms（防误触抖动）；入场 0–100ms |
| 退出更快 | exit faster than enter | 退场时长 ≈ 入场的 60–70%，否则拖沓 |
| 单向原则 | single direction | 同一屏内元素不要有的从左、有的从右进入 |
| 编排顺序 | choreography | 按阅读动线依次，不按 DOM 顺序 |

**总预算**：单次交互反馈 ≤ 300ms；单次组件过渡 ≤ 400ms；整页转场 ≤ 600ms；超 800ms 必须有明确理由（叙事、品牌）。

## 4. 缓动（Easing）

`cubic-bezier(x1, y1, x2, y2)` 两个控制点。**y 轴超出 0–1 就是过冲**（back 类缓动），这是「弹」的来源之一。

| 曲线 | 值 | 语义 | 用在哪 |
| --- | --- | --- | --- |
| linear | `linear` | 机械、匀速 | 进度条、无限循环的旋转/跑马灯。**别用在 UI 过渡上** |
| ease-out | `(0, 0, 0.58, 1)` | 快起慢收，自然停下 | 入场、出现、位移。默认首选 |
| ease-in | `(0.42, 0, 1, 1)` | 慢起加速离开 | 退场、消失 |
| ease-in-out | `(0.42, 0, 0.58, 1)` | 两头慢中间快 | 屏内位移、来回切换 |
| standard | `(0.2, 0, 0, 1)` | 通用 | 大多数状态切换 |
| standard-decelerate | `(0, 0, 0, 1)` | 强减速 | 从屏外进入 |
| standard-accelerate | `(0.3, 0, 1, 1)` | 强加速 | 离开屏幕 |
| emphasized-decelerate | `(0.05, 0.7, 0.1, 1)` | 长尾、贵气 | 大容器展开、页面转场 |
| emphasized-accelerate | `(0.3, 0, 0.8, 0.15)` | 果断离开 | 关闭弹层 |
| back-out | `(0.34, 1.56, 0.64, 1)` | 轻微过冲 | 只在「活泼」调性下用 |

> 数值与 Material 3 motion token 对齐。注意：各家对 `emphasized` 的具体曲线表述不完全一致，跨平台对齐时以项目 token 为准，不要混用两套。

## 5. 弹簧物理（Spring）

时长由物理决定，而不是你写死。**手势、拖拽、可打断的操作应该用弹簧；非交互触发的入场用时长制。**

| 参数 | 英文 | 作用 |
| --- | --- | --- |
| 刚度 | stiffness | 越大越快、越硬 |
| 阻尼 | damping | 越大越不弹；小到一定程度开始来回晃 |
| 质量 | mass | 越大越迟钝、惯性越强 |
| 初速度 | initial velocity | 从手势接过来时的速度，决定「接得住」 |

判定公式（阻尼比）：

```
ζ = damping / (2 × √(stiffness × mass))
ζ < 1  欠阻尼 → 会过冲回弹（活泼）
ζ = 1  临界阻尼 → 最快且不过冲（专业、克制）
ζ > 1  过阻尼 → 慢且肉（几乎不用）
```

实践规则：

- 表单、列表、键盘操作等高频场景 → **临界阻尼**，不要回弹
- 拖拽松手、点赞、磁贴吸附 → ζ 取 0.5–0.7，允许一次轻微过冲
- 过冲幅度超过位移的 15%，就会显得廉价
- 可打断（interruptible）：动画进行中接受新输入，并从当前速度接管，而不是重头播放。这是「丝滑」的真正来源

## 6. 页面转场范式

Material 的四种范式，比「左滑右滑」这种土办法清晰得多。

| 范式 | 英文 | 用在 | 实现要点 |
| --- | --- | --- | --- |
| 容器变形 | Container transform | 卡片 → 详情页（有明确父子关系） | FLIP 或 `clip-path`，起止元素同名 |
| 共享轴 X | Shared axis X | 同层级前进/后退 | 旧内容左移淡出，新内容右移淡入 |
| 共享轴 Y | Shared axis Y | 层级上下（弹层、分组切换） | 垂直位移 + 淡入淡出 |
| 共享轴 Z | Shared axis Z | 进入下一层（放大进入） | scale 0.8→1 + 透明度 |
| 淡出淡入 | Fade through | 无空间关系的切换（Tab、底部导航） | 先淡出（90ms）再淡入，两段不重叠 |
| 同名元素 | Shared element | 跨页保持同一个对象连续 | View Transitions 的 `view-transition-name` |

**判断口诀**：有父子关系用容器变形；有前后顺序用共享轴；毫无关系用 fade through。

## 7. 滚动驱动动画（Scroll-driven）

2026 年已进入 Baseline（Chrome 115+ / Firefox 132+ / Safari 18+，覆盖约 84%），但**必须写 `@supports` 兜底**。

| 能力 | 声明 | 替代什么 |
| --- | --- | --- |
| 容器滚动进度 | `animation-timeline: scroll(root block)` | 监听 scroll 算百分比 |
| 元素进入视口进度 | `animation-timeline: view()` | 滚动显现 |
| 区间控制 | `animation-range: entry 0% cover 40%` | 手动算阈值 |

```css
/* 渐进增强：不支持时元素保持最终态，内容始终可读 */
@supports (animation-timeline: view()) {
  .reveal { animation: fade-up linear both; animation-timeline: view(); animation-range: entry 0% cover 35%; }
}
```

取舍：

- 纯视觉的滚动效果 → 用 CSS 滚动驱动，跑在合成线程，比 JS 顺
- 需要读滚动位置做逻辑（加载数据、切 class）→ 仍用 `IntersectionObserver`，别监听 scroll 事件
- 视差位移超过 40px 的，reduced-motion 下必须关掉

## 8. 连续性与打断（Continuity）

「丝滑」不是缓动好看，是**动画不被打断、元素不瞬间跳位**。

| 术语 | 英文 | 要点 |
| --- | --- | --- |
| 可打断 | interruptible | 新输入到来时，从当前值继续，不回到起点重播 |
| 速度接管 | velocity handoff | 手势松手瞬间把速度交给动画，而不是从 0 开始 |
| 布局动画 | layout animation | 元素位置变化用 transform 模拟，不要真改布局 |
| FLIP | First / Last / Invert / Play | 记录首末位置，用反向 transform 抵消，再播放 |
| 形变 | morph | 同一元素在两个状态间连续插值，而非替换 |
| 首帧入场 | `@starting-style` | 元素第一次渲染时的入场动画，纯 CSS 触发，不用 JS 强制重绘 |

## 9. 中英对照速查

| 中文 | English | 中文 | English |
| --- | --- | --- | --- |
| 缓入缓出 | easing | 时长 | duration |
| 逐个延迟 | stagger | 交叠 | overlap |
| 预延迟 | delay | 停留 | hold |
| 编排 | choreography | 顺序 | sequencing |
| 弹簧物理 | spring physics | 阻尼比 | damping ratio |
| 过冲 | overshoot | 临界阻尼 | critical damping |
| 可打断 | interruptible | 速度接管 | velocity handoff |
| 容器变形 | container transform | 共享轴 | shared axis |
| 淡出淡入 | fade through | 同名元素过渡 | shared element transition |
| 布局动画 | layout animation | 滚动驱动 | scroll-driven |
| 合成属性 | compositor-only property | 重排 | reflow / layout |
| 掉帧 | jank | 长任务 | long task |
