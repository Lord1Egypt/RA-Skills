# wewe-rss WeChat Export

> 适配 **wewe-rss** 的公众号抓取与文档导出工具。

这是一个可安装到 OpenClaw、也可发布到 ClawHub 的 skill 仓库。
它把 wewe-rss 风格的公众号 JSON feed 批量导出为清洗后的 DOCX 文档，并支持可选 zip 打包。

## 功能简介

这个 skill 会完成：

- feed 分页抓取
- 正文提取与清洗
- 图片本地化
- Pandoc 转 DOCX
- `index.txt` 汇总
- 可选 zip 打包

## 为什么叫它“适配 wewe-rss 的公众号抓取工具”

因为它不是一个抽象的通用下载器，而是基于当前 `wewe-rss` 项目里已经验证过的 feed 导出链路整理出来的自包含 skill。
目标就是把 **wewe-rss 的公众号抓取 / 导出能力** 打包成别人也能安装和复用的 OpenClaw / ClawHub skill。

## 特性

- **适配 wewe-rss**：面向 wewe-rss / JSON Feed 风格公众号数据源
- **可交付**：支持直接生成 DOCX 文档包
- **支持打包**：导出后可额外生成 zip
- **支持验收模式**：`full` 模式保留 HTML / Markdown / 资源目录
- **文件名更稳**：支持日期前缀与非法字符清理
- **自包含**：包内包含导出脚本，不依赖外部仓库绝对路径

## 依赖

运行环境需要：

- `node`
- `pandoc`
- `curl`
- `python3`

## 使用方式

```bash
bash <skill_dir>/scripts/run-export-feed.sh <feed_url> [count] [output_dir] [--batch-size N] [--output-mode docx|full] [--rename-mode dated|plain] [--zip]
```

### 最终交付示例

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

### 验收示例

```bash
bash <skill_dir>/scripts/run-export-feed.sh \
  "https://example.com/feed.json" \
  3 \
  "./export/my-feed-smoke" \
  --batch-size 1 \
  --output-mode full \
  --rename-mode dated
```

## 输出结果

成功后通常会得到：

- 一组 `.docx`
- `index.txt`
- 可选 `.zip`
- 若是 `full` 模式，还会保留 `.html`、`.md` 和资源目录

## 安装与发布

- 本地安装见 [INSTALL.md](INSTALL.md)
- 发布到 ClawHub 的流程见 [PUBLISH.md](PUBLISH.md)

## License

[MIT](LICENSE)
