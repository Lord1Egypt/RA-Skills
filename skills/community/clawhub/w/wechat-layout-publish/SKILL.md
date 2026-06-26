name: welight-wechat-layout-publish
description: Welight standalone skill for turning an article into WeChat Official Accounts compatible Markdown/HTML, presenting built-in theme choices, and publishing to WeChat as a draft or formal post when publishing prerequisites are already configured.
---

# Welight WeChat Layout Publish

Use this skill as a self-contained OpenClaw capability for:

- obtaining article content from user input, local files, or a URL
- normalizing non-Markdown content into clean Markdown
- presenting real built-in theme options to the user
- applying the selected theme to produce WeChat-friendly output
- publishing to WeChat Official Accounts when the required credentials and publishing tools are already configured in the runtime

This skill must not depend on any specific local product codebase. Treat the instructions and references inside this skill folder as the complete operating guide.

## Built-In Runtime

This skill includes its own minimal rendering runtime:

- `scripts/normalize_to_markdown.py`
  - normalizes pasted text, HTML files, or article URLs into Markdown
- `scripts/list_themes.py`
  - prints the built-in theme list from the skill assets
- `scripts/render_wechat_html.py`
  - renders Markdown into WeChat-friendly HTML with inline styles
- `scripts/publish_wechat.py`
  - publishes the rendered HTML to WeChat Official Accounts when the runtime already has valid credentials and network access
- `assets/theme-pack.json`
  - the built-in theme token pack used by the renderer

After the user selects a theme, the expected execution path is:

1. normalize the article into Markdown with `scripts/normalize_to_markdown.py`
2. list or validate the theme with `scripts/list_themes.py`
3. render themed HTML with `scripts/render_wechat_html.py --theme <theme_id>`
4. publish the rendered HTML with `scripts/publish_wechat.py`

## Capability Contract

When invoked, this skill should aim to complete the following end-to-end flow:

1. Accept one of these inputs:
   - raw article text
   - a file containing article content
   - a URL that points to an article
2. Extract or rewrite the source into clean Markdown if it is not already usable Markdown.
3. Keep that Markdown as the canonical source of truth.
4. Read the built-in theme list from [references/theme-catalog.md](./references/theme-catalog.md).
5. Present the available themes in a compact format:
   `theme id + theme name + short style description`
6. If the user did not specify a theme:
   - ask the user to choose, or
   - recommend 3 to 5 themes from the built-in catalog only
7. Apply the selected theme to the Markdown and generate WeChat-compatible HTML.
8. If publishing prerequisites are already configured, continue to draft publish or formal publish.

## Working Rules

1. Never invent unsupported themes.
   - Only use theme ids listed in [references/theme-catalog.md](./references/theme-catalog.md).
   - Always preserve the real theme id in the output so the user can see exactly what was chosen.

2. Normalize content before styling.
   - If the source is plain text, HTML, rich text, OCR output, copied chat content, or scraped article content, first rewrite it into structured Markdown.
   - Preserve meaning. Improve hierarchy, paragraphing, headings, lists, quotes, and emphasis, but do not silently change the argument or facts.

3. Treat Markdown as the editable master.
   - Theme application and WeChat export happen after Markdown normalization.
   - If the user wants revisions, revise the Markdown first and then regenerate themed output.

4. Make theme selection explicit.
   - Show real choices before publishing.
   - If recommending themes, explain the recommendation in one short sentence each.
   - Keep recommendations inside the built-in catalog.

5. Produce WeChat-safe output.
   - Flatten overly complex nesting.
   - Avoid unsupported layout patterns.
   - Prefer predictable heading structure.
   - Keep list nesting shallow.
   - Ensure images use valid URLs and are suitable for WeChat-side upload or replacement.

6. Publish only when prerequisites already exist.
   - Required publishing prerequisites are described in [references/publish-spec.md](./references/publish-spec.md).
   - If the runtime lacks configured WeChat credentials, upload capability, or publish capability, stop and state exactly which prerequisite is missing.

## Standard Workflow

1. Determine the source.
   - User pasted article text
   - User gave a file
   - User gave a URL

2. Acquire the content.
   - If the content comes from a URL, extract the article body and metadata when possible.
   - If the content comes from a file, read and interpret it according to type.

3. Normalize to Markdown.
   - Create a readable heading hierarchy.
   - Merge broken lines into paragraphs.
   - Convert visual bullets into Markdown lists.
   - Convert emphasized phrases into Markdown emphasis.
   - Remove obvious navigation junk, ads, or unrelated footer text.

4. Prepare theme choice.
   - Read [references/theme-catalog.md](./references/theme-catalog.md).
   - List all available themes or a narrowed recommendation set.
   - Wait for the user to choose if the task requires explicit confirmation.

5. Apply the chosen theme.
   - Keep the selected theme id visible in the result.
   - Generate WeChat-friendly HTML from the Markdown plus theme by using `scripts/render_wechat_html.py`.

6. Publish if requested.
   - Follow [references/publish-spec.md](./references/publish-spec.md).
   - Use [references/runtime-config.md](./references/runtime-config.md) for the standalone script interfaces.
   - Prefer draft publish unless the user explicitly asks for formal publish and the account supports it.

## Output Expectations

Optimize for one of these outcomes:

- Clean Markdown generated from messy or non-Markdown source material
- A compact list of real available themes for user selection
- A recommended shortlist of real themes that fit the article tone
- WeChat-compatible themed HTML derived from the Markdown
- A successful WeChat draft publish
- A successful WeChat formal publish
- A precise explanation of which publishing prerequisite is missing or failing

## Validation

- Confirm the article is normalized into Markdown before styling.
- Confirm the chosen theme id exists in the built-in catalog.
- Confirm the generated output is suitable for WeChat rendering.
- For publishing, verify the sequence in [references/publish-spec.md](./references/publish-spec.md).
- If publishing fails, report the exact step that failed and the exact missing condition or error code.
