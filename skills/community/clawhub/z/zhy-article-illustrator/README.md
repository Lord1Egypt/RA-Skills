# zhy-article-illustrator

辅助 skill：为 Markdown 文章自动规划、生成并插入配图。

## Install

```bash
npx skills add https://github.com/zhylq/yuan-skills --skill zhy-article-illustrator
```

## What It Does

- 分析文章结构
- 生成 `visual-bible.md`
- 生成 `outline.md`
- 生成结构化 prompts
- 调用生图脚本输出图片
- 生成 `article.illustrated.md`
- 可选上传七牛云并替换为 CDN URL

## Environment Setup

本 skill 需要图像生成配置。

请先复制：

```bash
cp .env.example .env
```

然后按你的实际通道填写。

### 最小必填（至少一组）

#### 方案 A：通用 Gemini / 兼容接口

```env
IMAGE_PROVIDER=
IMAGE_MODEL=
IMAGE_BASE_URL=
IMAGE_API_KEY=
```

#### 方案 B：Xiaomi Gemini 兼容接口

```env
XIAOMI_API_KEY=
XIAOMI_BASE_URL=
XIAOMI_IMAGE_SIZE=1K
```

#### 方案 C：官方 Gemini / Google

```env
GEMINI_API_KEY=
# 或
GOOGLE_API_KEY=
```

#### 方案 D：OpenAI

```env
OPENAI_API_KEY=
```

### 如果要上传七牛云

还需要：

```env
QINIU_ACCESS_KEY=
QINIU_SECRET_KEY=
QINIU_BUCKET=
QINIU_DOMAIN=
QINIU_REGION=z0
```

## Key Inputs

- `article_path`：文章 Markdown 路径
- `slug`：输出 slug
- `density`：`minimal | balanced | rich`
- `upload`：是否上传图床
- `aspect_ratio`：如 `16:9`
- `prompt_profile`
- `text_language`
- `english_terms_whitelist`
- `image_provider`
- `image_model`
- `image_base_url`

## Outputs

- `article.illustrated.md`
- `illustrations/<slug>/visual-bible.md`
- `illustrations/<slug>/outline.md`
- `illustrations/<slug>/prompts/`
- `illustrations/<slug>/*.png`

## Notes

- 开源仓库中的 `.env.example` 不预设任何私有中转地址
- 若使用自建代理，请将 `IMAGE_BASE_URL` 或 `XIAOMI_BASE_URL` 改为你自己的地址
- 本 skill 会读取本地 `.env`，请勿提交真实配置
