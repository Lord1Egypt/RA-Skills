# wechat-toolkit 主题参考

wechat-toolkit 现在不只暴露 wenyan 的少数几个主题，而是维护了一份统一主题目录，发布、视频发布、参考图都走同一套配置。

## 快速查看

```bash
node scripts/publisher/publish.js --list-themes
node scripts/publisher/theme_catalog.js list
```

## 参考图

ClawHub 发布包默认**不附带 PNG 预览图**，避免非文本文件限制和 50MB 上传限制。

如果你本地想生成主题预览，请运行：

```bash
node scripts/publisher/publish.js --generate-theme-previews
```

生成后会得到：

```bash
scripts/publisher/theme_previews/theme-gallery.html
scripts/publisher/theme_previews/theme-gallery.png
scripts/publisher/theme_previews/<theme-id>.png
```

如果修改了主题 CSS 或推荐高亮，重新生成：

```bash
node scripts/publisher/publish.js --generate-theme-previews
```

## Bundled 主题

### 内置主题

- `default` - 简洁稳妥，适合资讯、总结、日报
- `orangeheart` - 暖色杂志感，适合人物、品牌、案例文章
- `rainbow` - 色彩活泼，适合活动、清单、创意内容
- `lapis` - 冷调科技蓝，适合教程、评测、工具介绍
- `pie` - 现代锐利，适合观点、方法论、深度分析
- `maize` - 浅暖纸感，适合教程、拆解、轻阅读
- `purple` - 柔和优雅，适合专栏、随笔、访谈
- `phycat` - 薄荷清新，适合科技资讯、产品上手、工具流

### 自定义主题

- `aurora` - 渐变标题和清爽层次，适合 AI 趋势、产品观察
- `newsroom` - 报刊专栏风，适合评论、行业观察、长文
- `sage` - 柔和笔记感，适合经验总结、个人成长、复盘
- `ember` - 暖调杂志封面感，适合故事、案例、品牌内容

## 推荐命令

```bash
# 默认稳妥
node scripts/publisher/publish.js article.md default

# 技术/工具类
node scripts/publisher/publish.js article.md lapis
node scripts/publisher/publish.js article.md aurora

# 长文/评论
node scripts/publisher/publish.js article.md pie
node scripts/publisher/publish.js article.md newsroom

# 个人表达/复盘
node scripts/publisher/publish.js article.md purple
node scripts/publisher/publish.js article.md sage

# 暖色案例/品牌文
node scripts/publisher/publish.js article.md orangeheart
node scripts/publisher/publish.js article.md ember
```

## 代码高亮主题

- `atom-one-dark`
- `atom-one-light`
- `dracula`
- `github`
- `github-dark`
- `monokai`
- `solarized-dark`
- `solarized-light`
- `xcode`

## 自定义 CSS 主题

除了 bundled 主题外，也支持直接传 CSS 路径：

```bash
node scripts/publisher/publish.js article.md /absolute/path/to/theme.css
node scripts/publisher/publish_with_video.js article.md /absolute/path/to/theme.css
```

## 原生 wenyan 能力

如果你要管理 wenyan 自己安装的主题：

```bash
wenyan theme -l
wenyan theme --add --name my-theme --path /path/to/theme.css
wenyan theme --rm my-theme
```
