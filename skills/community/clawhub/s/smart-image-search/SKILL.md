---
name: search-image
description: Search images from text queries and return the most relevant image result, candidate images, source pages, or ready-to-open search links. Use when the user asks to search for an image, find reference images, look up a character, person, brand, mascot, meme, wallpaper, avatar, or logo, wants several engines searched, wants the best match instead of the literal first result, or wants the best candidate sent as an attachment. Prefer multi-engine search with relevance ranking, then download and send the best match; if confidence is weak or downloading fails, return several candidate links and search URLs.
---

# Search Image

## Overview

Handle image-search requests triggered by phrases like `search image X` or `find a picture of X`.
Default behavior for this skill:
- Search multiple engines, not just one source
- Prefer the **most relevant result**, not the literal first result
- Download the best match locally, then send it as an attachment when possible
- If confidence is weak, provide several candidates instead of pretending one result is perfect

## Engines

Use as many available sources as practical, in this priority order:
- **Bing Images**
- **Baidu Images**
- **Sogou Images**

Notes:
- Bing is usually the most parseable server-side source
- Baidu may return a security-verification page; treat it as a soft failure
- Sogou can provide extra recall when Bing drifts or lacks meme-style results

## Workflow

1. Extract the search query after the trigger phrase.
2. Parse lightweight parameters first. Read `references/parameters.md`.
3. Detect intent on the cleaned core query. Read `references/intent-routing.md` when tuning or debugging routing.
4. Normalize the cleaned core query, but keep the original wording too.
5. Detect subject subtype when relevant, especially under `official`: `campus`, `emblem`, `mascot`, `poster`.
6. Search across multiple engines.
7. Collect several candidate image results instead of only one.
8. Rank candidates by relevance with intent-aware weighting, source trust, and subtype-aware boosts/penalties.
9. Classify confidence. Read `references/confidence.md` when tuning thresholds.
10. If confidence is high, download and send the best match.
11. If confidence is medium, prefer 2-3 candidates.
12. Apply quality filtering before final send. Read `references/quality-filtering.md` when tuning thresholds.
13. If confidence is low or downloading fails, return top candidates plus search links.

## Parameters

Support lightweight natural-language parameters inside the query.
Examples:
- `search image taylor swift 3 images`
- `search image acme logo official`
- `search image funny cat meme`
- `search image aurora wallpaper 4k landscape`
- `search image anime girl avatar 2 images`

Supported parameters:
- Count: `1` to `5` images
- Intent override: `official`, `meme`, `avatar`, `wallpaper`
- Orientation preference: `landscape`, `portrait`
- Quality preference: `hd`, `4k`, `high resolution`

Parse these first, then search the cleaned core entity query.

## Intent routing

Classify the request before ranking:
- `meme`: meme / reaction image / funny image / emoji style requests
- `official`: official / logo / emblem / mascot / poster / brand identity
- `portrait`: people, characters, or general image requests
- `wallpaper`: wallpaper / hd / high resolution / 4k
- `avatar`: avatar / profile picture / icon

When `official` is selected, also infer a subtype when possible:
- `campus`: campus / gate / building / landscape / map
- `emblem`: emblem / logo / crest / mark / badge
- `mascot`: mascot / character / brand character / official character / IP character
- `poster`: poster / promotional art / campaign art

Intent affects ranking:
- `meme` prefers meme and funny-image pages
- `official` prefers official domains, institutional pages, and reference pages
- `portrait` prefers representative images
- `wallpaper` prefers larger image results
- `avatar` prefers square or icon-like results

## Relevance policy

Do **not** blindly send the first result.
Use `references/relevance.md` and follow these rules.
For `official` intent, also read `references/official-sources.md` and `references/official-whitelist.md` when tuning or debugging official-result ranking.
Use `references/entity-consistency.md` to prevent official-looking but wrong-entity matches.
Use `references/entity-gating.md` when the query contains multiple strong entities and partial matches must be demoted to fallback-only.
- exact query match is best
- token matches in title/page/image URL matter
- semantically related domains help
- obvious news drift, spammy pages, or generic stock images should rank lower
- weak modifiers like `image`, `photo`, `meme`, `avatar`, and `wallpaper` should not outweigh the core entity
- in `official` mode, prefer trusted domains over visually appealing aggregators
- in `emblem` mode, prefer brand/identity signals and penalize maps, personal homepages, and generic banners
- in `mascot` mode, prefer official character/IP wording and penalize generic news coverage when cleaner source pages exist

