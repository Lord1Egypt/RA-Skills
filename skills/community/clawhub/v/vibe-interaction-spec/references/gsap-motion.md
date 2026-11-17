# GSAP 网页动效

什么时候该从 CSS 换到 GSAP：**需要时间线编排、需要打断与反向、需要滚动绑定、需要 SVG 形变**。CSS 能做到的（简单 state 切换）不要上 JS——零依赖、自动可打断，这是 CSS 的天然优势。

## 1. 授权（重要，别再写错）

自 **GSAP 3.13（2025-04-29）** 起，GSAP **全部功能免费，包括原先 Club GSAP 专属的插件**（SplitText、MorphSVG、ScrollSmoother、Flip、CustomEase 等），**商业项目同样免费**。插件已并入主仓库与公共 npm 包，不再需要私有源和 token。

所以「SplitText 要付费」这条旧认知可以删掉了。

## 2. 核心：tween 与 timeline

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
import { Flip } from 'gsap/Flip';
gsap.registerPlugin(ScrollTrigger, SplitText, Flip);
```

```js
// 单个补间
gsap.to('.card', { y: -4, duration: 0.2, ease: 'power2.out' });

// 时间线：把一串动作当一个整体控制
const tl = gsap.timeline({ defaults: { duration: 0.4, ease: 'power2.out' } });
tl.from('.hero-title', { y: 24, opacity: 0 })
  .from('.hero-sub', { y: 16, opacity: 0 }, '-=0.25')   // 与上一段重叠 0.25s
  .from('.hero-cta', { y: 12, opacity: 0, scale: 0.98 }, '<0.1');
```

**位置参数**是最该背下来的语法：

| 写法 | 含义 |
| --- | --- |
| `'-=0.25'` | 比上一段结束早 0.25s 开始（重叠） |
| `'<'` | 与上一段**同时**开始 |
| `'<0.1'` | 上一段开始后 0.1s |
| `'>'` | 上一段**结束**时开始 |
| `'+=0.5'` | 上一段结束后 0.5s |
| `2.0` | 时间线第 2 秒（绝对时间） |
| `'label'` | 命名锚点，`tl.addLabel('cta')` |

**编排原则**：交叠 60–80% 才有连贯感。逐段串行（`>`）看起来像 PPT 翻页。

## 3. 缓动

```js
gsap.registerEase('brand', 'M0,0 C0.2,0 0,1 1,1');  // CustomEase
```

- 入场用 `power2.out` / `expo.out`，退场用 `power2.in`
- 有回弹的场景用 `back.out(1.6)`，参数别超 2，超了像弹簧坏掉
- 品牌一致性：把 CSS 里的 `cubic-bezier` 换成 CustomEase，或直接对齐 token：

```js
const T = { dur: { 100: 0.1, 200: 0.2, 300: 0.3, 400: 0.4 }, ease: 'power2.out' };
gsap.to(el, { y: -4, duration: T.dur[200], ease: T.ease });
```

duration 是**秒**不是毫秒，这是从 CSS 迁过来最常踩的坑。

## 4. ScrollTrigger

```js
gsap.to('.panel', {
  y: -80,
  ease: 'none',                              // scrub 必须 none
  scrollTrigger: {
    trigger: '.panel',
    start: 'top 80%',                        // 元素顶部到视口 80% 处
    end: 'bottom 30%',
    scrub: 1,                                // 1s 追帧，0 = 硬绑，true = 直连
    pin: true,                               // 钉住
    pinSpacing: true,
    markers: false,                          // 调试时临时 true
    toggleActions: 'play none none reverse', // 无 scrub 时的进/出行为
  },
});
```

| 需求 | 写法 |
| --- | --- |
| 滚动进度直接驱动动画 | `scrub: true` |
| 带一点惯性 | `scrub: 0.5 ~ 1` |
| 批量元素依次触发 | `ScrollTrigger.batch('.card', { onEnter: batch => gsap.to(batch, {...}) })` |
| 横向滚动区里触发 | `containerAnimation: horizontalTween` |
| 移动端地址栏导致跳动 | `ScrollTrigger.normalizeScroll(true)` |
| 多个触发器互相打架 | `ScrollTrigger.config({ ignoreMobileResize: true })` |

**Refresh 时机**：图片加载完、字体加载完、折叠展开后，布局变了要 `ScrollTrigger.refresh()`。字体导致的位移是「滚动位置错乱」的头号原因。

## 5. SplitText（文字动效）

```js
const split = new SplitText('.headline', { type: 'lines,words,chars', mask: 'lines' });
gsap.from(split.chars, { y: '100%', opacity: 0, stagger: 0.02, duration: 0.6, ease: 'power3.out' });
```

新版 SplitText 自带无障碍处理：给原元素加 `aria-label`，给拆分出的元素加 `aria-hidden`，读屏不会念成一堆碎字。

**必须清理**：响应式重排或组件卸载时 `split.revert()`，否则 DOM 里留下一堆 span。用 `autoSplit: true` 可以让它自己重切。

## 6. Flip（布局动画）

列表排序、网格变列表、卡片展开——这些用 CSS 做不到（布局变了，没有起止值可插值）：

```js
const state = Flip.getState('.item');
container.classList.toggle('is-grid');
Flip.from(state, { duration: 0.5, ease: 'power2.inOut', absolute: true, stagger: 0.03 });
```

`absolute: true` 让元素在动画期间脱离文档流，避免互相推挤。

## 7. React / Vue 集成

React 用 `@gsap/react` 的 `useGSAP`，它本质是 `gsap.context()` 的封装，负责自动清理：

```jsx
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(useGSAP, ScrollTrigger);

