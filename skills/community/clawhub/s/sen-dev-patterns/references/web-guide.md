# Web开发规范

本文档沉淀Web前端开发的样式规范和最佳实践。

---

## 1. CSS变量定义

### 色彩系统

```css
:root {
    /* 主色调 - 渐变紫蓝 */
    --primary-start: #667eea;
    --primary-end: #764ba2;
    --primary: linear-gradient(135deg, var(--primary-start), var(--primary-end));

    /* 功能色 */
    --success: #48bb78;
    --warning: #f6ad55;
    --danger: #fc8181;
    --info: #63b3ed;

    /* 中性色 */
    --gray-100: #f7fafc;
    --gray-200: #edf2f7;
    --gray-300: #e2e8f0;
    --gray-400: #a0aec0;
    --gray-500: #718096;
    --gray-600: #4a5568;
    --gray-700: #2d3748;
    --gray-800: #1a202c;
    --gray-900: #171923;

    /* 文本色 */
    --text-primary: #2d3748;
    --text-secondary: #718096;
    --text-muted: #a0aec0;

    /* 背景色 */
    --bg-primary: #ffffff;
    --bg-secondary: #f7fafc;
    --bg-dark: #1a202c;
}
```

---

## 2. 常用组件样式

### 按钮样式

```css
/* 主按钮 */
.btn-primary {
    background: var(--primary);
    color: white;
    padding: 12px 24px;
    border-radius: 14px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:active {
    transform: translateY(0);
}

/* 次要按钮 */
.btn-secondary {
    background: var(--gray-200);
    color: var(--text-primary);
    padding: 12px 24px;
    border-radius: 14px;
    border: 1px solid var(--gray-300);
    font-weight: 500;
}

/* 成功按钮 */
.btn-success {
    background: var(--success);
    color: white;
}

/* 危险按钮 */
.btn-danger {
    background: var(--danger);
    color: white;
}
```

### 卡片组件

```css
.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border: 1px solid var(--gray-200);
}

.card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
    transition: all 0.2s ease;
}

.card-header {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--gray-200);
}

.card-body {
    color: var(--text-secondary);
}
```

### 输入框样式

```css
.input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid var(--gray-300);
    border-radius: 10px;
    font-size: 14px;
    transition: all 0.2s ease;
    outline: none;
}

.input:focus {
    border-color: var(--primary-start);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.input::placeholder {
    color: var(--gray-400);
}

.input-error {
    border-color: var(--danger);
}
```

### 标签页样式

```css
.tabs {
    display: flex;
    gap: 8px;
    border-bottom: 2px solid var(--gray-200);
}

.tab {
    padding: 12px 24px;
    background: var(--gray-100);
    border: none;
    border-radius: 8px 8px 0 0;
    cursor: pointer;
    font-weight: 500;
    color: var(--text-secondary);
    transition: all 0.2s ease;
}

.tab:hover {
    background: var(--gray-200);
}

.tab.active {
    background: white;
    color: var(--primary-start);
    border-bottom: 2px solid var(--primary-start);
    margin-bottom: -2px;
}
```

---

## 3. 响应式断点

```css
/* 移动端优先 */
/* 小屏幕手机 */
@media (max-width: 576px) {
    .container {
        padding: 0 16px;
    }
}

/* 大屏手机 / 小平板 */
@media (min-width: 577px) and (max-width: 768px) {
    .container {
        padding: 0 24px;
    }
}

/* 平板 */
@media (min-width: 769px) and (max-width: 992px) {
    .container {
        max-width: 720px;
    }
}

/* 小桌面 */
@media (min-width: 993px) and (max-width: 1200px) {
    .container {
        max-width: 960px;
    }
}

/* 大桌面 */
@media (min-width: 1201px) {
    .container {
        max-width: 1140px;
    }
}
```

### Flex布局工具类

```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.items-end { align-items: flex-end; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-end { justify-content: flex-end; }
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 16px; }
.gap-4 { gap: 24px; }
.flex-1 { flex: 1; }
```

### Grid布局工具类

```css
.grid { display: grid; }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

@media (max-width: 768px) {
    .md\:grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
    .md\:grid-cols-1 { grid-template-columns: 1fr; }
}

@media (max-width: 576px) {
    .sm\:grid-cols-1 { grid-template-columns: 1fr; }
}
```

---

## 4. 动画效果

### 过渡动画

```css
/* 标准过渡 */
.transition {
    transition: all 0.2s ease;
}

/* 弹性效果 */
.bounce {
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* 淡入 */
.fade-in {
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* 上滑淡入 */
.slide-up {
    animation: slideUp 0.3s ease;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 加载动画 */
.spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
```

