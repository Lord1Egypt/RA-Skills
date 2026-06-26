---
name: weixin-fetcher
version: 1.1.0
description: 获取微信公众号文章内容。当用户提供 mp.weixin.qq.com 链接时提取正文。
---

# 微信公众号文章获取

## 触发条件

- 用户发送 `mp.weixin.qq.com` 链接
- 用户要求获取/提取微信公众号文章内容

## 用法

```bash
python "{skill_dir}/scripts/fetch_weixin.py" "<文章URL>" -o "<输出目录>"
```

**参数说明：**
- `<文章URL>` — 微信公众号文章链接
- `-o <输出目录>` — 可选，输出文件保存目录（默认当前工作目录）
- `--headless` — 可选，无头模式（微信文章通常需要完整浏览器，慎用）

**输出文件：**
- `article_content_weixin.md` — 文章标题 + 正文（Markdown 格式）
- `article_screenshot_weixin.png` — 页面截图

## 示例

```bash
# 获取文章，输出到工作区
python "{skill_dir}/scripts/fetch_weixin.py" "https://mp.weixin.qq.com/s/EVdnYEzlrT3BZZUmlbxHQQ" -o "C:\Users\David\.qclaw\workspace"

# 无头模式（可能加载失败，慎用）
python "{skill_dir}/scripts/fetch_weixin.py" "https://mp.weixin.qq.com/s/xxxxx" --headless
```

## 依赖

首次使用前安装：`pip install -r {skill_dir}/scripts/requirements.txt`

## 工作原理

1. 启动 Chrome（默认有头模式），URL 追加 `?_t=毫秒时间戳` 绕过微信 CDN 缓存
2. 等待 `#js_content` 加载，提取正文文本
3. 输出 Markdown 文件 + 截图到指定目录

## 注意事项

- 需要系统已安装 Chrome 浏览器
- 首次运行会自动下载匹配的 ChromeDriver
