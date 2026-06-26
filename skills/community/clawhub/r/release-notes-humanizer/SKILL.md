---
name: cm-release-notes-humanizer
description: Turn a raw git log, PR title list, or changelog dump into customer-facing release notes that read like a human wrote them. Detects categories (new feature / improvement / fix / breaking change / removed), filters internal/refactor noise, groups items by user value, rewrites every line from "Added X" to user-benefit framing, and generates per-audience versions (in-app changelog, email blast, developer changelog, marketing tweet, status-page note). Covers tone modulation, emoji rules, version numbering schemes, and template patterns from Linear, Stripe, Vercel, Figma, Tailwind, and Notion. Triggers on "release notes", "changelog", "what's new", "version notes", "humanize changelog", "rewrite release", "v1.2 release", "ship notes", "product update post", "patch notes", "semver", "calver".
metadata:
  tags: ["release-notes", "changelog", "product-marketing", "developer-experience", "documentation", "writing", "shipping", "saas", "communications"]
---

# Release Notes Humanizer

Take a raw input — git log, list of merged PR titles, Linear cycle dump, or a half-written changelog draft — and produce polished release notes for every audience that needs to hear about the release. Acts as an experienced product marketer with a developer's understanding of the underlying changes, modeled on the changelogs of Linear, Stripe, Vercel, Figma, and Tailwind.

## Usage

Invoke this skill anytime you have a release going out and a pile of raw shipping artifacts that need to become readable customer communication.

**Basic invocation:**
> Humanize this git log into release notes: [paste]
> Turn these 30 PR titles into a v2.3 changelog
> Rewrite our draft release post in the Stripe style
> Generate the in-app changelog, email, and tweet for this release

**With context:**
> Here's the diff summary, the marketing tweet must be under 240 chars
> We use calver (2026.5) — adjust the heading
> Audience is mostly indie developers — keep the dev tone
> This release has one breaking change — make sure it's loud

The agent produces a categorized, audience-segmented release note set ready to publish to changelog page, in-app modal, email blast, social, and developer changelog.

## How It Works

### Step 1: Input Parsing

The agent accepts these raw inputs and normalizes them into a single line-per-change list:

| Input type | What the agent extracts |
|------------|------------------------|
| **Git log** (`git log --oneline v1.2..HEAD`) | Commit subject, drops merge commits, drops trivial chores |
| **PR titles** (GitHub / GitLab / Bitbucket) | Title, label, author, linked issue if present |
| **Linear cycle export** | Issue title, project, labels, type field |
| **CHANGELOG.md draft** | Existing markdown bullets, preserves manual notes |
| **Conventional Commits** (`feat:`, `fix:`, etc.) | Uses the prefix as the category hint |
| **Squashed PR descriptions** | Reads description body for "What" and "Why" sections |

Conventional Commit prefixes the agent recognizes for category routing:

```
feat:      → New feature
fix:       → Fix
perf:      → Improvement (performance)
refactor:  → INTERNAL — drop unless user-visible
chore:     → INTERNAL — drop
docs:      → Drop unless customer-facing docs
test:      → INTERNAL — drop
ci/build:  → INTERNAL — drop
revert:    → Mention if a previously-shipped feature is rolled back
breaking:  → Breaking change (always promote to its own section)
```

### Step 2: Noise Filtering

A typical release contains 60-80% noise from the customer's perspective. The agent drops these by default and flags them for review:

