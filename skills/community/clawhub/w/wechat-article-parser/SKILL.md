---
name: wechat-article-parser
description: 解析微信公众号文章，提取标题、作者、正文内容、图片等信息。当用户发送微信公众号链接（mp.weixin.qq.com）并希望获取文章内容、摘要或保存时触发。支持自动提取内容并可选保存到飞书表格。
---

# 微信公众号文章解析器

解析微信公众号文章，自动提取标题、作者、发布时间、正文内容等信息。

## 功能特性

- ✅ 自动提取文章标题、作者、发布时间
- ✅ 完整正文内容提取
- ✅ 图片链接提取
- ✅ 字数统计
- ✅ 支持保存为 JSON/TXT
- ✅ 可选保存到飞书表格

## 使用方法

### 基本用法：解析文章

```bash
python3 scripts/wechat_parser.py "https://mp.weixin.qq.com/s/xxxxx"
```

**输出示例：**
```
================================================================================
📰 标题: 文章标题
✍️  作者: 公众号名称
🕐 发布时间: 2026-03-10
📊 字数: 3500
🖼️  图片数: 5
================================================================================

📝 正文内容:

这是文章的正文内容...
================================================================================
```

### 保存到文件

```bash
# 保存为 JSON（包含全部信息）
python3 scripts/wechat_parser.py "URL" --save

# 指定输出文件名
python3 scripts/wechat_parser.py "URL" --save --output article.json
```

### 保存到飞书表格

```bash
python3 scripts/save_to_feishu.py "https://mp.weixin.qq.com/s/xxxxx"

# 手动指定标题
python3 scripts/save_to_feishu.py "https://mp.weixin.qq.com/s/xxxxx" "自定义标题"
```

### 在 OpenClaw 对话中使用

直接发送微信公众号链接，AI 会自动调用此 skill 解析内容：

```
https://mp.weixin.qq.com/s/xxxxx
```

或带指令：
```
解析这篇文章 https://mp.weixin.qq.com/s/xxxxx
```

```
收藏 https://mp.weixin.qq.com/s/xxxxx
```

## 输出格式

### JSON 格式

```json
{
  "title": "文章标题",
  "author": "公众号名称",
  "publish_time": "2026-03-10",
  "content": "正文内容...",
  "word_count": 3500,
  "images_count": 5,
  "images": ["url1", "url2", ...],
  "url": "原始链接",
  "parsed_at": "2026-03-10 12:00:00"
}
```

## 飞书保存配置

如需使用飞书保存功能，需配置 `.env` 文件：

```env
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_APP_TOKEN=your_bitable_app_token
FEISHU_TABLE_ID=your_table_id
```

## 支持的链接格式

- `https://mp.weixin.qq.com/s/xxxxx`
- `https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&idx=xxx`
- 微信短链接

## 常见问题

**Q: 提取内容不完整？**
A: 微信有反爬机制，部分文章可能提取不完整。建议：
1. 使用浏览器 Cookie（高级用法）
2. 手动复制重要段落

**Q: 图片无法显示？**
A: 微信图片有防盗链机制，需要带 Referer 头访问。

## 文件结构

```
wechat-article-parser/
├── SKILL.md              # 本文档
├── scripts/
│   ├── wechat_parser.py       # 核心解析脚本
│   └── save_to_feishu.py      # 飞书保存脚本
├── .env.example          # 配置模板
└── requirements.txt      # 依赖
```

## 依赖

```
requests
beautifulsoup4
python-dotenv
```

安装：
```bash
pip3 install requests beautifulsoup4 python-dotenv
```

## 许可证

MIT License
