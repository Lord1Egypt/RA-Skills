# Image and Draft Upload Integration

## Bundled Uploader

Use the bundled uploader when the user wants a WeChat draft-box entry:

```text
scripts/wechat-article-workbench
```

Resolve this path relative to this skill's root directory.

## First-Time Setup

Run these commands inside `scripts/wechat-article-workbench`:

```bash
npm install
cp config.example.env .env
```

Then edit `.env`:

```bash
WECHAT_APPID=...
WECHAT_APPSECRET=...
WECHAT_AUTHOR=短作者名
WECHAT_CREATION_SOURCE=个人观点，仅供参考
ALLOW_STATIC_COVER_FALLBACK=0
DRY_RUN=1
```

WeChat backend prerequisites:

- Official Account `AppID` and `AppSecret`.
- The machine/server public IP added to the WeChat API whitelist.
- Draft API permission enabled.
- `WECHAT_AUTHOR` short enough for the WeChat API, usually 8 Chinese characters or fewer.

Keep `DRY_RUN=1` until article JSON and images validate. Set `DRY_RUN=0` only when creating real draft-box entries.

Core commands:

```bash
npm run source -- --url="https://example.com/article" --mode=translate
npm run source -- --title="选题" --mode=original --text="写作要求或素材"
npm run validate -- --all
npm run draft -- --all
```

The uploader stops at the WeChat draft box. Publishing remains manual. After draft creation, remind the user that the WeChat backend `创作来源` selector still needs to be set manually to `个人观点，仅供参考` if that is the intended setting.

## Generated JSON Schema

Write one JSON file per source:

```text
scripts/wechat-article-workbench/data/generated/<sourceId>.json
```

Shape:

```json
{
  "sourceId": "same as source",
  "title": "微信公众号标题，建议28字以内",
  "digest": "80-120字以内摘要",
  "coverTitle": "封面主标题，短",
  "coverSubtitle": "封面副标题，说明文章价值",
  "coverKeywords": ["关键词1", "关键词2", "关键词3"],
  "coverImagePath": "必填，本地PNG/JPG路径，由 image2/imagegen 基于标题和正文生成，例如 data/images/source-cover.png",
  "inlineImages": [
    {
      "placeholder": "{{inline_image:workflow}}",
      "path": "data/images/source-workflow.png",
      "alt": "图片替代文本",
      "caption": "可选图片说明"
    }
  ],
  "contentHtml": "<section>...{{inline_image:workflow}}...<section>底部关注引导</section></section>"
}
```

Do not set `author` or `content_source_url`; the uploader uses `.env` for author and intentionally avoids the original-link field. Do not create a draft without `coverImagePath` unless the user explicitly enabled the static fallback.

## Body HTML Rules

- Use clean inline-styled HTML, not Markdown, for upload JSON.
- Use short paragraphs and clear section headings.
- Do not include visible `来源：`, `原文链接：`, `参考链接`, or `个人观点 仅供参考`.
- Do not include external `<img>` tags. Put placeholders in `contentHtml` and define them in `inlineImages`.
- Add a bottom follow CTA for publish-ready WeChat drafts unless the user explicitly asks to omit it. Keep it short, natural, low-pressure, and visually plain.
- Avoid card-like boxes, bordered summary panels, table-style blocks, large colored callouts, and heavy rounded containers in body HTML unless the user explicitly asks for them. They can render awkwardly in WeChat. Use plain headings, paragraphs, simple numbered points, and whitespace instead.
- Keep copied source text short. Summarize, reorganize, and add analysis.

Bottom CTA examples:

```html
<section style="margin: 30px 0 0; color: #4b5563;">
  <p style="margin: 0 0 8px;">如果你关注 AI 产品、技术趋势和真实落地，欢迎点个关注。</p>
  <p style="margin: 0;">我会继续用更少废话，把值得看的变化讲清楚。</p>
</section>
```

## Image Workflow

When preparing a draft-box upload:

1. Use the `imagegen` skill/tool to generate a cover through the available image2/imagegen path.
2. Save final project-bound images under:

   ```text
   scripts/wechat-article-workbench/data/images/
   ```

3. For cover images, set `coverImagePath`; this is required by default.
4. For body images / article stickers, decide from the content whether to generate none, one, or multiple images. When useful, insert placeholders such as `{{inline_image:workflow}}` or `{{inline_image:key_takeaway}}` in `contentHtml`, then add matching `inlineImages` entries. Use image2/imagegen for these images; do not leave them as external URLs.
5. Run `npm run validate -- --all` before draft upload.

Prompt cover images as clean editorial visuals:

- no watermark
- no UI chrome unless relevant
- no tiny text
- leave negative space for WeChat crop and title overlays
- match the article's actual subject, not a generic AI gradient
- use a strong visual metaphor or concrete scene derived from the article's main argument

Prompt body images as explanatory visuals:

- for technical articles: polished architecture diagram, workflow visual, system map, product-use scene, timeline, or concept diagram
- for non-technical articles: editorial illustration, symbolic scene, comparison, timeline, or visual metaphor
- avoid decorative images that do not add meaning
- no external brand logos unless user provided permission or the article requires them
- avoid tiny in-image text; if labels are necessary, keep them few and large
- place images after sections where they summarize or clarify the idea, not before the reader has context

## Original vs Link Workflows

### Original AI + Skill Writing

Use when the user gives a topic, audience, notes, or desired position.

1. Add a manual source if draft upload is requested:

   ```bash
   npm run source -- --title="选题" --mode=original --text="用户素材或写作要求"
   ```

2. Read the created `data/sources/<sourceId>.json`.
3. Generate an original article around one reader promise.
4. Add article-internal images only when they improve comprehension, pacing, or shareability. It is valid to use no body image when the draft reads better as text.
5. Add a bottom follow CTA unless the user asks to omit it.
6. Write `data/generated/<sourceId>.json`, validate, then draft if requested.

### Link Translation / Rewrite

Use when the user provides URLs.

1. Add a URL source:

   ```bash
   npm run source -- --url="https://example.com/article" --mode=translate
   ```

2. Read the extracted source JSON.
3. Do not translate paragraph-by-paragraph. Reorganize into a Chinese public-account article.
4. Keep direct quotes short and only when needed.
5. Add context, explanation, and the user's likely reader angle.
6. Decide whether article-internal images help; add none, one, or multiple images accordingly. Add a visually plain bottom follow CTA when preparing a publish-ready draft.
7. Do not expose source attribution text in the visible article body unless the user explicitly asks for it.
