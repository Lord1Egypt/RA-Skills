---
name: explainer
description: ~60-80s explainer video for any URL — GitHub repo, product page, docs site, blog post, or launch. Canonical workflow for URL walkthroughs. Use when the user asks to "explain this URL / repo / website / product", "make a walkthrough video for [url]", "demo this site", "Loom-style explainer of [url]", "explainer for github.com/...", or "explain this product link". Drives a real browser through the URL, generates an avatar lipsync, and composites in a 1280×800 macOS Sonoma frame with a 246-pixel bottom-left avatar circle. GitHub URLs activate a repo-aware mode (README scan + live-demo detection); other URLs use a generic page-walkthrough flow.
argument-hint: <url> [--focus angles] [--avatar url] [--voice id] [--live-url url] [--lipsync-provider pika|kling] [--no-captions] [--preview]
---

# /pika:explainer

Generate a ~60–80s URL explainer video: drive a real browser through the URL along a beat-sheet timeline, generate an avatar lipsync of the narration, and composite it all in a 1280×800 macOS Sonoma frame with a 240-pixel inner avatar (246-pixel outer including 3px white stroke ring) at canvas (20, 476) and element-targeted zoom on every mid-section beat. Works on any URL — product pages, docs sites, blog posts, launches. GitHub URLs activate a repo-aware mode (README scan + live-demo detection); all other URLs use a generic page-walkthrough flow.

**Usage:** `/pika:explainer <url> [--focus "angles"] [--avatar <url>] [--voice <id>] [--lipsync-provider pika|kling] [--preview] [--live-url <url>]`

## Behavior

### Defaults — fire fast, no mid-flow confirmation

- **Use identity-store defaults silently for avatar / voice.** Never ask "should I use your avatar?" or "which voice?" before firing. Honor explicit overrides (`--avatar`, `--voice`) when supplied; otherwise resolve via `identity_avatar_url` / `identity_voice_id` and proceed. See Step 1 for the full resolution waterfall (including the silent fallback when identity returns null).
- **No mid-flow "type yes to proceed" gates by default.** Step 5 preview is **opt-in via `--preview`** (for power users testing new avatar/voice combos before the long-pole render); the default flow runs end-to-end without pausing.
- **Do not solicit `--focus` either.** Make a confident first attempt from page structure; users re-run with `--focus "X"` if the angle missed.

These defaults match industry standard for media-gen tools (Midjourney / Sora / Runway / HeyGen / Pika.art): submit → render → return. Account credit balance + provider failover (Step 9) are the canonical guardrails.

### Local avatar images on Claude Desktop

Claude Desktop can't pass inline-pasted images to MCP tools yet (Anthropic-side limitation). If the user pastes a photo inline, or mentions a local file they want as `--avatar`, pause Step 1 and kindly send them this — something like:

> Heads up — pasted images don't reach MCP tools on Claude Desktop yet (Anthropic limitation). Two easy options for your avatar:
>
> - **Paste a URL** if it's already hosted (Imgur, S3, your site) — fastest
> - **Attach the image file** so I can upload it before generation.

When a local file arrives, convert it to a public URL with `upload_asset` and use the returned `public_url` as `--avatar <url>` before Step 1. Already-hosted `https://...` URLs work as-is and skip this entirely. If no avatar is supplied at all, the identity-store default fires.

### Step 0 — Resolve URL (empty-args menu)

Strip flags (`--focus`, `--avatar`, `--voice`, `--live-url`, `--lipsync-provider`, `--no-captions`, `--preview`, `--skip-preview`, `--yes`) and `key=value` parameters from `$ARGUMENTS`. **If what remains contains no `https://...` URL** (or is empty / whitespace-only), print this menu **verbatim** as your full response, then **stop and wait for the user's next message**. Calling a tool here risks recording or explaining the wrong page. If `$ARGUMENTS` already carries a URL, skip this step silently and proceed to Step 1.

> **Which URL would you like me to walk through?** Works on any of:
>
> - **A GitHub repo** — e.g. `https://github.com/anthropics/claude-code` (activates repo-aware mode: README scan + live-demo detection)
> - **A product page / launch page** — e.g. `https://pika.art`
> - **A docs site** — e.g. `https://docs.anthropic.com`
> - **A blog post / article URL**
>
> Output: 1280×800 macOS Sonoma frame with a bottom-left avatar lipsync and element-targeted zoom on every mid-section beat. Default flow runs end-to-end with no confirmation gates — pass `--preview` if you want a 3-second lipsync sanity check first.
>
> Reply with the URL and I'll start.
>
> *Tip: you don't need to type `/pika:explainer` — just say things like "walk me through <url>", "make a demo video of <url>", or "explain this repo: <github-url>" and I'll fire this skill automatically.*

When the user replies with a URL, treat it as the resolved input and proceed to Step 1. Do not re-prompt.

### Step 1 — Parse input + detect mode

Required: `url` (must be `https://...`).
Optional: `--avatar <url>` (overrides identity-store default), `--voice <minimax-voice-id>`, `--focus "..."` (editorial guidance woven into vo_text), `--live-url <url>` (force-supply live demo URL — GitHub mode only), `--lipsync-provider <pika|kling>` (defaults to **`pika`** — parrot a2v, ~2-5 min wall-clock, slightly more dramatic head motion. Pass `kling` for tighter face-centered output at ~5-30 min wall-clock — Kling produces minimal-head-motion presenter shots but is the long-pole stage; reserve for high-stakes renders), `--no-captions` (skip the Step 11 caption burn — default is captions on), `--preview` (opt-in to the Step 5 preview gate — ~3s lipsync of "Hi, I'm your presenter" for testing new avatar/voice combos before the long-pole render; default is no preview). `--skip-preview` and `--yes` are accepted as no-ops for backward compatibility.

**Mode detection:**
- **GitHub mode** — URL host is `github.com` AND path matches `/{owner}/{repo}` (no further path segments past the repo root). Activates the repo-aware extras: README scan, live-demo detection, GitHub-specific selectors.
- **Generic-URL mode** — anything else (a product page, docs site, blog post, deeper GitHub path like `/blob/HEAD/path`). Skips the GitHub extras; uses generic CSS selectors and walks through the URL itself.

