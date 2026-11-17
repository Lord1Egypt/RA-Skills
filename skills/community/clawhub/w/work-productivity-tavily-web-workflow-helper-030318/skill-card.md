## Description:

Helps agent users and skill authors plan, debug, harden, and validate Tavily-style web-search productivity workflows using local-friendly checklists, templates, analysis, and code-support artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn Tavily-style web-search workflow needs into practical plans, checklists, templates, code support, and validation notes. It is useful when improving reliability, setup safety, or adjacent productivity workflows without requiring cloud-only or large-training infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad web, search, API, and productivity trigger terms may invoke the skill outside its intended Tavily-style workflow-planning context.

Mitigation: Confirm that the user is asking for Tavily-style web research workflow planning, reliability guidance, or a closely related productivity workflow before applying the skill.

Risk: Workflow, checklist, code, shell command, or configuration suggestions may be incomplete or mismatched to the user's environment.

Mitigation: Validate outputs against the user's success criteria and review any operational commands or configuration changes before use.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-030318)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [Vector Search Discussion](https://news.ycombinator.com/item?id=48939470)
- [AZ Search API Priority Issue](https://github.com/az-digital/az_quickstart/issues/5783)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, templates, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's stated outcome and include a short verification note when useful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
