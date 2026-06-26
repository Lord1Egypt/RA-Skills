---
name: weibo-scraper
description: 抓取指定微博用户的帖子内容。当用户提到"抓微博"、"微博内容"、"看微博"、"weibo"、"某人微博"等关键词时使用此 skill。支持按日期筛选、自动获取长文全文、滚动加载防遗漏。基于 m.weibo.cn 移动端 + browser 工具实现，无需登录即可抓取公开微博。
---

# Weibo Scraper

抓取微博用户帖子的浏览器自动化工作流。

## 核心方案

使用 browser 工具访问 `m.weibo.cn`（移动端），无需登录即可查看公开微博。移动端比 PC 端结构简单、反爬弱、渲染快。

## 工作流

### 1. 获取目标用户 UID

如果已知 UID，跳到步骤 2。

否则，用 browser 导航到 `https://m.weibo.cn/search?luicode=10000011&lfid=100103type%3D1%26q%3D{URL编码的昵称}`，在搜索结果中找到用户主页链接，从中提取 UID（格式为 `/u/{UID}` 或 `/profile/{UID}`）。

### 2. 访问用户主页

```
navigate → https://m.weibo.cn/u/{UID}
```

页面加载后，snapshot 可见帖子列表。帖子结构：
- 每条帖子在一个 `banner` 块中
- 发布时间在 `heading` 元素中，格式如 `4-17 08:37 来自 微博网页版`
- 正文在 `article` 元素中
- 如果正文被截断，会有 `link "全文"` 元素，URL 为 `/status/{微博ID}`

### 3. 筛选目标日期的帖子

遍历 snapshot 中的所有帖子，匹配 `.time` heading 中的日期部分（如 `4-17`）。

注意：日期格式为 `M-D`，不补零（如 `4-17` 不是 `04-17`）。跨年帖子会显示年份（如 `2025-12-28`）。

### 4. 获取全文

**短帖**：主页 snapshot 中的 `article` 内容即为完整文本。

**长帖**（有"全文"链接）：
1. 记录 `/status/{微博ID}` 中的微博ID
2. `navigate → https://m.weibo.cn/status/{微博ID}`
3. snapshot 获取完整正文
4. 返回主页继续处理

### 5. 滚动加载

主页默认只显示最近的约 10 条帖子。如果目标日期的帖子不在首屏：

```javascript
window.scrollTo(0, document.body.scrollHeight)
```

执行后等 1-2 秒再 snapshot，检查是否加载了更多帖子。重复滚动直到目标日期的帖子全部出现。

### 6. 关闭浏览器

抓取完成后，关闭本次打开的浏览器标签页：

```
browser → close → targetId: {当前标签页的 targetId}
```

释放资源，避免残留标签页占用内存。

### 7. 输出格式

按时间从早到晚排序，每条帖子标注序号和发布时间：

```
① HH:MM
[正文内容]

② HH:MM
[正文内容]
```

## 注意事项

- **无需登录**：m.weibo.cn 可直接查看公开微博
- **不要用 API**：`m.weibo.cn/api/container/getIndex` 会被 432 反爬拦截
- **不要用 PC 端**：weibo.com 结构复杂，反爬更强
- **日期格式**：注意 `M-D` 不补零，如 `4-17` 而非 `04-17`
- **滚动后重新 snapshot**：滚动后必须重新 snapshot 才能看到新加载的内容
