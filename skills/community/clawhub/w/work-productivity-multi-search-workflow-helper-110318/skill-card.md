## Description:

Helps agent users, skill authors, maintainers, and teams create practical workflows, artifacts, checklists, analyses, and implementation support for Multi Search Engine-style productivity needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, AI-agent users, and teams use this skill to turn multi-search workflow needs into concrete plans, checklists, code changes, analysis, or adjacent skill designs. It emphasizes local-hardware-friendly execution and validation against explicit success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms and implicit invocation can activate the skill for unrelated search or productivity requests.

Mitigation: Narrow trigger terms during deployment or review the invocation context before relying on the skill output.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-multi-search-workflow-helper-110318)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [Agent Browser Demand Signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Coding Skills Development Report](https://news.ycombinator.com/item?id=48974093)
- [External Tool Integration Issue](https://github.com/ardelperal/codegraph-vba/issues/200)
- [Service Sandboxing Issue](https://github.com/juspay/services-flake/issues/705)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with optional code, shell command, checklist, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, limits, validation notes, and concrete next steps when useful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
