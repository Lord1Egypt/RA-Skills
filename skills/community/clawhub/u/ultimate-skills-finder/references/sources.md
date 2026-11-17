# Source Reference — Ultimate Skills Finder

Endpoints below were verified live against v1.3.5. Each entry records the
identifier shape the tool relies on and whether that identifier is
trustworthy enough to build an install command.

## Structured sources (installable)

These publish a machine-checkable identifier, so the tool validates it and
emits an argv array. Anything that fails validation yields no install
command rather than a mangled one.

### ClawHub — `clawhub.ai`

- **Endpoint:** `GET https://clawhub.ai/api/v1/search?q=<query>&limit=<n>`
- **Returns:** `results[]`

Two distinct entry shapes appear in the same list. `install.kind` is the
authoritative discriminator — **do not infer the format from the URL**:

| `install.kind` | `install.reference` | Emitted command |
|---|---|---|
| `clawhub` | `owner/slug` | `openclaw skills install @owner/slug` |
| `skills-sh` | `skills-sh:owner/repo/skill` | `openclaw skills install skills-sh:owner/repo/skill` |

ClawHub indexes skills.sh entries alongside its own, which is why a single
search returns both shapes. The `skills-sh:` prefix is stripped before
validation because `:` is not legal in a bare identifier.

Related endpoints, for reference only:

- `GET /api/v1/packages/<slug>` — package metadata
- `GET /api/v1/packages/<slug>/versions/<version>` — file manifest

`GET /api/v1/packages` is a **catalog listing**, not a search. It silently
ignores both `q` and `owner` and returns a recency-ordered feed. Use
`/api/v1/search`.

ClawHub search responses also carry `trust.upstreamScanners` — per-skill
verdicts from Snyk, Socket, and Agent Trust Hub. They arrive with the
search and involve no third-party disclosure. v1.3.5 does not yet surface
them; see the limitations note in SKILL.md.

### skills.sh — `skills.sh`

- **Endpoint:** `GET https://skills.sh/api/search?q=<query>&limit=<n>`
- **Returns:** `skills[]` with `id`, `source`, `skillId`, `name`, `installs`
- **Identifier:** `source` + `skillId`, both validated separately, composed
  into `skills-sh:<source>/<skillId>`

Backed by Algolia fuzzy search. The endpoint returns **no description
field**, so a skills.sh-only result shows a placeholder. Fetching detail per
skill would mean one extra request per hit, which v1.3.5 does not do.

## Browse-only sources

These surface text that a third party can freely edit. The tool shows a
name and a link and deliberately emits **no install command**, because an
identifier scraped from a README is not a product code.

### SkillsMP — `skillsmp.com`

- **Endpoint:** `GET https://skillsmp.com/api/skills?search=<query>&limit=<n>`
- **Returns:** `skills[]` with `name`, `description`, `author`, `githubUrl`
- **Curated:** no — raw aggregator

`stars` here is the **repository** star count, not a per-skill figure. v1.3.5
deliberately excludes it from ranking: treating it as skill popularity
saturates the popularity term and floated unrelated results above genuinely
installed ones.

### VoltAgent/awesome-openclaw-skills

- `https://raw.githubusercontent.com/VoltAgent/awesome-openclaw-skills/main/README.md`

### LeoYeAI/openclaw-master-skills

- `https://raw.githubusercontent.com/LeoYeAI/openclaw-master-skills/main/README.md`

Both are parsed as Markdown. Parsing degrades if the repositories change
their table format; there is no stable API.

## Third-party security scan (opt-in)

### Gen Digital — `ai.gendigital.com`

- **Endpoint:** `POST /api/scan/lookup` with `{"skillUrl": "..."}`
- **URL form:** the scanner parses exactly **two** path segments, `{owner}/{skill}`.
  ClawHub canonical URLs may carry a repo-style middle segment
  (`/owner/skills/name`), which the scanner reads as the skill name `skills`
  and answers "Skill not found". v1.3.5 rewrites ClawHub URLs to
  `{owner}/{last-segment}` before sending. Other hosts are sent unchanged.
- **All responses are HTTP 200.** Status must be read from the body. Two
  shapes were observed live on 2026-10-16:

  | Shape | Body |
  |---|---|
  | Verdict | `{"severity": "...", "reasons": [...], "author", "displayName"}` — **no `status` key** |
  | Error | `{"status": "error", "message": "...", "skillName", "author"}` |

