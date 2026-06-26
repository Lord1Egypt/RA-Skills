# DESIGN.md - 微博 (Weibo) Style

> 橙红活力，社交媒体，热点传播平台

---

## 1. Visual Theme & Atmosphere

**设计哲学**: 开放、热点、社交、传播  
**氛围**: 活力、热点、开放、社交  
**密度**: 信息流式，热点突出  
**设计语言**: 信息流、话题标签、热点卡片  
**目标用户**: 全年龄段、热点关注者、内容创作者  
**品牌个性**: 开放、活力、热点、社交

---

## 2. Color Palette & Roles

### 主色调

| 名称 | Hex | RGB | 角色 |
|------|-----|-----|------|
| `weibo-orange` | #FF8200 | rgb(255, 130, 0) | 品牌主色、热点 |
| `weibo-red` | #E6162D | rgb(230, 22, 45) | 点赞、推荐 |
| `weibo-text` | #333333 | rgb(51, 51, 51) | 主文本 |
| `weibo-bg` | #F7F9FA | rgb(247, 249, 250) | 背景色 |

### 辅助色

| 名称 | Hex | 角色 |
|------|-----|------|
| `orange-light` | #FFF4E5 | 热点背景 |
| `gray-100` | #F2F2F2 | 卡片背景 |
| `gray-300` | #999999 | 次要文本 |

### 语义色

| 名称 | Hex | 用途 |
|------|-----|------|
| `like` | #E6162D | 点赞 |
| `comment` | #FF8200 | 评论 |
| `repost` | #5BAF4F | 转发 |

---

## 3. Typography Rules

### 字体家族

```css
--font-cn: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
--font-number: 'DIN Alternate', sans-serif;
```

### 字体层级表

| 元素 | 大小 | 字重 | 行高 | 用途 |
|------|------|------|------|------|
| `h1` | 20px | 600 | 1.4 | 用户名、话题标题 |
| `h2` | 18px | 600 | 1.5 | 热点标题 |
| `h3` | 16px | 500 | 1.5 | 卡片标题 |
| `body` | 15px | 400 | 1.8 | 正文内容 |
| `body-small` | 13px | 400 | 1.7 | 辅助信息 |
| `caption` | 12px | 400 | 1.6 | 时间戳、标签 |
| `number` | 12px | 500 | 1.4 | 点赞数、评论数 |

---

## 4. Component Stylings

### 按钮

```css
.btn-primary {
  background: linear-gradient(135deg, #FF8200 0%, #FF6600 100%);
  color: #FFFFFF;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 130, 0, 0.3);
}

.btn-secondary {
  background: transparent;
  color: #FF8200;
  border: 1px solid #FF8200;
  padding: 7px 19px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #FFF4E5;
}

.btn-text {
  background: transparent;
  color: #FF8200;
  padding: 8px 12px;
  font-size: 14px;
  border: none;
  cursor: pointer;
}

.btn-text:hover {
  background: #FFF4E5;
  border-radius: 4px;
}
```

### 输入框

```css
.input {
  background: #FFFFFF;
  border: 1px solid #E5E5E5;
  border-radius: 4px;
  padding: 10px 14px;
  font-size: 15px;
  color: #333333;
  width: 100%;
  transition: all 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: #FF8200;
  box-shadow: 0 0 0 2px rgba(255, 130, 0, 0.1);
}

.input::placeholder {
  color: #999999;
}
```

### 卡片

```css
.weibo-card {
  background: #FFFFFF;
  border-bottom: 1px solid #F2F2F2;
  padding: 16px;
  transition: background 0.2s ease;
}

.weibo-card:hover {
  background: #FAFAFA;
}

/* 热点卡片 */
.hot-card {
  background: linear-gradient(135deg, #FFF4E5 0%, #FFE5CC 100%);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #FFD4B3;
}

.hot-card:hover {
  box-shadow: 0 4px 12px rgba(255, 130, 0, 0.15);
}

/* 用户信息 */
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
}

.user-meta {
  font-size: 12px;
  color: #999999;
}

/* 微博内容 */
.weibo-content {
  font-size: 15px;
  line-height: 1.8;
  color: #333333;
  margin-bottom: 12px;
}

/* 互动栏 */
.interaction-bar {
  display: flex;
  justify-content: space-around;
  padding-top: 12px;
  border-top: 1px solid #F2F2F2;
}

.interaction-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #999999;
  cursor: pointer;
  transition: color 0.2s ease;
}

.interaction-item:hover {
  color: #FF8200;
}

.interaction-item.active {
  color: #E6162D;
}
```

