# CLI Reference

## render.js — 主渲染命令

```bash
# 推荐用法
node scripts/render.js --theme <theme> --layout cover --platforms <ids>

# 从 content.json 生成
node scripts/render.js \
  --file /path/to/content.json \
  --theme dark-gold --layout cover \
  --platforms xiaohongshu-v,wechat-cover

# 直接传参数（不用 --file）
node scripts/render.js \
  --title "AI 如何改变内容创作" \
  --body "从写作到配图..." \
  --points "效率提升 10x|零门槛创作" \
  --theme 1 --platforms all

# 输出 HTML 不截图（调试）
node scripts/render.js --preview --theme dark-gold --platforms wechat-cover
```

## 完整参数

| 参数 | 说明 |
|------|------|
| `--theme <name>` | 12 个主题之一（见 themes-catalog.md） |
| `--layout <name>` | 布局类型，当前只有 `cover` |
| `--platforms <ids>` | 平台 ID 列表（见 platforms.md），逗号分隔 |
| `--file <path>` | content.json 路径 |
| `--output <dir>` | 自定义输出目录（默认 `output/<日期>_<标题>_<序号>/`） |
| `--preview` | 输出 HTML 不截图 |
| `--brand-spec <path>` | 指定 brand spec 文件 |
| `--refresh-brand` | 强制重新抓取（跳过缓存） |
| `--list-themes` | 列出所有主题 |
| `--list-layouts` | 列出所有布局 |

## 旧版 CLI 兼容

`--template 1` 自动映射到 `--theme minimal-white --layout cover`。

| 旧 ID | 新 theme | 旧 ID | 新 theme |
|------|---------|------|---------|
| `1` | minimal-white | `7` | data-infographic |
| `2` | dark-gold | `8` | eastern |
| `3` | editorial | `9` | magazine-cover |
| `4` | warm-handdrawn | `10` | split-screen |
| `5` | tech-modern | `11` | minimal-white |
| `6` | bold-poster | `12` | list-ranking |

> 注意：`11` 和 `1` 都映射到 `minimal-white`（重复）。
