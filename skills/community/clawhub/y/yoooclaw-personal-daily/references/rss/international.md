# 海外 RSS 源

仅在所选平台生成 reference 已设置 `acquisition=rss` 时读取本文件。固定使用以下 7 个直连 RSS/Atom 源：

| 来源 | URL | 侧重 |
|---|---|---|
| OpenAI News | `https://openai.com/news/rss.xml` | OpenAI 官方动态 |
| Google AI | `https://blog.google/technology/ai/rss/` | Google AI 动态 |
| Hugging Face Blog | `https://huggingface.co/blog/feed.xml` | 开源 AI |
| Hacker News | `https://hnrss.org/frontpage` | 英文技术社区热点 |
| Variety | `https://variety.com/feed/` | 影视与娱乐产业 |
| IGN | `https://www.ign.com/rss/articles/feed` | 游戏、影视与流行文化 |
| Pitchfork News | `https://pitchfork.com/feed/feed-news/rss` | 音乐资讯 |

RSS 只覆盖固定来源，不等同于全网搜索。最终回复注明“RSS 来源：国内 {国内成功数}/10，海外 {海外成功数}/7，总计 {总成功数}/17”；部分失败时再列出失败源名。没有匹配事件时，在空日报后注明相同的检查范围。

**完成条件：** 海外源不少于 5，抓取命令只使用表中 URL，最终结果披露国内、海外和总计的实际成功数量。
