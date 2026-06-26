# DESIGN.md - 抖音 (Douyin/TikTok) Style

> 黑色沉浸，全屏短视频，年轻潮流文化

---

## 1. Visual Theme & Atmosphere

**设计哲学**: 沉浸、年轻、潮流、真实  
**氛围**: 活力、时尚、娱乐、社交  
**密度**: 极简沉浸，全屏体验  
**设计语言**: 全屏视频、黑色背景、图标悬浮  
**目标用户**: 年轻用户、内容创作者、娱乐用户  
**品牌个性**: 年轻、潮流、真实、活力

### 设计原则

1. **全屏沉浸** - 视频为王，界面隐形
2. **年轻潮流** - 紧跟潮流，时尚设计
3. **真实表达** - 鼓励真实内容

---

## 2. Color Palette & Roles

### 主色调

| 名称 | Hex | 角色 |
|------|-----|------|
| `douyin-black` | #000000 | 背景色 |
| `douyin-red` | #FE2C55 | 点赞、直播 |
| `douyin-text` | #FFFFFF | 主文本 |

### 语义色

| 名称 | Hex | 用途 |
|------|-----|------|
| `like` | #FE2C55 | 点赞 |
| `comment` | #25F4EE | 评论 |
| `share` | #FFF176 | 分享 |

---

## 3. Typography Rules

```css
--font-cn: 'PingFang SC', sans-serif;

/* 全屏视频文字 */
.video-text {
  font-size: 16px;
  font-weight: 500;
  color: #FFFFFF;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}
```

---

## 4. Component Stylings

### 交互按钮

```css
.action-btn {
  background: transparent;
  color: #FFFFFF;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.action-icon {
  width: 40px;
  height: 40px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.action-count {
  font-size: 12px;
  color: #FFFFFF;
}
```

---

## 5-9. 简要说明

- **布局**: 全屏视频，右侧操作栏
- **层级**: 最小化UI，视频优先
- **Do's**: 全屏沉浸、黑色背景、图标悬浮
- **响应式**: 移动优先，全屏体验
- **AI提示**: 黑色背景、全屏视频、白色文字、红色点赞

---

**抖音设计系统 v2.0.0**