### 话题标签

```css
.topic-tag {
  display: inline-block;
  background: #FFF4E5;
  color: #FF8200;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.topic-tag:hover {
  background: #FFE5CC;
}

.topic-tag.hot {
  background: linear-gradient(135deg, #FF8200 0%, #FF6600 100%);
  color: #FFFFFF;
}
```

---

## 5. Layout Principles

### 间距系统

| 名称 | 值 | 用途 |
|------|-----|------|
| `xs` | 4px | 图标间距、紧密间距 |
| `sm` | 8px | 小间距、按钮内边距 |
| `md` | 16px | 卡片内边距、默认间距 |
| `lg` | 24px | 章节间距 |
| `xl` | 32px | 页面章节 |

### 网格系统

- **最大宽度**: 960px（内容区域）
- **侧边栏**: 240px
- **间距**: 16px

### 布局模式

- **信息流**: 垂直列表，卡片堆叠
- **三栏布局**: 侧边栏 + 内容 + 推荐
- **热点布局**: 热点列表 + 热度指数

---

## 6. Depth & Elevation

### 阴影系统

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
--shadow-orange: 0 4px 12px rgba(255, 130, 0, 0.2);
```

### z-index层级

| 名称 | 值 | 用途 |
|------|-----|------|
| `base` | 0 | 默认层级 |
| `dropdown` | 10 | 下拉菜单 |
| `sticky` | 20 | 固定导航 |
| `modal` | 30 | 弹窗 |
| `toast` | 40 | 提示消息 |

---

## 7. Do's and Don'ts

### ✅ 正确做法

- 使用橙红主色 #FF8200
- 保持信息流清晰
- 热点内容突出显示
- 使用话题标签
- 中文行高 1.8
- 实现互动效果
- 保持开放社交氛围
- 使用圆角 20px 按钮

### ❌ 错误做法

- 过度装饰界面
- 忽视热点突出
- 使用过多颜色
- 信息流过于拥挤
- 缺少互动反馈
- 忽视移动端体验
- 使用硬边角（使用圆角）
- 文字排版混乱

### 中文排版注意事项

1. **行高**: 正文保持 1.8
2. **话题标签**: 使用 #话题# 格式
3. **@提及**: 使用蓝色链接色
4. **表情**: 支持微博表情
5. **字数限制**: 提示剩余字数
6. **链接**: 自动识别并高亮

---

## 8. Responsive Behavior

### 断点系统

| 名称 | 最小宽度 | 最大宽度 | 目标设备 |
|------|----------|----------|----------|
| `mobile` | 0px | 767px | 手机 |
| `tablet` | 768px | 991px | 平板 |
| `desktop` | 992px | ∞ | 桌面 |

### 响应式策略

```css
/* 移动端: 单栏信息流 */
@media (max-width: 767px) {
  .sidebar { display: none; }
  .content { width: 100%; }
}

/* 桌面: 三栏布局 */
@media (min-width: 992px) {
  .layout { display: grid; grid-template-columns: 240px 1fr 240px; }
}
```

### 触摸目标

- **最小尺寸**: 44px × 44px
- **间距**: 8px

---

## 9. Agent Prompt Guide

### 快速参考

```css
/* 颜色 */
--color-primary: #FF8200;
--color-background: #F7F9FA;
--color-text: #333333;
--color-hot: #E6162D;

/* 字体 */
--font-cn: 'PingFang SC', sans-serif;
--font-number: 'DIN Alternate', monospace;

/* 间距 */
--spacing-base: 8px;
--border-radius: 20px; /* 药丸按钮 */