If confidence is weak, prefer sending 2-3 candidates or links rather than a low-quality single answer.
Read `references/confidence.md` for the high / medium / low decision rule.

## Output rules

- Be brief and lead with the result.
- If the image was sent successfully, say so in one short sentence.
- If the image cannot be sent directly, do **not** pretend the search succeeded.
- When falling back, provide clickable search links immediately.
- For meme or mascot queries, optimize for likely intent match, not formal source prestige.

## Ready-made search URLs

Use these patterns:

- Bing Images: `https://www.bing.com/images/search?q=<urlencoded_query>`
- Baidu Images: `https://image.baidu.com/search/index?tn=baiduimage&word=<urlencoded_query>`
- Sogou Images: `https://pic.sogou.com/pics?query=<urlencoded_query>`

If needed, use `scripts/build_image_search_urls.py` to generate encoded URLs safely.

## Scripts

### Build search URLs

Run:

```bash
python3 scripts/build_image_search_urls.py "official mascot"
```

### Parse the most relevant image automatically

Run:

```bash
PYTHONPATH=scripts python3 scripts/search_best_image.py "cat meme"
```

The script prints JSON containing:
- parsed parameters
- cleaned `search_query`
- per-engine status
- normalized query info
- detected `intent`
- `confidence`
- `best_image`
- `top_candidates`

### Download the best image for direct sending

Run:

```bash
PYTHONPATH=scripts python3 scripts/fetch_best_image.py "cat meme"
```

The script:
- searches Bing, Baidu, and Sogou
- ranks candidates by relevance
- computes confidence
- downloads the best match to `/home/mumu/clawd/tmp/search-image/`
- prints JSON with `path`, `image_url`, `engine`, `score`, `why`, and confidence info

### Download 2-3 candidates when confidence is not high

Run:

```bash
PYTHONPATH=scripts python3 scripts/fetch_candidate_images.py "cat meme" 3
```

Use this when confidence is `medium` or `low`.
The script downloads multiple top candidates and returns their local file paths for sending.

### Quality filtering

Use `scripts/image_quality.py` through the fetch scripts.
Default checks now include:
- reject obvious site assets / logos
- reject too-small files
- reject too-small dimensions
- penalize thumbnail-style URLs
- adjust scoring by intent

### Legacy first-result scripts

These remain available for debugging or quick comparison:
- `scripts/search_first_image.py`
- `scripts/fetch_first_image.py`

Prefer the **best-image** scripts in normal operation.

## Send-image handoff

After `fetch_best_image.py` succeeds, send the downloaded file as an attachment.

Preferred handoff:
- Use the local file path returned in `path`
- Use the best-match result, not the literal first result
- If confidence is low but still usable, mention it briefly or send multiple candidates instead
- If attachment sending fails, fall back to sending candidate image URLs and search links

Suggested flow:
1. Run `PYTHONPATH=scripts python3 scripts/fetch_best_image.py "<query>"`
2. Respect parsed parameters first: count / intent override / orientation / high-res hints
3. If confidence is `high` and JSON returns `ok: true`, use the returned local `path` for image sending
4. If confidence is `medium`, run `fetch_candidate_images.py` and send the requested count or 2-3 candidates
5. If confidence is `low`, send search links plus candidate links or candidate images
6. If JSON returns `ok: false`, send the search links and top candidate URLs instead

## Fallback template

Use this style when direct sending fails:

```text
Result: I could not get a single high-confidence direct image, so here are the best candidates.
Bing Images: <url>
Baidu Images: <url>
Sogou Images: <url>
Candidate 1: <url>
Candidate 2: <url>
Candidate 3: <url>
```
