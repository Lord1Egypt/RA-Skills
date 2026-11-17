## Description:

AI-powered financial data assistant for stock analysis and global market overview, combining multiple QVeris data sources for company profiles, real-time quotes, fundamentals, valuation, analyst ratings, and news sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buxibuxi](https://clawhub.ai/user/buxibuxi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve structured financial data, generate stock analysis reports, and produce global market overviews through QVeris-backed data tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is auto-invoked and sends requests with a QVeris API key to qveris.ai.

Mitigation: Review before installation, consider explicit invocation instead of auto-invoke, and scope the environment so the API key is only available when this skill is intended to run.

Risk: The included helper can discover and call broader QVeris tools than the finance workflows described by the skill.

Mitigation: Use host-enforced tool scoping or review discovered tools before execution when a finance-bounded workflow is required.

## Reference(s):

- [QVeris homepage](https://qveris.ai)
- [ClawHub skill page](https://clawhub.ai/buxibuxi/skills/qveris-finance)
- [Tool Routing](references/tool-routing.md)
- [Output Templates](references/output-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown financial analysis summaries, market overview text, and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data timestamps, source attribution, and investment-advice disclaimers when financial data is presented.]

## Skill Version(s):

1.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
