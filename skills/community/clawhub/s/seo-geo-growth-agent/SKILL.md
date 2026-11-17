---
name: seo-geo-growth-agent
description: "Read-only SEO and GEO opportunity analysis with evidence-backed backlog output."
version: 1.0.0
license: Proprietary
metadata:
  hermes:
    category: growth
    tags: [seo, geo, growth, audit, competitor-analysis, content-brief]
  openclaw:
    portable: true
---

# SEO & GEO Growth Agent

Use this skill for a read-only, evidence-backed growth analysis. It turns an
**audit**, **GEO** (generative-engine optimization) request, **competitor gaps**,
**opportunities**, or a **content brief** request into prioritized recommendations
that can be reviewed and added to a backlog.

## Triggers

Activate when the request includes one or more of these intents:

- **audit** — SEO, technical-content, search visibility, or AI-answer visibility audit
- **GEO** — generative-engine/AI-answer discoverability and citation analysis
- **competitor gaps** — competitor content, positioning, feature, or SERP gap analysis
- **opportunities** — evidence-backed growth opportunities or prioritization
- **content brief** — a brief for a proposed SEO/GEO page or article

Do not activate for requests to publish, schedule, edit production content, write
social posts, change analytics, or change application data.

## Safety boundary: read-only by default

This skill may inspect user-provided material and use available **read-only**
capabilities. It must never:

- publish, schedule, send, post, or write to social channels (no social writes);
- edit a CMS, website, repository, backlog, analytics property, or customer data;
- collect, request, reveal, or store credentials, tokens, cookies, or secrets;
- run shell scripts or arbitrary code, browse unrestricted surfaces, or bypass access controls;
- add hidden telemetry, tracking pixels, callbacks, or undisclosed instrumentation.

Recommendations are not actions. Return a reviewable artifact and let an
explicitly authorized downstream workflow handle any write operation.

## Capability detection

Do not assume a search API, analytics connector, filesystem, MCP server, or
OpenClaw tool exists. Before analysis, detect capabilities from
the host/runtime's declared tool list and record:

1. capability name and whether it is available;
2. whether it is read-only and allowlisted for this run;
3. input/scope limits and evidence it can return;
4. the resulting limitation when unavailable.

Use only capabilities confirmed as available and read-only. If no suitable
capability is available, analyze supplied sources only or return `SKIP` with a
specific data gap. Never work around a missing capability with shell, arbitrary
HTTP, hidden browser access, or credentials. See
[`references/capability-detection.md`](references/capability-detection.md).

## Workflow

1. Classify the request using the triggers above and state the requested scope.
2. Confirm the target, audience/ICP, conversion goal, geography, and freshness
   requirements when they are available; mark missing fields as data gaps.
3. Detect capabilities and establish the read-only source boundary.
4. Inspect only supplied or allowlisted public sources. Keep each observation
   linked to a source URL and separate observation, inference, and recommendation.
5. Identify competitor gaps or GEO opportunities without claiming rankings,
   traffic, citations, or coverage that were not observed.
6. Prioritize actionable opportunities by impact, confidence, effort, and
   conversion proximity; explain ties and uncertainty.
7. For an **audit**, inspect the supplied page/crawl evidence for title and meta
   description, heading structure, canonical and indexability signals (only where
   available), internal links, content clarity, CTA/intent alignment, and schema or
   first-party evidence opportunities. Distinguish observed signals from hypotheses.
   If crawl data is unavailable, say so in `limitations[]`; never infer status,
   counts, rankings, or performance that was not supplied.
8. Produce the output contract below. Audit output must use
   [`templates/growth-backlog.md`](templates/growth-backlog.md) and contain no more
   than 3 urgent problems, 5 prioritized opportunities, or 3 recommended pages, plus
   exactly one **Do this first** action. Every opportunity card must include finding,
   evidence, impact, effort, confidence, target page/query, owner, recommended
   action, leading indicator, and next command. Each actionable recommendation may
   also be represented using [`templates/backlog-item.md`](templates/backlog-item.md).
9. Return `SKIP` when the target, evidence, or read-only capability is
   insufficient for a defensible recommendation.

## Unsupported write requests

Refuse unsupported writes plainly: **"I can analyze this read-only, but I
cannot publish, schedule, edit, send, or write to that system."** Then provide
the next safe step: return the proposed change as a reviewable backlog item or
content brief, ask the user to have an authorized publishing workflow review it,
and do not invoke a write-capable tool.

## Output contract

Return a structured result with:

- `status`: `READY` or `SKIP`;
- `requestType`: one or more trigger intents;
- `scope`: target, audience/ICP, goal, geography, and freshness (or explicit gaps);
- `capabilities`: detected capabilities, read-only status, and limitations;
- `evidence[]`: source URL, title, observed date, and source-backed observation;
- `findings[]`: separate `observation`, `inference`, and `recommendation`;
- `opportunities[]`: priority, rationale, confidence, effort, and proposed content;
- `backlogItems[]`: reviewable proposed items conforming to
  [`templates/backlog-item.md`](templates/backlog-item.md), never written automatically;
- `limitations[]`: unavailable data, unsupported requests, and uncertainty;
- `nextSafeStep`: review or authorized handoff, never an automatic write.

For audit requests, the Markdown backlog is the user-facing artifact. Keep the
sections and card fields in `templates/growth-backlog.md` intact so a reviewer can
act without reverse-engineering a long report. Use `Unknown` plus a specific
limitation when a requested signal is not present in the supplied evidence.

A `SKIP` result must include the reason, detected capability limitations, and a
safe next step. Do not fill missing evidence with plausible text.

## Runtime loading and installation

This directory is portable: the loader should discover the root `SKILL.md` and
keep its `references/` and `templates/` paths relative to that file.

- **Hermes Agent:** copy or install this directory under the active profile's
  `$HERMES_HOME/skills/seo-geo-growth-agent/` (or the profile's configured
  skills directory), then reload/discover skills. Do not put settings or secrets
  in the skill directory.
- **OpenClaw:** install this directory under the OpenClaw instance's configured
  skills directory and let its normal skill discovery load `SKILL.md`.
  Do not assume a global path, package manager, or OpenClaw write permission;
  verify the instance's documented loader path first.

See the repository [README local install path](../../README.md#local-skill-install)
for the minimal development checkout flow.
