# LinkedIn post research standards

## Rankizz tool contract

Use `search_social_research` with:

- `platform`: `linkedin`
- `queries`: 1-20 query strings in one provider search
- `filters.datePosted`: `any`, `last-hour`, `last-day`, `last-week`, `last-month`, or `last-year`

One provider search costs one Rankizz credit. Paid MCP and API calls require at least 10 credits in the account before the call. The response includes `runId`, `searchedAt`, `creditsCharged`, `nextCursor`, and results with fields such as URL, title, description, author, published date, community, media, and nullable views, likes, comments, or score.

Use `list_social_research_history` to reuse saved runs when suitable. Do not delete history unless the user explicitly asks.

## What official guidance supports

- LinkedIn asks members to be authentic, constructive, and truthful, and to make a personal or financial benefit clear when endorsing a product: <https://www.linkedin.com/legal/professional-community-policies>
- LinkedIn's AI-content guidance favors the member's real voice, perspective, and experience over generic, recycled, low-effort content: <https://www.linkedin.com/help/linkedin/answer/a1481496>
- LinkedIn describes feed relevance as a combination of professional interests, profile and activity context, freshness, engagement, and sequential behavior. This is a multi-signal system, not a public writing formula: <https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed>
- LinkedIn has described dwell time as one signal used to improve feed quality and relevance: <https://www.linkedin.com/blog/engineering/feed/leveraging-dwell-time-to-improve-member-experiences-on-the-linkedin-feed>
- LinkedIn's sharing guide recommends useful professional insight, a point of view, timely topics, quick attention, conversation, and visual media when it adds value: <https://content.linkedin.com/content/dam/help/linkedin/en-us/LinkedIn-Sharing-Guide.pdf>
- LinkedIn's Page guidance emphasizes original, educational content and genuine responses to feedback: <https://business.linkedin.com/content/dam/lem/business/en/advertise/linkedin-pages/lms-linkedin-page-posting-best-practices-one-pager.pdf>
- The FTC says material relationships should be disclosed clearly and conspicuously. When an author owns, works for, or benefits from the featured app, plain relationship language is safer than a vague label: <https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers>

## Research interpretation

Treat Rankizz results as a bounded editorial sample. Compare only reasonably similar posts and state the search window. Raw likes or comments are not an engagement rate, and a post's appearance in search does not prove causation.

Separate:

- **Observed:** visible wording, format, date, and public metrics.
- **Inferred:** why the format may have worked for that audience.
- **Recommended:** how the user can express a distinct, evidence-backed point of view.

## Human-writing check

Remove generic scene-setting, stacked suspense fragments, fake quotations, hype, copied cadence, decorative em dashes, and repetitive conclusions. Keep the author's real terminology, defensible specifics, ordinary contractions, natural sentence variation, honest uncertainty, and a useful takeaway before any product mention.
