# 动画效果库

## 过渡时长

| 场景 | 时长 | 示例 |
|------|------|------|
| 微交互 | 100-200ms | 按钮hover、checkbox |
| UI反馈 | 200-300ms | 下拉展开、模态框 |
| 页面过渡 | 300-500ms | 路由切换、tab切换 |
| 装饰动画 | 500-1000ms | 加载动画、强调效果 |

## 缓动函数

```css
/* 标准 */
ease: cubic-bezier(0.4, 0, 0.2, 1)

/* 进入 */
ease-in: cubic-bezier(0.4, 0, 1, 1)

/* 离开 */
ease-out: cubic-bezier(0, 0, 0.2, 1)

/* 强调 */
ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)

/* 弹性 */
spring: cubic-bezier(0.175, 0.885, 0.32, 1.275)
```

## 常用动画组合

### 按钮 Hover
```css
button {
  transform: translateY(0);
  transition: all 0.2s ease;
}
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

### 卡片 Hover
```css
.card {
  transform: translateY(0);
  transition: all 0.3s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}
```

### 淡入
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.fade-in {
  animation: fadeIn 0.5s ease forwards;
}
```

## 微交互设计

### 点击反馈
- 缩放：scale(0.95)
- 颜色变化：背景变深5%
- 时长：100ms

### 加载状态
- 旋转动画：360deg / 1s linear infinite
- 脉冲动画：opacity 0.5 → 1

### 滚动动画
使用 IntersectionObserver：
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
});
```
