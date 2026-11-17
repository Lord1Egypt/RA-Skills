## Description:

Research Harness is an open prompt stack that routes public-market research tasks into structured workflows for company deep dives, industry maps, earnings reviews, model checks, red-team analysis, PM briefs, and research briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joansongjr](https://clawhub.ai/user/joansongjr)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, fund managers, and investment-research teams use the skill to plan data gathering, grade evidence, produce structured public-market research outputs, and archive work for later review across A-shares, Hong Kong stocks, US equities, funds, and cross-market themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prompt stack can broadly steer the assistant and route market-related or vague prompts into its workflow automatically.

Mitigation: Review the system-prompt enablement and routing behavior before installation, and enable it only in workspaces where automatic investment-research routing is desired.

Risk: The workflow can persist local task state and archived research outputs in the workspace.

Mitigation: Install it only where local research state and archived outputs are appropriate, and periodically review generated .task-pulse, .checkpoint, active task, coverage, and archive files.

Risk: Investment-research outputs may be mistaken for investment advice or definitive market data.

Mitigation: Use the documented compliance boundaries: do not treat outputs as investment advice, verify key facts and data sources, and require qualified human review for ratings, target prices, or forecast changes.

## Reference(s):

- [Research Harness on ClawHub](https://clawhub.ai/joansongjr/skills/research-harness)
- [Data Adapters](core/adapters.md)
- [Compliance](core/compliance.md)
- [Output Archive](core/output-archive.md)
- [Markets](core/markets.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, checklists, routing decisions, data-source plans, and workspace archive files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local task state and archived research outputs such as .task-pulse, .checkpoint, active task records, coverage folders, and dated research files when the workflow is enabled.]

## Skill Version(s):

0.7.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