**Always drop:**
- "Refactor X module" (unless it ships as a perf improvement)
- "Update dependencies" (unless it's a major framework bump customers care about)
- "Fix typo in internal docs"
- "Add unit test for Y"
- "Bump version"
- "Improve CI pipeline"
- "Add eslint rule"
- "Rename variable X to Y"

**Promote even if engineering tagged it internal:**
- Anything touching billing or subscriptions
- Anything touching auth or session management
- Any "fix" that resolves a customer-reported issue (label: `customer-reported`)
- Any rate limit, quota, or API change
- Any UI change visible without feature flag

**Ambiguous → flag for human review:**
- Library upgrades that change behavior (e.g. timezone library, markdown parser)
- Schema migrations
- Cron / background job changes that may affect data freshness

### Step 3: Category Routing

The agent puts every surviving line into one of five buckets, in this fixed display order:

```
1. BREAKING CHANGES   — anything requiring user action to keep working
2. NEW                — net-new functionality the customer can use
3. IMPROVED           — existing functionality made better (perf, UX, polish)
4. FIXED              — bugs squashed
5. REMOVED / DEPRECATED — features sunset or scheduled for removal
```

**Routing rules:**

| Trigger | Bucket |
|---------|--------|
| API endpoint signature changed, env var renamed, default behavior changed | BREAKING |
| New page, button, command, integration, plan tier, API endpoint | NEW |
| Faster, fewer clicks, better error messages, redesigned panel | IMPROVED |
| "Fix:" prefix or anything resolving a regression | FIXED |
| "Removed", "deprecated", end-of-life | REMOVED |

**The "user can do something they couldn't yesterday" test**: if yes → NEW. If they could already do it but it now works better → IMPROVED. The two buckets aren't interchangeable; getting them confused makes the changelog feel padded.

### Step 4: Rewriting from "Added X" to User Benefit

This is where most internal changelogs fail. They read as a developer log, not a product update. The agent applies four rewrite rules.

**Rule 1: Lead with the verb the user does, not the verb the team did.**

```
Before: "Added bulk export functionality"
After:  "Export up to 10,000 rows at once from any table"

Before: "Implemented dark mode"
After:  "Switch to dark mode in Settings → Appearance"

Before: "Created Slack integration"
After:  "Send notifications straight to Slack — connect in Integrations"
```

**Rule 2: Quantify whenever possible.**

```
Before: "Made dashboard load faster"
After:  "Dashboard loads 3.2× faster — average load time down from 1.4s to 430ms"

Before: "Improved search"
After:  "Search now returns results in under 100ms across workspaces with 50,000+ items"
```

**Rule 3: Drop developer artifacts.**

```
Before: "Migrated user settings to PostgreSQL JSONB column for performance"
After:  "Settings save instantly — no more 'saving…' spinner"

Before: "Refactored billing webhook handler with idempotency keys"
After:  "Plan changes apply immediately — no more delayed activations after upgrade"
```

**Rule 4: Tell the user what to do next.**

For NEW items, end with a CTA: "Try it in [path]" or "Read the guide".
For BREAKING changes, end with the migration step.
For FIXED items, no CTA needed — just confirm the fix.

**Anti-patterns the agent removes:**

- "We're excited to announce…" (zero information; if everything is exciting nothing is)
- "Under the hood improvements" (either it matters to users or it doesn't)
- "Various bug fixes and improvements" (lazy; itemize or drop)
- "As always, please reach out if you have feedback" (boilerplate; move to footer if at all)
- "We listened to your feedback" (condescending; just ship the fix)
- "🎉🚀✨" emoji clusters (one per section maximum)

### Step 5: Grouping by User Value

After rewriting, re-order within each bucket so highest-value-to-most-users items appear first:

1. Largest user segment first — features for everyone before features for power users.
2. Most-requested first — anything tagged customer-reported rises.
3. Hero feature first if the launch has one, even if narrower.
4. Visible UI changes before invisible — users can verify they got the update.

The agent also **clusters thematically related items**. Three small fixes to the search UI become one "Search polish" bullet with three sub-bullets — feels like progress, not random noise. Three loose fixes to dashboard tooltip, billing PDF, and export filename encoding stay separate under "Other fixes."

### Step 6: Per-Audience Generation

A single set of release notes can't serve every channel. The agent generates four-to-five distinct outputs from the same source.

**Audience 1 — In-app changelog modal**: 200-400 words, first-person present-tense. Structure: `# What's new in [version] — [date]` → headline feature with CTA button → "Also new" bullets → "Improvements" → "Fixes" → footer link to full changelog. Must work without context (reader is mid-task).

**Audience 2 — Email blast**: scannable on mobile, hook in preview text, single primary CTA. Subject = action verb the user can now do. Preview = concrete benefit + number. Body = one-sentence hook → 2-3 sentence elaboration with specific use case → primary CTA button → "What else is new" (3-5 bullets) → P.S. for one thing that would otherwise get buried (often a customer-requested fix). Tone warmer than in-app.

**Audience 3 — Developer changelog (CHANGELOG.md)**: thorough, technical, version-anchored. Sections: `### Breaking changes` (with old/new signatures + migration code), `### Added` (API endpoints, env vars with defaults), `### Changed` (behavior diffs), `### Deprecated` (with removal version), `### Fixed` (with issue ref), `### Security` (CVE, severity, action). One H2 per version, dated YYYY-MM-DD.

**Audience 4 — Marketing post**: Twitter/X 240 chars max — `[Hero feature] is live in [Product] [version]. [Specific benefit with number]. [link] [image/GIF]`. LinkedIn 600 chars — hook line, 3-line elaboration (why, who, what it replaces), 1-line CTA + link.

**Audience 5 — Status-page note** (for breaking changes/migrations only): factual, timestamped, action-required. `[Date Time TZ] — [Version] released. This release includes a breaking change to [component]. Action required by [date]: [step]. Affected: [segment]. Guide: [link].`

### Step 7: Tone Modulation

The agent matches tone to product persona. Three calibrated modes:

| Mode | Voice | Examples |
|------|-------|----------|
| **Developer-tool** (Vercel, Linear, Stripe, Tailwind) | Terse, technical, dry humor allowed, no emoji clusters, code-first | "We rewrote the build pipeline in Rust. Builds are 4× faster." |
| **Prosumer-SaaS** (Notion, Figma, Superhuman) | Warm, polished, present-tense, sparing emoji, designer-led | "Pages now load smoother. Try a long doc — you'll feel the difference." |
| **Mass-market** (consumer apps, freemium tools) | Energetic, friendly, emoji acceptable, GIFs and screenshots heavy | "Dark mode is here! 🌙 Toggle it in Settings." |

Mode is set per-product and propagates across all five audience outputs. The agent never mixes modes — a Vercel-style in-app changelog with a mass-market email is jarring.

### Step 8: Emoji Rules

Emoji misuse is the single biggest tell of an unedited changelog. Hard rules:

- **Maximum one emoji per section heading**, never inside body sentences.
- **No emoji clusters** — `🎉🚀✨` is amateur.
- **Functional > decorative**: ✅ for fixed, ⚠️ for breaking, 🆕 for new, 🚀 only for genuinely big launches (annual, not weekly).
- **Skip emoji entirely** in developer-tool mode and in any breaking-change section. Authority requires sobriety.
- **Mass-market mode** can use one emoji per bullet but only if the brand voice already does.
- **Never use 💩 / 😎 / 🤯** in product communications even if the team Slack does.

### Step 9: Version Numbering

The agent uses your chosen scheme consistently across all outputs.

**Semver** (`MAJOR.MINOR.PATCH`, e.g. `2.3.1`)

```
MAJOR — incompatible API changes
MINOR — backward-compatible new functionality
PATCH — backward-compatible bug fixes
```

Use when: API stability matters (libraries, SDKs, public APIs, infrastructure tools). Breaking changes are loud and require a major bump.

**Calver** (`YYYY.MM` or `YYYY.MM.DD`, e.g. `2026.5` or `2026.05.02`)

Use when: continuous deployment, no formal API contract, rapid iteration. The version conveys recency, not stability. Examples: Ubuntu, Unity, JetBrains, OpenClaw.

**Marketing version** (`v1`, `v2`, `v3` or named like Apple's `iOS 17`)

Use when: external announcements, hero releases, app store listings. Decoupled from internal semver.

**Hybrid** (most common in SaaS):

```
Internal:    2026.5 (calver) for daily releases
Marketing:   v3 "Atlas release" for the quarterly hero feature
API:         /v1, /v2 (semver-style) for breaking endpoint changes
```

The agent recommends hybrid for any product with both a marketing surface and a developer surface. Linear and Vercel both use this pattern.

### Step 10: Template Patterns from Best-in-Class Changelogs

The agent draws from these canonical examples:

**Linear** — Dated reverse-chronological, single-page scroll, GIF per release, terse headline + 2-3 sentence body, subtle emoji per category, RSS feed.

**Stripe** — API-first changelog separate from product blog. Strict Added/Changed/Deprecated/Removed. Every breaking change ships with a migration code sample. No emoji in the API changelog.

**Vercel** — Marketing-style hero post for big launches; concise per-feature pages; technical depth one click away; branded illustration per release.

**Figma** — Quarterly hero release ("Config 2026") with named features; weekly small updates in an in-app "What's new" panel; annotated screenshots for every UI change.

**Tailwind CSS** — Long-form blog post for major versions with extensive before/after code samples; plays as both marketing and upgrade guide; OSS migration tooling links.

**Notion** — In-app modal on launch day, archived to a public changelog page; heavy on screenshots and short videos; friendly tone, single primary CTA per release.

The agent picks the closest template to your product's persona unless you specify.

### Step 11: Breaking Change Handling

Most teams botch breaking changes. The agent always:

1. Promotes the breaking change to the top of every audience output, even ahead of a flagship feature.
2. Declares the deprecation timeline: announcement → default-behavior change → old-behavior removal dates.
3. Provides a migration code sample (before/after) in the developer changelog.
4. Sends a separate email to affected customers, segmented from the general newsletter.
5. Posts to the status page with action-required language.
6. Tags the email subject with `[Action Required]`.

Template fields: `## ⚠️ Breaking — [component]` → What changed (1 sentence) → Why (perf/security/correctness) → Action required → Deadline → Migration (before/after code) → Questions link.

## Worked Examples

### Example 1: Raw Git Log → In-App Changelog

**Input** (10 commits from a developer-tool product):

```
feat: add bulk export to CSV
feat: dark mode
fix: search highlighting on mobile
fix: csv export filename encoding on windows
perf: reduce dashboard p95 latency by 60%
refactor: extract billing module
chore: bump deps
fix: rare double-charge on plan upgrade webhook race
docs: update api reference
feat: slack notifications for workspace events
```

**Agent output** (in-app, developer-tool tone):

```
## What's new — 2026.5

### New
**Bulk CSV export** — Export up to 10,000 rows from any table at once.
Available in the table toolbar.

**Slack notifications** — Get pinged in Slack when workspace events fire.
Connect in Settings → Integrations → Slack.

**Dark mode** — Switch in Settings → Appearance.

### Improved
- Dashboard 60% faster — p95 load time down from 1.2s to 480ms.

### Fixed
- ⚠️ Resolved a rare double-charge that could occur during a plan upgrade if
  the webhook retried within 200ms. Affected ~0.05% of upgrades; we are
  refunding identified cases automatically.
- CSV exports with non-ASCII filenames open correctly on Windows.
- Search result highlighting now works on mobile.
```

Note: the agent dropped `refactor`, `chore`, `docs`. It promoted the double-charge fix with a warning indicator and named the impact explicitly because money + correctness deserves transparency.

### Example 2: Same Input → Marketing Tweet + Email Subject

**Tweet** (240 chars):

```
v2026.5 is live.

Dashboard now 60% faster (p95: 1.2s → 480ms), bulk CSV export up to 10k rows,
Slack notifications, dark mode.

Patch notes: [link]
```

**Email subject options** (the agent generates 3, picks one):

```
A. "Bulk export, Slack, and a 60% faster dashboard"   ← picked
B. "What's new in [Product] — May release"
C. "Dark mode is here (and four other things)"
```

Reasoning: A leads with the most concrete benefit + a number. B is generic. C buries the lead behind dark mode (lower-impact than perf for this audience).

### Example 3: Breaking Change Promotion

**Input**: `breaking: rename API param customer_id to customerId for consistency`

**Output** (developer changelog): `## ⚠️ Breaking — API parameter renamed`. Lists affected endpoints (`POST /v1/orders`, `POST /v1/subscriptions`, `GET /v1/customers/:id/invoices`). Declares 60-day deprecation window — old param logs warning until 2026-07-01, returns HTTP 400 after. Before/after JSON sample. Notes that SDK v3.4+ auto-handles. Agent also drafts separate `[Action Required]` email to affected customers and a status-page note timed to the deprecation deadline.

## Output

The agent produces:

- **Filtered + categorized line list** — every input line dropped, kept, or flagged with the bucket
- **In-app changelog** — modal-ready markdown, 200-400 words
- **Email blast** — subject (3 options), preview text, body, primary CTA
- **Developer changelog** — CHANGELOG.md-format markdown with semver/calver heading
- **Marketing post** — Twitter/X (≤240 chars) and LinkedIn (≤600 chars) variants
- **Status-page note** — only if breaking changes or migrations are present
- **Migration guide stub** — for any breaking change, with before/after code samples
- **Tone-mode setting** — declared up-front (developer-tool / prosumer-SaaS / mass-market)
- **Version heading** — formatted to your scheme (semver / calver / hybrid)

## Common Scenarios

### "We have weekly releases — write less per release"
Use the Linear pattern: dated entry, 1-line headline, 3-5 bullets max. Skip the email blast unless something is genuinely user-impacting. The in-app changelog is enough.

### "We have a quarterly hero release with 100+ items"
Use the Tailwind / Figma pattern: long-form blog post for the hero, with named feature sections, before/after screenshots, and a TL;DR at the top. Bury minor items in a collapsed section at the bottom or link to the developer changelog for details.

### "Half of our changes are internal, what stays?"
Use the noise filter (Step 2). When in doubt, ask: would a customer notice this if we didn't tell them? If no, drop it. The exception is anything touching auth, billing, or data — those get mentioned even if the change is invisible.

### "Our team writes the changelog and it sounds robotic"
Replace every "Added" / "Updated" / "Implemented" verb with the user's verb. "Added a filter" → "Filter the inbox by sender". Run the rewrite as the very first pass, before categorization — once the verbs are right, the rest follows.

### "Should every release have an email?"
No. Email blasts have a fatigue cost. Send for: (1) hero releases, (2) breaking changes, (3) anything that changes the user's billing or workflow defaults. Weekly UI polish does not need an email — let the in-app changelog handle it.

### "Our product has free and enterprise tiers — same notes for both?"
Tier-segment the email. Free users get the marketing-tone note about consumer features. Enterprise gets a calmer note that highlights compliance, security, audit log, and SSO changes — and never mentions consumer features they don't have access to.

## Tips for Best Results

- Paste the raw git log or PR list directly — the agent extracts more signal from raw input than from a half-edited draft.
- State the version number scheme (semver, calver, hybrid) up-front so headings come out right.
- Tell the agent your product's tone mode (developer-tool, prosumer-SaaS, mass-market) — it changes every output.
- Flag any breaking changes explicitly so the agent promotes them; commit messages don't always make this obvious.
- Provide last release's notes as a reference style — the agent will match the voice and section pattern.
- Mention the audience size split (e.g. 80% indie devs, 20% enterprise) so tone calibrates correctly.

## When NOT to use

- **Open-source library with strict semver and a CONTRIBUTING.md changelog format** — keep the auto-generated `Added/Changed/Fixed` from `git-cliff` or `release-please`. Customer-friendly rewrites are wrong tone for this audience.
- **Regulated industries (HIPAA, PCI, SOX) where every release needs a formal audit trail** — use compliance-grade release notes (timestamps, commit hashes, sign-offs) generated by the audit pipeline. A humanized note is supplementary, not primary.
- **Internal tools used by 5 employees** — overhead exceeds value; a Slack message in #engineering covers it.
- **Pre-launch alpha/beta with a shifting feature set** — release notes imply stability that doesn't exist yet. Use a known-issues board instead.
- **Status-page incident reports** — different format (incident timeline, root cause, action items). Don't mix these into release notes; users get confused about what's broken vs what's new.
- **Marketing launch posts for a hero feature** — those need a full narrative, customer quotes, social proof, and pricing context. Release notes are a supporting artifact, not the launch asset itself.
