---
name: wewe-rss-wechat-export
description: "适配 wewe-rss 的公众号抓取与导出工具：把微信公众号 / JSON feed 批量导出为清洗后的 DOCX 文档，并支持日期前缀命名与 zip 打包。适用于导出公众号文章、批量生成 Word 交付包、保留正文清洗结果等场景。"
---

# wewe-rss WeChat Export

> 适配 **wewe-rss** 的公众号抓取与文档导出工具。

## 它做什么

这个 skill 用于把符合 wewe-rss / JSON Feed 风格的公众号 feed 批量导出为清洗后的 Word 文档，并按需要生成 zip 交付包。

核心能力：

- 分页抓取 feed
- 清洗公众号文章正文
- 过滤脚本、样式和页面级垃圾标签
- 图片本地化
- Pandoc 转 DOCX
- 生成 `index.txt` 汇总
- 可选打包为 zip

## 适用场景

当用户想做这些事情时使用本 skill：

- 导出微信公众号文章为 DOCX
- 把 wewe-rss feed 做成可交付文档包
- 给导出文件自动加日期前缀
- 批量抓取公众号文章并打包
- 保留 HTML / Markdown / DOCX 作为验收产物

## 执行原则

1. 统一通过 `scripts/run-export-feed.sh` 调用。
2. 不在 skill 内重复实现导出逻辑。
3. 默认交付参数优先选择：
   - `--output-mode docx`
   - `--rename-mode dated`
   - `--zip`
4. 导出前检查依赖：`node`、`pandoc`、`curl`、`python3`。
5. 若未指定输出目录，默认输出到当前工作目录下的 `export/`。
6. `--batch-size` 最大限制为 `5`，避免过度抓取。

## 参数格式

```text
bash <skill_dir>/scripts/run-export-feed.sh <feed_url> [count] [output_dir] [--batch-size N] [--output-mode docx|full] [--rename-mode dated|plain] [--zip]
```

### 位置参数

- `feed_url`：必填，公众号 / wewe-rss feed JSON 地址
- `count`：可选，默认 `100`
- `output_dir`：可选，默认落到当前工作目录 `export/`

### 可选项

- `--batch-size N`：分页批大小，默认 `2`，最大 `5`
- `--output-mode docx|full`
  - `docx`：仅保留适合交付的 DOCX 结果
  - `full`：保留 HTML / Markdown / DOCX 与资源目录
- `--rename-mode dated|plain`
  - `dated`：`YYYY-MM-DD-序号-标题.docx`
  - `plain`：`序号-标题.docx`
- `--zip`：导出完成后额外生成 zip

## 推荐用法

### 最终交付型导出

```bash
bash <skill_dir>/scripts/run-export-feed.sh \
  "https://example.com/feed.json" \
  100 \
  "./export/my-feed" \
  --batch-size 5 \
  --output-mode docx \
  --rename-mode dated \
  --zip
```

### 小样本验收

```bash
bash <skill_dir>/scripts/run-export-feed.sh \
  "https://example.com/feed.json" \
  5 \
  "./export/my-feed-smoke" \
  --batch-size 1 \
  --output-mode full \
  --rename-mode dated
```

## 输出约定

成功后，至少返回：

- `output_dir`
- `index_path`
- `zip_path`（如果启用了 `--zip`）
- `output_mode`
- `rename_mode`

## 目录结构

```text
wewe-rss-wechat-export/
├── CHANGELOG.md
├── INSTALL.md
├── LICENSE
├── README.md
├── SKILL.md
├── _meta.json
├── manifest.yaml
└── scripts/
    ├── export-feed-single-pages.mjs
    └── run-export-feed.sh
```
