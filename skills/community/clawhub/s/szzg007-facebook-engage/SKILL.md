---
name: szzg007-facebook-engage
description: Facebook 自动关注与留言技能。访问指定 Facebook 主页，点击关注，并在最新帖子下留言。用于社交媒体互动、粉丝 engagement、品牌互动等场景。
---

# szzg007-facebook-engage - Facebook 自动关注与留言

## 技能描述
自动访问 Facebook 用户/公共主页，完成关注操作，并在最新帖子下留下友好评论。

## 触发条件
- 用户要求关注某个 Facebook 账号并留言
- 需要进行社交媒体互动/engagement
- 品牌/产品需要在目标账号下建立存在感

## 输入参数
| 参数 | 必填 | 说明 |
|------|------|------|
| facebookUrl | 是 | Facebook 主页 URL，如 https://www.facebook.com/tayediggs |
| commentText | 否 | 留言内容（如不提供则自动生成友好评论） |
| profile | 否 | 浏览器配置，默认 chrome-relay |

## 执行步骤

### 1. 打开 Facebook 主页
```
browser open → facebookUrl
```

### 2. 等待页面加载
```
browser act wait → 10-15 秒
```

### 3. 获取页面快照，找到关注按钮
```
browser snapshot → 查找"关注"按钮的 ref
```

### 4. 点击关注按钮
```
browser act click → 关注按钮 ref
```

### 5. 滚动页面找到最新帖子
```
browser act evaluate → window.scrollBy(0, 500)
browser act wait → 3 秒
```

### 6. 获取帖子区域快照，找到评论框
```
browser snapshot → 查找评论输入框 ref
```

### 7. 输入留言内容
```
browser act type → 评论框 ref + commentText
```

### 8. 点击发布评论
```
browser act click → 发布按钮 ref
```

### 9. 确认提交成功
```
browser act wait → 等待"评论已提交"提示
```

## 留言内容建议

### 通用友好型
- "Love this! Keep up the great work! 🌟"
- "Such an inspiring post! Thanks for sharing!"
- "This made my day! 💫"

### 支持鼓励型
- "Your work has inspired so many people. Keep shining!"
- "Love this positive message! You're amazing!"
- "Always love your content! Never stop creating!"

### 互动提问型
- "Great post! What's next for you?"
- "Love this! Any tips for fans who want to follow in your footsteps?"

## 注意事项

### ⚠️ 避免封禁
1. **不要频繁刷新页面** - 每次操作间隔至少 3-5 秒
2. **不要短时间内大量操作** - 建议每小时不超过 10 次关注/留言
3. **留言内容要自然** - 避免重复相同内容，每条留言要有差异化
4. **像真人一样操作** - 滚动页面、等待加载、自然浏览

### ⚠️ 技术注意
1. **浏览器连接** - 确保 chrome-relay 扩展正常运行
2. **页面加载** - 等待足够时间让页面完全加载
3. **元素定位** - 使用 aria-ref 定位，如找不到需重新 snapshot
4. **网络问题** - 如遇 ERR_NETWORK_CHANGED，暂停后重试

### ⚠️ 内容安全
1. **留言要正面积极** - 避免争议性内容
2. **符合平台规范** - 不发布垃圾信息
3. **尊重对方** - 留言要真诚友好

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| tab not found | 标签页已关闭 | 重新 open 新标签页 |
| TimeoutError | 元素未加载 | 增加 wait 时间或重新 snapshot |
| ERR_NETWORK_CHANGED | 网络波动 | 暂停 5 秒后重试 |
| 关注按钮找不到 | 已关注或页面结构变化 | 检查页面状态 |

## 成功标志
- 关注按钮变为"已关注"或"Following"
- 评论显示在帖子下方
- 系统提示"你的评论已提交"

## 示例调用

```
任务：关注 Taye Diggs 并留言
参数：
  - facebookUrl: https://www.facebook.com/tayediggs
  - commentText: Love this positive message! Your work has inspired so many people. Keep shining! 🌟
```

## 输出汇报格式

```
## ✅ Facebook 互动完成

### 关注状态
- [用户名] 已关注 ✓

### 留言详情
- **帖子**：[帖子内容摘要]
- **留言**：[留言内容]
- **状态**：评论已提交 ✓
```