**Avatar resolution (silent — never ask the user):**
1. If `--avatar <url>` was passed, use it.
2. Else call `mcp__pika__identity_avatar_url`. If non-null, use it.
3. Else (fresh user, no identity avatar set yet) call `mcp__pika__generate_image` once with prompt `"professional presenter, friendly tech narrator, studio portrait, 1:1, natural lighting"` and use the returned URL. Do **not** ask the user "should I generate one?" — just generate silently.

**Voice resolution (silent — never ask the user):**
1. If `--voice <id>` was passed, use it.
2. Else call `mcp__pika__identity_voice_id`. If non-null, use it.
3. Else pick a casual MiniMax `speech-2.8-hd` preset matching the resolved avatar's apparent gender:
   - **Female-coded avatar** → `English_PlayfulGirl` (warm, casual, clearly female-voiced — verified)
   - **Male-coded avatar** → `English_Jovialman` (warm, casual male)
   - **Unclear / gender-neutral** → `English_Jovialman` (default)

   Determine gender from `mcp__pika__identity_persona_read` (look for a gender / pronouns field) when identity exists; otherwise infer from the resolved avatar image. Do **not** call `analyze_media` for this — it's not worth the extra ~30s round-trip. Do **not** ask the user.

   **Do NOT use `English_FriendlyPerson`** — despite being categorized under "female" in MiniMax's catalog, its display name is "Friendly Guy" and it reads as male in playback. `English_PlayfulGirl` is the canonical casual-female pick. Other verified-female alternates: `English_Upbeat_Woman`, `English_LovelyGirl`, `English_radiant_girl`.

The flow below is annotated per step: **GitHub-only**, **Generic-only**, or **Both** modes.

### Step 2 — Read source (no MCP call)

**Both modes:** use Claude's `WebFetch` on the input URL to pull the page's main content (h1, hero section, headings, primary copy).

**GitHub mode additions:** also fetch top-level file tree, (best-effort) `package.json` / `pyproject.toml`, and GitHub API repo metadata via `gh api repos/{owner}/{repo}` for `homepage`, `description`, `language`, `topics`. Detect a candidate `live_url` in this priority:

1. User-supplied `--live-url`.
2. **GitHub API `meta.homepage` field** — set when the maintainer configured the repo's homepage in GitHub settings (matches tarball `repo_analyzer.py:66-77`).
3. `package.json` `"homepage"` field.
4. First match in README of `https?://[^\s)\"'<>]+(?:vercel\.app|netlify\.app|github\.io|fly\.dev|railway\.app|render\.com|herokuapp\.com|surge\.sh)[^\s)\"'<>]*`.
5. **Any other URL in README that the badge area / "Live Demo" / "Project Page" / "Demo" text points at.** The allowlist regex above misses arbitrary custom domains (e.g. `<project>-project-page.com`); when the README explicitly designates a project page, prefer that over the github.io fallback.
6. GitHub Pages convention `https://{owner}.github.io/{repo}` — but only if the deep tree contains a frontend signal (one of `index.html`, `App.tsx`, `App.jsx`, `App.vue`, `app.py`, `main.py`).

If no candidate resolves, the beat sheet skips beats 6–7.

**Generic-URL mode:** the input URL itself is the only URL the beats walk through — no `live_url` inference, no extra metadata fetches. Skip Step 2.5 and Step 3.0; jump straight to Step 3.

### Step 2.5 — Verify `live_url` reachability (GitHub mode only, no MCP call)

If a candidate `live_url` was selected, verify it serves real content **before** authoring beats 6–7. Use `WebFetch` on the candidate and check the response:

- If the response status is 4xx / 5xx, **drop `live_url` to None** and skip beats 6–7. The github.io fallback in particular is reachable as a hostname but often returns 404 ("There isn't a GitHub Pages site here") for repos that haven't enabled Pages — recording that 404 page wastes ~12s of the explainer on wrong content.
- If the response renders the GitHub Pages "404 — There isn't a GitHub Pages site here." template (heuristic: response body contains `"There isn't a GitHub Pages site here"`), drop `live_url` and skip beats 6–7.
- Otherwise, keep `live_url` for beats 6–7.

This mirrors the original tarball's `requests.head(live_url, timeout=6, allow_redirects=True)` reachability gate.

### Step 2.6 — Generic-URL pre-flight (Generic-URL mode only, no MCP call)

Before authoring beats for a non-GitHub URL, WebFetch the input URL and inspect the response. This step prevents three common Generic-URL failure modes: (a) recording a captcha / bot-block page instead of content, (b) the cookie/consent banner eating the first ~3 seconds of video, (c) generic CSS selectors missing the page's actual hero / sections.

**A. Bot-block / captcha detection — abort if matched:**

If the response body contains any of:

- `"Verify you are human"` / `"verify you are not a robot"`
- `"captcha"` / `"CAPTCHA"` / `"reCAPTCHA"`
- `"403 Forbidden"` / `"Access Denied"`
- `"Just a moment"` + `cf-chl-bypass` (Cloudflare challenge)
- `"We're sorry, something went wrong"` (Amazon-style bot block)
- A `<title>` or h1 of just "Robot Check" / "Are you a robot?"

→ **ABORT** with a clear error to the user: "Generic-URL mode can't render this site — the page is showing a bot-detection / captcha challenge under headless Chrome. Try a different URL, or run a real-user version of the page first to verify it loads cleanly."

**B. Cookie / consent-banner detection — defuse with `extra_css` + optional click:**

Scan the response for these patterns (case-insensitive):

- IDs / classes starting with `onetrust-`, `truste-`, `cookie-banner`, `cookie-consent`, `gdpr-`, `consent-`, `cmp-`
- Buttons matching `(?i)accept (all )?cookies` / `(?i)agree.{0,10}cookies` / `(?i)i (accept|agree)`
- Apple-specific banner: id `ac-gdpr-banner` or class `as-globalfooter-curtain`
- Google consent: `[role="dialog"]` with text "Before you continue"

If detected, set `cookie_banner_present = true`. Defense in depth — the recording uses BOTH:

