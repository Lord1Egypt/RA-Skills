# UI Design Patterns Reference

从 Uiverse Galaxy 组件库中提炼的设计模式，供 AI 智能体学习并应用到实际页面设计中。

## 目录

1. [仪表盘设计模式](#仪表盘设计模式)
2. [监控面板设计模式](#监控面板设计模式)
3. [管理后台设计模式](#管理后台设计模式)
4. [组件组合模式](#组件组合模式)

---

## 仪表盘设计模式

### 卡片网格布局

仪表盘核心是卡片网格。从 Cards/ 和 Buttons/ 中学习：

```
┌─────────────────────────────────────────────┐
│  Header Bar (logo + nav + user avatar)      │
├───────┬───────┬───────┬───────┬─────────────┤
│ KPI 1 │ KPI 2 │ KPI 3 │ KPI 4 │  (Cards)    │
├───────┴───────┼───────┴───────┼─────────────┤
│  Chart Area   │  Chart Area   │  (Patterns) │
├───────────────┼───────────────┼─────────────┤
│  Table/Feed   │  Quick Actions│  (Buttons)  │
└───────────────┴───────────────┴─────────────┘
```

**学习路径：**
1. 浏览 `Cards/` 中的 `card` 标签组件 → 学习卡片样式
2. 浏览 `loaders/` 中的 `loading` 组件 → 学习数据加载态
3. 浏览 `Buttons/` 中的 `animated` 组件 → 学习操作按钮

**关键设计要素：**
```css
/* 卡片基础样式 */
.dashboard-card {
  background: rgba(255, 255, 255, 0.05); /* 半透明背景 */
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px); /* 毛玻璃效果 */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
```

### KPI 数字展示

从 Cards/ 中的数字类组件学习：

```css
.kpi-value {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.kpi-trend {
  font-size: 0.875rem;
  color: #10b981; /* green for up */
}
```

---

## 监控面板设计模式

### 暗色主题基础

监控面板通常使用暗色主题。从 `Patterns/` 和 `Cards/` 的 `dark` 标签组件学习：

```css
/* 暗色主题变量 */
:root {
  --bg-primary: #0f172a;     /* 深蓝黑 */
  --bg-secondary: #1e293b;   /* 卡片背景 */
  --bg-tertiary: #334155;    /* 输入框/按钮 */
  --text-primary: #f1f5f9;   /* 主文字 */
  --text-secondary: #94a3b8; /* 次要文字 */
  --accent-green: #10b981;   /* 正常/在线 */
  --accent-red: #ef4444;     /* 告警/离线 */
  --accent-yellow: #f59e0b;  /* 警告 */
  --accent-blue: #3b82f6;    /* 信息/链接 */
}
```

### 状态指示器

从 Notifications/ 和 Toggle-switches/ 学习状态展示：

```css
/* 状态点 */
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  animation: pulse 2s infinite;
}
.status-dot.online  { background: #10b981; }
.status-dot.warning { background: #f59e0b; }
.status-dot.error   { background: #ef4444; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

### 数据加载与骨架屏

从 `loaders/` 学习加载动画：

```css
/* 骨架屏 */
.skeleton {
  background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

---

## 管理后台设计模式

### 表格样式

从 Forms/ 和 Inputs/ 学习表单/表格设计：

```css
.data-table {
  width: 100%;
  border-collapse: collapse;
  background: #1e293b;
  border-radius: 12px;
  overflow: hidden;
}
.data-table th {
  background: #334155;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}
.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #334155;
}
.data-table tr:hover {
  background: rgba(59, 130, 246, 0.05);
}
```

### 操作按钮组

从 Buttons/ 学习按钮设计：

```css
/* 主按钮 */
.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

/* 次要按钮 */
.btn-secondary {
  background: transparent;
  color: #94a3b8;
  padding: 10px 20px;
  border-radius: 8px;
  border: 1px solid #334155;
  transition: all 0.2s;
}
.btn-secondary:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}
```

---

## 组件组合模式

### 搜索栏 = Input + Button + Tooltip

```
┌──────────────────────────────────┬──────┐
│ 🔍 搜索...                      │ 搜索 │
└──────────────────────────────────┴──────┘
```

**学习路径：** `Inputs/` (search标签) + `Buttons/` (button标签)

### 用户卡片 = Card + Avatar + Button + Tooltip

```
┌─────────────────────────────┐
│  👤  用户名                  │
│      @handle                │
│                             │
│  [关注]  [私信]             │
└─────────────────────────────┘
```

**学习路径：** `Cards/` (card标签) + `Buttons/` (button标签) + `Tooltips/`

### 设置项 = Toggle-switch + Description

```
┌─────────────────────────────────────────┐
│  深色模式                       [●──]   │
│  切换界面主题为深色                       │
└─────────────────────────────────────────┘
```

**学习路径：** `Toggle-switches/` (switch标签)

### 通知卡片 = Notification + Button + Animation

```
┌─────────────────────────────────────────┐
│  ✅ 操作成功                    [关闭]   │
│  您的更改已保存                           │
└─────────────────────────────────────────┘
```

**学习路径：** `Notifications/` (notification标签) + `Buttons/`

---

## 色彩方案速查

### 深色系（监控/仪表盘）
```css
--bg: #0f172a; --card: #1e293b; --border: #334155;
--text: #f1f5f9; --muted: #94a3b8;
```

### 浅色系（管理后台）
```css
--bg: #f8fafc; --card: #ffffff; --border: #e2e8f0;
--text: #0f172a; --muted: #64748b;
```

### 渐变配色（Landing/产品页）
```css
--gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
--gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
```
