## Description:

Xiaodi Financial Team coordinates finance-focused agents for stock and fund analysis, portfolio review, asset allocation, sentiment monitoring, and investment-style reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mx6315909](https://clawhub.ai/user/mx6315909)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-analysis workflows use this skill to coordinate multiple analyst roles for stock research, fund screening, holding diagnostics, asset-allocation planning, and market sentiment checks. Outputs are informational and should be independently verified before investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and broad file access.

Mitigation: Install only after review, remove or tightly scope exec access, and confine file reads and writes to a dedicated report/output area.

Risk: The skill can use memory around sensitive portfolio, trading-history, or risk-profile details.

Mitigation: Disable memory by default or require explicit consent before storing personal financial details.

Risk: The skill retrieves live market data from third-party finance sources and produces investment-style suggestions.

Mitigation: Verify market data and recommendations independently, avoid entering sensitive account data, and treat outputs as informational rather than investment instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mx6315909/skills/xiaodi-financial-analysis-team)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Architecture](artifact/architecture.json)
- [ClawHub metadata](artifact/clawhub.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with structured tables, ratings, recommendations, risk notes, and occasional JSON or command-oriented configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use live third-party market-data sources and user-provided portfolio details; outputs are advisory analysis, not execution.]

## Skill Version(s):

2.0.0 (source: server release evidence, artifact frontmatter, README, and ClawHub metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
