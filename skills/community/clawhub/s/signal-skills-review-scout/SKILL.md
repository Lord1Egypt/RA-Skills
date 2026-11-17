---
name: review-scout
description: Mine user reviews for whatever kind of product this repo actually is (mobile app, browser extension, web/SaaS) and turn them into ranked findings — pain points, regressions, feature-request clusters, praise worth keeping. Use when the user asks what reviews/feedback say, wants a release-quality check against real user complaints, or asks "what are people saying about the app."
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/signal-skills
    requires:
      bins: [python3]
---

Turn scattered star ratings and free-text reviews into extracted, ranked
findings — the same extract-don't-summarize discipline as the `podcast`
skill, applied to user feedback instead of episode transcripts. Raw
reviews never dump into main context; subagents eat the noise, you keep
the signal.

## Why this exists

50 reviews of a mobile app is mostly "great app!" and "worst update ever"
with no specifics. Reading them one by one is slow and the 3 reviews that
actually describe a reproducible bug get lost in the noise. This skill
extracts SHAPES (what broke, on what version, how often) instead of
vibes.

## Step 1 — Detect the product type, don't assume "app store"

```bash
python3 ~/.claude/skills/review-scout/resolve.py detect --path .
```

Only reach for an app store as a source if this actually IS an app.
Detection checks for `pubspec.yaml` (Flutter), `android/`/`ios/`
directories, React Native/Expo in `package.json`, or a `manifest.json`
with `manifest_version` (browser extension). Falls back to `web-saas` if
it's a plain web app, `unknown` if nothing matches — ask the user rather
than guessing at that point.

Map the detected kind to a source:

| kind | source | compliant path |
|---|---|---|
| `mobile-app` (iOS) | App Store | `resolve.py fetch-ios` — free public RSS feed, works for ANY app (yours or a competitor's), no auth |
| `mobile-app` (Android) | Play Store | `resolve.py fetch-android` — official Play Developer API, needs a service account, **only works for an app you own** |
| `browser-extension` | Chrome Web Store / Firefox Add-ons | `resolve.py guidance chrome-extension` — no compliant public API, manual export from your own Dev Dashboard |
| `web-saas` | G2 / Capterra / TrustRadius | `resolve.py guidance web-saas` — no compliant free API either; manual export or your own in-app feedback/NPS is usually the better source anyway |
| desktop | Mac App Store / other | `resolve.py guidance desktop` — Mac App Store reuses `fetch-ios`; others have no free feed |

**Do not scrape review sites whose ToS disallows it** (Play Store web
pages, Chrome Web Store, G2, Capterra). Where no compliant path exists,
say so and point at the manual export — never silently scrape anyway,
and never silently skip without telling the user why.

## Step 0 — Check the ledger before doing anything

```bash
python3 ~/.claude/skills/review-scout/ledger.py mined --app "<app name>"
```

Cross-reference against the batch you're about to fetch (e.g.
`ios-2026-07-23`) and skip straight to Step 3.5/4 if it's already mined.

## Step 2 — Fetch

```bash
python3 ~/.claude/skills/review-scout/resolve.py fetch-ios --app-id <id> --country us --pages 5 --download tx/
python3 ~/.claude/skills/review-scout/resolve.py fetch-android --package <pkg> --credentials sa.json --download tx/
```

Both write a flattened `.txt` plus a manifest (source, count, date range,
path) to `tx/`, same shape as `podcast`'s transcript output.

## Step 3 — Fan out extractors

One subagent per ~100 reviews (or per version if a release is small), run
in parallel. Each reads its batch IN FULL and returns structured findings
only. Never read the raw review batch yourself.

The extraction prompt must demand SHAPES:

1. **Reproducible bugs** — what broke, which app version, how many
   reviews describe the same thing (frequency is the whole point; one
   angry review is noise, fifteen describing the same crash is a signal).
2. **Feature requests** — clustered by theme, not listed individually.
3. **Praise worth keeping** — what's explicitly working, so a redesign
   doesn't accidentally remove it.
4. **Regression candidates** — a complaint that matches something you'd
   expect to already be fixed (check against Step 3.5's known-issues
   dump before flagging this).
