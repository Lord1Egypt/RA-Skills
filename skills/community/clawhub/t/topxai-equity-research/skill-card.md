## Description:

Institutional-grade equity, industry and macro research workflow for AI agents. Use it whenever the user wants a stock deep dive, an industry or value-chain report, a macro / strategy note, an earnings-season update of an existing report, a valuation with scenarios and a settleable rating, a bull/bear debate on a company, an adversarial audit of a research draft, SEC EDGAR / XBRL financial pulls, or to register, track and settle research calls (coverage watch, call ledger, track record). Also use it for Chinese requests such as 写研报, 个股深度, 产业链报告, 更新研报, 结算台账, 跑值守, even when the user does not say "research report". Every number must trace to a primary source with an evidence grade; every conclusion must be falsifiable; ratings are research judgments, never personalised investment advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unbelievablet](https://clawhub.ai/user/unbelievablet)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and research teams use the skill to create, update, and audit evidence-graded equity, industry, and macro research, and to track and settle research calls. Ratings are research judgments rather than personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The exhibit downloader could send contact details to an unintended website.

Mitigation: Fix and verify hostname and redirect checks before supplying contact information.

Risk: Monthly changes could alter the skill instructions without clear approval.

Mitigation: Require approval before applying monthly instruction changes.

Risk: Financial calculations or performance claims in published reports may be unreliable.

Mitigation: Preserve independent ledger history and verify calculated financial figures before publishing reports or relying on performance claims.

Risk: Research files persist in the project, and optional parallel research can consume substantial tokens.

Mitigation: Account for project-file persistence and monitor optional parallel research usage.

Risk: Secrets placed in SEC_USER_AGENT could be exposed during research requests.

Mitigation: Keep secrets out of SEC_USER_AGENT.

## Reference(s):

- [TopxAI Equity Research on ClawHub](https://clawhub.ai/unbelievablet/skills/topxai-equity-research)
- [TopxAI](https://ai.topxea.com)
- [Research framework](references/framework.md)
- [Research workflow](references/pipeline/02-research.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown research reports with supporting structured records and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-graded conclusions and ratings presented as research judgments, not personalized investment advice.]

## Skill Version(s):

1.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
