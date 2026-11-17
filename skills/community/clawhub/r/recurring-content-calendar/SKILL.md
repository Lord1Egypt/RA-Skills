---
name: recurring-content-calendar
description: Build and run a recurring social content calendar — designed carousels, single-image posts, and short videos, written fresh each run and scheduled ahead to LinkedIn, Instagram, TikTok, and Threads. Use this skill whenever the user wants a content calendar, a daily or weekly posting routine, automated or scheduled social posts, recurring content for their brand, or carousels and short-form video for social — and whenever they mention PostNitro, which is the publishing engine this skill drives. Also use it to audit why previously scheduled posts failed to publish.
---

# Recurring content calendar

Stand up a content calendar that keeps running: each run writes new posts, designs them, and places them in future publish slots, while checking that the last batch actually went live.

Publishing runs on **PostNitro** (carousels, single-image posts, short videos → LinkedIn, Instagram, TikTok, Threads). Sections 1–8 are specific to it. If the user wants a calendar on a different publishing tool, the intake, content, dedup, and audit logic still apply, but the tool-call mechanics do not.

Three layers to keep separate:

- **Config** (section 0) — the user's brand, accounts, cadence, timezone, voice, topics. Captured per user, never hardcoded into this file.
- **API constraints** (sections 2–8, and whatever the live schema says) — real limits. Breaking one returns an error.
- **House rules** — editorial and defensive choices that the API would happily let you break. Each is marked where it appears. A user setting this up for their own brand may change any of them; an agent mid-run should not.

The house rules, so a new user can see them in one place: the 50-second video ceiling, LinkedIn carousels as `document`, always filling TikTok `postTitle`, passing `postSettings` on every scheduled reel, `DESIGN` output rather than PDF/PNG, the slide and caption formatting tags, and the async import-then-poll pattern. All exist because something broke without them.

**Look up live tool schemas every run** rather than trusting parameter names remembered from a previous session. Never carry another workspace's IDs, API keys, publish times, or captions into this one — every value below comes from the user or from a live tool call.

## 0. Config

This is the whole per-user surface. Fill it during intake, echo it back in the recap, and store the filled version with the saved routine so later runs don't re-interview.

```
BRAND            — what is being promoted (company/product/person + one line on what it does)
AUDIENCE         — who the posts are for
VOICE            — educational tips (default) | product-led | founder-personal | other
LANES            — 5–8 recurring topics (derive from BRAND + AUDIENCE, see section 3)
ACCOUNTS         — the specific social account IDs to publish to
POSTS_PER_DAY    — distinct posts created per run
JOB_TIME         — clock time the routine runs (creation time, not publish time)
WINDOWS          — one publish window per daily post
DAYS             — weekdays only | all 7
TIMEZONE         — user's timezone (offset recomputed per run)
FORMAT_MIX       — how carousel / image / video rotate
IG_STORY         — feed only | feed + story
STATUS           — DRAFT while testing, SCHEDULED after approval
TEMPLATE/BRAND/PRESET IDs — from section 2
```

### Intake

Ask **one question at a time**, skipping anything already answered in this chat. Use a question widget when there are a few real options. Do not assume a cadence, timezone, voice, or account list.

**Required before anything goes live:** API key (if not already connected), `ACCOUNTS`, `POSTS_PER_DAY`, `JOB_TIME`, `WINDOWS`, `DAYS`, `TIMEZONE`.

**Ask, but take these defaults if they say "you pick":** `VOICE` educational; `FORMAT_MIX` rotate so a week covers all three formats; `IG_STORY` feed + story; `STATUS` draft test first; `LANES` derived from `BRAND` and `AUDIENCE`.

`BRAND` and `AUDIENCE` are the ones most likely to be assumed wrongly — ask for them explicitly rather than inferring from the connected accounts' names. Do not import or schedule until the required items are answered. Then recap the filled config in one short message and wait for a yes.

## 1. Connect the publishing tool

Publishing runs through PostNitro. If it is not connected, it is usually absent from the catalog, so add the remote server:

- URL: `https://mcp.postnitro.ai/mcp`
- Header: `Authorization: Bearer <pn- key>`

Confirm with the user, then add. The key lives at PostNitro profile → Embed → Generate API Key, and starts with `pn-`. Tools appear on the next message, not immediately.

At **first setup only**, refresh capability facts from `https://postnitro.ai/llms-full.txt` or `https://postnitro.ai/facts` — which platforms publish natively, which post formats exist. Re-check if a platform or format later behaves unexpectedly, or if `BRAND` happens to be PostNitro itself. This is not worth fetching on every run of a daily routine; the live tool schemas are the authority for anything an API call depends on.