5. **Rating trend context** — is this batch's average rating up or down
   vs. the prior mined batch for this app.

Rules for every extractor:
- Tag each finding with the app version(s) it was reported against.
- Quote at most one short review verbatim if the phrasing is itself the
  evidence (e.g. exact crash description); paraphrase otherwise.
- Empty category → say "none". Never manufacture content.
- Close with a fenced JSON block mirroring `podcast`'s shape so the
  ledger/dedup machinery has something to record:

```json
{
  "app": "<app name>",
  "batch": "<batch label>",
  "date_range": "<start>..<end>",
  "findings": [{"claim": "...", "tag": "bug|feature-request|praise", "version": "...", "count": 1}],
  "regressions": ["<short regression note>", "..."]
}
```

After each extractor returns, record it:

```bash
python3 ~/.claude/skills/review-scout/ledger.py record --app "<app>" --batch "<batch>" \
  --source ios-app-store --date-range "<range>" --findings-path "<path>" \
  --regressions-json '["<regression note>", "..."]'
```

## Step 3.5 — Check known issues, surface cross-version regressions

```bash
python3 ~/.claude/skills/review-scout/ledger.py known-issues --app "<app name>"
python3 ~/.claude/skills/review-scout/ledger.py dedup --threshold 0.5
```

A complaint that token-overlaps with an older regression note, in a LATER
version, is the single most valuable output of this skill: something that
was supposedly fixed came back. Surface it explicitly, don't bury it in
the general bug list.

## Step 4 — Synthesize across batches/versions

- **Frequency across independent reviews** = signal. One person's rant
  isn't a bug report; fifteen people describing the same crash is.
- **Version correlation** = the most valuable read. Did the complaint
  volume spike exactly at a release? That's a regression, not background
  noise.
- **Rating trend** — is this getting better or worse release over
  release, not just "what does this batch say."
- **Filter against the actual release/roadmap context** if you have one
  (open issues, current sprint) — "what does this confirm or contradict
  about what we're already planning to ship" beats a generic feedback
  dump.

## Step 4.5 — Cross-check against your own analytics (optional)

If reviews claim something checkable against product data ("crashes on
checkout", "can't complete onboarding"), see `analytics-check.md` (shared
with the `podcast` skill, same backend-agnostic contract: PostHog,
Amplitude, Mixpanel, GA4, detected at runtime). Twenty reviews complaining
about a checkout crash plus a matching error-tracking spike is a very
different priority than twenty reviews with no supporting telemetry at
all.

## Step 5 — Report (shared renderer, no external skill invocation)

Same `render_report.py`/`template.html` as `podcast` and `signal-report`
(a real copy here, kept in sync with the canonical one in `signal-report`
— packaged plugins ship real files, not symlinks, so this installs
standalone; see those skills' `SKILL.md` files for the full rule set:
rank don't cut, no em dashes enforced by the
script, confidence tags required, theme-safe by construction). Build the
JSON payload (tiers like "Fix before next release", "Regression, was
already fixed once", "Feature-request cluster", "Keep doing this") and
run:

```bash
python3 ~/.claude/skills/review-scout/render_report.py payload.json out.html
```

Publish with `Artifact` on Claude Code; elsewhere use `--open` or report
the path (see `AGENTS.md`).

For actionable text/prompt output instead of (or alongside) the Artifact,
add a `.md` target in the same invocation:

```bash
python3 ~/.claude/skills/review-scout/render_report.py payload.json out.html out.md
```

## Hygiene

- Raw review batches go to the scratchpad, never the repo.
- State lives in `~/.claude/skills/review-scout/config.json` (preferences,
  e.g. `analytics_backend`) and `state/<app-slug>.json` (per-app ledger).
  Deliberately NOT shared/symlinked with `podcast`'s ledger even though
  the code is nearly identical — state correctness requires each skill to
  own its own files (a shared symlink was tried and reverted: resolving
  `__file__` through a symlink follows it back to the *other* skill's
  directory and silently writes into its config/state instead of this
  skill's own).