1. **CSS injection (`extra_css`)** in the `capture_website` call to hide common banners universally — even if the click below misses, the banner is visually gone.
2. **A `click` `timed_action`** at `at_s: 0.0` against the most likely dismissal selector (extracted from the WebFetch DOM, e.g. `#onetrust-accept-btn-handler`, `[aria-label*="Accept all" i]`, `button[id*="accept"]`).

The `extra_css` payload (use this verbatim — covers ~80% of consent platforms):

```
#onetrust-banner-sdk, #onetrust-pc-sdk, #onetrust-consent-sdk { display: none !important; }
#truste-consent-track, #truste-consent-content, .truste_box_overlay { display: none !important; }
[id*="gdpr-cookie"], [id*="cookie-consent"], [id*="cookie-banner"] { display: none !important; }
[class*="cookie-banner"], [class*="cookie-consent"], [class*="consent-banner"] { display: none !important; }
[class*="CookieBanner"], [class*="CookieConsent"], [class*="ConsentBanner"] { display: none !important; }
#ac-gdpr-banner, .as-globalfooter-curtain { display: none !important; }  /* Apple */
[role="dialog"][aria-label*="cookie" i], [role="dialog"][aria-label*="consent" i] { display: none !important; }
.cmp-container, .cmp-modal, .cmp-banner { display: none !important; }
```

**C. Real-DOM element identification — emit concrete selectors:**

Generic CSS selectors (`h1`, `[class*="hero"]`, `section h2`) work on semantic / well-marked-up sites but miss obfuscated class names on big-name corporate sites (apple.com uses `tile-headline` / `as-headline-section-title`, not `hero-*`). For each beat, prefer the **actual DOM elements** observed in the WebFetch:

- Read the rendered HTML/markdown WebFetch returned. Note the page's actual primary `<h1>` text and class.
- Note the page's section structure (h2 headings + their parent containers).
- Note any prominent CTA / signup / pricing element.
- Emit `zoom_target.selector` using **the actual class or id observed**, falling back to semantic structure (`main > section:nth-of-type(N) h2`) when class names look auto-generated (Tailwind `_1a2b3c`, CSS modules `module__hero___xYz`).

**D. SPA / lazy-render detection — bump initial wait:**

If the WebFetch response has fewer than 3 visible headings / minimal text content, the page may be SPA-rendered post-`domcontentloaded`. Emit a longer initial `wait` action (`{type: "wait", at_s: 0.0, ms: 2500}`) before any beat fires, instead of the default 600ms settle.

**E. `--focus` is honored when supplied (do not solicit):**

Without `--focus`, select beats from generic structure cues — proceed silently with a confident first attempt. Do **not** ask the user "what should I focus on?" before firing; users iterate by re-running with `--focus "the X feature"` if the first pass misses the angle they wanted. With `--focus` supplied, anchor beat selection on the phrase: uses concrete page sections that match it, ignores irrelevant marketing chrome.

### Step 3.0 — Required README section scan (GitHub mode only, no MCP call)

Before authoring the beat sheet, **scan the README** (case-insensitive, full-text) for any of these section names. If a match is found, you **must** add a dedicated beat for that section in Step 3, replacing one of the generic beats 4–5 if necessary:

| README contains... | Required beat |
|---|---|
| `how it works` | scroll_to that heading; zoom `article h2:has(#user-content-how-it-works)` |
| `audio layer` / `audio timeline` | scroll_to the audio-layer diagram; zoom on the rendered figure or its surrounding heading |
| `claude code` / `mcp integration` | scroll_to that section; zoom `article pre` or `.highlight` (terminal screenshot / code block) |
| `architecture` / `system design` | scroll_to that section; zoom `article h2:has(#user-content-architecture)` |
| `features` (when prominent at top) | scroll_to that heading; zoom `article h2:has(#user-content-features)` |
| `getting started` / `quick start` / `installation` | scroll_to that heading; zoom `article h2:has(#user-content-installation)` (or the matching slug) — falls back to `article pre` if you want the install code block instead |
| `usage` / `examples` | scroll_to that heading; zoom `article h2:has(#user-content-usage)` (or the matching slug) — or the first code block under it |

**GitHub heading slug rule:** lowercase, spaces → dashes, strip non-`[a-z0-9-]` characters. So "How it works" → `#user-content-how-it-works`, "Quick Start" → `#user-content-quick-start`. GitHub injects the `<a id="user-content-{slug}">` anchor inside each rendered `<hN>`, so `hN:has(#user-content-{slug})` reliably grabs the heading element across any GitHub README.

**Selector contract:** `bbox_selector` needs to be vanilla CSS that resolves via `document.querySelector` (`capture_website` runs the post-action smooth-scroll JS via `page.evaluate`, which uses the browser's native selector engine). Avoid Playwright extensions like `:has-text("...")`, `text=...`, or `:visible`: those resolve in Playwright's `page.query_selector` (so the bbox capture finds the element) but silently fail in the smooth-scroll's `document.querySelector` (so the page never scrolls to the target, and `bbox.y` ends up at document-Y instead of `top - 60 px`, which trips Step 8b's `bbox.y > recording_viewport.h` degenerate filter and falls back to default-position zoom). CSS Level 4 `:has(...)` is vanilla and supported in modern Chromium.

These sections are the highest-information visuals in most explainer-worthy repos. Missing them produces a generic walkthrough; including them gives the explainer a concrete "show, don't tell" beat. The original tarball SKILL.md flagged the first four with `SPECIAL` rules in the Gemini prompt; this Step 3.0 promotes them from incidental guidance to a hard requirement and adds three more high-signal headings common in OSS READMEs.

### Step 3 — Author beat sheet (main thread, no MCP call)

Write a JSON array of 8–10 beats, **with a hard total duration of 65–80 seconds and a hard total word count of 165–200 words** (assuming a speaking rate of 2.5 words/sec). Each beat:

```jsonc
{
  "t_start": 0.0,
  "t_end": 7.5,
  "action": { "type": "navigate" | "scroll_to" | "hover", "url": "...", "selector": "..." },
  "zoom_target": { "selector": "...", "description": "..." },
  "vo_text": "exact words to speak — 1 to 2 conversational sentences"
}
```

