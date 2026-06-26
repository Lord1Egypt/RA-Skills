# Execution Spec

This file defines the self-contained execution model for the `welight-wechat-layout-publish` skill.

Do not treat this as a repository map. Treat it as the skill's built-in operating contract.

## Input Modes

The skill should support three input modes:

- pasted article text
- local file content
- article URL

For URL mode, the skill should try to extract:

- title
- author if available
- publish time if available
- clean article body
- lead image if available

If extraction is partial, continue with the usable content and state what metadata is missing.

Recommended command:

- `python3 scripts/normalize_to_markdown.py --url 'https://example.com/article' --output article.md --meta-output article.meta.json`

## Markdown Normalization Rules

When the source is not already good Markdown, normalize it using these rules:

1. Preserve the original meaning and factual structure.
2. Rebuild headings so the document has a clear top-down structure.
3. Merge hard line breaks inside paragraphs.
4. Convert bullet-like text into Markdown lists.
5. Convert obvious callouts or quoted passages into blockquotes.
6. Remove obvious boilerplate such as:
   - share hints
   - follow-us footers
   - navigation labels
   - ad-like fragments
7. Keep links when they matter to the article context.
8. Keep image positions if image URLs are present and useful.

## Theme Presentation Rules

Theme choices must come from [theme-catalog.md](./theme-catalog.md).
The executable theme source is `../assets/theme-pack.json`.

When listing themes for the user:

- show theme id
- show Chinese theme name
- show the short style description

Preferred display shape:

`w001 玉兰 - 经典主题`

If the user asks for recommendations, recommend only from the built-in catalog and tie the recommendation to the article tone.

## Theme Application Rules

After a theme is selected:

1. Keep the Markdown source unchanged except for necessary formatting cleanup.
2. Apply the theme at render/export time by running `scripts/render_wechat_html.py`.
3. Generate WeChat-friendly HTML that avoids fragile or unsupported constructs.
4. Prefer predictable typography and shallow layout structure over overly complex visual tricks.

Recommended commands:

- normalize source:
  `python3 scripts/normalize_to_markdown.py --input article.html --output article.md`
- list themes:
  `python3 scripts/list_themes.py`
- render themed HTML:
  `python3 scripts/render_wechat_html.py --theme w022 --input article.md --output article.wechat.html`

## Publish Decision Rules

Use draft publish by default.

Use formal publish only when:

- the user explicitly asks for it
- publishing prerequisites are already configured
- the account capability supports formal publish

When prerequisites are missing, do not pretend the publish succeeded. State the exact missing prerequisite.

Recommended command:

- dry run:
  `python3 scripts/publish_wechat.py --html article.wechat.html --mode draft --dry-run`
- real publish:
  `python3 scripts/publish_wechat.py --html article.wechat.html --config wechat.json --mode draft`
