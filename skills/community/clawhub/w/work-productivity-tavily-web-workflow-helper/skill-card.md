## Description:

Helps agent users and skill authors create, troubleshoot, harden, and adapt Tavily-style web-search workflows into practical plans, checklists, code changes, and verification notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn demand for Tavily-style web-search workflows into concrete artifacts such as setup plans, bug-fix guidance, reliability checklists, adjacent skill designs, or implementation support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad routing language and implicit invocation may cause the skill to activate for ordinary web, search, or API requests.

Mitigation: Tighten activation keywords or require explicit invocation when deploying in environments where accidental routing could distract from the user's intended workflow.

Risk: Workflow guidance for web-search setup, bug fixes, or hardening may be incomplete or context-dependent.

Mitigation: Review generated plans, code, shell commands, and configuration changes before execution, and validate outputs against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Work Productivity Tavily Web Workflow Helper](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [Agent Browser Demand Signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Alternative to Internet Archive](https://news.ycombinator.com/item?id=49309061)
- [V2EX Web Workflow Demand Signal](https://www.v2ex.com/t/1234656)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code, shell command, checklist, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, limits, validation steps, and remaining risks when relevant.]

## Skill Version(s):

0.20260816.40342 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
