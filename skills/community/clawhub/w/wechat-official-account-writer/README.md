# 微信公众号写作发布助手 / WeChat Official Account Writer

中文：一个面向微信公众号创作者、技术博主、AI 资讯号、产品团队和内容运营的 Codex skill。它可以把一个主题、一段素材、一个链接或一组 AI 热点整理成可发布的公众号草稿，并支持封面图、正文插图、微信 HTML、发布前检查和草稿箱上传。

English: A Codex skill for WeChat Official Account creators, technical bloggers, AI-news writers, product teams, and content operators. It turns a topic, notes, a link, or AI-news items into a publish-ready WeChat draft, with cover images, body illustrations, WeChat HTML, pre-publish checks, and draft-box upload support.

## 能完成什么 / Capabilities

- 中文：从一句话主题生成公众号标题、大纲、正文和结尾。
  English: Generate WeChat titles, outlines, body copy, and endings from a short topic.
- 中文：把英文/中文链接翻译、消化、重组为原创中文公众号文章。
  English: Translate, digest, and reorganize English or Chinese links into original Chinese WeChat articles.
- 中文：把 AI 新闻、AI HOT 条目、产品发布、技术资料改写成适合公众号阅读的内容。
  English: Rewrite AI news, AI HOT items, product launches, and technical materials for WeChat readers.
- 中文：生成封面图和正文插图方案，并可使用 image2/imagegen 生成实际图片。
  English: Plan cover/body visuals and generate actual images with image2/imagegen.
- 中文：输出微信安全 HTML 和上传 JSON。
  English: Produce WeChat-safe HTML and upload JSON.
- 中文：调用内置 `wechat-article-workbench` 创建微信公众号草稿箱条目。
  English: Use the bundled `wechat-article-workbench` to create WeChat draft-box entries.
- 中文：做发布前检查，识别标题夸张、事实缺口、敏感表述、排版问题和读者理解断点。
  English: Run pre-publish checks for overpromising titles, factual gaps, sensitive phrasing, layout issues, and reader comprehension breaks.

## 适合谁用 / Who It Is For

- 中文：写技术长文、AI 热点解读、产品文章、教程文章和商业内容的公众号作者。
  English: WeChat writers creating technical posts, AI trend analysis, product articles, tutorials, or business content.
- 中文：希望从链接或材料快速生成原创中文稿件的内容团队。
  English: Content teams that want to turn links or materials into original Chinese drafts quickly.
- 中文：希望文章生成、配图、校验和草稿箱上传在一个流程内完成的 Codex 用户。
  English: Codex users who want writing, illustration, validation, and draft-box upload in one workflow.

## 基本用法 / Basic Usage

中文：在 Codex 中调用：

English: Invoke it in Codex:

```text
Use $wechat-official-account-writer 帮我把这个主题写成公众号文章，并生成封面图和正文插图。
```

中文：如果要创建真实草稿箱条目，先进入内置工作台：

English: To create real draft-box entries, enter the bundled workbench first:

```bash
cd scripts/wechat-article-workbench
npm install
cp config.example.env .env
```

中文：然后在 `.env` 中填写公众号配置，并先使用 `DRY_RUN=1` 验证。确认无误后再设置 `DRY_RUN=0` 创建真实草稿。

English: Fill the WeChat credentials in `.env`, validate first with `DRY_RUN=1`, then set `DRY_RUN=0` to create real drafts after everything looks correct.

## 隐私说明 / Privacy

中文：发布包只包含 `config.example.env`，不会包含真实 `.env`。`.env`、`node_modules/`、`data/` 和日志文件应始终保留在本地，不要上传到公开平台。

English: The published package includes only `config.example.env`, not a real `.env`. Keep `.env`, `node_modules/`, `data/`, and logs local; do not upload them to public platforms.

中文：本 skill 只负责创建草稿箱条目，不会直接发布文章。微信公众号后台的原创声明、创作来源、最终排版和发布动作仍需要人工确认。

English: This skill only creates draft-box entries. Originality declarations, creation source, final layout, and publishing still need to be confirmed manually in the WeChat backend.
