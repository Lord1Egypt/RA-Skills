## Description:

Helps agent users and skill authors plan, fix, harden, and improve browser-based agent workflows with practical artifacts, checklists, analysis, and implementation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to convert browser-agent workflow needs into actionable plans, templates, checklists, code outlines, analysis, or implementation support. It is intended for practical workflow improvement, bug fixing, setup hardening, and reliability work around agent-browser tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate this skill for generic browser, CLI, automation, or bug-fix requests where a more specific skill would be better.

Mitigation: Review trigger terms and prefer a narrower skill when the user request clearly belongs to a more specific workflow.

Risk: Workflow, code, shell command, or configuration suggestions may be incomplete or incorrect for the user's local environment.

Mitigation: Validate outputs against the user's stated success criteria, inspect commands before execution, and keep assumptions and remaining risks visible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-agent-browser-workflow-helper-070243)
- [Requirement Plan](references/requirement-plan.md)
- [Agent Browser demand source](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Browser automation demand discussion](https://news.ycombinator.com/item?id=48974402)
- [CLI workflow feature request](https://github.com/ysbing/AudioShare/issues/6)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, limits, verification steps, and remaining risks when helpful.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
