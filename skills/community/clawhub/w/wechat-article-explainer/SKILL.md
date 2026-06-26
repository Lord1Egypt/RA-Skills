---
name: wechat-article-explainer
version: 1.0.1
description: 微信公众号文章通俗内容解释技能。当用户需要总结或解释微信公众号链接或url时使用这个技能。技能包含：根据用户提供的链接或URL，读取链接内容，用通俗的语言解释内容。
---

# 微信公众号文章通俗内容解释技能

## 概述

这个 Skill 用于阅读和用通俗的语言总结微信公众号链接的内容。

## 使用方法

当用户提供微信公众号文章链接时，按照以下步骤执行：

### 1. 验证链接格式

确认是有效的微信公众号链接，格式如下：
- `https://mp.weixin.qq.com/s/xxx`
- `https://mp.weixin.qq.com/s?xxx`

### 2. 执行 Python 工具获取文章内容

使用 `wechat_reader.py` 工具抓取文章：

```bash
python3 scripts/wechat_reader.py "<文章链接>"
```

### 3. 总结文章内容

根据获取的文章内容，提供通俗内容解释：

- **文章标题**：
- **作者/来源**：
- **发布时间**：
- **内容总结**（通俗内容解释）：

## 技术细节

- **Python 依赖**：
  - `requests`（基础 HTTP 请求）
  - `playwright`（浏览器模拟，更稳定）

- **安装依赖**：
  ```bash
  pip install requests
  # 或使用浏览器模式
  pip install playwright
  playwright install chromium
  ```

- **使用浏览器模式**：默认使用 Playwright，更稳定但需要安装浏览器
- **不使用浏览器**：`python3 wechat_reader.py <url> --no-browser`

## 注意事项

- 微信文章可能有防盗链限制，直接 HTTP 请求可能失败
- 浏览器模式更稳定但速度较慢
- 如果抓取失败，提示用户在微信中打开文章并复制内容
