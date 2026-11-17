## Description:

Ticker Pipeline is a Chinese-language multi-agent equity research workflow that analyzes a ticker and date across fundamentals, valuation, market heat, news, and risk controls to produce an investment research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run a coordinated ticker research workflow that gathers market data, financial facts, news, and risk checks before producing a structured Markdown report. It is intended as research support and not as guaranteed investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial ratings and target prices may be incorrect, stale, or unsuitable for a user's situation.

Mitigation: Treat outputs as research support, verify source data independently, and do not rely on the generated report as guaranteed investment advice.

Risk: The workflow may call market, news, or web tools and use subagents to gather current information.

Mitigation: Install only when those tool calls are expected, and review tool access policies before running the skill in sensitive environments.

Risk: The skill can create persistent Markdown report files in the workspace.

Mitigation: Run it in a workspace where report creation is acceptable and review generated files before sharing or acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fize/skills/ticker-pipeline)
- [Publisher profile](https://clawhub.ai/user/fize)
- [Skill definition](artifact/SKILL.md)
- [Ticker report template](artifact/templates/ticker_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance, files]

**Output Format:** [Markdown reports with JSON fact blocks and YAML frontmatter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent report files under ./report/ticker/ in the user's workspace.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
