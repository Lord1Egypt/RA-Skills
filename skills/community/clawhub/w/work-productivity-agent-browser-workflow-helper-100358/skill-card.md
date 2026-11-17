## Description:

Helps agent users, skill authors, maintainers, and teams create practical Agent Browser-style workflows for bug fixing, setup hardening, safety, reliability, and adjacent skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn Agent Browser-style automation needs into actionable workflows, checklists, analyses, code changes, or implementation support. It is intended for practical work-productivity tasks that should remain local-hardware friendly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser and automation trigger wording may activate the skill for requests where the user did not intend to use it.

Mitigation: Prefer explicit invocation or narrow the trigger policy before installation in environments with many browser or automation skills.

Risk: Workflow guidance may be applied to browser automation tasks without enough user-specific constraints.

Mitigation: Restate the desired outcome, constraints, available inputs, and success criteria before producing implementation guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-agent-browser-workflow-helper-100358)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Agent Browser](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Chrome DevTools MCP issue: Persist CLI defaults for automatic daemon startup](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/2388)
- [Hacker News discussion: Is GPT-5.6 Sol Max Worth It?](https://news.ycombinator.com/item?id=48947713)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, validation notes, and remaining risks when helpful.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
