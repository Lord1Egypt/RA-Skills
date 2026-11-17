## Description:

Helps agent users, skill authors, maintainers, and teams create practical Gog-style Google Workspace workflows, checklists, analyses, code changes, and reliability improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn Google Workspace and Gog-style productivity requests into concrete workflows, templates, checklists, analysis, code changes, or decision support. It is intended for practical bug fixing, setup hardening, reliability improvement, and adjacent workflow design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad Google Workspace or bug-fix wording, including Gmail, Calendar, Drive, or other sensitive productivity contexts.

Mitigation: Prefer explicit invocation and review the active context before using the skill with sensitive workspace data.

Risk: Workflow, checklist, automation, or code suggestions may be incorrect or incomplete for the user's environment.

Mitigation: Validate outputs against the stated success criteria and test scripts or configuration changes locally before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-020416)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Gog](https://clawhub.ai/skills/gog)
- [Hacker News Gmail storage discussion](https://news.ycombinator.com/item?id=48969253)
- [Hacker News local Git-backed notes workflow discussion](https://news.ycombinator.com/item?id=48968447)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code, shell command, checklist, template, or configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, validation steps, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
