## Description:

Helps agent users and skill authors turn Tavily-style web search workflow needs into practical plans, checklists, implementation support, and verification notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, skill authors, maintainers, and teams use this skill to adapt popular Tavily-style web search workflow demand into concrete local-friendly artifacts, workflows, checklists, analysis, code changes, or decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to activate for general web, search, or API requests where a more specific skill should handle the task.

Mitigation: Review and narrow trigger keywords before deployment when precise routing matters.

Risk: The skill can produce workflow advice, code changes, shell commands, or configuration snippets that may be incomplete or unsuitable for a specific environment.

Mitigation: Review generated artifacts before use and validate them against the user's stated success criteria.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-200354)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [Agent Browser Demand Signal](https://clawhub.ai/skills/agent-browser-clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, with code blocks or configuration snippets when implementation support is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, validation notes, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
