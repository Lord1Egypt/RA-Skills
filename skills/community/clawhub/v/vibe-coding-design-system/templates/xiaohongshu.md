# DESIGN.md - 小红书 (Xiaohongshu) Style

> 珊瑚红社交平台，瀑布流布局，年轻人的生活方式分享

---

## 1. Visual Theme & Atmosphere

**设计哲学**: 年轻、活力、真实、分享  
**氛围**: 活泼、友好、时尚、社交  
**密度**: 信息丰富但视觉舒适，瀑布流布局  
**设计语言**: 卡片式设计、瀑布流、社交驱动  
**目标用户**: 年轻用户、生活方式爱好者、内容创作者  
**品牌个性**: 真实、分享、时尚、活力

### 设计原则

1. **真实分享** - 鼓励真实内容，反对过度修饰
2. **视觉优先** - 图片/视频为王，文字辅助
3. **社交驱动** - 点赞、收藏、评论、分享

### 视觉隐喻

- **珊瑚红**: 活力、热情、年轻
- **瀑布流**: 发现、探索、无限浏览
- **圆角卡片**: 友好、温和、现代

---

## 2. Color Palette & Roles

### 主色调

| 名称 | Hex | RGB | 角色 |
|------|-----|-----|------|
| `xiaohongshu-red` | #FF2442 | rgb(255, 36, 66) | 品牌主色、按钮、点赞 |
| `xiaohongshu-bg` | #FFFFFF | rgb(255, 255, 255) | 背景色 |
| `xiaohongshu-text` | #333333 | rgb(51, 51, 51) | 主文本 |
| `xiaohongshu-secondary` | #666666 | rgb(102, 102, 102) | 次要文本 |

### 辅助色

| 名称 | Hex | 角色 |
|------|-----|------|
| `gray-100` | #F5F5F5 | 背景色、分割线 |
| `gray-200` | #EEEEEE | 边框、分割线 |
| `gray-300` | #CCCCCC | 禁用状态 |
| `gray-400` | #999999 | 占位符 |

### 语义色

| 名称 | Hex | 用途 |
|------|-----|------|
| `success` | #52C41A | 成功、已关注 |
| `warning` | #FAAD14 | 警告 |
| `error` | #FF2442 | 错误、删除 |
| `info` | #1890FF | 信息提示 |

### 中性色系（用于图标、边框等）

```css
/* 文本颜色 */
--text-primary: #333333;      /* 主要文本 */
--text-secondary: #666666;    /* 次要文本 */
--text-tertiary: #999999;     /* 辅助文本 */
--text-disabled: #CCCCCC;     /* 禁用文本 */

/* 背景颜色 */
--bg-primary: #FFFFFF;        /* 主背景 */
--bg-secondary: #F5F5F5;      /* 次背景 */
--bg-tertiary: #EEEEEE;       /* 三级背景 */

/* 边框颜色 */
--border-light: #F0F0F0;      /* 轻边框 */
--border-base: #E8E8E8;       /* 基础边框 */
--border-dark: #D9D9D9;       /* 深边框 */
```

### 无障碍访问

- **对比度**: 4.5:1 (AA) 文本对比度
- **色盲友好**: 是（已测试）
- **焦点指示器**: 红色轮廓

---

## 3. Typography Rules

### 字体家族

```css
/* 中文字体系统 */
--font-cn-heading: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
--font-cn-body: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
--font-cn-code: 'Source Code Pro', 'Consolas', monospace;

/* 英文字体系统 */
--font-en-heading: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
--font-en-body: 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif;

/* 数字字体 */
--font-number: 'DIN Alternate', 'SF Mono', monospace;
```

### 字体层级表

| 元素 | 字体 | 大小 | 字重 | 行高 | 字间距 |
|------|------|------|------|------|--------|
| `h1` | PingFang SC | 24px | 600 | 1.4 | 0 |
| `h2` | PingFang SC | 20px | 600 | 1.5 | 0 |
| `h3` | PingFang SC | 18px | 500 | 1.5 | 0 |
| `h4` | PingFang SC | 16px | 500 | 1.6 | 0 |
| `body-large` | PingFang SC | 16px | 400 | 1.8 | 0 |
| `body` | PingFang SC | 14px | 400 | 1.8 | 0 |
| `body-small` | PingFang SC | 13px | 400 | 1.7 | 0 |
| `caption` | PingFang SC | 12px | 400 | 1.6 | 0 |
| `number` | DIN Alternate | 14px | 500 | 1.6 | 0 |

### 中文字体使用规范

#### 标题

