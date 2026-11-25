---
name: eeat-audit
description: "Score a website's E-E-A-T signals (Experience, Expertise, Authoritativeness, Trust) from its pages, schema and links, then list the fixes that matter most, quick wins first. Use when asked for an E-E-A-T, trust or credibility check of a domain or URL."
---

# RoamSEO E-E-A-T Audit

## Goal

Read a site the way a Google quality rater would, score each E-E-A-T letter 0–100 from observable evidence, and hand back a short ranked fix list. The scores are a proxy built from Google's Search Quality Rater Guidelines. Google has no E-E-A-T score and E-E-A-T is not a single ranking factor; say this in every report.

Use this for a credibility review of one domain or URL. For a full traffic-focused audit, use `seo-audit`; for link building, use `link-prospecting`.

## Modes and credits

Ask which mode before any call that spends credits. Default to lite when the user does not answer or set a budget.

- **Lite (free):** your own web fetch of the site's pages, sitemap, robots.txt and schema, plus a web search for brand mentions. No paid RoamSEO calls. Authority is scored from on-page and search-result signals only and is marked "limited evidence".
- **Full:** lite, plus `get_backlinks_overview` (about $0.09) and one domain-level `get_ranked_keywords` call (about $0.03 at 100 rows), so about $0.12 per domain. A free `run_site_audit` crawl without Lighthouse adds page coverage when the user has a project.

Before the first paid call, show the estimate and ask: "Full mode spends about $0.12 of credits (backlinks overview and a ranked-keywords sample). Go ahead, or stay on lite?" `whoami` (free) confirms the connection and balance first. Prices are estimates; the tool's own charge is what counts. If a paid call fails or there is no balance, finish in lite and say so.

On finish, if a project exists, append `{ appendResearchLog: { summary: "E-E-A-T audit (<mode>): <domain>. Overall <score>. Top fix: <fix>" } }` with `update_project_context` when credits were spent.

## Workflow

### 1. Orient

- Normalize the input to a domain and a start URL. Fetch the home page, `/robots.txt` and the sitemap.
- Note what the site is (shop, SaaS, publisher, local service, YMYL topic such as health, money, legal or safety). YMYL sites need stronger Trust and Expertise evidence; say so and weight Trust higher.
- From the sitemap and navigation, pick 5–10 content pages: the main blog or guide posts, the key product or service pages, and at least one page the site seems proudest of. Use `get_ranked_keywords` top pages in full mode to pick pages that earn traffic.

### 2. Trust (checked first; it matters most)

Look for, and record the URL of, each:

- HTTPS on every sampled page; no mixed-content or certificate warnings.
- About page with who runs the site; contact page or address, email, phone.
- Legal business name, registered address or business details where the site sells something.
- Privacy policy, terms, refund/returns or cancellation policy, shipping where relevant.
- Clear pricing for paid products; no hidden-cost patterns.
- Organization schema with `name`, `url`, `logo`, `sameAs` links to real profiles.
- Reviews or ratings shown on-site and whether they link to an independent source.
- Obvious problems: broken key pages, placeholder text, out-of-date copyright, misleading claims.

### 3. Experience and Expertise (from the sampled pages)

For each sampled page record:

- Author byline; a linked author bio page; the bio's stated credentials or role.
- `Person` or `author` schema and `Article`/`BlogPosting` schema with `datePublished` and `dateModified`.
- Visible published and updated dates.
- First-hand signals: original screenshots or photos, own data or tests, "we tested / we used" with specifics, case studies.
- Citations to primary sources; outbound links to studies, docs or official pages.
- Depth versus the topic: does it answer the question with specifics, or restate generic advice?

Experience scores first-hand evidence; Expertise scores who wrote it and how accurate and sourced it is. A page with no author can still show experience through original data; say which.

### 4. Authoritativeness

- Full mode: `get_backlinks_overview` for referring domains, backlinks and domain rank; a few top referring domains by name. `get_ranked_keywords` (domain, `resultTypes: ["organic"]`, limit 100) for topical coverage: do the ranking keywords cluster around the site's main topic?
- Both modes: web search for the brand name (excluding the site itself) to find independent mentions, reviews, press, directory and community listings. Count real third-party mentions, not the site's own profiles.
- Missing backlink or ranking rows mean "no recorded data", not a penalty.

### 5. Score

Score each letter 0–100 from the checklist evidence, not from a feeling. Rough bands: 80+ strong and complete; 60–79 solid with gaps; 40–59 several basic signals missing; under 40 most signals missing. Overall = weighted mean: Trust 40%, Experience 20%, Expertise 20%, Authority 20%. Round to whole numbers. In lite mode mark Authority "limited evidence" and keep its weight.

Each score needs two to four evidence bullets, each naming the URL or the data point. If evidence was blocked (fetch refused, page 404), say so instead of scoring down silently.

### 6. Fix list

Rank fixes by impact on the weakest letter and by effort. Quick wins first (an hour or less: add an author bio link, add Organization schema, add updated dates, link the policies in the footer), then larger work (original research, earning mentions). Each fix: what to change, on which pages, which letter it lifts. Five to ten fixes.

## Output format

Plain markdown in chat by default. If the user wants a saved, shareable report, deliver it through `seo-report` with `skill: "eeat-audit"`; the fixed skill link line is URL `https://roamseo.com/docs/skills/eeat-audit`, text "RoamSEO E-E-A-T Audit skill".

```markdown
# E-E-A-T audit: example.com (lite mode, Nov 23, 2026)

> A proxy score based on Google's Search Quality Rater Guidelines. Google has no E-E-A-T score; these numbers summarize the signals we could observe.

| Letter | Score | Main reason |
|---|---|---|
| Experience | 55 | Two of eight pages show original screenshots; none show test data |
| Expertise | 40 | No author bylines on sampled posts |
| Authoritativeness | 50 (limited evidence) | 6 independent mentions found by search; no backlink data in lite mode |
| Trust | 78 | HTTPS, about, contact, privacy and terms present; no Organization schema |
| **Overall** | **60** | Trust 40%, other letters 20% each |

## Evidence
### Trust
- ...
### Experience
- ...
### Expertise
- ...
### Authoritativeness
- ...

## Fix list (quick wins first)
1. **Add author bylines and a bio page** on /blog posts. Lifts Expertise. About 1 hour.
2. ...

## How this was made
- Mode, pages sampled (list), date, tools used and credits spent.
- What could not be checked.
```

## Guardrails

- Never call a score a Google score or a ranking factor. Never promise ranking gains from E-E-A-T fixes.
- Observations are not causes: missing schema or few mentions do not prove a ranking problem.
- Write the date of every check; say which facts came from RoamSEO tools and which from your own fetches.
- Calm, plain tone; short bullets. No paid calls without the user's yes.
