## Description:

Helps agent users, skill authors, maintainers, and teams turn multi-search-engine workflow demand into practical plans, checklists, analysis, code changes, and reliability improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to plan, debug, harden, and adapt multi-search-engine-style workflows. It emphasizes reusable local-friendly artifacts such as decision aids, templates, checklists, scripts, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loose trigger terms may cause the skill to be selected for ordinary search or workflow requests.

Mitigation: Confirm the requested outcome before using the workflow and tighten routing or explicit invocation settings where the platform allows.

Risk: Workflow proposals could introduce incorrect or misleading guidance into downstream skills or processes.

Mitigation: Review generated artifacts against the stated success criteria and scan any resulting skill before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-multi-search-workflow-helper-120220)
- [Popular ClawHub Skill Demand: Multi Search Engine](https://clawhub.ai/skills/multi-search-engine)
- [Popular ClawHub Skill Demand: Ontology](https://clawhub.ai/skills/ontology)
- [Popular ClawHub Skill Demand: Agent Browser](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Popular ClawHub Skill Demand: Tavily Search](https://clawhub.ai/skills/openclaw-tavily-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional code blocks, command snippets, templates, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and follow-up risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
