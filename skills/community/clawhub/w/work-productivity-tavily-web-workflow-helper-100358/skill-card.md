## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical Tavily-style web search workflows, checklists, analyses, and implementation support for bug fixes, setup hardening, and reliability improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent users, skill authors, maintainers, and teams use this skill to turn Tavily-style web search and productivity needs into practical workflows, checklists, decision aids, code changes, or setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms and implicit invocation may cause the skill to be selected for unrelated web, API, or productivity requests.

Mitigation: Review trigger keywords and implicit invocation policy before deployment, and narrow activation terms if unrelated invocations appear during testing.

Risk: Workflow, checklist, code, or configuration guidance may be incomplete or misleading for a user's specific environment.

Mitigation: Require visible assumptions, success criteria, validation steps, and remaining risks in outputs, then review and test changes before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-100358)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [Ask HN: Claude Code for Ordinary User](https://news.ycombinator.com/item?id=48955119)
- [V2EX Daily Hotspot API Discussion](https://www.v2ex.com/t/1228342)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional checklists, code blocks, command snippets, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's stated goal and should expose assumptions, limits, validation steps, and remaining risks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
