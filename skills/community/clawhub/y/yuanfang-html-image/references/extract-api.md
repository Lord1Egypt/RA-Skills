# extract.js — 内容提取 API

agent 调用 `extract.js` 提取内容。

**前置**: Node.js 18+ (自带 `fetch`)。

## 命令

```bash
# URL 提取（项目根目录执行）
node scripts/extract.js "https://..." > content.json

# 纯文本提取
node scripts/extract.js --text "标题\n正文内容\n- 要点1\n- 要点2" > content.json

# 从文件读取
node scripts/extract.js --file article.md > content.json
```

## 输出格式

```json
{
  "title": "主标题",
  "body": "正文描述",
  "points": ["要点1", "要点2"],
  "brand": "品牌名 (从 og:site_name 抓, 可选)",
  "brandImage": "data:image/png;... (从 og:image 抓, 可选)"
}
```

`source` 字段已废弃，不再生成。**无 Python 依赖** — 全栈 Node.js。

## 提取逻辑

| 字段 | URL 来源 | 文本来源 |
|------|---------|---------|
| `title` | `<h1>` / og:title / twitter:title | 首行 |
| `body` | og:description / description / 第一段 | 中间段落 |
| `points` | ul/ol li / h2-h3 标题 | `-` / `•` / `*` 开头行 |
| `brand` | og:site_name / application-name / 域名 | 匹配 "公众号/来源/来自" 前缀 |
| `brandImage` | og:image / apple-touch-icon / favicon | — |

## 边界与提示

- 文本输入**没有语义分析**，纯结构化（首行/段落/bullet 模式）
- body 中用 `、` 列举时会自动拆为 points（中文顿号 splitter）
- 失败时输出友好错误（`HTTP 404`、`SyntaxError` 等）
- 缓存：brand-spec 缓存 7 天，强制刷新用 `--refresh-brand`（在 `extract-brand.js`）
