# UI 组件规范

本文档定义 PWA 生成器使用的设计系统，从豆仓（Coffee Vault）PWA 提取。所有生成的 PWA 应遵循此规范以保持一致的品质基线。

---

## CSS 变量体系

所有组件通过 CSS 自定义属性（Custom Properties）驱动，便于主题切换。

```css
:root {
  /* 主色调 */
  --color-bg: #1a1510;           /* 页面背景 */
  --color-surface: #2a2018;      /* 卡片/面板背景 */
  --color-surface-2: #332a1e;    /* 次级面板背景 */
  --color-border: #4a3828;       /* 边框 */
  --color-text: #f5ede0;         /* 主文字 */
  --color-text-2: #b89878;       /* 次要文字 */
  --color-text-muted: #7a6050;   /* 弱化文字 */
  --color-accent: #c8a96e;       /* 强调色（按钮、高亮） */
  --color-accent-hover: #d4b87e; /* 强调色 hover */

  /* 状态色（卡片左侧色条） */
  --color-status-active: #4a9e6a;   /* 在用/活跃 */
  --color-status-retired: #6b6b6b;  /* 退役/归档 */
  --color-status-reserve: #c8a96e;  /* 备货/待处理 */
  --color-status-default: #4a7ab5;  /* 其他/默认 */

  /* 字体 */
  --font-display: 'Cormorant Garamond', 'Georgia', serif;
  --font-body: 'Noto Sans SC', 'PingFang SC', sans-serif;
  --font-size-xs: 0.7rem;
  --font-size-sm: 0.8rem;
  --font-size-base: 0.9rem;
  --font-size-lg: 1rem;
  --font-size-xl: 1.3rem;
  --font-size-display: 1.5rem;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 999px;

  /* 间距 */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 24px;
  --space-2xl: 32px;

  /* 阴影 */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.5);

  /* 动画 */
  --transition-fast: 0.15s ease;
  --transition-base: 0.25s ease;
}
```

---

## 主题系统

提供 4 套预设主题。通过 `data-theme` 属性切换。允许微调强调色和字体，但背景明暗层级必须保持一致。

**设计纪律（来自 tasteskill anti-slop 框架）：**
- 不用纯黑 `#000`，不用纯白 `#fff` —— off-black/off-white 保持视觉深度
- 强调色饱和度控制在 55%-78% —— 和中性底色融合不刺眼
- 每套主题底色和文字色保持同一色温（Dark Roast 的底色和文字色都偏暖，Obsidian 都偏冷）
- 字体选择有场景意图：衣线=手作质感、等宽=极客感、大写无衣线=力量感、紧凑无衣线=效率感

### 主题 1：深色暖调 `data-theme="dark-roast"`
适合：食品/饮品/收藏/手作。像精品咖啡店菜单板——暖而不甜。
```css
[data-theme="dark-roast"] {
  --bg: #1a1412;          /* 焦糖深褐，不是纯黑 */
  --surface: #231e1a;
  --accent: #d4a574;      /* 蜂蜜金，饱和度 ~55% */
  --text: #f0e8e0;        /* 暖米色，不是纯白 */
  --font-display: 'Cormorant Garamond', Georgia, serif;
  /* 衣线仅用于标题/展示名，传递手作质感 */
}
```

### 主题 2：浅色简约 `data-theme="frost"`
适合：健康/生活/效率/清爽。像北欧极简药房——干净、专业、不攻击。
```css
[data-theme="frost"] {
  --bg: #f5f6f8;          /* 冷灰调 off-white，不是纯白 */
  --surface: #ffffff;
  --accent: #2d6be6;      /* 沉稳蓝，饱和度 ~78%，避开 AI 默认紫 */
  --text: #1c1f26;        /* 墨灰，不是纯黑 */
  --font-display: 'Inter Tight', 'Inter', -apple-system, sans-serif;
  /* Inter Tight 比 Inter 多一点性格，紧凑但不压迫 */
}
```

### 主题 3：深色冷调 `data-theme="obsidian"`
适合：科技/数据/极客/装备/数码。像 VS Code 暗色主题——冷静、精确。
```css
[data-theme="obsidian"] {
  --bg: #0f1117;          /* 深蓝灰，不是纯黑 */
  --surface: #1a1d27;
  --accent: #818cf8;      /* 薰衣草蓝紫，饱和度 ~70% */
  --text: #e4e6ed;        /* 冷灰白 */
  --font-display: 'JetBrains Mono', 'SF Mono', monospace;
  /* 等宽字体带代码感，“终端标题+人类正文”的对比 */
}
```

