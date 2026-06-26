# xhs-comment-scraper

小红书评论爬虫。用户在小红书博主主页复制链接发给你，自动抓取全部笔记评论，保存为 JSON 并生成分析可视化报告。

## 功能

- 自动抓取博主主页下所有笔记的评论区
- 评论字段：昵称、内容、时间、点赞数
- 每篇笔记独立 JSON 文件
- 自动展开嵌套回复
- 生成 HTML 分析报告（词云、意图分析、高频词、双笔记对照阅读）
- 自动检测小红书页面结构（Vue 动态渲染兼容）

## 使用方式

1. 安装 skill 后，在聊天中发送小红书博主主页链接
2. 机器人自动打开浏览器，用户扫码登录
3. 等待抓取完成，JSON 文件保存在 `下载\xhs_comments\`
4. 分析报告保存在 `下载\xhs_comments_analysis\`

## 平台要求

- Windows
- Python 3（用于生成分析报告，可选）

## 核心技巧

- 使用内置 Chrome 而非 Browser Relay，避免 token 问题
- Vue 渲染页面用 `innerText` 提取文本
- 验证码需用户手动完成

## 权限

需要 browser tool 和 exec tool。

## License

MIT
