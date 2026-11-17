# HTML 演示文稿生成规范

> S5 生成时必须遵守的技术规范。基准 = 命中的 L2 风格正文 + `assets/common/slide_patterns.md`。

## 1. 文件结构

- **单文件**：CSS/JS 全部内联在 `<style>`/`<script>`，零外部请求。
- **结构**：`<!DOCTYPE html>` → `<head>`（meta + title + style）→ `<body>`（多个 `<section class="slide">`）→ 可选翻页 `<script>`。
- **编码**：`<meta charset="UTF-8">`；`<meta name="viewport" content="width=device-width, initial-scale=1.0">`。

## 2. 设计 token（CSS 变量）

```css
:root{
  --bg:#...; --card:#...; --ink:#...; --mu:#...; --ac:#...; --line:#...;
  --font:'Noto Sans SC',system-ui,sans-serif;
}
```

- 配色必须来自 L2 风格正文「配色 Token」表，禁止凭记忆编。
- 风格切换只改 `:root` 变量，不改结构。

## 3. 排版

- **标题**：`clamp()` 流式字号；封面主标题最大。
- **正文**：`line-height:1.6–1.8`；首行不缩进（网页惯例）。
- **层级**：`<h1>`（封面/章节主标）→ `<h2>`（小节）→ `<h3>`（卡片标题）。
- **字体**：L2 正文的字体族；无联网时用系统字体栈。

## 4. 布局

- **卡片网格**：`display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1.25rem;`
- **圆角/阴影/边框**：按 L2 正文「形状与特效」抄用。
- **留白**：`padding:8vh 8vw` 起步，浅色族留白更多，深色族可紧凑。

## 5. 响应式（1024 / 640 双断点）

```css
@media (max-width:1024px){ /* 多栏改双栏 */ }
@media (max-width:640px){ /* 单列、字号下调、padding 收窄 */ }
```

- 窄屏：网格单列、标题 `clamp` 自动缩小、导航横排改竖排。

## 6. 左右翻页与底部进度条（必做）

### 6.1 左右翻页

- **三种触发方式**：键盘 `←`/`→`、屏幕左右箭头按钮、移动端左右滑动（`touchstart`/`touchend` 判定）。
- **逐页切换**：一次只切一页；默认到边界停住（可加"回到首页"按钮）。
- **结构**：每页 `<section class="slide">`；JS 维护 `current` 索引，切换时 `classList` 控制显隐（或 `scrollIntoView`）。
- **平滑过渡**：切换用淡入/位移动画（按 L2 正文 keyframes 风格），时长 250–400ms。

```js
// 最小翻页核心
const slides=[...document.querySelectorAll('.slide')]; let cur=0;
function go(i){ cur=Math.max(0,Math.min(slides.length-1,i));
  slides.forEach((s,k)=>s.classList.toggle('on',k===cur)); updateBar(); }
document.addEventListener('keydown',e=>{ if(e.key==='ArrowRight')go(cur+1); if(e.key==='ArrowLeft')go(cur-1); });
```

### 6.2 底部页码总数与进度条

- **固定底栏**：`position:fixed; bottom:0; left:0; right:0;`，跨页常驻。
- **页码**：`当前页 N / 总页数 M`（N 从 1 起），实时同步。
- **进度条**：宽度 = `N / M * 100%`，颜色用风格强调色 `var(--ac)`；可加过渡动画。

```html
<div class="progress-bar">
  <span class="page-num" id="pageNum">1 / 12</span>
  <div class="dots" id="dots"></div>
  <div class="track"><div class="fill" id="pageFill" style="width:8.3%"></div></div>
</div>
```
```css
.progress-bar{ position:fixed; left:0; right:0; bottom:0; display:flex; align-items:center;
  gap:12px; padding:10px 24px; background:var(--card); border-top:1px solid var(--line);
  font-size:.85rem; color:var(--mu); z-index:99; }
.progress-bar .track{ flex:1; height:4px; background:var(--line); border-radius:999px; overflow:hidden; }
.progress-bar .fill{ height:100%; background:var(--ac); border-radius:999px; transition:width .3s ease; }
```

### 6.3 圆点跳页（默认开启，点击圆点直达对应页）

- **呈现方式**：底栏中部一排可点击圆点，每个圆点对应一页；当前页圆点拉长成胶囊 + 强调色高亮。
- **交互**：点击圆点跳转对应页；`hover` 放大 + `title` 提示「第 N 页」；翻页时同步高亮。
- **页数自适应**：页数 ≤12 用圆点；页数 >12 圆点自动缩小（或改用进度条分段胶囊，每段可点）。
- **配色**：未激活 `var(--line)` 或半透明；激活 `var(--ac)` + 光晕。

```css
.dots{ flex:1; display:flex; align-items:center; justify-content:center; gap:10px; }
.dot{ width:8px; height:8px; border-radius:999px; border:none; padding:0;
      background:var(--line); cursor:pointer; transition:all .25s ease; }
.dot:hover{ background:var(--ac); transform:scale(1.3); }
.dot.on{ width:24px; background:var(--ac); }
```
```js
// 构建圆点 + 跳页同步高亮
const dotsWrap=document.getElementById('dots');
dotsWrap.innerHTML=slides.map((_,i)=>
  `<button class="dot" title="第 ${i+1} 页" onclick="go(${i})"></button>`).join('');
// go() 内追加：
dotsWrap.querySelectorAll('.dot').forEach((d,k)=>d.classList.toggle('on',k===cur));
```

### 6.4 动画

- 封面淡入、内容页渐次上移（`animation` + `animation-delay` 错峰）；按 L2 正文的 keyframes 风格。
- 尊重 `prefers-reduced-motion`（用户减少动效时关闭动画）。

## 7. 无障碍

- 语义化标签；图片加 `alt`；按钮/链接可聚焦且焦点可见。
- 对比度达标（见 palette_guide.md）；字体不强制字号（用相对单位）。
- `lang="zh-CN"`。

## 8. 内容铁律

- **只填用户给的事实**：数据、数字、品牌名、日期一律用用户提供的；缺口用 `【待补充】` 占位。
- **禁止编造**：不虚构数据、客户名、指标、成就。
- 占位符用统一格式：`【待补充：XXX】`。
