---
name: wechat-mp-reader
description: |
  抓取微信公众号文章并转换为 Markdown 格式。支持提取标题、作者、发布时间、封面图、正文内容（含图片、视频链接）。
  当用户提到以下场景时触发：
  - 读取/抓取/下载微信公众号文章
  - 将公众号文章转为 Markdown
  - 提取 mp.weixin.qq.com 链接内容
  - 保存公众号文章到本地
  - 微信文章备份、存档
  关键词：微信公众号、公众号文章、mp.weixin.qq.com、微信文章抓取、微信文章转 Markdown
---

# WeChat MP Reader — 微信公众号文章抓取工具

## 功能

抓取微信公众号文章（`mp.weixin.qq.com` 链接），提取完整内容并转换为 Markdown 格式保存到本地。

## 支持提取的信息

- **标题** — 文章标题
- **公众号名称** — 作者/来源
- **发布时间** — 文章发布日期
- **封面图** — 文章封面图片链接
- **正文内容** — 完整的文章正文，包含：
  - 文本段落、标题层级
  - 图片（保留原图链接）
  - 视频链接
  - 超链接
  - 列表、引用、加粗/斜体等格式

## 使用方法

### 命令行方式

```bash
python scripts/fetch_wechat_article.py <文章链接> [选项]
```

**参数：**
- `url` — 微信公众号文章链接（必需）
- `-o, --output` — 输出目录（默认：当前目录）
- `--images` — 下载图片到本地（开发中）
- `--json` — 以 JSON 格式输出元数据

**示例：**

```bash
# 基本用法
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/xxxxx"

# 指定输出目录
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/xxxxx" -o ./articles

# 只输出 JSON 元数据
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/xxxxx" --json
```

### Python API 方式

```python
from scripts.fetch_wechat_article import fetch_article

result = fetch_article(
    url="https://mp.weixin.qq.com/s/xxxxx",
    output_dir="./articles"
)

print(result['title'])      # 文章标题
print(result['author'])     # 公众号名称
print(result['content'])    # Markdown 正文
print(result['filepath'])   # 保存的文件路径
```

## 输出格式

生成的 Markdown 文件结构：

```markdown
# 文章标题

**公众号**: 公众号名称
**发布时间**: 2024-01-01
**封面**: ![封面](封面图链接)
**原文链接**: https://mp.weixin.qq.com/s/xxxxx

---

正文内容...

![图片](图片链接)

[视频](视频链接)
```

## 依赖

- Python 3.8+
- `requests` 库（用于 HTTP 请求）

安装依赖：
```bash
pip install requests
```

## 注意事项

1. **网络要求** — 需要能访问 `mp.weixin.qq.com`
2. **反爬机制** — 频繁抓取可能触发微信的反爬机制，建议适当控制请求频率
3. **链接有效性** — 确保文章链接未过期或被删除
4. **图片链接** — 生成的 Markdown 中图片使用微信 CDN 原链接，长期有效性取决于微信策略

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 无法提取正文 | 页面结构变化 | 检查微信是否更新了页面结构 |
| 返回 403 | 被反爬拦截 | 稍后再试，或更换 IP |
| 标题为空 | 文章被删除/受限 | 确认链接可在浏览器正常打开 |
| 图片不显示 | 微信 CDN 链接过期 | 使用 `--images` 下载到本地 |
