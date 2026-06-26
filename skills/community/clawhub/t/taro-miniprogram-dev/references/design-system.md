# 设计系统

## 品牌色

| 变量 | 色值 | 用途 |
|------|------|------|
| `$bg` | `#fff8f1` | 页面背景 |
| `$paper` | `#ffffffcc` | 卡片背景 |
| `$ink` | `#5e3930` | 主文字 |
| `$muted` | `#8f6d64` | 次要文字 |
| `$pink` | `#f7b8c8` | 按钮渐变起点 |
| `$pink-deep` | `#ec89a7` | 按钮渐变终点 |
| `$brown` | `#eab79f` | 强调色 |
| `$line` | `#f5e1d8` | 分割线 |

## 页面背景

```scss
background: linear-gradient(180deg, #fffdfa 0%, #fff5ec 100%);
```

## 组件样式

### 卡片

```scss
.card {
  background: $paper;
  border: 2px solid #fff;
  box-shadow: 0 14px 30px rgba(109, 74, 63, 0.08);
  border-radius: 24px;
  padding: 16px;
  margin-bottom: 14px;
}
```

### 主按钮

```scss
.btn-primary {
  width: 100%;
  height: 48px;
  border-radius: 18px;
  border: 0;
  background: linear-gradient(135deg, $pink, $pink-deep);
  color: #fff;
  font-size: 15px;
  font-weight: 900;
  box-shadow: 0 14px 26px rgba(236, 137, 167, 0.24);
  line-height: 48px;
}
```

### 次要按钮

```scss
.btn-ghost {
  width: 100%;
  height: 48px;
  border-radius: 18px;
  border: 2px solid #f5ddd4;
  background: #fff;
  color: #916761;
  font-size: 15px;
  font-weight: 900;
  line-height: 44px;
}
```

### 胶囊标签

```scss
.pill {
  padding: 8px 12px;
  border-radius: 999px;
  background: #fff3ec;
  border: 2px solid #f7ddd4;
  font-size: 12px;
  font-weight: 700;
  color: #9e6d61;
}
```

### 底部导航

```scss
.bottom-nav {
  position: fixed;
  left: 14px;
  right: 14px;
  bottom: 14px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 10px;
  border-radius: 22px;
  background: #fffdf8;
  border: 2px solid #fff;
  box-shadow: 0 14px 30px rgba(109, 74, 63, 0.08);
  z-index: 100;

  .nav-item {
    font-size: 11px;
    text-align: center;
    padding: 6px 0;
    border-radius: 14px;
    color: #9a7b71;
    &.active {
      background: #fff1f4;
      color: #d96b8a;
      font-weight: 900;
    }
  }
}
```

## 字体规范

- 标题：22px, font-weight: 900
- 副标题/名称：16px, font-weight: 900
- 正文：14px, font-weight: 400
- 辅助文字：12px, font-weight: 700
- 状态栏文字：12px

## 圆角规范

| 元素 | 圆角 |
|------|------|
| 页面主卡片 | 28px |
| 通用卡片 | 24px |
| 按钮 | 18px |
| 输入框 | 14px |
| 胶囊标签 | 999px（圆形）|
| 底部导航 | 22px |

## 安全区

```scss
.safe-bottom {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}
```

页面底部需预留 120px（底部导航高度 + 固定定位偏移）。