/* 阴影 */
--shadow-orange: 0 4px 12px rgba(255, 130, 0, 0.2);
```

### 常用提示词

**创建微博信息流**:
```
创建一个微博风格的信息流页面：
- 橙红主色 #FF8200
- 信息流卡片布局
- 话题标签 #话题#
- 互动栏（点赞、评论、转发）
- 中文 PingFang SC 字体，行高 1.8
```

**创建热点卡片**:
```
创建一个热点卡片组件：
- 渐变背景 #FFF4E5 到 #FFE5CC
- 橙红边框 #FFD4B3
- 热度指数显示
- 话题标签
```

### 代码模板

#### React 组件（微博卡片）

```tsx
import React from 'react';
import styles from './WeiboCard.module.css';

interface WeiboCardProps {
  user: {
    avatar: string;
    name: string;
    verified?: boolean;
  };
  content: string;
  images?: string[];
  stats: {
    likes: number;
    comments: number;
    reposts: number;
  };
  timestamp: string;
}

export function WeiboCard({ user, content, images, stats, timestamp }: WeiboCardProps) {
  return (
    <div className={styles.card}>
      <div className={styles.userInfo}>
        <img src={user.avatar} alt={user.name} className={styles.avatar} />
        <div className={styles.userMeta}>
          <span className={styles.userName}>{user.name}</span>
          <span className={styles.timestamp}>{timestamp}</span>
        </div>
      </div>
      <div className={styles.content}>{content}</div>
      {images && images.length > 0 && (
        <div className={styles.images}>
          {images.map((img, idx) => (
            <img key={idx} src={img} alt="" className={styles.image} />
          ))}
        </div>
      )}
      <div className={styles.interactionBar}>
        <button className={styles.interactionItem}>
          <span>👍</span>
          <span>{stats.likes}</span>
        </button>
        <button className={styles.interactionItem}>
          <span>💬</span>
          <span>{stats.comments}</span>
        </button>
        <button className={styles.interactionItem}>
          <span>🔄</span>
          <span>{stats.reposts}</span>
        </button>
      </div>
    </div>
  );
}
```

#### CSS Module

```css
.card {
  background: white;
  border-bottom: 1px solid #F2F2F2;
  padding: 16px;
  transition: background 0.2s ease;
}

.card:hover {
  background: #FAFAFA;
}

.userInfo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.userMeta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.userName {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
}

.timestamp {
  font-size: 12px;
  color: #999999;
}

.content {
  font-size: 15px;
  line-height: 1.8;
  color: #333333;
  margin-bottom: 12px;
}

.images {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}

.image {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 8px;
}

.interactionBar {
  display: flex;
  justify-content: space-around;
  padding-top: 12px;
  border-top: 1px solid #F2F2F2;
}

.interactionItem {
  display: flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: none;
  color: #999999;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.interactionItem:hover {
  color: #FF8200;
  background: #FFF4E5;
}
```

### AI Agent 指令

生成基于此 DESIGN.md 的 UI 代码时：

1. **使用橙红主色** - #FF8200
2. **中文 PingFang SC 字体** - 行高 1.8
3. **信息流布局** - 垂直卡片堆叠
4. **药丸按钮** - border-radius: 20px
5. **热点突出** - 使用渐变背景
6. **话题标签** - #话题# 格式
7. **互动反馈** - 点赞、评论、转发
8. **响应式设计** - 移动优先
9. **保持开放** - 社交氛围
10. **简化界面** - 不过度装饰

### 组件生成清单

生成组件前，检查：

- [ ] 使用橙红主色 #FF8200
- [ ] 中文字体 PingFang SC
- [ ] 行高 1.8
- [ ] 信息流布局
- [ ] 实现互动效果
- [ ] 响应式设计
- [ ] 话题标签支持
- [ ] 热点突出显示
- [ ] 圆角 20px 按钮
- [ ] 开放社交氛围

---

**微博设计系统 v2.0.0**  
**最后更新**: 2026-04-09  
**支持语言**: 中文  
**许可证**: MIT
