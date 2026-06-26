# 微信公众号文章工作台 / WeChat Article Workbench

中文：这个项目用于把选题、链接、素材或精选资讯加工成微信公众号草稿箱文章。

English: This project turns topics, links, notes, or curated items into WeChat Official Account draft-box articles.

```text
手动选题 / 自定义链接 / AIHOT 精选来源 -> 素材抽取 -> Codex 写作与配图 -> 微信公众号草稿箱
Manual topic / custom URL / AIHOT curated source -> extraction -> Codex writing and images -> WeChat draft box
```

中文：工作流只创建「草稿箱」内容，不会直接发布文章。最终发布、原创声明、创作来源等后台选项仍由人工在微信公众号后台确认。

English: The workflow only creates draft-box entries. Publishing, originality declaration, creation source, and final backend settings remain manual in the WeChat backend.

## 项目定位 / Positioning

中文：这是一个本地公众号内容生产工作台，不是 AIHOT 专用翻译器。

English: This is a local WeChat article production workbench, not an AIHOT-only translator.

- 中文：原创写作：把选题、目标读者、素材和要求写成公众号文章。
  English: Original writing: turn a topic, target audience, notes, and requirements into a WeChat article.
- 中文：链接翻译/改写：抽取来源链接的关键信息，翻译必要部分，再重组为原创中文文章。
  English: Link translation/rewrite: extract key source information, translate what is needed, and reorganize it into an original Chinese article.
- 中文：精选来源模式：把 AIHOT 精选条目作为 AI 行业选题来源之一。
  English: Curated-source mode: use AIHOT featured items as one optional AI-industry topic source.
- 中文：配图与草稿上传：校验文章 JSON，上传封面图和正文图片，并创建微信公众号草稿箱条目。
  English: Image and draft upload: validate article JSON, upload cover/body images, and create WeChat draft-box entries.

## 为什么不需要 OPENAI_API_KEY / Why No OPENAI_API_KEY Is Required

中文：推荐使用 Codex 协作模式。

English: Codex-assisted mode is recommended.

1. 中文：Node.js 负责收集/抽取素材、校验文章 JSON、上传封面和正文图片、创建微信草稿。
   English: Node.js collects/extracts sources, validates article JSON, uploads cover/body images, and creates WeChat drafts.
2. 中文：Codex 使用自身模型能力完成写作、改写、翻译、总结、文章 JSON 打包，以及 image2/imagegen 封面图和正文插图生成。
   English: Codex uses its own model capability for writing, rewriting, translation, summarization, JSON packaging, and image2/imagegen cover/body illustration generation.
3. 中文：因此本项目默认不需要 `OPENAI_API_KEY`。
   English: Therefore this project does not require `OPENAI_API_KEY` by default.

中文：如果未来改成纯 Node.js 调用模型 API，则需要自行配置对应模型服务商的密钥；当前仓库实现的是 Codex 协作模式。

English: If this later becomes a pure Node.js model-API workflow, provider API keys must be configured separately. The current repository implements Codex-assisted mode.

## 安装与配置 / Setup

```bash
cd scripts/wechat-article-workbench
npm install
cp config.example.env .env
```

中文：编辑 `.env`：

English: Edit `.env`:

```bash
WECHAT_APPID=
WECHAT_APPSECRET=
WECHAT_AUTHOR=
WECHAT_CREATION_SOURCE=个人观点，仅供参考
ALLOW_STATIC_COVER_FALLBACK=0
DRY_RUN=1
```

中文：首次验证时保持 `DRY_RUN=1`。确认文章 JSON、图片和微信配置都没问题后，再设置 `DRY_RUN=0` 创建真实草稿。

English: Keep `DRY_RUN=1` for the first validation. After article JSON, images, and WeChat configuration look correct, set `DRY_RUN=0` to create real drafts.

## 隐私与发布安全 / Privacy and Publishing Safety

- 中文：`.env` 只用于本地运行，里面可能包含 `WECHAT_APPID`、`WECHAT_APPSECRET` 等敏感信息。
  English: `.env` is local-only and may contain sensitive values such as `WECHAT_APPID` and `WECHAT_APPSECRET`.
- 中文：`.env`、`node_modules/`、`data/` 和日志文件都在 `.gitignore` 中，发布 skill 或打包时必须排除。
  English: `.env`, `node_modules/`, `data/`, and logs are in `.gitignore` and must be excluded from skill publication or packages.
- 中文：对外分发时只应包含 `config.example.env`，不要包含真实 `.env`。
  English: Public distributions should include only `config.example.env`, never a real `.env`.
- 中文：本项目不会把密钥写进代码，也不应在日志或 README 中粘贴真实凭据。
  English: This project does not write secrets into code, and real credentials should not be pasted into logs or README files.

## 添加素材来源 / Source Intake

中文：添加一个自定义链接，适合做链接翻译或链接改写：

English: Add a custom source URL for link translation or rewriting:

```bash
npm run source -- --url="https://example.com/article" --mode=translate --title="可选标题"
```

中文：添加一个手动原创选题：

English: Add a manual/original topic:

