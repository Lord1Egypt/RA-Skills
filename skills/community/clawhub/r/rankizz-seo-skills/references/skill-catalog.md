# Rankizz specialist skill catalog

Use this catalog to route the user's task. Install only the skills required for the current outcome.

## Foundation and planning

| User need | Skill | Rankizz usage | Expected result |
| --- | --- | --- | --- |
| Create durable context for a site or client | `rankizz-setup-seo-project` | Optional | `PROJECT.md`, evidence inventory, next workflow |
| Build a 1, 3, 7, 15, or 30-day plan | `rankizz-build-seo-roadmap` | Required | Authority and traffic diagnosis, execution queue, backlink goal |

## Audits

| User need | Skill | Rankizz usage | Expected result |
| --- | --- | --- | --- |
| Crawl with the current device and public network | `rankizz-audit-site-local` | None | Bounded crawl, prioritized technical findings |
| Run and persist a hosted crawl | `rankizz-audit-site-cloud` | Required | Hosted audit, issue priority, page evidence |
| Check one page or template before publishing | `rankizz-audit-on-page-seo` | Optional | Metadata, canonical, hreflang, images, links, schema, indexability QA |

Choose local audit by default when either method can answer the question. Choose cloud audit for persistence, scale, or Rankizz-specific evidence. Do not run both merely to produce more output.

## Search research

| User need | Skill | Rankizz usage | Expected result |
| --- | --- | --- | --- |
| Find query opportunities and current metrics | `rankizz-research-keywords` | Optional | Prioritized keywords, intent, evidence |
| Group a keyword list into pages | `rankizz-cluster-keywords` | Optional | Intent clusters, page map, cannibalization findings |
| Identify the sites winning a market | `rankizz-map-competitive-landscape` | Optional | Search competitors, formats, defensible gaps |
| Analyze one competitor | `rankizz-analyze-competitor` | Optional | Ranking, page, traffic, authority, and strategy gaps |
| Find relevant sites that could link | `rankizz-prospect-links` | Optional | Qualified domains, editorial fit, outreach angles |

Use local files or public research when the user already supplied sufficient evidence. Add Rankizz MCP or REST when fresh keyword metrics, SERPs, domain ratings, backlink data, Search Console, analytics, or saved project data changes the decision.

## Editorial content

| User need | Skill | Rankizz usage | Expected result |
| --- | --- | --- | --- |
| Write a source-backed natural article | `rankizz-write-human-blog-post` | Optional | Brief, human draft, publication package |
| Write a best-tools roundup | `rankizz-write-tool-listicle` | Optional | Criteria, fair ranking, current tradeoffs |
| Write alternatives to a competitor | `rankizz-write-alternatives-page` | Optional | Switching criteria, alternatives, migration-aware draft |
| Compare the user's product with a competitor | `rankizz-write-comparison-page` | Optional | Equal evidence matrix, pricing normalization, buyer verdict |
| Review competitor capabilities and pricing | `rankizz-write-competitor-review-pricing` | Optional | Current pricing snapshot, limitations, buyer recommendation |

Do not start drafting until the workflow has enough current evidence. Fresh product claims and pricing must be verified from primary sources.

## Social and outreach

| User need | Skill | Rankizz usage | Expected result |
| --- | --- | --- | --- |
| Draft a subreddit-native post | `rankizz-write-reddit-post` | Optional | Rule-aware human post with one transparent mention |
| Find Reddit discussions and prepare reply drafts | `rankizz-find-reddit-reply-opportunities` | Required | Thread queue, links, transparent local Markdown reply report |
| Research and draft a LinkedIn post | `rankizz-write-linkedin-post` | Required | Observed patterns and knowledge-first post report |
| Find public outreach contacts | `rankizz-find-outreach-emails` | None | Role-relevant emails with source evidence |
| Write a backlink outreach message | `rankizz-write-backlink-outreach-email` | Optional | Page-specific subject, body, CTA, and send checklist |

Never automate publishing, voting, commenting, unsolicited bulk sending, or disguised promotion. The user reviews and sends every social or outreach draft.

## Common multi-skill sequences

- New site with no durable context: project setup, then the one audit or research skill that matches the immediate goal.
- Technical launch review: local site audit, then on-page SEO audit for priority templates.
- Content opportunity plan: keyword research, clustering, then the matching editorial-writing skill.
- Competitive landing page: competitor analysis, then comparison, alternatives, or review/pricing writing.
- Link campaign: link prospecting, outreach email finder, then backlink outreach email writing.
- Broad growth roadmap: SEO roadmap first; install its recommended execution skill only after the roadmap identifies the bottleneck.

Do not install every skill in a sequence upfront. Install the next specialist only when its input is ready.