## 2. Discover the workspace

List templates, brands, AI presets, social accounts, audio, and saved defaults. Page if needed.

**Check defaults every run.** Call the get-defaults tool. If it returns `hasDefaults: false`, defaults are NOT set — pass `templateId`, `brandId`, and `responseType` explicitly on every import that run. Never assume defaults exist because you offered to save them earlier; a save can be wiped between runs.

If there is exactly one template / brand / preset, offer to save them as defaults with `DESIGN` (do not switch to PDF unless the user needs file URLs). `MP4` cannot be stored as a default — pass it per call on the video tools, where a saved `PDF`/`PNG` default is treated as `DESIGN` anyway.

Show the social accounts you found and ask which to use. Store those IDs as `ACCOUNTS` — they are needed for scheduling **and** for the history/dedup query. If a platform in the plan turns out not to be connected, say so and skip it rather than failing the run.

## 3. Content rules

Content should solve a problem the `AUDIENCE` recognizes: strategies, tactics, specifics. `BRAND` is how you *run* the tactic, not the subject of a feature dump. No generic self-promo, no founder-personal voice unless `VOICE` says so.

**Deriving `LANES`:** from `BRAND` + `AUDIENCE`, propose 5–8 recurring topics the brand can credibly own, each narrow enough to yield many distinct posts. Show the list and let the user cut or add. Rotate through them so consecutive posts sit in different lanes. As illustration only — a project-management tool for agency owners might run: scoping, client comms, pricing, capacity planning, handoffs, retros, tool stacks.

**Structure**

- **Carousel / video (5–7 slides or scenes):** 1 `starting_slide`, 1 `ending_slide`, 3–5 `body_slide`s. First slide moderate (curiosity), last slide moderate (close + where the brand fits), body elaborates.
- **Single image:** one slide object (not an array), no slide `type`. Only `heading` is required; add `sub_heading`, `description`, `cta_button` as needed. One complete thought. Infographic layout is allowed on this single slide.
- Infographics where they help. Call the import-template tool first for the exact structure.
  - `layoutType: infographic` replaces the image.
  - `cycle`: sequential, counters, **all items in the first column**.
  - `grid`: comparison, max 3 columns.
  - Caller-provided `id`s on every column and item. Item `description` is HTML.

### Formatting reference

PostNitro's own markup, not markdown. An agent that reaches for `**bold**` or a real newline produces slides and captions with literal junk in them, so treat this as the complete allowed set. None of it appears in the import schema — the schema accepts any string — so do not "correct" these tags toward something that looks more standard.

**Slide text** (`heading`, `sub_heading`, `description`, `cta_button`) accepts:

| Tag | Use | Limit |
| --- | --- | --- |
| `<strong>` | The single most important phrase on the slide | Max one per slide |
| `<em>` | Light emphasis, a term being introduced | Sparingly |
| `<u>` | Underline | Sparingly; never inside `<c>` |
| `<c>` | Brand-colour highlight on headline words | 1–3 words per headline; never combined with `<u>` |
| `<br/><br/>` | Paragraph break | The only way to break a line |

Restraint is the point: a slide with three highlighted phrases reads as noise. One `<c>` on the hook and one `<strong>` in the body is a fully formatted slide.

**Infographic item descriptions** are HTML, not plain text, and want a wrapped paragraph: `<p dir="ltr">3–5 posts per week</p>`. A bare string may render unstyled. Column and item `id`s are caller-provided and never auto-generated.

**Captions** are one single line of plain text — see section 5. No markdown, no real newlines, `<br/><br/>` for breaks. The slide tags above do **not** apply in captions; `<strong>` in a caption publishes as visible characters on every platform. Hashtags are extracted automatically, so write them inline where they belong.

**Everything else is out.** No markdown headers, lists, links, or code formatting. No emoji as structural markup (as decoration in copy is a voice decision, not a formatting one). No single `<br/>` — the double form is the break.

**CTA rotation:** one CTA per post, differing from the most recent post (Save / Share / Follow). Use "Follow" sparingly, roughly 1 in 3. No engagement bait, no fake urgency.

**Write copy in chat and lock it before importing**, unless the user has already approved an ongoing pipeline.

## 4. Import

You write the copy. Import onto the saved template/brand, or the explicit IDs from section 2 when no defaults are set.

**Use the async import pattern.** Wait/synchronous convenience tools can take 15–60s and time out at the transport layer while the job keeps running server-side — so a retry after a timeout creates duplicate designs. Instead:

1. Call the async import tool (`import_carousel` / `import_image` / `import_video`) — it returns an `embedPostId` immediately.
2. Poll `check_status` with that `embedPostId` until `COMPLETED`, or until a step reports `FAILED`.
3. Call `get_output` to read the `designId` (and file URLs if PNG/PDF).

On a timeout, **poll — never re-call the import**. On a 429, wait ~15–55s and retry the same call.

- **Carousel:** `slides` array — exactly 1 `starting_slide` first, at least 1 `body_slide`, exactly 1 `ending_slide` last. Minimum 3 slides; `type` and `heading` are the only required fields per slide.
- **Video:** same `slides` array, each slide a scene. Duration and audio are set once in `videoSettings`, never per slide. `videoDuration` is variable, ≥5s per scene where it fits, and **capped at 50s** — the API accepts anything under 60, but 50 is the deliberate house ceiling, so do not raise it. `videoSettings` is required when `responseType` is `MP4` and should be **omitted on `DESIGN` imports** — a `DESIGN` import creates no render, so duration and audio belong at schedule time instead (see section 6). Only reach for `MP4` when the user explicitly needs file URLs. Video output is `MP4` or `DESIGN` only — never PDF or PNG. `audioId` is a media ID from the library, not a URL.
- **Single image:** `slide` as **one object**, not an array, no `type`. Only `heading` is required. Use the image import tools, not the carousel ones.

Always pass:

```
generateImages: {
  context: "<you write this from the post>",
  imagePlacement: "auto",
  imageStrategy: "strategic"
}
```

Make `context` a text-safe composition brief: describe the theme, keep the focal subject in a lower or side third with clean negative space in the upper-center where the heading sits, high contrast, one clear visual metaphor, no text in the image.

AI images require a paid plan and draw on a separate AI-image quota (distinct from post credits). They are best-effort — the post still completes if they fail or the quota is exhausted. Confirm they landed via the `GENERATE_IMAGES` step in `check_status`. Infographic slides never receive an image; that is expected, not a failure.

Keep `DESIGN` unless the user needs file URLs. Do not use generate-from-topic unless they ask for it.

## 5. Captions

Unique per platform. Fill each one in; do not pad to the cap.

**Captions are one single line of plain text.** No markdown, no real newlines, no other formatting. For a line break, insert `<br/><br/>` and nothing else. Open every caption with the same hook line as slide 1.

| Platform | Max | How |
| --- | --- | --- |
| LinkedIn | 3000 | Longer, professional, light or no hashtags |
| Instagram | 2000 | Hook first, scannable, hashtags at the end |
| TikTok | 2200 | Spoken, hook first, native hashtags |
| Threads | 500 | Conversational, must stay under 500 |

Captions go in `postContent`, keyed by platform. The object also accepts `common` as a shared fallback and a `facebook` key, though Facebook is not among the four platforms the accounts tool returns. Hashtags are extracted automatically, so write them inline. Prefer per-platform keys over `common` — the point of this section is that each platform reads differently.

Lock captions on the first few posts the same way as slides.

## 6. Platform settings

Look up the live schema. Which settings blocks are *required* is conditional: Instagram, TikTok, and Threads settings are required when an account of that platform is selected **and** a `designId` is set, while **LinkedIn settings are required whenever a LinkedIn account is selected**, designId or not.

These are the defaults unless the config overrides them:

- **Instagram:** `postType` matches the asset (`carousel` | `image` | `reel`). `postAsStory: true` unless `IG_STORY` is feed only.
- **TikTok:** **carousel or reel only — never `image`** (the enum has no image option). Required fields: `postType`, `canComment`, `isBrandedContent`, `isYourBrand`, `isThirdPartyBrand`, `isAIGeneratedContent`. **Always set `postTitle` to the post's title** — treat it as required even though the schema marks it optional. `SCHEDULED` → `privacyLevel: PUBLIC_TO_EVERYONE`. `canComment: true`. Carousel: `autoAddMusic` (required for carousel). Reel: `canDuet` + `canStitch` (required for reel). Branded flags false — and note that if `isBrandedContent` is ever true, at least one of `isYourBrand`/`isThirdPartyBrand` must also be true, and it cannot combine with `SELF_ONLY`. `isAIGeneratedContent: false` unless the user says otherwise.
  - Single-image design: schedule LinkedIn/Instagram/Threads as `image`, then create a **separate** TikTok scheduled post as a `reel` with `postSettings` (duration ≤50) **and a `postTitle`**.