```bash
npm run source -- --title="你的选题" --mode=original --text="写作素材或要求"
```

中文：收集 AIHOT 精选条目作为可选选题来源：

English: Collect AIHOT featured items as optional topic sources:

```bash
npm run collect:aihot -- --limit=3
```

中文：素材命令会写入：

English: Source intake writes:

```text
data/pending.json
data/sources/<sourceId>.json
```

中文：随后由 Codex 生成文章文件：

English: Codex then creates:

```text
data/generated/<sourceId>.json
```

## 文章 JSON 格式 / Generated Article JSON

中文：生成文章默认要求提供 image2/imagegen 生成的本地封面图，也支持正文内图片。

English: Generated articles require a local image2/imagegen cover image by default and support inline body images.

```json
{
  "sourceId": "与输入素材一致的 sourceId",
  "title": "微信公众号标题",
  "digest": "摘要",
  "coverTitle": "封面主标题",
  "coverSubtitle": "封面副标题",
  "coverKeywords": ["关键词1", "关键词2"],
  "coverImagePath": "data/images/example-cover.png",
  "inlineImages": [
    {
      "placeholder": "{{inline_image:workflow}}",
      "path": "data/images/example-workflow.png",
      "alt": "流程示意图",
      "caption": "可选图片说明"
    }
  ],
  "contentHtml": "<section>...{{inline_image:workflow}}...</section>"
}
```

中文：`coverImagePath` 应指向基于标题和正文生成的 PNG/JPG 封面。`inlineImages` 中的正文图片也应是本地 PNG/JPG 文件。创建草稿时，脚本会上传正文图片并替换 `contentHtml` 中的占位符。

English: `coverImagePath` should point to a PNG/JPG cover generated from the title and article content. Body images in `inlineImages` should also be local PNG/JPG files. During draft creation, the script uploads body images and replaces placeholders in `contentHtml`.

## 校验与创建草稿 / Validate and Draft

中文：校验所有已生成文章：

English: Validate all generated articles:

```bash
npm run validate -- --all
```

中文：创建微信公众号草稿：

English: Create WeChat drafts:

```bash
npm run draft -- --all
```

中文：如果 `DRY_RUN=1`，脚本只会模拟执行和打印状态，不会真实创建草稿。

English: When `DRY_RUN=1`, the script only simulates execution and prints status; it does not create real drafts.

## Codex 自动化 / Codex Automation

中文：重复生产文章时，可以使用 `AUTOMATION.md` 中的提示词。建议先暂停自动化，直到 `.env` 配好且至少完成一次 dry run。

English: For repeated article production, use the prompt in `AUTOMATION.md`. Keep automation paused until `.env` is configured and at least one dry run has passed.

## 微信公众号后台要求 / WeChat Backend Requirements

- 中文：获取并填写 `AppID` 和 `AppSecret`。
  English: Get and fill `AppID` and `AppSecret`.
- 中文：把当前机器或服务器公网 IP 加入接口白名单。
  English: Add the current machine or server public IP to the API whitelist.
- 中文：确认草稿箱 API 权限可用。
  English: Confirm draft API permission is available.
- 中文：每篇文章默认必须提供 `coverImagePath`，封面图应由 image2/imagegen 生成并保存到 `data/images/`。
  English: Each article must provide `coverImagePath` by default; the cover should be generated with image2/imagegen and saved under `data/images/`.
- 中文：`WECHAT_THUMB_MEDIA_ID` 和 `DEFAULT_COVER_PATH` 只作为紧急静态封面兜底，且仅在 `ALLOW_STATIC_COVER_FALLBACK=1` 时启用。
  English: `WECHAT_THUMB_MEDIA_ID` and `DEFAULT_COVER_PATH` are emergency static-cover fallbacks only when `ALLOW_STATIC_COVER_FALLBACK=1`.
- 中文：正文图片必须是本地 PNG/JPG 文件；过大的正文图片会在上传前自动压缩。
  English: Body images must be local PNG/JPG files; oversized body images are compressed before upload.
- 中文：`WECHAT_AUTHOR` 要短，建议不超过 8 个中文字符，否则微信草稿 API 可能拒绝。
  English: Keep `WECHAT_AUTHOR` short, preferably within 8 Chinese characters, or the WeChat draft API may reject it.

## 微信 API 已知限制 / Known WeChat API Limit

中文：微信草稿 API 不开放后台的「创作来源」选择器。脚本会读取 `WECHAT_CREATION_SOURCE=个人观点，仅供参考` 并在创建草稿后提醒，但最终仍需要在微信公众号后台手动设置。

English: The WeChat draft API does not expose the backend "creation source" selector. The script reads `WECHAT_CREATION_SOURCE=个人观点，仅供参考` and prints a reminder after creating drafts, but the final selector still needs to be set manually in the WeChat backend.

中文：本项目不保存、不打印真实密钥。发布或分享前，请再次确认包内没有 `.env`、`data/`、`node_modules/` 和运行日志。

English: This project does not store or print real secrets. Before publishing or sharing, confirm again that the package does not contain `.env`, `data/`, `node_modules/`, or runtime logs.
