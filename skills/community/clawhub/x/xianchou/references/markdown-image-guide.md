# Markdown/MDX 配图指南

本文档说明如何为任意 Markdown/MDX 自动生成并插入图片。

## 通用模式

```bash
xianchou markdown images ./article.md --count 3 --write
```

行为：

- 读取 frontmatter、标题和二级标题。
- 根据标题和摘要生成图片提示词。
- 下载图片到资源目录。
- 在相关标题后插入 Markdown 图片。
- 使用 `<!-- xianchou:image ... -->` 标记保证重复执行时可更新。

默认输出目录为同级 `article-assets/`。

## 路径参数

```bash
xianchou markdown images ./docs/guide.md \
  --assets-dir ./docs/assets \
  --public-url-prefix ./assets \
  --write
```

| 参数 | 含义 |
|------|------|
| `--assets-dir` | 本地图片保存目录 |
| `--public-url-prefix` | 写入 Markdown 的 URL 前缀 |

## 封面图

普通 Markdown 只有传入 `--cover` 才更新 frontmatter：

```bash
xianchou markdown images ./article.md --cover --write
```

会更新：

```yaml
cover: "<url>"
coverAlt: "<alt>"
```

## Dry-run

不传 `--write` 时不会修改 Markdown，但仍会生成和下载图片，并输出 JSON 结果。确认结果无误后再加 `--write`。