- **H1**: 笔记标题、页面主标题
- **H2**: 章节标题、卡片标题
- **H3**: 小节标题、对话框标题
- **H4**: 列表项标题、标签

#### 正文

- **Large**: 重要内容、首段
- **Regular**: 正文内容、列表、描述
- **Small**: 辅助说明、元数据
- **Caption**: 时间戳、标签、提示

### 中英文混排

```css
/* 中英文混排 */
.mixed-text {
  font-family: 'PingFang SC', 'SF Pro Text', sans-serif;
  line-height: 1.8;
  letter-spacing: 0; /* 中文无字间距 */
}

/* 纯英文 */
.english-text {
  font-family: 'SF Pro Text', -apple-system, sans-serif;
  line-height: 1.6;
  letter-spacing: -0.01em;
}

/* 数字强调 */
.number-highlight {
  font-family: 'DIN Alternate', 'SF Mono', monospace;
  font-weight: 500;
}
```

### 特殊排版

```css
/* 笔记标题 */
.note-title {
  font-size: 20px;
  font-weight: 600;
  line-height: 1.5;
  color: #333333;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 最多显示 2 行 */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 用户名 */
.username {
  font-size: 14px;
  font-weight: 500;
  color: #333333;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 点赞数、收藏数 */
.stat-number {
  font-family: 'DIN Alternate', sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: #999999;
}
```

---

## 4. Component Stylings

### 按钮

#### 主按钮

```css
.btn-primary {
  /* 基础样式 */
  background: #FF2442;
  color: #FFFFFF;
  padding: 8px 16px;
  border-radius: 20px; /* 药丸形状 */
  font-weight: 500;
  font-size: 14px;
  font-family: 'PingFang SC', sans-serif;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* 悬停状态 */
.btn-primary:hover {
  background: #E6203B;
  transform: scale(1.02);
}

/* 激活状态 */
.btn-primary:active {
  transform: scale(0.98);
}

/* 禁用状态 */
.btn-primary:disabled {
  background: #CCCCCC;
  cursor: not-allowed;
  transform: none;
}
```

#### 次要按钮

```css
.btn-secondary {
  background: transparent;
  color: #FF2442;
  border: 1px solid #FF2442;
  padding: 7px 15px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 14px;
  font-family: 'PingFang SC', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: rgba(255, 36, 66, 0.05);
}
```

#### 关注按钮

```css
.btn-follow {
  background: #FF2442;
  color: #FFFFFF;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-follow.following {
  background: #F5F5F5;
  color: #999999;
}

.btn-follow.following:hover {
  background: #EEEEEE;
}
```

### 输入框

#### 文本输入

```css
.input {
  /* 基础样式 */
  background: #FFFFFF;
  border: 1px solid #E8E8E8;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  font-family: 'PingFang SC', sans-serif;
  color: #333333;
  width: 100%;
  transition: all 0.2s ease;
}

/* 占位符 */
.input::placeholder {
  color: #CCCCCC;
}

/* 聚焦状态 */
.input:focus {
  outline: none;
  border-color: #FF2442;
  box-shadow: 0 0 0 2px rgba(255, 36, 66, 0.1);
}

/* 错误状态 */
.input.error {
  border-color: #FF2442;
}

/* 禁用状态 */
.input:disabled {
  background: #F5F5F5;
  color: #CCCCCC;
  cursor: not-allowed;
}
```

#### 搜索框

```css
.search-input {
  background: #F5F5F5;
  border: none;
  border-radius: 20px;
  padding: 8px 16px 8px 36px;
  font-size: 14px;
  color: #333333;
  width: 100%;
  transition: all 0.2s ease;
}

.search-input:focus {
  background: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
```

### 卡片

#### 笔记卡片（瀑布流）

```css
.note-card {
  background: #FFFFFF;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}

.note-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 封面图 */
.note-cover {
  width: 100%;
  aspect-ratio: auto;
  background: #F5F5F5;
  display: block;
}

/* 卡片内容 */
.note-content {
  padding: 10px;
}

/* 标题 */
.note-title {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  color: #333333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 8px;
}

/* 作者信息 */
.note-author {
  display: flex;
  align-items: center;
  gap: 6px;
}

.author-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  object-fit: cover;
}

.author-name {
  font-size: 12px;
  color: #999999;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.note-likes {
  font-size: 12px;
  color: #999999;
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 4px;
}
```

#### 用户卡片