### 主题 4：深色玫红 `data-theme="blaze"`
适合：运动/健身/挑战/目标追踪。像夜间健身房 LED 氛围灯——有能量但不刺眼。
```css
[data-theme="blaze"] {
  --bg: #1a0a14;          /* 暗玫瑰，底色带红调不是中性灰 */
  --surface: #261520;
  --accent: #f43f7a;      /* 玫红，饱和度 ~75% */
  --text: #f5e8f0;        /* 暖粉白，和底色同色温 */
  --font-display: 'Bebas Neue', Impact, sans-serif;
  /* 大写无衣线 + 宽字距，像健身房墙上标语 */
}
```

主题选择器实现：
```html
<div class="theme-switcher">
  <button data-theme-value="dark-warm" onclick="setTheme(this)">暖调</button>
  <button data-theme-value="light-minimal" onclick="setTheme(this)">简约</button>
  <button data-theme-value="dark-cool" onclick="setTheme(this)">冷调</button>
  <button data-theme-value="blaze" onclick="setTheme(this)">激励</button>
</div>
<script>
function setTheme(btn) {
  document.documentElement.setAttribute('data-theme', btn.dataset.themeValue);
  localStorage.setItem('theme', btn.dataset.themeValue);
}
// 启动时恢复
document.documentElement.setAttribute('data-theme',
  localStorage.getItem('theme') || 'dark-warm');
</script>
```

---

## TopBar 组件

位于页面顶部，sticky 固定。包含：logo（可选 emoji）+ 标题 + 数据计数。

```html
<header class="topbar">
  <div class="topbar-logo">☕</div>
  <div class="topbar-title">
    <span class="topbar-name">豆仓</span>
    <span class="topbar-count" id="item-count">0 条</span>
  </div>
</header>
```

```css
.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-lg) var(--space-xl);
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
  backdrop-filter: blur(10px);
}
.topbar-logo { font-size: 1.8rem; }
.topbar-name {
  font-family: var(--font-display);
  font-size: var(--font-size-display);
  color: var(--color-accent);
}
.topbar-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  margin-left: var(--space-sm);
}
```

---

## Overview 概览卡（可选）

顶部一张统计卡：大数字（总量）+ 分状态统计 + 一条彩色比例条。让用户一眼看清全局。**适用场景**：任何有“状态分布”的管理类 App（在用/备用/已停、架上/冰箱/喝完等）。已在补剂管家实战验证。

```html
<div id="overview" class="overview"></div>  <!-- JS 填充 -->
```

```css
.overview {
  margin: var(--space-lg) var(--space-lg) var(--space-xs);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-lg);
  display: flex; align-items: center; gap: var(--space-lg);
  box-shadow: var(--shadow-md);
  animation: fadeUp .35s ease both;
}
.overview:empty { display: none; }
.ov-num {
  font-family: var(--font-display);
  font-size: 38px; font-weight: 600; line-height: .9;
  letter-spacing: -.02em; color: var(--color-text);
}
.ov-cap { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-top: 6px; letter-spacing: .08em; }
.ov-div { width: 1px; height: 48px; background: var(--color-border); flex-shrink: 0; }
.ov-right { flex: 1; min-width: 0; }
.ov-stats { display: flex; gap: var(--space-lg); }
.ov-stat b { font-size: var(--font-size-lg); font-weight: 600; }   /* 可用等宽字体 */
.ov-stat span { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-left: 5px; }
.ov-bar { display: flex; height: 6px; border-radius: 3px; overflow: hidden; margin-top: var(--space-md); gap: 2px; }
.ov-bar i { flex-basis: 0; min-width: 3px; border-radius: 2px; }
```

```js
// 按状态分组统计，比例条 flex-grow 驱动（用 0.001 防 0 宽）
function renderOverview() {
  const ov = document.getElementById('overview'); if (!ov) return;
  const total = items.length;
  const nActive = items.filter(x => x.status === '在用').length;
  const nReserve = items.filter(x => x.status === '备用').length;
  const nStop = items.filter(x => x.status === '已停').length;
  ov.innerHTML =
      '<div><div class="ov-num">' + total + '</div><div class="ov-cap">总计</div></div>'
    + '<div class="ov-div"></div>'
    + '<div class="ov-right"><div class="ov-stats">'
    +   '<div class="ov-stat"><b style="color:var(--color-status-active)">' + nActive + '</b><span>在用</span></div>'
    +   '<div class="ov-stat"><b style="color:var(--color-status-reserve)">' + nReserve + '</b><span>备用</span></div>'
    +   '<div class="ov-stat"><b style="color:var(--color-text-muted)">' + nStop + '</b><span>已停</span></div>'
    + '</div><div class="ov-bar">'
    +   '<i style="flex-grow:' + (nActive||0.001) + ';background:var(--color-status-active)"></i>'
    +   '<i style="flex-grow:' + (nReserve||0.001) + ';background:var(--color-status-reserve)"></i>'
    +   '<i style="flex-grow:' + (nStop||0.001) + ';background:var(--color-border)"></i>'
    + '</div></div>';
}
```

