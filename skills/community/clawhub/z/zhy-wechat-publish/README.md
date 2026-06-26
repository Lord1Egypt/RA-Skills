# zhy-wechat-publish

辅助 skill：将 HTML 上传到微信公众号草稿箱，并自动处理 CSS 变量、正文图片和列表兼容性。

## Install

```bash
npx skills add https://github.com/zhylq/yuan-skills --skill zhy-wechat-publish
```

## What It Does

- 上传 HTML 到微信公众号草稿箱
- 自动展开 CSS 变量
- 自动上传正文图片到微信正文图片接口
- 自动去掉首个 `h1`
- 自动把 `ul/ol` 转成公众号编辑态更稳定的段落列表
- 可选自动生成封面并上传

## Environment Setup

请先复制：

```bash
cp .env.example .env
```

### 最小必填

```env
WECHAT_APP_ID=
WECHAT_APP_SECRET=
```

### 可选但常用

```env
WECHAT_DEFAULT_THUMB_MEDIA_ID=
WECHAT_DEFAULT_AUTHOR=
```

### 如果要自动生成封面

还需要可用的生图环境。可填写：

```env
IMAGE_PROVIDER=
IMAGE_MODEL=
IMAGE_BASE_URL=
IMAGE_API_KEY=
IMAGE_SIZE=
XIAOMI_API_KEY=
XIAOMI_BASE_URL=
XIAOMI_IMAGE_SIZE=
GEMINI_API_KEY=
GOOGLE_API_KEY=
OPENAI_API_KEY=
```

## WeChat Requirements

- 运行机器公网 IP 需要加入微信公众号后台 IP 白名单
- 使用微信官方草稿接口，需要有效的公众号 AppID / AppSecret
- 如果未提供 `--thumb` 且未配置 `WECHAT_DEFAULT_THUMB_MEDIA_ID`，草稿上传可能失败

## Common Inputs

### 直接上传 HTML

- `--title`
- `--file`
- `--author`
- `--digest`
- `--thumb`
- `--source-url`
- `--need-open-comment`
- `--only-fans-can-comment`

### 自动封面上传

- `--article`
- `--html`
- `--title`
- `--author`
- `--cover-output`
- `--cover-ar`
- `--source-url`

## When To Use Which Entry

### 用 `wechat_draft.js`

适合：

- 你已经有最终 HTML
- 你已经有封面 `media_id`
- 你只想稳定上传草稿

### 用 `publish_with_cover.js`

适合：

- 你已经有文章文件和 HTML
- 你希望自动生成封面
- 你本机有可用的 `bun` 和生图环境

## Notes

- 本 skill 不会自动最终发布，只会保存到草稿箱
- 标题长度建议不超过 64 字符
- 不要把真实 `.env`、AppSecret、media_id 提交回仓库
