## Description:

Build a prioritized 1–30 day SEO roadmap from a site's Ahrefs Domain Rating, referring domains, backlink quality, Search Console and Google Analytics traffic, current rankings, landing pages, keyword metrics, live SERPs, and authority-matched SEO competitors. Use when the user asks what to do next for SEO, wants a 1-day, 3-day, 1-week, 15-day, or 30-day plan, needs a low-authority growth path, or wants to improve existing rankings toward the top results. Requires Rankizz MCP or REST API for the evidence-led workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners and SEO practitioners use this skill to turn Rankizz authority and search data, together with connected Search Console and Analytics evidence, into a prioritized SEO plan. It organizes work by timeline, page opportunity, backlink activity, and measurable outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rankizz-hosted API and MCP calls require at least 10 credits, and research calls may consume credits.

Mitigation: Check the available credits and explain the purpose of paid calls before using them; stop Rankizz calls on a low-credit response and refer the user to https://www.rankizz.com/billing.

Risk: API credentials could be exposed if shared in chat.

Mitigation: Do not ask the user to paste credentials into chat; direct them to https://www.rankizz.com/api-access for API access.

Risk: SEO recommendations could be mistaken for guaranteed ranking outcomes or precise measurements when data is incomplete or estimated.

Mitigation: Label evidence sources and limitations, keep unavailable metrics visible, distinguish estimates from first-party outcomes, and do not promise ranking positions.

## Reference(s):

- [Rankizz roadmap tool sequence](artifact/references/rankizz-roadmap-tools.md)
- [Roadmap decision rules](artifact/references/roadmap-decision-rules.md)
- [SEO roadmap output contract](artifact/references/roadmap-output-contract.md)
- [Google helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search ranking systems](https://developers.google.com/search/docs/appearance/ranking-systems-guide)
- [Google Search Console performance use cases](https://support.google.com/webmasters/answer/17010961)
- [Ahrefs Domain Rating definition](https://help.ahrefs.com/en/articles/1409408-what-is-domain-rating-dr)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown SEO roadmap with an evidence snapshot, prioritized actions, opportunity queue, backlink workstream, and measurement plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations distinguish first-party evidence, provider estimates, and inference; unavailable metrics remain identified as unavailable.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
