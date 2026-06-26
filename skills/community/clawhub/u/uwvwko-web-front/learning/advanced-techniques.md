# 高级CSS技巧

## 1. CSS Grid 自动布局

### auto-fill vs auto-fit
```css
/* auto-fill: 尽可能多地填充列，即使有些是空的 */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}

/* auto-fit: 将现有列扩展填充空间，不创建空列 */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
```

### Subgrid（子网格）
```css
.parent-grid {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
}

.grid-item {
  grid-column: 2 / 7;
  display: grid;
  grid-template-columns: subgrid; /* 继承父网格的列 */
}
```

## 2. CSS变量高级用法

### 条件化变量
```css
:root {
  --spacing: 16px;
}

@media (max-width: 768px) {
  :root {
    --spacing: 8px; /* 在小屏幕上减小间距 */
  }
}
```

### 带后备值的变量
```css
:root {
  --primary-color: var(--brand-color, #667eea); /* 如果 --brand-color 未定义，使用 #667eea */
}
```

### 带计算的变量
```css
:root {
  --base-spacing: 8px;
  --double-spacing: calc(var(--base-spacing) * 2);
}
```

## 3. 性能优化技巧

### will-change 提示
```css
/* 提示浏览器即将发生变化的属性 */
.animated-element {
  will-change: transform, opacity;
}

/* 动画结束后移除 will-change */
.animated-element.animated {
  will-change: auto;
}
```

### contain 优化渲染
```css
/* 限制浏览器重绘范围 */
.card {
  contain: layout style paint;
}
```

### 避免强制同步布局
```javascript
// ❌ 错误：会导致强制同步布局
element.style.height = element.offsetHeight + 10 + 'px';

// ✅ 正确：先读取，后写入
const height = element.offsetHeight;
element.style.height = height + 10 + 'px';
```

## 4. 响应式图片

### srcset 和 sizes
```html
<img 
  src="image-800.jpg"
  srcset="image-400.jpg 400w,
         image-800.jpg 800w,
         image-1200.jpg 1200w"
  sizes="(max-width: 600px) 100vw,
         (max-width: 1200px) 50vw,
         33vw"
  alt="描述性文本"
>
```

### picture 元素
```html
<picture>
  <source media="(min-width: 1200px)" srcset="large.jpg">
  <source media="(min-width: 600px)" srcset="medium.jpg">
  <img src="small.jpg" alt="描述性文本">
</picture>
```

### 懒加载
```html
<img loading="lazy" src="image.jpg" alt="描述性文本">
```

## 5. 可访问性最佳实践

### 减少动画
```css
/* 尊重用户的动画偏好设置 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 焦点样式
```css
:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* 移除默认焦点样式时，必须提供替代样式 */
:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* 鼠标点击时不显示焦点样式，键盘导航时显示 */
:focus:not(:focus-visible) {
  outline: none;
}
```

### 语义化HTML
```html
<!-- 使用语义化标签 -->
<header>
  <nav aria-label="主导航">
    <a href="#home">首页</a>
  </nav>
</header>

<main>
  <article>
    <h1>文章标题</h1>
    <section>
      <h2>章节标题</h2>
    </section>
  </article>
</main>

<footer>
  <p>&copy; 2026</p>
</footer>
```

### ARIA标签
```html
<!-- 按钮标签 -->
<button aria-label="菜单" aria-expanded="false">
  <span class="hamburger"></span>
</button>

<!-- 实时区域 -->
<div role="alert" aria-live="polite">
  操作成功
</div>

<!-- 隐藏装饰性元素 -->
<span class="icon" aria-hidden="true">🎨</span>
```

## 6. 现代CSS函数

### min() / max()
```css
.element {
  /* 最小宽度 300px，最大宽度 50% */
  width: max(300px, 50%);
  
  /* 最大宽度 800px，但不超过 100% - 40px */
  width: min(800px, 100% - 40px);
  
  /* 字体大小：最小 16px，首选 2vw，最大 24px */
  font-size: clamp(16px, 2vw, 24px);
}
```

### fit-content()
```css
.element {
  /* 宽度适应内容，但不超过 300px */
  width: fit-content(300px);
}
```

## 7. CSS计数器
```css
ol {
  counter-reset: section;
  list-style-type: none;
}

li::before {
  counter-increment: section;
  content: "Section " counter(section) ": ";
}
```

## 8. CSS形状
```css
/* 文字环绕形状 */
.shape {
  float: left;
  shape-outside: circle(50%);
  clip-path: circle(50%);
}

/* 多边形形状 */
.shape {
  shape-outside: polygon(0 0, 100% 0, 100% 100%, 0 100%);
}
```