### 悬停效果

```css
/* 缩放 */
.hover-scale:hover {
    transform: scale(1.05);
}

/* 上浮 */
.hover-lift:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* 颜色变化 */
.hover-color:hover {
    background: var(--primary);
    color: white;
}
```

---

## 5. 日志/状态显示样式

### 深色日志区域

```css
.log-container {
    background: var(--bg-dark);
    color: #e2e8f0;
    border-radius: 8px;
    padding: 16px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    overflow-y: auto;
    max-height: 400px;
}

.log-line {
    padding: 4px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.log-info {
    color: #63b3ed;
}

.log-warning {
    color: #f6ad55;
}

.log-error {
    color: #fc8181;
}

.log-success {
    color: #68d391;
}
```

### 状态徽章

```css
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.badge-success {
    background: rgba(72, 187, 120, 0.15);
    color: var(--success);
}

.badge-warning {
    background: rgba(246, 173, 85, 0.15);
    color: var(--warning);
}

.badge-danger {
    background: rgba(252, 129, 129, 0.15);
    color: var(--danger);
}

.badge-info {
    background: rgba(99, 179, 237, 0.15);
    color: var(--info);
}
```

---

## 6. 表格样式

```css
.table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

.table th {
    background: var(--gray-100);
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 2px solid var(--gray-200);
}

.table td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--gray-200);
    color: var(--text-secondary);
}

.table tr:hover {
    background: var(--gray-100);
}

.table-striped tr:nth-child(even) {
    background: var(--gray-100);
}
```

---

## 7. 常用工具类

```css
/* 文本 */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-primary { color: var(--primary-start); }
.text-success { color: var(--success); }
.text-warning { color: var(--warning); }
.text-danger { color: var(--danger); }
.text-muted { color: var(--text-muted); }
.font-bold { font-weight: 700; }
.text-sm { font-size: 12px; }
.text-lg { font-size: 18px; }
.text-xl { font-size: 24px; }

/* 间距 */
.m-0 { margin: 0; }
.m-1 { margin: 4px; }
.m-2 { margin: 8px; }
.m-3 { margin: 16px; }
.m-4 { margin: 24px; }
.mt-2 { margin-top: 8px; }
.mb-2 { margin-bottom: 8px; }
.ml-2 { margin-left: 8px; }
.mr-2 { margin-right: 8px; }

.p-0 { padding: 0; }
.p-1 { padding: 4px; }
.p-2 { padding: 8px; }
.p-3 { padding: 16px; }
.p-4 { padding: 24px; }

/* 圆角 */
.rounded { border-radius: 8px; }
.rounded-lg { border-radius: 16px; }
.rounded-full { border-radius: 9999px; }

/* 阴影 */
.shadow-sm { box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); }
.shadow { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
.shadow-lg { box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15); }

/* 显示 */
.hidden { display: none; }
.block { display: block; }
.inline-block { display: inline-block; }
.overflow-hidden { overflow: hidden; }
.overflow-auto { overflow: auto; }
```

---

## 8. HTML模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>应用标题</title>
    <style>
        /* CSS变量定义 */
        :root { /* ... */ }

        /* 基础样式 */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Microsoft YaHei', sans-serif; }

        /* 布局 */
        .container { max-width: 1200px; margin: 0 auto; padding: 0 16px; }

        /* 组件 */
        /* ... */
    </style>
</head>
<body>
    <div class="container">
        <!-- 页面内容 -->
    </div>
</body>
</html>
```

### 应用布局模板

```html
<div class="app-layout">
    <!-- 顶部导航 -->
    <header class="app-header">
        <div class="header-content">
            <h1 class="app-title">应用标题</h1>
            <nav class="header-nav">
                <!-- 导航项 -->
            </nav>
        </div>
    </header>

    <!-- 主内容区 -->
    <main class="app-main">
        <div class="content-wrapper">
            <!-- 侧边栏 -->
            <aside class="sidebar">
                <!-- 菜单 -->
            </aside>

            <!-- 内容区 -->
            <section class="content">
                <!-- 具体内容 -->
            </section>
        </div>
    </main>

    <!-- 底部 -->
    <footer class="app-footer">
        <!-- 页脚 -->
    </footer>
</div>
```

### 卡片布局模板

```html
<div class="cards-grid">
    <div class="card">
        <div class="card-header">
            <span class="card-icon">📊</span>
            <span class="card-title">标题</span>
        </div>
        <div class="card-body">
            <div class="card-value">1,234</div>
            <div class="card-trend up">↑ 15%</div>
        </div>
    </div>
    <!-- 更多卡片 -->
</div>
```
