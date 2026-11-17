---
name: tasteprint
description: |
  Use when the user asks for product, shopping, gift, gear, or purchase recommendations; compares options; asks what to buy; wants to build, update, inspect, sync, or delete their Tasteprint preference profile; asks to analyze shopping/content/social behavior; or volunteers durable recommendation signals in conversation, including likes, dislikes, owned/bought/returned items, avoid rules, stable constraints, budget habits, style/material/brand/category preferences, evidence/source preferences, recommendation-format preferences, or corrections such as "remember", "do not remember", "I usually", "I no longer", or "avoid".
---

# Tasteprint.skill

## Core Principles

1. **Profile is user-owned but not proactively displayed.** Do not proactively show profile content, analysis summaries, raw preference details, or private behavioral evidence in normal recommendations or profile-build conclusions. If the user explicitly asks to manage their profile, help them open `<skill-root>/.tasteprint/` or delete the requested profile files/directory. For deletion, confirm the exact target when ambiguous and follow the environment's destructive-action approval rules.
2. **Consent gates collection.** Read and confirm `<skill-root>/.tasteprint/platform-consent.json` before browser collection. If consent is missing, use the questionnaire workflow.
3. **User statements win.** When behavioral data conflicts with the user's own statement, follow the user and note the tension internally.
4. **Profile priors are hypotheses.** Profile-derived signals must enter a recommendation task through `<skill-root>/.tasteprint/task-hypotheses/{task_id}.json` before affecting filtering, ranking, or explanation.
5. **Complete authorized collection.** Attempt every authorized platform and every applicable data type. Record technical failures with status envelopes; do not silently treat failures as empty data.
6. **UI control is runtime-selected, but collection identity is strict.** Treat host-native browser automation (for example Browser Use, Codex Browser, or Chrome), desktop UI automation (for example Computer Use), and `agent-browser` as optional providers whose availability, session identity, and APIs vary by environment. Honor an explicit user choice; otherwise choose the provider through `references/browser-connection.md`. Read the selected provider's current skill before use and never guess or copy its internal bootstrap/API. For signed-in/private collection, require a verified user-owned persistent identity context. Chrome for Testing, bundled test Chromium, fresh or ephemeral profiles, and isolated automation sessions are public-research/smoke-test only; their success never establishes private-collection compatibility.
7. **Navigate like a human.** Prefer visible clicks and in-page controls. URLs are fallback paths only when platform guidance allows them.

---

## Reference Loading Contract

This `SKILL.md` is a router. Before performing any specialized action, read the matching reference file. Do not continue that action from memory.

| Situation | Must read before action |
|-----------|-------------------------|
| User states reusable preference, ownership, purchase, avoidance, evidence preference, or correction | `references/conversation-signals.md` |
| Product recommendation, product search, or negative recommendation feedback | `references/task-hypotheses.md`, then `references/recommender.md` |
| Missing questionnaire/consent or login precheck before collection | `references/questionnaire-and-consent.md`; for browser login precheck also read `references/browser-connection.md` |
| Any browser operation, or desktop UI automation acting on a browser | `references/browser-connection.md` first; after provider selection succeeds, `references/browser-guidelines.md` and the selected provider's current skill |
| Raw-data file read/write, collection status, or schemas | `references/data-schemas.md` |
| Platform collection | `references/platforms/README.md`, then only the authorized platform files |
| Full profile analysis and profile synthesis | `references/profile-analysis.md`, `references/domain-profile-template.md`, `references/profile-template.md` |

If this file and a reference appear to conflict, this file controls routing, consent, privacy, and high-level principles; the specific reference controls implementation details for its action.

---

## Runtime Paths

The profile root is always inside this skill directory:

`<skill-root>/.tasteprint/`

`<skill-root>` means the directory containing this `SKILL.md`. Use absolute paths under `<skill-root>/.tasteprint/` whenever possible. Do not resolve profile files relative to the user's current project, shell working directory, or host-agent memory directory.

Storage details and schemas live in `references/data-schemas.md`.

---

## Workflow

### Step 0 — Route

Check `<skill-root>/.tasteprint/user-profile.md` (just a file read — fast).

| User wants... | Profile exists? | Action |
|---------------|----------------|--------|
| Product recommendation | Yes | **→ "Product Recommendations" section.** No collection needed. |
| Product recommendation | No | Offer: build profile first, or recommend without one. Yes → Step 1. |
| Build/update profile | Either | → Step 1. |
| User shares explicit recommendation-relevant preference, ownership, purchase/return, avoidance rule, stable constraint, evidence preference, format preference, or correction | Either | Update `<skill-root>/.tasteprint/conversation.json`; do not start browser collection. |

Before editing `conversation.json`, read `references/conversation-signals.md`.

