# 常用组件模板

## 按钮

### 主要按钮
```html
<button class="btn btn-primary">
  主要操作
</button>
```
```css
.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-primary {
  background: #3B82F6;
  color: white;
  border: none;
}
.btn-primary:hover {
  background: #2563EB;
  transform: translateY(-1px);
}
```

### 次要按钮
```html
<button class="btn btn-secondary">
  次要操作
</button>
```
```css
.btn-secondary {
  background: transparent;
  color: #3B82F6;
  border: 2px solid #3B82F6;
}
```

### 禁用状态
```css
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

## 卡片

```html
<div class="card">
  <div class="card-image">
    <img src="..." alt="...">
  </div>
  <div class="card-content">
    <h3 class="card-title">标题</h3>
    <p class="card-text">描述文字</p>
  </div>
</div>
```
```css
.card {
  border-radius: 12px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}
```

## 表单

```html
<div class="form-group">
  <label class="form-label" for="email">邮箱</label>
  <input type="email" id="email" class="form-input" placeholder="请输入邮箱">
</div>
```
```css
.form-group {
  margin-bottom: 16px;
}
.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}
.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  transition: border-color 0.2s ease;
}
.form-input:focus {
  outline: none;
  border-color: #3B82F6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

## 导航栏

```html
<nav class="navbar">
  <div class="navbar-brand">Logo</div>
  <ul class="navbar-menu">
    <li><a href="#">首页</a></li>
    <li><a href="#">关于</a></li>
    <li><a href="#">联系</a></li>
  </ul>
</nav>
```
```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.navbar-menu {
  display: flex;
  gap: 24px;
  list-style: none;
}
.navbar-menu a {
  color: #4B5563;
  text-decoration: none;
  transition: color 0.2s ease;
}
.navbar-menu a:hover {
  color: #3B82F6;
}
```

## Hero 区域

```html
<section class="hero">
  <div class="hero-content">
    <h1 class="hero-title">大标题</h1>
    <p class="hero-subtitle">副标题描述</p>
    <div class="hero-actions">
      <button class="btn btn-primary">开始使用</button>
      <button class="btn btn-secondary">了解更多</button>
    </div>
  </div>
</section>
```
```css
.hero {
  padding: 80px 24px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 16px;
}
.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 32px;
}
.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}
```
