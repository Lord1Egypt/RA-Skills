## Description:

Helps agent users, skill authors, maintainers, and teams turn Tavily-style web workflow demand into practical plans, checklists, scripts, analysis, or implementation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to clarify Tavily or web-search workflow needs and produce actionable workflow artifacts. It supports bug fixing, setup hardening, reliability improvements, adjacent skill creation, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation language for Tavily and web-search workflow tasks, which may cause irrelevant use.

Mitigation: Prefer explicit Tavily, web-search, or workflow requests before invoking it, and confirm the user's outcome and success criteria before producing artifacts.

Risk: Generated plans, scripts, or configuration guidance can introduce incorrect workflow assumptions.

Mitigation: Review outputs against the user's stated constraints and include validation notes plus remaining risks before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-041220)
- [Requirement Plan](references/requirement-plan.md)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [GitHub API Missing Data Discussion](https://news.ycombinator.com/item?id=49003232)
- [Dependency Inventory Issue](https://github.com/kevensjames/wheellsverse-bots/issues/53)
- [Article Link Preview Feature Request](https://github.com/souravdasbiswas/linkedin-mcp-server/issues/4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with optional code, shell command, checklist, template, and validation sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should expose assumptions, limits, required inputs, validation notes, and remaining risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
