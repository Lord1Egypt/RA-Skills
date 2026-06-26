---
name: wechat-article-fetcher
description: 微信公众号文章抓取工具。当用户发送 mp.weixin.qq.com 链接时自动触发，将文章内容提取为 Markdown/文本，无需 API 密钥。
---

# 微信公众号文章抓取（wechat-article-fetcher）

## 安装方法

将本目录（`wechat-article-fetcher/`）复制到 OpenClaw 的 skills 目录下即可：

```
~/.openclaw/skills/wechat-article-fetcher/SKILL.md
```

无需配置、无需密钥、即装即用。

## 触发条件

用户消息中包含 `mp.weixin.qq.com` 链接时自动触发。

## 核心接口（一行命令）

```bash
curl -s "https://down.mptext.top/api/public/v1/download?url=<URL编码>&format=markdown"
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `url` | 文章链接，需 URL 编码 |
| `format` | 输出格式：`html`（默认）/ `markdown` / `text` / `json` |

## 完整使用示例

### 在 OpenClaw 中使用（示例提示词）

当用户发送微信公众号链接时，运行以下命令获取文章内容：

```bash
curl -s "https://down.mptext.top/api/public/v1/download?url=$(python3 -c "import urllib.parse; print(urllib.parse.quote(input()))" <<< 'https://mp.weixin.qq.com/s/xxxx')&format=markdown"
```

或使用 Python 脚本：

```python
#!/usr/bin/env python3
import urllib.request, urllib.parse, sys

url = sys.argv[1] if len(sys.argv) > 1 else input("微信文章链接: ")
encoded = urllib.parse.quote(url, safe='')
api_url = f"https://down.mptext.top/api/public/v1/download?url={encoded}&format=markdown"

req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=20) as r:
    print(r.read().decode('utf-8'))
```

### 使用格式

```bash
# 直接指定链接
curl -s "https://down.mptext.top/api/public/v1/download?url=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2Fxxxx&format=markdown"

# 在 Python 中使用
python3 -c "
import urllib.parse
url = 'https://mp.weixin.qq.com/s/xxxx'
encoded = urllib.parse.quote(url, safe='')
print(f'https://down.mptext.top/api/public/v1/download?url={encoded}&format=markdown')
"
```

## 注意事项

- **无需 API 密钥**，接口公开免费
- **部分文章**可能有字数限制或反爬处理
- **图片链接**有时效性，建议尽快保存
- 如 `markdown` 格式抓取失败，可尝试换 `text` 格式
- 部分文章被发布者设置了禁止转载，接口可能无法获取全文

## 来源

使用 `mptext.top` 公共接口：`https://down.mptext.top`