```css
.user-card {
  background: #FFFFFF;
  border: 1px solid #E8E8E8;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.2s ease;
}

.user-card:hover {
  border-color: #D9D9D9;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 16px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 4px;
}

.user-bio {
  font-size: 12px;
  color: #999999;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

### 导航

#### 顶部导航

```css
.header {
  background: #FFFFFF;
  border-bottom: 1px solid #F0F0F0;
  padding: 12px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-tabs {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-tab {
  font-size: 16px;
  font-weight: 500;
  color: #666666;
  cursor: pointer;
  transition: color 0.2s ease;
  position: relative;
}

.nav-tab.active {
  color: #FF2442;
}

.nav-tab.active::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 0;
  right: 0;
  height: 2px;
  background: #FF2442;
}
```

#### 底部导航（移动端）

```css
.bottom-nav {
  background: #FFFFFF;
  border-top: 1px solid #F0F0F0;
  padding: 8px 0;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  justify-content: space-around;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 4px 16px;
}

.nav-icon {
  width: 24px;
  height: 24px;
  color: #999999;
}

.nav-item.active .nav-icon {
  color: #FF2442;
}

.nav-label {
  font-size: 10px;
  color: #999999;
}

.nav-item.active .nav-label {
  color: #FF2442;
}
```

---

## 5. Layout Principles

### 间距系统

| 名称 | 值 | 用途 |
|------|-----|------|
| `xs` | 4px | 图标间距、紧密间距 |
| `sm` | 8px | 小间距、列表项 |
| `md` | 12px | 卡片内边距、默认间距 |
| `lg` | 16px | 卡片内边距、大间距 |
| `xl` | 24px | 章节间距 |
| `2xl` | 32px | 页面章节 |

### 网格系统

- **列数**: 12
- **间距**: 16px
- **最大宽度**: 1200px
- **容器边距**: 24px

### 瀑布流布局

```css
/* 瀑布流容器 */
.waterfall-container {
  column-count: 2; /* 默认 2 列 */
  column-gap: 8px;
}

/* 响应式 */
@media (min-width: 768px) {
  .waterfall-container {
    column-count: 3;
    column-gap: 12px;
  }
}

@media (min-width: 1024px) {
  .waterfall-container {
    column-count: 4;
    column-gap: 16px;
  }
}

/* 瀑布流项目 */
.waterfall-item {
  break-inside: avoid;
  margin-bottom: 8px;
}
```

### 断点定义

```css
--breakpoint-xs: 0px;      /* 超小屏 */
--breakpoint-sm: 576px;    /* 小屏手机 */
--breakpoint-md: 768px;    /* 平板 */
--breakpoint-lg: 992px;    /* 小桌面 */
--breakpoint-xl: 1200px;   /* 大桌面 */
```

### 留白哲学

- **适度留白**: 不过密不过疏，视觉舒适
- **内容优先**: 内容区域留白更多
- **呼吸感**: 卡片间保持适当间距
- **层次感**: 通过留白区分内容层级

---

## 6. Depth & Elevation

### 阴影系统

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
--shadow-xl: 0 8px 24px rgba(0, 0, 0, 0.16);
```

### 层级系统

| 名称 | 值 | 用途 |
|------|-----|------|
| `base` | 0 | 默认层级 |
| `dropdown` | 10 | 下拉菜单 |
| `sticky` | 20 | 固定导航 |
| `modal` | 30 | 弹窗 |
| `toast` | 40 | 提示消息 |

### 层级原则

- **轻量阴影**: 卡片使用轻阴影，不过重
- **悬停增强**: 悬停时阴影增强
- **层级分明**: 弹窗、导航层级清晰
- **视觉反馈**: 通过阴影提供交互反馈

---

## 7. Do's and Don'ts

### ✅ 正确做法

- 使用中文字体系统（PingFang SC）
- 中文行高保持 1.8 左右
- 中文无字间距
- 使用药丸形状按钮（border-radius: 20px）
- 保持卡片圆角 8px
- 使用珊瑚红作为主色
- 图片优先，文字辅助
- 实现瀑布流布局
- 保持视觉年轻活力

### ❌ 错误做法

- 使用过小的中文行高（<1.6）
- 中文添加字间距
- 使用硬边角（使用圆角）
- 过度使用阴影
- 信息过载
- 忽视移动端体验
- 使用冷色调（保持温暖）
- 文字过多，图片过少
- 布局过于规整（瀑布流更自然）

### 中文排版注意事项

1. **行高**: 中文行高应比英文高（1.8 vs 1.5）
2. **字间距**: 中文不添加字间距
3. **段间距**: 段落间保持 16px 间距
4. **标点**: 使用中文全角标点
5. **首行缩进**: 正文首行缩进 2 字符
6. **数字**: 使用 DIN 或等宽字体突出显示

---

## 8. Responsive Behavior

### 断点系统

| 名称 | 最小宽度 | 最大宽度 | 目标设备 |
|------|----------|----------|----------|
| `xs` | 0px | 575px | 小屏手机 |
| `sm` | 576px | 767px | 大屏手机 |
| `md` | 768px | 991px | 平板 |
| `lg` | 992px | 1199px | 小桌面 |
| `xl` | 1200px | ∞ | 大桌面 |

### 触摸目标

- **最小尺寸**: 44px × 44px
- **间距**: 8px
- **按钮高度**: 移动端至少 36px

### 瀑布流响应式

```css
/* 手机: 2 列 */
.waterfall { column-count: 2; }

/* 平板: 3 列 */
@media (min-width: 768px) {
  .waterfall { column-count: 3; }
}

/* 桌面: 4 列 */
@media (min-width: 992px) {
  .waterfall { column-count: 4; }
}

/* 大桌面: 5 列 */
@media (min-width: 1200px) {
  .waterfall { column-count: 5; }
}
```

### 折叠策略

- **移动端优先**: 底部导航 + 简化内容
- **平板**: 侧边导航 + 3 列瀑布流
- **桌面**: 顶部导航 + 4-5 列瀑布流
- **大屏**: 最大化利用空间

---

## 9. Agent Prompt Guide

### 快速参考

```css
/* 颜色 */
--color-primary: #FF2442;
--color-background: #FFFFFF;
--color-text: #333333;
--color-secondary: #666666;

/* 字体 */
--font-cn: 'PingFang SC', sans-serif;
--font-number: 'DIN Alternate', monospace;

/* 间距 */
--spacing-base: 8px;
--border-radius: 8px;
--border-radius-pill: 20px;

/* 阴影 */
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
```

### 常用提示词

**创建中文页面**:
```
创建一个[页面名称]页面，使用小红书设计风格：
- 珊瑚红主色 #FF2442
- PingFang SC 字体，行高 1.8
- 药丸形状按钮（border-radius: 20px）
- 瀑布流布局
- 年轻活力的风格
```

**创建组件**:
```
创建一个[组件名称]组件，遵循小红书设计规范：
- 背景色: #FFFFFF
- 边框: 1px solid #E8E8E8
- 圆角: 8px
- 悬停: box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08)
- 中文字体: PingFang SC
```

### 代码模板

#### React 组件（中文）

```tsx
import React from 'react';
import styles from './NoteCard.module.css';

interface NoteCardProps {
  title: string;
  cover: string;
  author: {
    avatar: string;
    name: string;
  };
  likes: number;
}

export function NoteCard({ title, cover, author, likes }: NoteCardProps) {
  return (
    <div className={styles.card}>
      <img src={cover} alt={title} className={styles.cover} />
      <div className={styles.content}>
        <h3 className={styles.title}>{title}</h3>
        <div className={styles.footer}>
          <img src={author.avatar} alt={author.name} className={styles.avatar} />
          <span className={styles.authorName}>{author.name}</span>
          <span className={styles.likes}>{likes}</span>
        </div>
      </div>
    </div>
  );
}
```

#### CSS Module（中文）

```css
.card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.cover {
  width: 100%;
  display: block;
}

.content {
  padding: 10px;
}

.title {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  color: #333333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 8px;
}

.footer {
  display: flex;
  align-items: center;
  gap: 6px;
}

.avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.authorName {
  font-size: 12px;
  color: #999999;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.likes {
  font-size: 12px;
  color: #999999;
}
```

### AI Agent 指令

生成基于此 DESIGN.md 的 UI 代码时：

1. **始终使用中文字体系统** - PingFang SC、微软雅黑
2. **中文行高 1.8** - 比英文更高
3. **中文无字间距** - letter-spacing: 0
4. **使用珊瑚红主色** - #FF2442
5. **实现所有状态** - hover、active、disabled
6. **响应式设计** - 检查所有断点
7. **瀑布流布局** - 使用 CSS columns
8. **图片优先** - 图片 > 文字
9. **药丸按钮** - border-radius: 20px
10. **年轻活力** - 保持视觉活力

### 组件生成清单

生成组件前，检查：

- [ ] 使用中文字体系统
- [ ] 中文行高 1.8
- [ ] 无字间距
- [ ] 使用珊瑚红主色
- [ ] 实现所有交互状态
- [ ] 响应式设计
- [ ] 无障碍访问（对比度）
- [ ] 图片优先设计
- [ ] 瀑布流布局（如适用）
- [ ] 年轻活力风格

---

**小红书设计系统 v2.0.0**  
**最后更新**: 2026-04-09  
**支持语言**: 中文  
**许可证**: MIT
