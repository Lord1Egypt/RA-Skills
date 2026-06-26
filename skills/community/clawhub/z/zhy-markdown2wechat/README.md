# zhy-markdown2wechat

辅助 skill：将 Markdown 转换为微信公众号可用的内联 HTML，并支持主题样式。

## Install

```bash
npx skills add https://github.com/zhylq/yuan-skills --skill zhy-markdown2wechat
```

## What It Does

- 读取 Markdown 文件
- 读取主题 CSS
- 转换为 HTML
- 输出根容器为 `<section id="MdWechat">` 的微信风格 HTML

## Environment

本 skill 不需要 `.env`。

## Usage Notes

- 主题文件位于 `resources/themes/`
- 当前支持：`default.css`、`apple.css`、`blue.css`、`dark.css`、`green.css`、`notion.css`、`vibrant.css`
- 若后续要配合 `zhy-wechat-publish` 上传草稿箱，推荐先用本 skill 生成 HTML，再交给发布 skill 处理 CSS 变量、图片和列表兼容

## Output

- 输出 HTML 文件，例如 `article.zhy.html`

## Limitations

- 当前脚本会在临时目录安装运行所需依赖
- 它更适合作为 skill 内部转换步骤，而不是通用生产级 npm CLI