function Hero() {
  const ref = useRef(null);
  useGSAP(() => {
    gsap.from('.line', { y: 20, opacity: 0, stagger: 0.08 });
    // 这里创建的动画与 ScrollTrigger 会在卸载时自动 revert
  }, { scope: ref, dependencies: [] });
  return <section ref={ref}>…</section>;
}
```

不用 `useGSAP` 的话，必须手动 `ctx.revert()`，否则热更新会叠出十几套动画。

## 8. 响应式与无障碍

```js
const mm = gsap.matchMedia();

mm.add('(prefers-reduced-motion: reduce)', () => {
  gsap.set('.fade', { opacity: 1, y: 0 });      // 直接到位
  return () => {};                               // 清理函数
});

mm.add('(min-width: 768px) and (prefers-reduced-motion: no-preference)', () => {
  gsap.from('.fade', { y: 24, opacity: 0, stagger: 0.08, scrollTrigger: {…} });
});
```

`matchMedia` 比手写 `window.innerWidth` 好在：断点变化时自动 revert 并重建，不会两套动画同时活着。

## 9. 性能

| 做法 | 原因 |
| --- | --- |
| 只补间 `transform` / `opacity` | 走合成层，不触发布局 |
| 高频跟随用 `gsap.quickTo()` | 复用同一个 tween，不产生垃圾 |
| 不要给所有元素加 `will-change` | 图层爆炸，显存吃满 |
| `ScrollTrigger` 的 `trigger` 别选 `body` | 整页刷新计算，滚动卡顿 |
| 大量元素用 `ScrollTrigger.batch` + `stagger` | 一次计算，避免每元素一个触发器 |
| 动画结束后 `clearProps` | 清掉残留内联样式，避免和 CSS 冲突 |

```js
// 鼠标跟随：高频更新必须用 quickTo
const xTo = gsap.quickTo('.cursor', 'x', { duration: 0.4, ease: 'power3' });
const yTo = gsap.quickTo('.cursor', 'y', { duration: 0.4, ease: 'power3' });
addEventListener('pointermove', (e) => { xTo(e.clientX); yTo(e.clientY); });
```

## 10. 反模式

- **用 GSAP 做 CSS 能做的事**：单纯 hover 变色上 GSAP，白搭 70KB 且丢失 CSS 的可打断优势
- **`duration` 写毫秒**：`duration: 300` 等于 5 分钟
- **scrub 加了 ease**：手停了画面还在动
- **不 revert**：SPA 里切几次路由，动画叠成一团
- **所有动画都 `repeat: -1`**：一屏都在动，没有重点且违反无障碍
- **SplitText 不处理响应式**：换行错位、断词难看
- **忽略 `prefers-reduced-motion`**：前庭功能敏感用户会直接关掉页面
