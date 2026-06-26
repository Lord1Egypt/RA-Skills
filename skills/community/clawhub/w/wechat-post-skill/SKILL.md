---
name: wechat-post-skill
homepage: https://github.com/jiao1yin2he3/wechat-post-skill
description: User-authorized WeChat Official Account article workflow for topic selection, drafting, editing, image planning, pre-publish review, and handoff to the user's configured WeChat publishing tool. Use when the user asks to 发公众号, 写公众号文章, 做公众号推送, or 发布草稿箱. Requires the user to provide and control any WeChat account access through environment variables or a vetted companion publisher.
metadata:
  openclaw:
    emoji: "📰"
    homepage: https://github.com/jiao1yin2he3/wechat-post-skill
    requires:
      env:
        - WECHAT_APP_ID
        - WECHAT_APP_SECRET
      anyBins:
        - bun
        - npx
    primaryEnv: WECHAT_APP_SECRET
    companionSkills:
      - baoyu-post-to-wechat
      - gemini-browser-image
    notes:
      - Requires a user-authorized WeChat Official Account environment.
      - This skill does not include publishing code or credentials; it orchestrates vetted companion tools.
---

# WeChat Post Skill

Use this skill to prepare a polished WeChat Official Account draft and hand it off to a user-authorized publishing tool. It is an orchestration workflow, not a credential manager and not a browser-control package.

## Safety boundaries

- Use only for the user's own WeChat Official Account or an account they are authorized to operate.
- Do not ask the user to paste secrets into chat. Use environment variables or an agent-managed private config controlled by the user.
- Do not store, print, commit, or publish AppSecret, tokens, cookies, browser profile data, or private account config.
- Do not publish final content without explicit user direction; default target is the WeChat draft box unless instructed otherwise.
- If API access is blocked by credentials, permissions, or IP allowlist settings, ask the user to fix account settings; do not bypass controls.
- Browser-based publishing or image generation is out of scope for this skill. If needed, use a dedicated companion skill in an isolated, user-controlled browser profile.

## Core workflow

1. **Pick topic**
   - If the user already gives a topic: use it directly.
   - If not: search current hot topics and offer 3 options.
   - Prefer topics with local relevance, clear public interest, conflict, usefulness, or share value.

2. **Write article**
   - Create an article folder under the project/workspace, e.g. `articles/YYYY-MM-DD-short-title/`.
   - Write `article.md` at roughly 900–1300 Chinese characters unless the user asks otherwise.
   - Include image placeholders in Markdown syntax only: `![](img0.png)`, `![](img1.png)`, etc.
   - Use a strong opening, varied paragraph rhythm, useful subheads, and a hard ending with a comment/share prompt.

3. **Humanize/self-edit**
   - Remove generic AI phrases, over-formal transitions, excessive bold, and excessive em dashes.
   - Keep the article concrete, local, useful, and conversational.
   - If an AI-humanizer skill/tool exists, use it for analysis and targeted revision.

4. **Prepare images**
   - Prepare or generate the article assets in the article folder:
     - `cover.png` — WeChat cover, 2.35:1 preferred.
     - `img0.png` … — body images, usually 16:9.
   - Use only image-generation tools explicitly available and authorized in the current environment.
   - For Gemini web UI image generation, use the separate `gemini-browser-image` companion skill rather than embedding browser instructions here.

5. **Self-review before draft handoff**
   - Verify image placeholders use `![](imgX.png)`.
   - Verify all referenced image files exist.
   - Verify no secrets, local-only credentials, cookies, or tokens are embedded in `article.md`.
   - Choose theme by topic:
     - tech/hard analysis: `modern`
     - finance/business/career: `grace`
     - emotion/life/soft topics: `simple`
     - controversy/hot news: `default`
     - unsure: `grace`

6. **Hand off to authorized publisher**
   - Use a vetted WeChat publishing companion tool when available, such as `baoyu-post-to-wechat`.
   - Confirm the required environment variables or private config already exist before running the publisher.
   - Do not print secret values. Only report whether required configuration is present or missing.
   - If publishing fails because of WeChat account settings, credentials, permissions, or IP allowlist, stop and ask the user to resolve those settings.

7. **Clean up**
   - Remove temporary generated-image downloads when safe.
   - Keep the article folder and source assets unless the user asks to delete them.

## Quality bar

- The article must have a clear traffic goal: clicks, saves, comments, shares, or follower growth.
- The first 100–300 characters must create tension, curiosity, usefulness, or emotional resonance.
- Every image must serve the article: cover for click-through, body images for pacing/comprehension.
- Never hand off for publishing before self-review.

## Optional references

- `references/content-playbook.md` — article structure, title/opening/ending patterns.
- `references/publishing-notes.md` — WeChat draft handoff checks and common failures.
