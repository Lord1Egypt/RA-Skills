## Description:

Helps agent users, skill authors, maintainers, and teams turn Gog-style Google Workspace workflow demand into practical plans, artifacts, checklists, analysis, code changes, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to create local-hardware-friendly workflows for Google Workspace, CLI, Gmail, Calendar, Drive, Contacts, and related bug-fix or reliability tasks. It helps turn a live request into a concrete deliverable with assumptions, success criteria, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to trigger on ordinary Google, Workspace, CLI, Gmail, Calendar, Drive, Contacts, or bug-fix requests.

Mitigation: Prefer explicit invocation for sensitive work and narrow triggers or require confirmation before applying the workflow in production contexts.

Risk: Workflow, code, shell command, or configuration guidance could be incorrect or incomplete for a user's environment.

Mitigation: Review proposed changes before execution, validate them against the stated success criteria, and scan resulting skill artifacts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-002325)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Gog](https://clawhub.ai/skills/gog)
- [Hacker News discussion: Google Workspace CLI](https://news.ycombinator.com/item?id=48653245)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, remaining risks, and next-step guidance.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
