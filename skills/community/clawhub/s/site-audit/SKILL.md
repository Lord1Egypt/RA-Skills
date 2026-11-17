---
name: site-audit
description: Use when the user wants a current site audit, technical SEO findings, Core Web Vitals interpretation, or a fresh TrustGrowth audit when connected. Supports connected, imported, and public/local evidence.
---
# Site Audit

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Sources

- Connected: TrustGrowth `issues` (open actionable by default; `?severity=critical|warning|info`, `?scope=backlog` for non-actionable open issues, `?status=fixed|all` for history), `summary`, and `changes`; manual audit only when explicitly requested and plan/scope allow it.
- Import: validated crawl/audit evidence supplied by the user.
- Open: inspect publicly observable pages and local artifacts. Report observations, not a proprietary score or historical trend.

Categories used: `~~web crawler`, `~~page speed`, `~~search console`. `references/connectors.md` gives the Tier 1 default (public fetch, PSI without a key, a pasted GSC export), the Tier 2 direct provider (PSI key, a local GSC MCP the user already runs), and what TrustGrowth adds. Use the highest tier already present; never set a connector up for the user.

## Interpret

Group pages by root cause. Separate directly observed facts from interpretation. Report `critical` findings first, `warning` next, `info` and externally owned/informational findings as context, and missing data as unknown. Do not estimate score impact. Treat one-off lab performance results as low confidence unless corroborated; distinguish lab from field evidence.

## Manual TrustGrowth audit

`POST /api/v1/sites/{slug}/trigger_audit` requires write scope and explicit user intent. Responses to handle:

- `202` — queued; response includes `data.job_id`. Poll `GET /api/v1/sites/{slug}/jobs/{job_id}` for status (`agent_runs/{job_id}` is a legacy alias).
- `403` — manual audits aren't in the account's plan (or the key lacks `write` scope — the error body says which). **Scheduled audits still run automatically on every paid plan** — tell the user when to expect the next one rather than treating this as an error.
- `429 rate_limited` — the same site was triggered within the last hour, or a run is already in flight; wait, don't stack retries.

Hand safe code-fixable findings to `fix-my-site`.

## When not to use

- Implementing fixes in the repository → `fix-my-site` (this skill finds and interprets; it does not edit code).
- AI-crawler reachability and answer-engine readiness → `ai-visibility`.
- Keyword or content planning from audit context → `keyword-scout`.
- A stakeholder-facing summary of results → `score-report`.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
