## Description:

Run and interpret a hosted Rankizz website audit through Rankizz MCP or REST API, including a robots-aware crawl, prioritized SEO issues, crawled-page evidence, and optional Lighthouse measurements. Use when the user explicitly wants a Rankizz, cloud, hosted, large-site, or repeatable site audit. Do not use for a local-only audit without Rankizz access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners, SEO practitioners, and developers use the skill to run a hosted Rankizz crawl and turn its findings into an evidence-based audit report with prioritized actions and explicit coverage limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud crawl and Lighthouse work can consume account credits.

Mitigation: Confirm the page budget and Lighthouse choice before starting; stop cloud calls if Rankizz reports insufficient credits.

Risk: Blocked or partial crawls and heuristic checks can limit what the report supports.

Mitigation: Report actual coverage and page evidence, and mark GEO or AEO dimensions not assessed when retrieved content does not support them.

Risk: The workflow uses hosted account credentials.

Mitigation: Use OAuth or client-side secret storage and never paste an API key into chat.

## Reference(s):

- [Rankizz cloud audit tool sequence and scope controls](artifact/references/rankizz-audit-tools.md)
- [Site audit report contract](artifact/references/report-contract.md)
- [Rankizz MCP endpoint](https://www.rankizz.com/mcp)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Concise chat summary and Markdown or HTML audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based findings include severity, affected scope, observed evidence, recommended action, impact, effort, source, and retrieval date; the report states crawl coverage and limitations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
