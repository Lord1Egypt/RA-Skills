---
name: save-article-miaoyan
description: 文章自动保存到 Miaoyan。抓取任意网页文章（微信、博客、技术文章等），生成摘要，保存为 Markdown 到 Miaoyan/待学习 文件夹。Use when user wants to save an article/webpage to Miaoyan notes.
---

# Save Article to Miaoyan

自动抓取任意网页文章，生成摘要，保存到 Miaoyan 笔记应用。

## 支持的链接类型

- ✅ 微信公众号文章 (`mp.weixin.qq.com`)
- ✅ 个人博客/技术博客
- ✅ Medium、Substack
- ✅ GitHub 文档/README
- ✅ 知乎文章
- ✅ 掘金、少数派等技术平台
- ✅ 任意可访问的网页

## 功能

- 🔄 多种抓取方式（Jina Reader → curl → Tavily），自动 fallback
- 📝 智能生成要点摘要
- 💾 保存为 Markdown 到 Miaoyan/待学习
- 📤 回复确认

## 使用方式

### 方式 1：直接调用脚本

```bash
python3 save_article_to_miaoyan.py "https://example.com/article"
```

### 方式 2：通过 OpenClaw 集成

在 OpenClaw 中发送文章链接，自动触发保存流程。

## 抓取策略

脚本会按以下顺序尝试抓取：

1. **Jina Reader** — 最适合博客/技术文章，直接返回 Markdown
2. **curl** — 直接 HTTP 请求，适合微信公众号等
3. **Tavily Extract** — 备用方案，处理复杂场景

## 配置

### Miaoyan 路径

默认保存路径：
```
/Users/andy/Library/Mobile Documents/iCloud~com~tw93~miaoyan/Documents/待学习
```

如需修改，编辑脚本中的 `MIAOYAN_DIR` 变量。

### 必需配置

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| `TAVILY_API_KEY` | Tavily API Key（备用抓取） | [tavily.com](https://tavily.com) 注册获取 |

配置方式：
```bash
export TAVILY_API_KEY="your_api_key"
```

## 配置

1. **检测链接类型** — 识别网站，选择最佳抓取策略
2. **抓取内容** — 多种方式自动 fallback
3. **解析** — 提取标题、正文
4. **摘要** — 智能识别关键句生成摘要
5. **保存** — 写入 Markdown 文件到 Miaoyan

## 输出格式

保存的 Markdown 文件包含：

```markdown
# 文章标题

> 保存时间: YYYY-MM-DD
> 源链接: [原文链接](url)

## 📌 要点

[自动生成的摘要]

---

## 正文

[完整文章内容]
```

## 依赖

- Python 3.7+
- curl
- Miaoyan 应用（iCloud 同步）

## 错误处理

- 网络超时：20 秒自动放弃
- 单一方式失败：自动尝试下一种
- 文件保存失败：自动创建目录

## 扩展

可修改的部分：

- `MIAOYAN_DIR` — 保存路径
- `generate_summary()` — 摘要生成算法
- `detect_site_type()` — 网站类型检测规则
