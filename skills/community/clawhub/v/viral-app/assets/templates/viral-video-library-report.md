# Viral Video Library Report Template

Recommended filename: `viral-video-library-report.md`

Use this template for Slack-ready reports based on Viral Video Library results.

## Instructions

- Use linked titles in the form `[Name](https://viral.app/app/library/viral-videos/<platformSlug>/<platformVideoId>)`.
- Use abbreviated metrics, for example `473K` and `18.2%`.
- Include a hashtags line for every entry.
- Use a single hook line in the form:
  `**Hook (<hookArchetype>):** summary using text + visual + audio`
- Avoid the phrase `Audio not surfaced`.
- Do not invent fields when data is missing; use `not confidently detected`.
- Use the compact version when Felix asks for a paste-friendly Slack report.

## Link format to use

```text
https://viral.app/app/library/viral-videos/<platformSlug>/<platformVideoId>
```

Use `platformSlug` values like:

- `tiktok`
- `instagram`
- `youtube`

---

## Full Template

Copy this block and replace placeholders.

```md
# Viral Video Library Report — {{reportTitle}}

**Scope:** {{scopeDescription}}
**Date:** {{reportDate}}
**Filters:** `{{filters}}`
**Sort:** `{{sortBy}}`

{{note}}

{{#each videos}}
## {{video.rank}}) [{{video.accountDisplayName}}](https://viral.app/app/library/viral-videos/{{video.platformSlug}}/{{video.platformVideoId}})
- **{{video.viewCountHuman}} views** • **{{video.likeCountHuman}} likes** • **{{video.engagementRateHuman}} ER**
- **Hashtags:** `{{video.hashtags}}`
- **Hook ({{video.hookArchetype}}):** {{video.hookSummary}}
- **Brand/Product:** {{video.brandProductLine}}
- **Match Terms:** {{video.matchedTermsLine}}
- **Published / Region:** {{video.publishedAt}} / {{video.region}}

{{/each}}

## Top Gainers / Highlights (if requested)
{{gainerNotes}}

## Suggested Actions
- **Content angles to test:** {{contentAngleSuggestions}}
- **Promising hooks:** {{hookSuggestions}}
- **Potential brand targets:** {{brandTargets}}
```

Notes for placeholder values:

- `video.brandProductLine` should already be rendered as either:
  - `[Brand](brandLink) / [Product](productLink)`
  - `not confidently detected`
- `video.matchedTermsLine` should already be rendered as either:
  - `` `term1, term2` ``
  - `—`
- `note` may be omitted entirely if there is no note for the report.

---

## Compact Version

Use this when Felix wants a paste-friendly Slack report.

```md
{{#each videos}}
{{video.rank}}) **[{{video.accountDisplayName}}](https://viral.app/app/library/viral-videos/{{video.platformSlug}}/{{video.platformVideoId}})** — {{video.viewCountHuman}} • {{video.likeCountHuman}} • {{video.engagementRateHuman}} | {{video.hashtags}}
   **Hook ({{video.hookArchetype}}):** {{video.hookSummary}}
   **Brand/Product:** {{video.brandProductLine}}

{{/each}}
```