Before any product recommendation workflow, read `references/task-hypotheses.md` and `references/recommender.md`.

### Step 1 — Authorization and Setup

Before launching the questionnaire, reading consent, or checking platform login state, read `references/questionnaire-and-consent.md`.

Use existing `cold-start-questionnaire.json` and `platform-consent.json` when present and non-empty. If consent is missing, use the questionnaire workflow rather than verbally asking the user to list platforms.

After consent is available, show authorized platforms and data range for confirmation, select and preflight a UI provider per `references/browser-connection.md`, then complete login precheck with that provider per `references/questionnaire-and-consent.md` and `references/browser-guidelines.md`.

---

### Step 2 — Data Collection

Before collection, read:

1. `references/browser-connection.md`
2. `references/browser-guidelines.md`
3. `references/data-schemas.md`
4. `references/platforms/README.md`
5. Only the platform files for authorized platforms

Complete all applicable data types for one platform before moving to the next. Basic types are `purchases`, `cart`, `bought_shops`, `favorites`, `follows`, and `bookmarks`; deep-dive types are `reviews`, `content`, and `footprint`.

After each data-type attempt, immediately write `<skill-root>/.tasteprint/raw-data/{platform}/{type}.json` using the envelope in `references/data-schemas.md`. Use exact statuses only: `collected`, `empty`, `partial`, `login_required`, `challenged`, `inaccessible`, or `unsupported`.

Never save whole-page text as records. Extract only from the active visible main content container. When an accessibility or DOM representation includes hidden/stale content, use the selected provider's supported visual or geometry checks; if it cannot isolate the active content safely, record `partial` instead of broadening extraction. Debug screenshots belong under `<skill-root>/.tasteprint/debug/` or a temporary directory and are not profile data.

**Per-platform completion check** — after each platform:
```
✓ Taobao done [1/6] — purchases collected | cart empty | bought_shops collected | favorites partial | follows collected | reviews collected | footprint collected
```

**Full collection check** — after all platforms, scan `<skill-root>/.tasteprint/raw-data/` to confirm coverage. Go back for any overlooked platform. Only proceed to Step 3 after passing this check.

---

### Step 3 — Analysis

Before analysis, scan `<skill-root>/.tasteprint/raw-data/` to confirm every authorized platform/data type has a status file or explicit failure. Do not build a profile from partial platform coverage unless the missing platforms were explicitly failed or skipped.

Then read `references/profile-analysis.md`. Read raw-data files one at a time; never load all raw data into context at once.

---

### Step 4 — Profile Synthesis

Follow `references/profile-analysis.md`, `references/domain-profile-template.md`, and `references/profile-template.md`.

Write domain profiles under `<skill-root>/.tasteprint/domain-profiles/` when a domain has sufficient data, then write `<skill-root>/.tasteprint/user-profile.md` as durable recommendation priors. Do not include current-task hypotheses, temporary constraints, raw dumps, or a long Deep Portrait.

---

### Step 5 — Conclusion

Output **only**: which platforms succeeded, which failed (with reasons), and that files have been saved.

```
User profile has been built.

Collection results:
- Taobao: ✓ Success
- JD.com: ✓ Success
- Xiaohongshu: ✗ Login expired; needs manual login to re-collect

Profile files have been saved and are ready for personalized recommendations.
```

Do not proactively include profile details, analysis summaries, or preference findings in the conclusion. The profile is a working document for recommendations, but it belongs to the user: if they ask to open the profile directory or delete profile data, help them do so according to their request.

---

## Platform Priority

When platforms are inaccessible or time is limited, use this priority:

| Priority | Platforms | Rationale |
|----------|-----------|-----------|
| Highest | Taobao/Tmall, JD, Amazon, Shopee | Complete order records, clear purchase intent |
| High | Xiaohongshu, Douyin (shopping) | Content highly correlated with purchase intent |
| Medium | YouTube, ChatGPT | Supplementary signals |
| Low | Bilibili, X, Facebook, LinkedIn | Content preference; weaker purchase signals |

Downgrade: can't login → skip and note; sparse data (<5 purchases/12mo) → basic only; user requests speed → prioritize highest/high platforms, deep-dive top 3 categories only.

---

## Update Run

1. Re-execute Steps 1–4 with incremental data. Append new raw records to the front of files and cap at 100.
2. Incorporate a "changes" dimension into domain profiles
3. Append a Changelog entry to `<skill-root>/.tasteprint/user-profile.md`
4. Do not merge old task hypotheses into the profile unless they satisfy durable profile-update rules in `references/task-hypotheses.md`

---

## Product Recommendations

### Workflow

For any product recommendation request, read `references/task-hypotheses.md`, then `references/recommender.md`, and follow the minimum viable recommendation workflow.