---

## Filter Chips 组件

横向滚动的状态筛选条，active 状态使用 accent 色高亮。

```html
<div class="filter-bar">
  <button class="chip active" data-status="all" onclick="filterBy(this)">全部</button>
  <button class="chip" data-status="active" onclick="filterBy(this)">在用</button>
  <button class="chip" data-status="retired" onclick="filterBy(this)">退役</button>
</div>
```

```css
.filter-bar {
  display: flex;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-xl);
  overflow-x: auto;
  scrollbar-width: none;
}
.filter-bar::-webkit-scrollbar { display: none; }
.chip {
  flex-shrink: 0;
  padding: var(--space-xs) var(--space-md);
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-2);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.chip.active, .chip:hover {
  background: var(--color-accent);
  color: var(--color-bg);
  border-color: var(--color-accent);
}
```

---

## Search 组件

带搜索图标的输入框，实时筛选数据。

```html
<div class="search-wrapper">
  <span class="search-icon">🔍</span>
  <input type="search" id="search-input"
         placeholder="搜索..."
         oninput="handleSearch(this.value)">
</div>
```

```css
.search-wrapper {
  position: relative;
  padding: 0 var(--space-xl) var(--space-md);
}
.search-icon {
  position: absolute;
  left: calc(var(--space-xl) + var(--space-md));
  top: 50%;
  transform: translateY(-50%);
  font-size: var(--font-size-base);
  pointer-events: none;
}
#search-input {
  width: 100%;
  padding: var(--space-sm) var(--space-md) var(--space-sm) 2.2rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  color: var(--color-text);
  font-size: var(--font-size-base);
  box-sizing: border-box;
}
```

### 搜索折叠模式（可选变体 / 方案 B）

默认把搜索框收起成 TopBar 里的🔍图标，点击才展开。**适用场景**：项目数量不多（< 50 条）、以筛选 chips 为主、想让顶部更简洁不被搜索框占地时。已在豆仓/补剂管家实战验证。

```html
<!-- TopBar 右侧加🔍切换按钮 -->
<button class="icon-btn" id="searchToggle" aria-label="搜索">
  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>
</button>

<!-- 搜索框默认 hidden，带✕关闭按钮 -->
<div class="search-wrapper hidden" id="searchWrap">
  <span class="search-icon">🔍</span>
  <input type="search" id="search-input" placeholder="搜索..." oninput="handleSearch(this.value)">
  <button type="button" class="search-clear" id="searchClear" aria-label="关闭搜索">✕</button>
</div>
```

```css
.search-wrapper.hidden { display: none; }
.search-clear {
  position: absolute; right: calc(var(--space-xl) + var(--space-sm)); top: 50%;
  transform: translateY(-50%);
  width: 28px; height: 28px; border-radius: var(--radius-md);
  background: var(--color-surface-2); border: 1px solid var(--color-border);
  color: var(--color-text-muted); font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.search-clear:hover { color: var(--color-text); }
.icon-btn.active {  /* 搜索展开时🔍图标高亮 */
  background: var(--color-accent); border-color: var(--color-accent); color: #fff;
}
```

```js
// 展开 = 显示+聚焦；关闭 = 隐藏+清空并重新筛选
const searchWrap = document.getElementById('searchWrap');
const searchToggle = document.getElementById('searchToggle');
const searchInput = document.getElementById('search-input');
function openSearch() {
  searchWrap.classList.remove('hidden');
  searchToggle.classList.add('active');
  setTimeout(() => searchInput.focus(), 30);
}
function closeSearch() {
  searchWrap.classList.add('hidden');
  searchToggle.classList.remove('active');
  if (searchInput.value) { searchInput.value = ''; handleSearch(''); }
}
searchToggle.addEventListener('click', () =>
  searchWrap.classList.contains('hidden') ? openSearch() : closeSearch());
document.getElementById('searchClear').addEventListener('click', closeSearch);
```

