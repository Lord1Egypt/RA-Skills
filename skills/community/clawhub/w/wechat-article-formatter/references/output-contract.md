# Output Contract

## Purpose

Use this contract when the output must be copied into the WeChat Official Account backend or handed off as article-body HTML.

## Required Body Shape

Use this wrapper for the final article body:

```html
<article id="wechatArticle">
  <!-- article body -->
</article>
```

If a preview page is generated, keep the real article body isolated inside this node so it can be copied or extracted directly.

## Preview Shell Rule

When generating a full HTML preview file, use the Python script `scripts/generate_preview.py` which automatically includes preview controls outside `article#wechatArticle`:

- a theme switcher that lists all supported presets from `theme-presets.md`;
- a `复制到公众号` copy action;
- a small status message for copy success or failure.

The copy action must target `article#wechatArticle`, copy rich HTML when the browser supports it, and keep a plain-text fallback available.
Preview controls, toolbar CSS, and preview JavaScript must not be nested inside `article#wechatArticle`.
The preview file must be self-contained. Theme presets, component styles, toolbar CSS, and toolbar JavaScript must be embedded in the generated HTML rather than shipped as required sidecar files.

## HTML-First Rule

- Treat HTML as the final working format.
- Markdown can be an upstream source, but not the required final form.
- Do not ship a result that depends on client-side JavaScript to finish rendering core content.

## Copy-Ready Rule

- Keep the final body clean and article-focused.
- Exclude preview controls, testing widgets, debug text, and unrelated page scaffolding from the copy target.
- Use stable structure that survives copy-paste into rich-text editors.
- If a preview shell exists, the selected theme must be materialized into inline styles on the copied `article#wechatArticle`.

## Image Rule

- Keep image sources static in the HTML.
- Do not rely on runtime scripts to assign `img.src`.
- Preserve source-backed `figure`, `img`, and `figcaption` structure when article images are already selected by the writing step.
- Keep captions close to their images and avoid moving source attribution away from the related image.
- For copy-ready output, prefer `data:image/*` or stable HTTPS image URLs. Do not leave local relative paths in final HTML.

## Handoff Rule

- Default body selector: `article#wechatArticle`
- If the user provides another selector, keep it explicit in the handoff.
