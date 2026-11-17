## Description:

Guides an agent through Qinghu AI-powered Ozon competitor-shop research, including shop selection, product mix analysis, trend checks, potential new-product monitoring, and concise replication recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and agents use this skill to analyze Ozon competitor shops, understand their product and price structure, monitor promising new listings, and produce actionable follow-up recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Qinghu credentials for Ozon competitor research.

Mitigation: Install and use it only when the agent is allowed to handle Qinghu credentials, and provide credentials through the disclosed token flow or environment variables.

Risk: Qinghu tool calls can consume account credits.

Mitigation: Review the planned Qinghu tools and expected purpose before approving calls, and require the agent to report actual credit usage from the returned envelope.

Risk: Large competitor-shop result sets may be written to local exported files.

Mitigation: Treat exported files as business data, share only intended paths, and remove files that should not remain on the local machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-ozon-shop-intercept)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys)
- [Qinghu login](https://www.iqinghu.com/workbench/login?type=1&urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with API-call examples, concise analysis, tables or exported files when result sets are large.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local exported data files for larger Qinghu result sets; user-visible outputs should include clear data scope and credit usage when paid calls are made.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