**两种模式怎么选：**
- **常驻模式**（上面默认）：数据多、搜索是高频动作时，搜索框始终可见。
- **折叠模式**（方案 B）：数据少、chips 筛选足够、追求顶部简洁时，收起为🔍图标。

---

## Card 组件

数据列表的基本单元。左侧有状态色条，包含主标题、副信息行、标签、底部信息行。

```html
<div class="card status-active" onclick="openEditor(item.id)">
  <div class="card-status-bar"></div>
  <div class="card-body">
    <div class="card-header">
      <span class="card-name">耶加雪菲 G1</span>
      <span class="card-price">¥128</span>
    </div>
    <div class="card-meta">
      <span>品牌名称</span>
      <span>·</span>
      <span>产地信息</span>
    </div>
    <div class="card-tags">
      <span class="tag">浅烘</span>
      <span class="tag">花果香</span>
    </div>
    <div class="card-footer">
      <span class="card-date">2024-03-15</span>
      <span class="card-status-text">在用</span>
    </div>
  </div>
</div>
```

```css
.card {
  display: flex;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  overflow: hidden;
  cursor: pointer;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
  animation: fadeUp 0.3s ease both;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.card-status-bar {
  width: 4px;
  flex-shrink: 0;
}
.card.status-active .card-status-bar { background: var(--color-status-active); }
.card.status-retired .card-status-bar { background: var(--color-status-retired); }
.card.status-reserve .card-status-bar { background: var(--color-status-reserve); }

.card-body { padding: var(--space-md); flex: 1; }
.card-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: var(--space-xs); }
.card-name { font-size: var(--font-size-lg); font-weight: 600; color: var(--color-text); }
.card-price { font-size: var(--font-size-sm); color: var(--color-accent); }
.card-meta { font-size: var(--font-size-sm); color: var(--color-text-2); margin-bottom: var(--space-xs); }
.card-tags { display: flex; flex-wrap: wrap; gap: var(--space-xs); margin-bottom: var(--space-sm); }
.tag {
  font-size: var(--font-size-xs);
  padding: 2px var(--space-sm);
  background: var(--color-surface-2);
  border-radius: var(--radius-full);
  color: var(--color-text-2);
}
.card-footer { display: flex; justify-content: space-between; font-size: var(--font-size-xs); color: var(--color-text-muted); }
```

---

## FAB 按钮

固定在右下角的浮动操作按钮，适配 safe area。

```html
<button class="fab" onclick="openEditor()">＋</button>
```

```css
.fab {
  position: fixed;
  right: var(--space-xl);
  bottom: calc(var(--space-xl) + env(safe-area-inset-bottom));
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--color-accent);
  color: var(--color-bg);
  font-size: 1.5rem;
  border: none;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--transition-fast), background var(--transition-fast);
  z-index: 200;
}
.fab:hover { transform: scale(1.1); background: var(--color-accent-hover); }
```

---

## Editor Dialog（Modal 表单）

编辑/新增数据的浮层表单，支持 grid 布局，包含 Smart Select 交互。

```html
<div class="dialog-overlay" id="editor-overlay" onclick="handleOverlayClick(event)">
  <div class="dialog">
    <div class="dialog-header">
      <h2 class="dialog-title" id="dialog-title">新增记录</h2>
      <button class="dialog-close" onclick="closeEditor()">✕</button>
    </div>
    <form id="editor-form" class="dialog-form">
      <!-- 字段由 schema 动态生成 -->
    </form>
    <div class="dialog-footer">
      <button type="button" class="btn-danger" id="delete-btn" onclick="deleteItem()">删除</button>
      <div class="dialog-actions">
        <button type="button" class="btn-secondary" onclick="closeEditor()">取消</button>
        <button type="submit" form="editor-form" class="btn-primary">保存</button>
      </div>
    </div>
  </div>
</div>
```

```css
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  z-index: 300;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}
@media (min-width: 520px) {
  .dialog-overlay { align-items: center; }
}
.dialog {
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  background: var(--color-surface);
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
  overflow-y: auto;
  padding: var(--space-xl);
  padding-bottom: calc(var(--space-xl) + env(safe-area-inset-bottom));
}
@media (min-width: 520px) {
  .dialog { border-radius: var(--radius-xl); }
}
.dialog-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}
.form-group { display: flex; flex-direction: column; gap: var(--space-xs); }
.form-group.full-width { grid-column: 1 / -1; }
.form-group label { font-size: var(--font-size-sm); color: var(--color-text-2); }
.form-group input,
.form-group select,
.form-group textarea {
  padding: var(--space-sm) var(--space-md);
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text);
  font-size: var(--font-size-base);
  font-family: var(--font-body);
}
.form-group textarea { resize: vertical; min-height: 80px; }
.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--space-xl);
}
.dialog-actions { display: flex; gap: var(--space-sm); }
.btn-primary {
  padding: var(--space-sm) var(--space-xl);
  background: var(--color-accent);
  color: var(--color-bg);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
}
.btn-secondary {
  padding: var(--space-sm) var(--space-xl);
  background: transparent;
  color: var(--color-text-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
}
.btn-danger {
  background: transparent;
  color: #e85555;
  border: none;
  cursor: pointer;
  font-size: var(--font-size-sm);
}
```

