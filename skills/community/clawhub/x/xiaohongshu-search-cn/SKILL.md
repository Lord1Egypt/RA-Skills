---
name: xiaohongshu-search
description: 小红书内容搜索工具。通过 browser 工具操控已登录的 Chrome，搜索小红书公开笔记，提取标题、正文、话题标签、点赞数，分析消费趋势。用于市场调研中的消费者趋势研究。
---

# 小红书搜索 Skill

## 前置条件

browser 工具需要 Chrome 开启远程调试模式：

```
chrome.exe --remote-debugging-port=9222
```

## 搜索流程

### Step 1：搜索关键词

在发现页搜索框输入关键词：

```
browser type <搜索框ref> "<关键词>"
browser press <搜索框ref> Enter
```

或者直接访问搜索结果 URL：
```
browser open "https://www.xiaohongshu.com/search_result?keyword=<关键词>&source=web_explore_feed"
```

### Step 2：等待并获取快照

```
browser wait "<selector>" --load networkidle
browser snapshot
```

### Step 3：提取内容

从 snapshot 中提取：
- 笔记标题和链接
- 作者昵称
- 点赞/收藏数

### Step 4：读取单篇笔记正文

点击进入详情页：
```
browser click <ref>
browser wait "#detail-content" --load networkidle
browser evaluate --fn "() => ({
  title: document.querySelector('.title')?.innerText,
  author: document.querySelector('.author')?.innerText,
  content: document.querySelector('#detail-content')?.innerText,
  tags: Array.from(document.querySelectorAll('.hashtag')).map(el => el.innerText),
  likes: document.querySelector('.like-wrapper .count')?.innerText
})"
```

## 消费趋势研究示例

**关键词**：`2025消费趋势`、`社区商业`、`新中式`、`亲子餐厅`

**操作序列**：
```
browser open "https://www.xiaohongshu.com/search_result?keyword=2025消费趋势&source=web_explore_feed"
browser wait ".note-item" --load networkidle
browser snapshot
```

## 输出格式

```
【小红书趋势搜索】关键词：2025消费趋势

📌 热门笔记：
1. [标题] @作者 - 👍N
   摘要...
2. [标题] @作者 - 👍N
   摘要...

🏷️ 高频话题：#消费趋势 #2025 #...

💡 趋势洞察：
- （AI 综合分析这段趋势，可用于商业定位参考）
```

## 在商业市调报告中的应用

整合到 `shangyecehua.skill` Step 1 数据收集中：

```
【补充】小红书趋势研究：
browser 搜索 "<城市> <业态> 消费趋势" 或 "<业态> 探店"
→ 提取消费者偏好、热门话题、新兴业态
→ 作为商业定位和业态规划的参考
```
