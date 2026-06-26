# Web Reader

智能网页阅读器 for Claude Code。抓取文章/下载视频，自动归档，支持后续分析。

## 功能

- **智能路由**: 根据 URL 自动选择最佳抓取策略
- **图文下载**: 文章 + 图片一键保存为本地 Markdown
- **自动归档**: 按分类整理到指定目录
- **后续分析**: 下载后支持摘要、分析、衍生、对比等操作

## 支持平台

| 平台 | 类型 | 方法 |
|------|------|------|
| 微信公众号 | 文章 | scrapling |
| 飞书文档 | 文章 | 虚拟滚动采集 |
| 知乎 | 文章 | scrapling |
| 头条 | 文章 | scrapling |
| 小红书 | 文章 | camoufox |
| B站 | 视频 | yt-dlp |
| YouTube | 视频 | yt-dlp |
| 抖音 | 视频 | yt-dlp |

## 安装

```bash
clawhub install web-reader
```

或手动克隆：

```bash
git clone https://github.com/inspirai-store/skill-market ~/.claude/skills/web-reader
```

## 依赖

```bash
pip install scrapling html2text  # 文章
pip install yt-dlp               # 视频
pip install camoufox             # 反检测（可选）
```

## 使用

```bash
# 抓取文章
python3 fetcher.py "https://mp.weixin.qq.com/s/xxx" -o ~/docs/

# 带分类归档
python3 fetcher.py "URL" -o ~/docs/articles --category "AI工具"

# 下载视频
python3 fetcher.py "https://b23.tv/xxx" -o ~/videos/
```

## License

MIT