---

## Sort Bar

排序维度切换按钮组，当前激活维度高亮。

```html
<div class="sort-bar">
  <span class="sort-label">排序：</span>
  <button class="sort-btn active" data-sort="date" onclick="sortBy(this)">日期</button>
  <button class="sort-btn" data-sort="name" onclick="sortBy(this)">名称</button>
  <button class="sort-btn" data-sort="price" onclick="sortBy(this)">价格</button>
</div>
```

```css
.sort-bar {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-xl);
}
.sort-label { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.sort-btn {
  padding: 2px var(--space-sm);
  background: transparent;
  color: var(--color-text-muted);
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  cursor: pointer;
}
.sort-btn.active {
  color: var(--color-accent);
  border-color: var(--color-accent);
}
```

---

## Empty State

无数据时的提示组件。

```html
<div class="empty-state" id="empty-state">
  <div class="empty-icon">📭</div>
  <p class="empty-text">还没有记录</p>
  <p class="empty-hint">点击右下角 ＋ 添加第一条</p>
</div>
```

```css
.empty-state {
  text-align: center;
  padding: var(--space-2xl) var(--space-xl);
  color: var(--color-text-muted);
}
.empty-icon { font-size: 3rem; margin-bottom: var(--space-md); }
.empty-text { font-size: var(--font-size-lg); margin-bottom: var(--space-sm); }
.empty-hint { font-size: var(--font-size-sm); }
```

---

## 动画：fadeUp 卡片入场

```css
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

卡片列表渲染时，通过 `animation-delay` 实现错落感：
```js
card.style.animationDelay = `${index * 0.04}s`;
```

---

## 移动端适配

### 断点
- 主断点：`520px`（宽于此时切换为居中卡片模式）
- 窄屏：单列布局，form grid 折叠为单列

```css
@media (max-width: 520px) {
  .dialog-form { grid-template-columns: 1fr; }
  .form-group.full-width { grid-column: 1; }
}
```

### Standalone 模式适配（iOS PWA）
```css
@media (display-mode: standalone) {
  .topbar {
    padding-top: calc(var(--space-lg) + env(safe-area-inset-top));
  }
  body {
    padding-bottom: env(safe-area-inset-bottom);
  }
}
```

### Viewport Meta（必须）
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

---

## 字体加载

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Noto+Sans+SC:wght@400;500;600&display=swap">
```

不同主题可覆盖 `--font-display` 变量切换字体风格（如冷调主题使用等宽字体）。

---

## Smart Select 管理功能

每个 `type: 'smart-select'` 字段都带“管理”功能，允许用户对历史值进行改名和删除。

### HTML 结构

Smart Select 字段在编辑器中的 HTML：
```html
<label>
  <span>品牌</span>
  <div class="smart-select-wrap">
    <select class="smart-select" data-field="brand">
      <option value="">请选择</option>
      <option value="__custom__">✏️ 手动输入…</option>
    </select>
    <button type="button" class="smart-manage-btn" data-field="brand" title="管理">⚙</button>
  </div>
  <input type="hidden" name="brand" />
  <input type="text" class="smart-input" data-field="brand" placeholder="输入品牌名" style="display:none" />
</label>
```

关键点：
- `<select>` 和 `⚙` 按钮用 `.smart-select-wrap` 包裹，flex 布局
- ⚙ 按钮的 `data-field` 必须与字段 key 一致
- 管理面板是共用的 `#smartSelectManager` dialog，已在模板中内置

### 功能
- **改名**：弹出 prompt 输入新名称，批量更新所有使用该值的记录
- **删除**：确认后清空所有使用该值的记录的对应字段
- 操作后自动刷新列表和 Smart Select 下拉框

### JS 逻辑
已内置在 `template-app.js` 的 `openSmartSelectManager()` 函数中，通过 `data-field` 属性自动适配任意 smart-select 字段。
