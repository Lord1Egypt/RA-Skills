---
name: tieba-spider
description: 贴吧帖子爬虫 - 从百度贴吧抓取帖子内容并导出为 Markdown（支持图片下载、楼中楼解析）。Tieba thread crawler - crawl Tieba threads to Markdown with images and sub-posts.
metadata:
  {
    "openclaw": { "emoji": "🕷️", "requires": { "anyBins": ["python3"] } },
  }
---

# Tieba Spider 🕷️

贴吧帖子爬虫 - 把百度贴吧帖子连图片带回复全扒下来

Crawl Tieba threads with full content, images, and sub-posts to Markdown.

## 功能 | Features

- 爬取帖子所有楼层内容
- 下载帖子中的图片到本地
- 解析楼中楼（子回复）内容
- 导出为整洁 Markdown 格式
- 支持指定输出目录和请求延迟

## 用法 | Usage

```bash
# 帖子链接或 ID
python3 tieba_spider.py "https://tieba.baidu.com/p/7487460366"
python3 tieba_spider.py "7487460366"

# 指定输出目录
python3 tieba_spider.py "7487460366" --output ~/downloads

# 不下载图片
python3 tieba_spider.py "7487460366" --no-images
```

## 参数 | Options

| 参数 | 说明 | Description |
| --- | --- | --- |
| `帖子` | 帖子链接或纯数字 ID | Thread URL or ID |
| `--output/-o` | 输出目录 (默认: 当前目录) | Output directory |
| `--no-images` | 不下载图片 | Skip image download |
| `--delay/-d` | 请求间隔秒数 (默认: 0.5) | Request delay |

## 输出结构 | Output

```
{帖子ID}_{标题}/
├── {标题}.md        # 帖子内容 Markdown
└── images/          # 下载的图片
```

## 示例 | Example

```bash
python3 tieba_spider.py 7487460366 --output ./output
```

输出文件会保存在 `./output/7487460366_xxx/` 目录。

## 技术说明

使用百度贴吧移动端 API，无需登录即可抓取。内置 0.5 秒延迟防止请求过快。