- **LinkedIn:** carousels are always `postType: document` with a `postTitle` of 5–90 chars when `SCHEDULED` (missing or too short returns 400). The enum also allows `carousel`, which is the PNG-output path — do not switch to it. A `designId` is required when `SCHEDULED`; text-only LinkedIn posts can only exist as drafts. Single image: `image`. Video: `reel`.
- **Threads:** `postType` matches the asset (`carousel` | `image` | `reel`).
- **Reels:** `postSettings` is schema-optional but **necessary for video here**. A `DESIGN` import carries no `videoSettings`, so omitting `postSettings` makes the API fall back to 30 seconds and silence. Pass `videoDuration` (≤50) and `audioId` on every reel.

## 7. History: dedupe + failure audit

Before writing, list social accounts, then list scheduled posts. This is both the dedup source and the health check.

**Always pass `socialAccountIds`** (the `ACCOUNTS` from config) on the list call. It is schema-optional, but omitting it returns every post in the workspace and can exceed the tool's output limit. Note the filter is post-level, not account-level: a post targeting two of the filtered accounts comes back with its full `accounts` array intact, so this narrows *which* posts return, not how large each one is — the response can still be big. Window: **30 days back through the next 7 days** (`fromDate`/`toDate` are both required).

The result can be large. If it overflows, parse it with `jq` or hand it to a subagent to extract only what you need — do not read the raw blob into context.

**Dedupe:** do not repeat a design name, hook, or topic inside that window. Rotate the CTA away from the most recent post. Skip a publish window that already holds a `SCHEDULED` post for these accounts.

**Failure audit (every run):** `SCHEDULED` does not mean it went live. Scan for post-level `FAILED` or `PARTIALLY_FAILED`, and any per-account entry with a failed status or `errorMessage`. Known fragile cases: Instagram and Threads connections that silently fail — often with no per-account error string, where the aggregate status is the only signal — and render errors such as "Preparation failed: Render service failed". Surface these to the user (which post, which platform, what error). This routine cannot force a republish; flagging is the deliverable.

## 8. Schedule

`scheduledAt` is a future ISO-8601 time inside the chosen `WINDOWS`. This applies to **drafts too** — the API rejects a past time even for `DRAFT`, so a draft test still needs a real future slot. Never publish immediately on first setup.

A post needs either a `designId` or non-empty `postContent`. `designId` may be omitted or null only for `DRAFT`.

Pass the time with the user's UTC offset (for example `+05:00` or `-08:00`); the API stores it as UTC. Recompute the offset per run for timezones with DST — never hardcode it.

Randomize the minute within the window and avoid reusing the exact minute from the previous day.

If the job runs late and a window has already passed, do not error and do not pick a past time. Use the next future slot and note the deviation in the run summary.

Use `designId`, never `embedPostId` — passing an `embedPostId` here fails with "Design not found." If import succeeds but scheduling fails, retry only the schedule; do not re-import. The combined import-and-schedule tool returns the created `designId` on a scheduling failure precisely so the design can be reused, which is the same reason to keep import and schedule as separate steps. When scheduling several posts in one run and a later one fails, keep the successes and report exactly what did and did not schedule.

First test is `DRAFT`. Only move to `SCHEDULED` after explicit approval.

## 9. First test, then automate

1. Recap the filled config from section 0. Get a yes.
2. Lock one post (copy + captions) in chat. Prefer a carousel for the first test unless the user asks otherwise.
3. Import `DESIGN` + `generateImages` using the async pattern in section 4.
4. Create a **DRAFT** on the chosen accounts, plus the extra TikTok reel draft if the design was a single image.
5. Send the editor URL. Stop creating posts until the user says to continue.
6. After approval, save a **recurring routine as an intent, not a frozen tool recipe**, carrying the filled config. Each run: dedupe + failure audit (section 7), write, import, caption using `<br/><br/>` only, apply platform settings including TikTok `postTitle`, schedule, then report what went out and flag any prior-run publish failures. If PostNitro auth fails, pause the routine and tell the user rather than retrying silently.

The calendar is the accumulated result, not a stored artifact: each run fills the next open slots and section 7's 30-day-back / 7-day-forward query is what reads the calendar back. So the run summary should say where things now stand — what was added, which slots are filled ahead, and anything from a previous run that failed to publish — rather than only confirming today's posts.

## 10. Product facts

- AI **writes** content (from a topic, URL, X post, or pasted text) **and** designs carousels, single-image posts, and videos. Users can also import their own copy.
- Native publish targets: LinkedIn, Instagram, TikTok, Threads. X is a source or export, not a native target.
- A brand kit's handle or tagline field may carry marketing copy. That is brand context, **not** a required closer on slides or captions.
