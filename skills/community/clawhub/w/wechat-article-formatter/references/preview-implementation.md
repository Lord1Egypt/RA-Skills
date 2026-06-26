# Preview Page Contract

When generating a complete HTML preview file, **you MUST use the local Python script `scripts/generate_preview.py`** instead of generating the outer HTML shell from scratch or manually replacing template placeholders. The HTML template is now modularized to prevent context bloat.

## Using the Preview Generator Script

1. Generate your dynamic article content (HTML with `data-role` attributes). Save it to a temporary file (e.g., `dist/temp_content.html`).
2. Run the python script to generate the final HTML. The script inlines built-in theme and component style data by default, so the deliverable is a single transferable `.html` file:
   ```bash
   python skills/wechat-article-formatter/scripts/generate_preview.py --title "Your Article Title" --content dist/temp_content.html --output dist/preview.html
   ```
   To automatically prompt the user to open the output HTML in their default browser after generation, append the `--open` flag:
   ```bash
   python skills/wechat-article-formatter/scripts/generate_preview.py --title "Your Article Title" --content dist/temp_content.html --output dist/preview.html --open
   ```
   Alternatively, you can run the standalone [open_preview.py](../scripts/open_preview.py) script on the output file to prompt and open it:
   ```bash
   python skills/wechat-article-formatter/scripts/open_preview.py dist/preview.html
   ```
3. (Optional) If a task explicitly needs custom theme or style JSON for experimentation, pass `--themes` or `--styles`. These files are build inputs only; do not deliver them as companion files. **Crucially, any custom `styles` JSON object MUST contain exactly the following keys**:
   - `article`, `hero`, `eyebrow`, `moduleLabel`, `h1`, `dek`, `p`, `section`, `h2`, `h3`, `quote`, `quoteText`, `figure`, `image`, `figcaption`, `callout`, `calloutTitle`, `ul`, `ol`, `li`, `summary`, `summaryTitle`, `summaryText`, `table`, `th`, `td`, `code`, `pre`, `strong`, `a`, `hr`.
   - The `h1` and `h2` styles must not include `border-bottom`, `text-decoration: underline`, or underline-like full-width bottom rules. Use color, font weight, spacing, or small inline markers for heading emphasis instead.
   - For the default `warm-editorial` theme, style values should support a warm long-read rhythm: `h2` around `20px`, `p` around `16px / 1.8`, compact monospace `eyebrow` and `moduleLabel`, serif quote text, and wrapped table/code content.
4. Clean up temporary input files after successful generation when they are no longer needed.

## Toolbar and Copy Behavior (Handled by Template)

The generated HTML automatically provides a compact toolbar outside `article#wechatArticle`. Its built-in functionality includes:
- A theme switcher listing every supported preset.
- A "复制到公众号" (Copy to WeChat) action.
- Automatic copying of `article#wechatArticle` as rich HTML.
- Self-contained image inlining during copy time: It clones the article and attempts to inline readable images as `data:image/*;base64,...` URLs (local images, blob URLs, and CORS-readable network images). 
- If an image cannot be inlined, it keeps the original static `src` and shows a status message.
- If clipboard APIs fail, it provides a visible status message for manual copying.

The final preview must not require adjacent `.json`, `.css`, `.js`, or font files. Everything required to open, preview, switch themes, and copy the article is embedded into the single HTML file.

Do not recreate or modify the outer HTML structure or the script logic when outputting the final file, unless explicitly requested. Keep all your generated content strictly focused on the article body.
