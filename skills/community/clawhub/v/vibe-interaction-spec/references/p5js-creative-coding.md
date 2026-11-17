# p5.js 创意编程

p5.js 适合**生成**而不是**编排**：图案、纹理、粒子场、数据艺术、海报底纹。它的价值在于「每次运行都不一样，但可以被固定成一张可以印刷的图」。

和 GSAP 的分工：GSAP 编排**已有的元素**，p5.js **生成元素本身**。

## 1. 版本前提（2.0 起有破坏性变更）

p5.js 2.0 已发布，写法与 1.x 不同。新项目按 2.0 写：

| 1.x | 2.0 |
| --- | --- |
| `function preload() { img = loadImage(...) }` | `async function setup() { img = await loadImage(...) }` |
| `curveVertex()` 且首尾点要重复 | `splineVertex()`，不再重复控制点 |
| 仅 RGB/HSB | 增加 `OKLCH` / `OKLAB` / `HWB`，渐变不出灰 |
| 手写 GLSL | `baseMaterialShader().modify()` 用 JS 改着色器 |
| 固定字重 | 可变字体 `textWeight()` 动态调重 |

老草图可以靠编辑器里的 Preload 兼容附加组件继续跑，但新代码不要用 `preload()`。

## 2. 最小骨架（实例模式，用于嵌进网页）

全局模式（`setup` / `draw` 裸写）只适合草图本。嵌进页面必须用实例模式，否则一个页面只能有一个 sketch：

```js
import p5 from 'p5';

const sketch = (p) => {
  p.setup = () => {
    const c = p.createCanvas(p.windowWidth, 420);
    c.parent('canvas-host');
    p.pixelDensity(Math.min(window.devicePixelRatio, 2)); // 同 three.js，别跟 3x 屏跑
    p.noiseSeed(7);      // 固定噪声
    p.randomSeed(7);     // 固定随机 —— 可复现的前提
    p.noLoop();          // 静态生成物不需要每帧重绘
  };

  p.draw = () => {
    p.background('#faf8f5');
    // …绘制
  };

  p.windowResized = () => { p.resizeCanvas(p.windowWidth, 420); p.redraw(); };
};

new p5(sketch);
```

**`randomSeed` + `noiseSeed` 是可复现的关键**：不固定种子，今天好看的图明天复现不出来。做品牌物料时必须固定。

## 3. 五种真正好用的生成手法

### 3.1 Perlin 噪声流场

最稳的「有機感」来源，比随机点更像自然。

```js
p.noStroke();
for (let i = 0; i < 4000; i++) {
  const x = p.random(p.width), y = p.random(p.height);
  const n = p.noise(x * 0.004, y * 0.004);
  const angle = n * p.TWO_PI * 2;
  p.push();
  p.translate(x, y);
  p.rotate(angle);
  p.fill(27, 58, 46, 40);
  p.rect(0, 0, 18, 1.5);      // 短线段，方向由噪声决定
  p.pop();
}
```

参数手感：`0.002–0.006` 是最舒服的尺度区间，越大越碎。

### 3.2 粒子系统

```js
const parts = Array.from({ length: 600 }, () => ({
  x: p.random(p.width), y: p.random(p.height),
  vx: p.random(-0.4, 0.4), vy: p.random(-0.4, 0.4),
}));

p.draw = () => {
  p.background(250, 248, 245, 18);   // 半透明清屏 = 拖尾
  parts.forEach((q) => {
    q.x += q.vx + (p.noise(q.y * 0.01) - 0.5);   // 噪声给一点风
    q.y += q.vy;
    if (q.x < 0) q.x = p.width; if (q.x > p.width) q.x = 0;
    p.circle(q.x, q.y, 2);
  });
};
```

拖尾别用 `clear()`，用低 alpha 的 `background()` 叠出来更自然。

### 3.3 递归细分

做纹样、地图、建筑感的图形：

```js
function split(x, y, w, h, depth) {
  if (depth === 0) { p.rect(x, y, w, h); return; }
  if (w > h) {
    const cut = w * p.random(0.3, 0.7);
    split(x, y, cut, h, depth - 1);
    split(x + cut, y, w - cut, h, depth - 1);
  } else {
    const cut = h * p.random(0.3, 0.7);
    split(x, y, w, cut, depth - 1);
    split(x, y + cut, w, h - cut, depth - 1);
  }
}
```