- **Severity vocabulary:** `SAFE`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
  **All five verified live on 2026-10-16** across an 87-skill scan:
  `SAFE` x16, `MEDIUM` x7, `LOW` x4, `HIGH` x4, `CRITICAL` x1, and **no
  verdict x55**. Observed examples: `claw-shell` returned `CRITICAL`;
  `Code`, `BT Download`, `remote-ssh-bridge` and `Safe Shell` returned
  `HIGH`. Anything unrecognised is discarded and reported as "no verdict",
  never passed through as one.
- **No verdict is common.** 55 of 87 lookups returned nothing — the scanner
  could not resolve the slug. This is the scanner's limitation, not a clean
  result, and must never be rendered as an indication of safety.
- **Reasons:** the verdict body carries a `reasons` list, shown under the
  label (first three) and included in `--json` as `security_reasons`.
- **Retry:** 3 attempts, linear backoff. Retried: HTTP 429, HTTP 5xx, and the
  in-band outage `"Skill analyzer temporarily unavailable"` (which arrives at
  HTTP 200). Not retried: `"Skill not found on ClawHub or failed to fetch
  metadata"`, and any other 4xx — these are permanent.
- **No API key required**

v1.0.0 gated on `status == "done"`, a key no live response carries, so every
scan silently returned no result. It also sent the URL verbatim, so any
skill under a repo-style path (`/owner/skills/name`) was reported as not
found. Both are fixed.

`None` means "no verdict was available" and is displayed as such. It is
never rendered as an indication that a skill is safe.

## What leaves this machine

Corrected in v1.2.2. An earlier version of this file claimed the scan was
"the only part of the tool that sends data to a third party". **That was
false, and it is the one error in this package that could lead a user into
disclosing something they meant to keep private.**

| Action | Sends | To |
|---|---|---|
| **Any search** | the raw query string | clawhub.ai, skills.sh, skillsmp.com, raw.githubusercontent.com |
| `--scan` | every result URL | ai.gendigital.com |

So a plain search already discloses what the user is looking for. A client
name, an unreleased codename, or a confidential project typed into the query
lands in four third-party logs **before any consent flag is involved**,
because there is no flag for it. The query is not sent to Gen Digital; that
requires `--scan --share-urls`.

Mitigations actually in place: every response read is bounded by
`MAX_RESPONSE_BYTES`; every URL is scheme-checked before it can be sent;
`--scan` prints the disclosure count to stderr before transmitting; and
`--scan` alone exits without transmitting.

## Ranking

```
score = fit * 0.40 + breadth * 0.20 + popularity * 0.25 + authority * 0.15
```

- `fit` — `relevance(query, result)`: how well the result answers the query.
  Name matches count double description matches, prefix matches count 0.6,
  and an exact normalised name match saturates the term. An empty or
  all-stopword query returns a neutral 0.5 rather than 0, so a query with no
  signal cannot bury every result.
- `breadth` — how many of the 5 sources listed it, normalised
- `popularity` — **log-scaled**: `log1p(installs) / log1p(1e6)`, falling back
  to `log1p(stars) / log1p(2000)` when installs are absent. The earlier
  linear `installs / 10,000` clamped at 1.0 pinned 21 of 93 results in a
  measured corpus at exactly 1.00, so the term carried no information
  between popular skills — 11 installs and 1,069,913 scored alike. Raising
  that term's weight without fixing the scale would have added no signal.
- `authority` — the **strongest** source seen, not the first

`score()` called with no query keeps the legacy `breadth * 0.35 +
popularity * 0.35 + authority * 0.30` weighting, so existing callers do not
silently change rank. `--popular` sorts on raw installs and deliberately
bypasses relevance.

| Source | Weight |
|---|---|
| clawhub | 1.00 |
| awesome-list | 0.90 |
| skills.sh | 0.85 |
| master-skills | 0.85 |
| skillsmp | 0.70 |

Dedup requires normalised equality, or else token-prefix alignment *and* a
0.90 similarity floor. Raw substring containment was tried and rejected: it
merged distinct skills (`mail`/`email`, `sql`/`mysql`, `bar`/`foobar`) and
composed transitively, so `pdf`, `pdf-editor`, `pdf-editor-pro` and
`pdf-editor-pro-max` collapsed into a single result that then inherited all
four sources — inflating its own breadth score while hiding three real
skills.