**Hard constraints (validate before emitting the beat sheet — reject the draft if any fails):**
1. Every beat needs all five fields: `t_start`, `t_end`, `action` (with `type` and `url`), `zoom_target` (with `selector`), `vo_text`. Missing fields ⇒ reject and re-author. (Mirrors tarball's `github_explainer.py:183-190` validation pass.)
2. `t_start` of beat 0 = 0.0; `t_end[i] == t_start[i+1]` (continuity).
3. `len(vo_text.split()) / 2.5` ≈ `t_end - t_start` per beat. Aim for ±10% of this estimate; if your draft is denser than 2.5 wps, tighten the `vo_text` until it fits.
4. **Total `t_end` of last beat ≤ 80 seconds.** (Reference output is 86.5s including intro; lipsync audio is ~83s. Kling avatar/image2video stalls reliably past ~90s of audio under current load — going over 80s risks a 20-min Kling timeout.)
5. **Total spoken word count between 165 and 200 words.**
6. Every beat's `zoom_target.selector` needs to be a valid CSS selector for the page that beat lands on. **GitHub mode prefers** GitHub-specific selectors: `h1.f1`, `#readme`, `article h2`, `.blob-code-inner`, `.highlight`, `.octicon-star`, `nav`. **Generic-URL mode prefers** robust generic selectors: `h1`, `[role="main"]`, `main`, `header`, `nav`, `.hero`, `.feature`, `section h2`, `[class*="cta"]`, `[class*="hero"]`, `button`, `a[href]`. **Selectors need to resolve on the rendered page after the beat's action settles** — verify against the DOM you can see via WebFetch before emitting.
7. `vo_text` is 1-2 conversational sentences. Dev voice. No stage directions. No markdown.
8. `action.url` is a valid `https://...` URL when `action.type == "navigate"`; required.

**Self-check before Step 4:** verify `total_words` is in `[165, 200]` AND `total_seconds` (= `beats[-1].t_end`) is in `[65, 80]`. If either misses bounds, re-author the beat sheet — do not proceed to TTS. (No need to "print" anywhere — this is an internal draft validation; just reject the draft and re-author until it passes.)

**Structural skeleton — GitHub mode (load-bearing for the visual contract — match origin, but Step 3.0 overrides if applicable):**

- **Beat 1:** `navigate` repo root, zoom `h1.f1` (repo title), hook sentence.
- **Beats 2–3:** `navigate` to specific source files (`https://github.com/{owner}/{repo}/blob/HEAD/<path>`), zoom `.blob-code-inner` or `.highlight`. Pick files that match the narration's claim — don't navigate to a file you won't talk about.
- **Beats 4–5:** `scroll_to` README sections, zoom `article h2` or `#readme`. **If Step 3.0 surfaced required sections, replace these slots with the required ones.**
- **Beats 6–7 (only if `live_url` survived Step 2.5):** `navigate` to `live_url`, zoom `nav` / `h1` / `.hero` / `main` / `button` / `.feature`.
- **Beat 8:** back to repo root, zoom `.octicon-star`, outro.

**Structural skeleton — Generic-URL mode:**

- **Beat 1:** `navigate` to the input URL, zoom `h1` or `[class*="hero"] h1` (the page's primary headline), hook sentence.
- **Beats 2–3:** `scroll_to` the page's hero / value-prop / first feature section. Zoom `.hero`, `[class*="hero"]`, `[class*="feature"]`, or `section:nth-of-type(1) h2`. Pick visible elements the narration references.
- **Beats 4–5:** `scroll_to` deeper sections — feature lists, screenshots, pricing, social proof. Zoom `section h2`, `[class*="feature"] img`, `[class*="testimonial"]`, `[class*="pricing"]`, or any prominent semantic element on the page.
- **Beats 6–7:** `scroll_to` CTA / signup / demo embed. Zoom `[class*="cta"]`, `button`, `a[class*="button"]`, or `[id*="signup"]`. (No live-demo navigation in generic mode — the input URL IS the demo.)
- **Beat 8:** `scroll_to` footer / closing element, zoom `footer h2`, `footer`, or back to top with `h1`. Outro sentence.

If `--focus` is supplied, weave its angles into `vo_text` without mutating the structural skeleton. Prefer **CSS selectors over `text_content`** in `zoom_target.selector` — bbox capture is selector-only (see Known gaps).

### Step 4 — TTS

Call `mcp__pika__generate_speech` with `provider: "minimax-tts"`, `text: <full vo_text join>`, optional `voice_id`. Capture `result.audio_url` (the dispatcher returns audio under `audio_url`, not `url`) and `result.duration_seconds`. Voice defaults to identity-store injection in plugin mode.

**Stale-voice fallback detection (AGNT-231):** the dispatcher retries once with the default `Calm_Woman` voice on Minimax `status_code:2054` (voice id not found — typically a per-agent workspace pointer that Minimax auto-deleted after 7 days of inactivity). On retry success the response carries two extra fields beyond the documented schema (passthrough): `voice_id_requested` (the planted-but-stale id the worker tried first) and `fallback_reason: "invalid_minimax_voice_id"`. **If you see `fallback_reason == "invalid_minimax_voice_id"` in the response, surface a one-line note to the user along the lines of:** "your registered voice expired on Minimax (auto-GC'd after 7 days of inactivity); we used the system default. Re-clone via `clone_voice` if you want personalization back." The render does NOT fail — it just uses the default voice — so this is informational, not a retry trigger.

**Cookie-banner audio padding (Generic-URL mode with `cookie_banner_present == true` from Step 2.6 §B):** prepend MiniMax's pause marker `<#1.5#>` to the `text:` argument **before** calling `generate_speech`. MiniMax's `speech-2.8-hd` honors `<#N#>` as N-second silence; the returned `audio_url` and `duration_seconds` include the 1.5s lead-in natively. This aligns the audio with the screen recording's cookie-dismissal +1.5s offset applied in Step 4.5.

**Fallback** (only if smoke-test shows the marker is ignored on this voice): call `generate_speech` normally, then `mcp__pika__edit_audio_mix` to overlay the result onto a 1.5s silent base at offset 1.5s. **Then call `mcp__pika__analyze_media(url=<padded_audio_url>)` to probe the padded duration and rebind `duration_seconds = result.duration_seconds`** before Step 4.5 consumes it. `analyze_media` is the **single authoritative duration probe** — do not rely on `edit_audio_mix`'s return payload (its duration field is not contractually guaranteed).

### Step 4.5 — Audio length verification + beat-sheet rescale

Applied to `audio_duration_seconds` post Step 4 (which includes any cookie lead-in pad). End state: `beats[].t_start` / `t_end` are absolute wall-clock seconds matching the audio playback timeline. **All `beats[]` mutations happen here**; Steps 6 and 8 are read-only consumers.

**Gate 1 — Kling stall ceiling (provider cap, raw audio_duration_seconds):**
If `audio_duration_seconds > 90`, abort and re-author the beat sheet with a tighter word budget. Kling avatar/image2video stalls past ~90s.

**Gate 2 — Degenerate TTS (spoken-content length):**
Compute `narration_duration = audio_duration_seconds - (1.5 if cookie_banner_present else 0.0)`. If `narration_duration < 30s`, retry Step 4 once (and recompute `narration_duration` from the retry's audio). If the retry also returns `narration_duration < 30s`, abort and investigate — likely failure modes: truncated MiniMax response, silent audio, vo_text not joined correctly.

**Gate 3 — Rescale:**
- `narration_duration = audio_duration_seconds - (1.5 if cookie_banner_present else 0.0)`
- `scale = narration_duration / beats[-1].t_end`
- If `scale < 0.5` or `scale > 1.5`, abort and re-author. Structurally broken TTS (or wildly off word budget); rescaling won't save it.
- For each beat: `beat.t_start *= scale; beat.t_end *= scale`
- If `cookie_banner_present`: for each beat, `beat.t_start += 1.5; beat.t_end += 1.5`
- **Final clamp:** `beats[-1].t_end = audio_duration_seconds` (exact). Guarantees float equality of the invariant regardless of cookie mode or accumulated float drift.

**After Gate 3 passes**, emit a one-line operator log to surface the scale value for post-run diagnosis:

```
Rescaled beats by scale=X.XX (audio=Y.YYs, narration_duration=Z.ZZs, cookie_pad=W.Ws)
```

**Advisory (not a gate):** scale near 1.0 is ideal. `scale > 1.2` means audio is meaningfully slower than predicted — visuals feel "stretched" but stay in-sync. `scale < 0.85` means audio is faster — visuals feel "rushed" but in-sync. Both pass the gates; if the user reports "feels off-pace" rather than "out of sync," re-author with a tighter / looser word budget.

### Step 5 — Preview gate (opt-in via `--preview`)

**Skip Step 5 entirely by default.** Proceed directly to Step 6 unless the user explicitly passed `--preview` — do **not** generate a preview, do **not** ask for confirmation. This matches industry standard for media-gen tools (Midjourney / Sora / Runway / HeyGen / Pika.art): submit → render → return; account credit balance + provider failover are the canonical guardrails.

`--skip-preview` and `--yes` are accepted as no-ops for backward compatibility — they were the old opt-out flags.

If `--preview` was supplied:

1. `mcp__pika__generate_speech` with `text: "Hi, I'm your presenter. Let's explore this repo together."` → `preview_audio_url`.
2. `mcp__pika__generate_lipsync` with `provider: <resolved_lipsync_provider>` (defaults to `pika`; honor `--lipsync-provider kling` if supplied), `image: <avatar>`, `audio: preview_audio_url` → `preview_lipsync_url` (bare lipsync, ~3s). Use the same provider here as Step 9 will use for the full audio — the preview's job is to confirm the avatar+voice+provider combo before the long-pole render.
3. Present to the user verbatim:

   > Preview ready: `<preview_lipsync_url>`
   > This confirms the avatar + voice combo. The full render is a long pole (~5–30 min Kling lipsync on the full audio).
   > Reply `yes` to proceed, or anything else to cancel.

4. Match `^(yes|go|proceed|confirm|y)$` (case-insensitive). Anything else → STOP, no further MCP calls.

### Step 6 — Build `timed_actions` and record

Translate the beat sheet into `capture_website` `timed_actions`. **One `timed_action` per beat** — set `bbox_selector` to the beat's `zoom_target.selector` and `capture_website` captures the post-action bbox of that element internally (legacy 600 ms settle → smooth-scroll-to-`top - 60 px` → 1300 ms post-anim → measure, all server-side).

For each beat in order, emit one entry:

- **`navigate` beats**: `{type: "navigate", at_s: <t_start>, url: <action.url>, bbox_selector: <zoom_target.selector>}`. The worker navigates, waits to absolute `at_s + 0.6 s`, scrolls `bbox_selector` into view, and measures the bbox — all without the caller scheduling a follow-up step.
- **`scroll_to` / `hover` beats**: `{type: "scroll", at_s: <t_start>, selector: <action.selector or zoom_target.selector>, bbox_selector: <zoom_target.selector>}`. The action's own `selector` drives the page scroll; `bbox_selector` drives the bbox measurement (it can be the same selector or different — usually the same). (`capture_website` has no `hover`; scroll-into-view is the analog.)

**Do NOT prepend the eight-step intro scroll-through** that the tarball ran. The lipsync audio is timed from `t=0` of the beat sheet; a prepended intro shifts the screen recording forward by ~3 s while leaving the audio un-shifted, causing audio/video desync. The capture_website recording begins at `t=0` with beat 0's URL already loaded — that's the orientation the tarball's intro scroll provided, minus the desync.

Call `mcp__pika__capture_website`:

- `url: <beat 0's action.url>`
- `timed_actions: <the N-element list built above>` (one entry per beat)
- `duration_s: ceil(audio_duration_seconds)` — `beats[].t_start` and `t_end` have already been rescaled to the TTS audio timeline by Step 4.5, so `duration_s` is simply the audio length. The old `max(...)` defense against TTS overrun is no longer needed.

**Generic-URL mode additions** (per Step 2.6 pre-flight):

- `extra_css: <the cookie-banner-hiding CSS payload from Step 2.6 §B>` — defensive: hides common consent platforms via `display: none !important;` so even if the optional click misses, the banner is invisible in the recording.
- **Prepend a `wait` action** `{type: "wait", at_s: 0.0, ms: 2500}` for SPA / lazy-render pages (per Step 2.6 §D); use 1500ms for "normal" pages. This gives time for hero images to lazy-load, fonts to swap, and scroll-triggered animations to be ready before the first beat fires.
- **If `cookie_banner_present` from Step 2.6 §B**, also prepend a `click` action `{type: "click", at_s: 0.5, selector: <detected dismissal selector from WebFetch DOM>}`. **The `beats[]` array has already been shifted by `+1.5s` in Step 4.5 to account for the cookie-dismissal lag, and the TTS audio has already been padded with 1.5s of silence (Step 4); no further shifting is required here. Beat 1's `timed_action.at_s` reads `beats[0].t_start` directly, which is 1.5 in cookie mode.**
- **No cookie banner action needed** if `cookie_banner_present == false`; just the prepended wait action.

Capture `video_url`, `recording_viewport`, `action_bboxes`. The result returns `recording_viewport: {w, h}` and `action_bboxes: [{idx, selector, found, bbox: {x,y,w,h}}]` alongside `video_url`.

**`action_bboxes[].idx` semantics:** the `idx` field is the position in the **input** `timed_actions` array.

- **GitHub mode**: with one timed_action per beat, `idx` maps 1:1 to beat index — Step 8 uses `entry.idx` directly as `beat_idx`.
- **Generic-URL mode**: the prepended `wait` (and optional cookie-dismissal `click`) shift the array by 1 or 2. Compute `beat_idx = entry.idx - prepend_count` where `prepend_count` is 1 (wait only) or 2 (wait + click). Skip entries where `beat_idx < 0` (those are the prepended setup actions, not beats).

The `selector` field on each entry reports `bbox_selector` (i.e. `zoom_target.selector`), not the action's own `selector`.

### Step 7 — Browser chrome

`mcp__pika__edit_browser_frame`:

- `video_url: <Step 6 video_url>`
- `url: (live_url if GitHub-mode and survived Step 2.5 else input_url, truncated to 65 chars)`
- `tab_title: <30-char title>` — GitHub mode: `(meta.description or repo_name or "")[:30]`. Generic-URL mode: the page's `<title>` (from WebFetch in Step 2) or the URL's hostname, truncated to 30 chars. Guard against `None`/empty.

Returns `framed_url` (1280×800 Sonoma + chrome).

### Step 8 — Build `zoom_keyframes` and apply

Constants:

- `INTRO_BEATS = 2` — gates by **beat-sheet index**. Skips zoom on beat indices 0 and 1 ("Beat 1" and "Beat 2" in the structural skeleton above).
- `HOLD_GAP = 0.6` — seconds of 1.0× before each zoom-in and after each zoom-out.
- `MIN_BEAT_DUR = 1.5` — beats shorter than this are skipped (no room for a meaningful zoom).
- `SCALE = 1.35` (precise element-targeted zoom).
- `FALLBACK_SCALE = 1.25` (default-position fallback when no usable bbox).
- `FALLBACK_RAMP = 0.4`.

**Note:** `beats[].t_start` / `t_end` were rescaled (and cookie-shifted if applicable) to the audio timeline by Step 4.5. HOLD_GAP (0.6s), MIN_BEAT_DUR (1.5s), and the 1.0s interior-interval check all operate on those final values — they are real visual seconds on the rendered video.

`edit_browser_frame`'s inner-content offsets: `CONTENT_X=56, CONTENT_Y=108, CONTENT_W=1168, CONTENT_H=637` (verified against the worker's `edit_browser_frame/main.py`).

Coord transform (recording px → framed px):

```
cx_framed = 56  + (bbox.x + bbox.w/2) * (1168 / recording_viewport.w)
cy_framed = 108 + (bbox.y + bbox.h/2) * (637  / recording_viewport.h)
```

**Build the zoom list with a per-beat default + bbox override pattern.** The legacy rig followed an "every non-intro beat gets a zoom — bbox-derived if available, default-position otherwise" rule. Reproduce that here:

**Step 8a — Pre-fill default-position keyframes for every non-intro, long-enough beat.**

Constants for the default position:
- `DEFAULT_CX = 56 + 1168 // 2` (screen center of the framed canvas)
- `DEFAULT_CY = 108 + 637 // 3` (upper-third of the content area, where most GitHub UI prominence lives)

Walk the beat sheet from index `INTRO_BEATS` (= 2) to the end. For each beat:

- If `t_end - t_start < MIN_BEAT_DUR` (1.5s), skip — too short for a meaningful zoom.
- Compute the keyframe's interior interval as `[t_start + HOLD_GAP, t_end - HOLD_GAP]`. If that interval is shorter than 1.0s, skip.
- Otherwise pre-fill that beat's slot in a per-beat map (call it `zoom_keyframes_by_beat[beat_idx]`) with `{cx: DEFAULT_CX, cy: DEFAULT_CY, scale: FALLBACK_SCALE (1.25), ramp_s: FALLBACK_RAMP (0.4)}` plus the trimmed `t_start`/`t_end`.

**Step 8b — Override with bbox-derived precise zoom where `action_bboxes` provided a usable measurement.**

For each entry in `action_bboxes`:

- `beat_idx = entry.idx` (since Step 6 emits one timed_action per beat). If `beat_idx < INTRO_BEATS`, skip.
- If `entry.found` is false, skip.
- If the beat isn't already in `zoom_keyframes_by_beat` (was filtered out in Step 8a by `MIN_BEAT_DUR`/`1.0s` rules), skip.
- **Filter degenerate bboxes:** skip if `bbox.y > recording_viewport.h` (offscreen capture — page didn't scroll the element into view in time) or `bbox.h > recording_viewport.h * 1.5` (full-page `<main>` element — yields a meaningless zoom center).
- Compute `cx_framed`/`cy_framed` from the bbox center using the recording-px → framed-px transform shown above. Override the beat's slot with `{cx: cx_framed, cy: cy_framed, scale: SCALE (1.35), ramp_s: min(0.5, (t_end - t_start) * 0.15)}`.

**Final list:** sort the values of `zoom_keyframes_by_beat` by `t_start` to produce the `zoom_keyframes` array.

This guarantees every non-intro, long-enough beat gets a zoom — precise when bbox capture worked, default-positioned otherwise. Avoids the "flat video for the whole runtime" failure mode.

If `len(zoom_keyframes) > 0`, call `mcp__pika__edit_animate_zoom` with `video_url: framed_url, zoom_keyframes`. Returns `zoomed_url`. Otherwise (no qualifying beats — should be rare given Step 3's 65-80s constraint) skip and use `framed_url` as `zoomed_url`.

### Step 9 — Lipsync the full audio

`mcp__pika__generate_lipsync`:

- `provider: <resolved_lipsync_provider>` — **default: `pika`** (parrot a2v). Honor `--lipsync-provider kling` if explicitly passed.
- `image: <avatar>`
- `audio: <Step 4 audio_url>`
- **kling-only knobs** (since `pika-mcp-server` BACK-339, 2026-05-10): when `provider == "kling"`, add `mode: "pro"` and `prompt: "talking head, face centered, mouth syncs to audio, minimal head movement, professional presenter"` for the polished-presenter feel. Both are silently ignored on `pika` (parrot has its own driver).

**Provider tradeoffs:**

| Provider | Wall-clock | Head motion | When to use |
|---|---|---|---|
| **`pika`** (default) | ~2–5 min | Slightly more dramatic, naturalistic | Default for most runs — fast iteration, watchable output, ~10× faster than kling |
| `kling` (opt-in) | ~5–30 min | Minimal, face-centered, presenter-style | High-stakes renders where the avatar must read like a polished presenter; tolerate the long pole |

Server-side-await covers the call inline; if the response shape is `{task_id, status: "queued"}`, poll `mcp__pika__task_status` in a tight loop (no sleep) until the status reaches a terminal state (`completed`, `failed`, or `cancelled`). On `completed`, capture `lipsync_url`. On `failed` / `cancelled`, fall back to the **other** provider (kling ↔ pika) per the failover note below.

**Failover:**
- If `pika` fails (rare — parrot a2v is robust at typical explainer audio lengths) → retry once with `provider: "kling"`.
- If `kling` stalls past the worker's 1200s ceiling (visible as repeated `processing` status with no completion) → fall back to `provider: "pika"`. Step 4.5's audio-length gate should catch the long-audio case before it gets here, but the failover handles the residual risk.

**Why pika is the default:**
- Speed — typical explainer wall-clock drops from ~10–15 min to ~5–7 min total because lipsync is the long pole.
- Quality is good enough — parrot a2v is naturalistic; the slight extra head motion reads as engaging rather than distracting in a 60-80s clip with avatar circle PiP.
- Kling-mode-pro polish is mostly invisible inside the 246-pixel circle anyway — face area is too small for the minimal-head-motion difference to register on most viewers.

For the canonical "polished presenter" feel of the original tarball reference output, pass `--lipsync-provider kling` explicitly.

### Step 10 — PiP composite

`mcp__pika__edit_pip`:

- `main_video_url: <zoomed_url>`
- `overlay_video_url: <lipsync_url>`
- `shape: "circle"`
- `size_px: 246`                    ← pixel-pinned 246px outer diameter (240 inner avatar + 3+3 stroke ring); matches tarball's `CIRCLE_OUT = CIRCLE_SIZE + STROKE * 2`
- `stroke_width_px: 3`
- `stroke_color: "white"`
- `position_px: {x: 20, y: 476}`    ← `800 − 246 − 78` for dock clearance (matches tarball's `H − CIRCLE_OUT − 78`)

Pass `size_px`, not `size`; the fields are mutually exclusive. Returns `final_url`.

**Master-duration / audio-source contract** (matching tarball `github_explainer.py:418-419, 531-533, 578-582`): `edit_pip` uses `shortest=1` semantics by default, which means the composite's duration is the shorter of (zoomed screen recording) and (lipsync video). Step 6's `duration_s = ceil(audio_duration_seconds)` ensures the screen recording length matches the lipsync exactly (Step 4.5 rescaled beats to the audio timeline). The composite duration is set by the lipsync via `edit_pip`'s `shortest=1` semantics. Audio comes from the lipsync video's audio track (the lipsync embeds the original TTS audio); the standalone `audio_url` is not re-mixed. If the lipsync video is shorter than the screen recording (Kling sometimes trims trailing silence), the screen will get cut off at the lipsync end — accept this; the alternative (looping the screen) is worse for explainer content.

### Step 11 — Burn captions

Call `mcp__pika__add_captions(video_url=<final_url>, style="classic")`. `classic` renders a bottom subtitle bar — the right register for an explainer video (use `tiktok` / `hormozi` / `karaoke` only when the user explicitly asks for word-level highlight). The audio is extracted server-side from the PiP composite's lipsync track, so transcription matches the narration verbatim. Capture the result as `captioned_url`.

Skip this step only if the user passed `--no-captions` (parsed in Step 1) — the default is captions on. (Note: `/pika:podcast` does **not** burn captions — narration in an explainer is more transcription-friendly than fast two-host dialogue.)

### Step 12 — Return

Emit `captioned_url` (or `final_url` if Step 11 was skipped) on one line: `Done: <url>`.

## Load-bearing phrases

These anchors preserve the visual contract across page types:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `vanilla CSS that resolves via document.querySelector` | Selector contract | Keeps scroll, bbox capture, and zoom targeting aligned inside `capture_website`. |
| `GitHub URLs activate repo-aware mode` | Mode detection | Prevents generic product-page beats from replacing README/code walkthrough beats. |
| `8-10 beats`, `65-80 seconds`, `165-200 words` | Beat-sheet authoring | Keeps narration, screen recording, lipsync, and captions within the reliable duration envelope. |
| `all beats[] mutations happen here` | Audio rescale step | Ensures later capture/zoom/composite steps consume one stable timeline. |
| `extra_css` cookie-banner hiding payload | Generic URL pre-flight | Reduces first-frame banner occlusion when a banner click misses. |

## Engine choice: Pika lipsync default, Kling opt-in

Default to Pika/parrot lipsync because it is faster and keeps most explainers in a short iteration loop. Use Kling only when the user explicitly requests `--lipsync-provider kling` or when a high-stakes render needs a more centered presenter look and can tolerate a much longer long-pole stage. Screen capture, browser frame, zoom, PiP, and captions remain deterministic edit/composite steps around that lipsync choice.

## Runtime expectations

Typical wall-clock is 5-10 minutes with Pika lipsync, or 10-30+ minutes with Kling lipsync:

| Step | Wall clock | Notes |
|---|---:|---|
| URL read + pre-flight | 10-60s | GitHub README scan or generic URL DOM/cookie checks |
| TTS + audio rescale | 30-90s | Beat timing is normalized after actual audio length |
| Screen recording | 60-180s | Depends on page load and navigation count |
| Browser frame + zooms | 1-3 min | Deterministic edit/composite stages |
| Lipsync | 2-5 min Pika / 5-30 min Kling | Kling is opt-in because it is the long pole |
| PiP + captions | 1-3 min | Captions skipped when `--no-captions` is set |

## Known gaps (carried as follow-up server-side work)

- ~~**Kling avatar `mode:"pro"` and `prompt` not exposed.**~~ **Resolved** by `pika-mcp-server` BACK-339 (PR #186, shipped 2026-05-10): `generate_lipsync` now wires both `mode` (e.g. `"pro"`) and `prompt` end-to-end for the kling provider. To enable polished-presenter mode here, pass `--lipsync-provider kling` and the Step 9 call should add `mode: "pro"` plus a prompt like `"talking head, face centered, mouth syncs to audio, minimal head movement, professional presenter"`. Real quality lever for reducing dramatic head motion in the lipsync — no longer a server-side gap.
- **No caller-controlled white-frame trim on the screen recording.** `capture_website` has internal trim heuristics but doesn't expose them to the caller. Visible as a brief white flash at the start of the explainer when the page is still loading. The 800ms `wait` action at `at_s: 0.0` mitigates this somewhat by giving the page time to paint, but doesn't trim already-recorded white frames. Worker enhancement.
- **No `networkidle` wait on per-beat navigation.** Tarball uses `page.goto(url, wait_until="networkidle", timeout=20000)` plus `wait_for_timeout(600)` after every navigate. `capture_website` settles to `domcontentloaded` plus the bbox-capture branch's 600 ms post-action settle (server-side, when `bbox_selector` is set), but SPA blob pages whose final render happens after `domcontentloaded` can still get bbox'd against unmounted code blocks. Worker enhancement: expose a `wait_until` knob on `timed_actions[].navigate`.
- **No per-step output-size verification gates.** Tarball's `verify()` helper at `github_explainer.py:35-39` checked TTS ≥ 50KB, preview ≥ 100KB, screen ≥ 200KB, lipsync ≥ 500KB, final ≥ 1MB after each step. The MCP path returns URLs only; verifying file size would require an extra `mcp__pika__analyze_media` call per step (~30s overhead each). Worth adding once user-side latency budget allows it. For now, a downstream-failure cascade (e.g. zero-byte TTS → silent lipsync → blank composite) only surfaces at Step 11.
- **`text_content` bbox capture not implemented.** `capture_website` v1 returns `action_bboxes` only for steps with a CSS `selector`. `text_content`-only steps produce no entry. Prefer CSS selectors in `zoom_target` for guaranteed zoom coverage.
- **Beat-sheet wording is non-deterministic.** Running the same input twice produces different vo_text and different zoom positions. Visual *kind* is the contract, not pixel-exact reproduction.
- **Generic-URL mode quality varies by site.** Modern indie / SaaS landing pages with semantic markup (`<h1>` + clear `<section>` + named class hooks) work well. Big-name corporate sites (apple.com, microsoft.com, amazon.com) hit several known limits: (a) **bot detection** — the page may serve a degraded version under headless Chrome, or a captcha; Step 2.6 §A aborts on these but the heuristics aren't exhaustive; (b) **obfuscated class names** — `tile-headline` instead of `hero-title` defeats generic selectors; Step 2.6 §C's WebFetch DOM scan helps but isn't perfect; (c) **scroll-triggered animations don't play** — IntersectionObserver-driven hero reveals fire on real user scrolls, not Playwright's `scrollIntoView`; the recorded frame may be a static placeholder; (d) **lazy-loaded images** — picture/source elements with `loading="lazy"` may not have resolved by the 600ms-or-2500ms settle window; the bbox lands on a transparent placeholder. Workarounds: prefer simpler / smaller marketing pages for launch demos, always pass `--focus "the X feature"` to anchor beat selection, accept that big-name sites need a follow-up server PR (cookie-banner click retry + `wait_until=networkidle` + animation-trigger via `IntersectionObserver` polyfill).
- **Cookie-banner click is single-attempt.** Step 2.6 §B emits one `click` against the dismissal selector extracted from the WebFetch DOM. If the WebFetch's HTML doesn't include the banner (rendered post-JS) or the selector is wrong, the click silently misses — the `extra_css` payload is the load-bearing defense. Worker enhancement: support a list of fallback selectors per `click` action so the worker tries each in order.
- **Step 8b ↔ Step 6 `idx`-mapping mismatch in Generic-URL mode.** Step 6 maps `beat_idx = entry.idx - prepend_count`, but Step 8b uses `beat_idx = entry.idx` naively. Pre-existing bug independent of rescaling.

## Auth

If any call returns 401: the user's OAuth token has expired or hasn't been issued. The next authenticated MCP call triggers OAuth automatically (browser opens for `@pika.art` Google login). For non-interactive environments, set `MCP_AUTH_TOKEN`.

## Examples

GitHub-mode (repo-aware: README scan + live-demo detection):

- `/pika:explainer https://github.com/leigest519/OpenGame`
- `/pika:explainer https://github.com/anthropics/claude-cookbooks --focus "Claude Code MCP integration"`
- `/pika:explainer https://github.com/openai/whisper --preview` (opt-in to the preview gate when testing a new avatar)

Generic-URL mode (any non-GitHub URL — drives through the page directly):

- `/pika:explainer https://pika.art`
- `/pika:explainer https://vercel.com --focus "the deployment workflow"`
- `/pika:explainer https://docs.anthropic.com/en/docs/claude-code/plugins`
- `/pika:explainer https://your-product-page.com --avatar https://cdn.example.com/me.png --preview`