加 0.5–1px 的描边就是「建筑图纸感」，去掉描边填色就是「蒙德里安」。

### 3.4 字体轮廓变形

2.0 的 `textToContours()` 能把字变成可编辑的轮廓点，做扭曲标题：

```js
const font = await p.loadFont('https://fonts.gstatic.com/s/inter/…ttf');
const contours = font.textToContours('造型', 0, 0, 160);

p.beginShape();
for (const pts of contours) {
  p.beginContour();
  for (const pt of pts) {
    // 沿 y 做正弦扰动，得到「液化」效果
    p.vertex(pt.x + 6 * Math.sin(pt.y * 0.05), pt.y);
  }
  p.endContour(p.CLOSE);
}
p.endShape();
```

### 3.5 色带与抖动（Risograph 感）

```js
p.colorMode(p.OKLCH, 1, 0.4, 360);   // 2.0 的感知均匀色彩空间
for (let i = 0; i < 60; i++) {
  p.fill(0.7, 0.15, 200 + i * 0.6);  // 色相缓慢推移，不会中途发灰
  p.rect(0, i * 8, p.width, 8);
}
```

OKLCH 的价值：在 sRGB 里从蓝到紫会在中间穿过灰区，OKLCH 不会。

## 4. 性能与电量

| 手段 | 效果 |
| --- | --- |
| `p.noLoop()` + `redraw()` | 静态图的核心优化，别让不动的画面跑 60fps |
| `pixelDensity(1)`（装饰用） | 像素量降到 1/4 |
| 离屏 `createGraphics()` | 把固定背景画一次，之后只叠动态层 |
| 限制粒子数 400–800 | 超过 2000 在低端机上必然掉帧 |
| `IntersectionObserver` 暂停 | 不在视口内就 `noLoop()` |

**移动端策略**：装饰性 sketch 直接不加载，用静态图代替；必须加载时把粒子数降到 1/3、`pixelDensity(1)`。

## 5. 导出与印刷

```js
p.saveCanvas('texture', 'png');            // 屏幕用
p.pixelDensity(4); p.redraw();             // 印刷前临时提到 4 倍
```

- 印刷导出前把 `pixelDensity` 提到 3–4，导出后调回，避免常驻高分辨率。
- 需要矢量（logo、丝网版）时，改用 p5 的 SVG 渲染器或直接把坐标输出为 SVG 路径。
- 固定种子 + 固定尺寸 = 可复现的印刷品，这条比任何滤镜都重要。

## 6. 嵌进网页的三种位置

| 位置 | 做法 | 注意 |
| --- | --- | --- |
| 首屏背景 | 全屏 canvas + 内容层 `position: relative; z-index: 1` | 必须控帧率，别抢主线程 |
| 卡片底纹 | 固定尺寸 canvas，`noLoop` 生成一次 | 一张图就够，别做动画 |
| 数据艺术板块 | 由数据驱动 `draw`，参数来自接口 | 数据变了要 `redraw()` 而不是重建 sketch |

canvas 默认是 inline 元素，会出现下方 4px 空隙：`display: block`。

## 7. 无障碍与降级

1. 装饰性 canvas 加 `aria-hidden="true"`，另给文字说明。
2. `prefers-reduced-motion: reduce` 时 `noLoop()`，只显示第一帧。
3. 生成内容如果承载信息（数据可视化），必须另有表格或文字版本。
4. 不要在 canvas 上做唯一交互入口。

## 8. 廉价信号清单

- [ ] `random()` 满屏撒点，没有种子也没有结构 —— 一眼「教程作品」
- [ ] 粒子数 5000+ 且每帧 `background()` 全清，低端机直接卡死
- [ ] 只用 RGB 插值做渐变，中间发灰
- [ ] 全屏 canvas 铺在正文下面，文字完全读不清
- [ ] 每次刷新图案都不同，无法交付品牌物料
- [ ] `preload()` 留在 2.0 项目里（已废弃写法）
- [ ] 没有 `resizeCanvas`，窗口一变就错位
