## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn Humanizer-style productivity requests into practical workflows, checklists, analyses, code changes, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to convert Humanizer-style productivity and reliability requests into practical plans, templates, checklists, analyses, code changes, or decision aids. It is intended for local-hardware-friendly work where assumptions, limits, success criteria, and validation notes should remain visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad activation wording may cause the skill to activate for ordinary writing or editing requests.

Mitigation: Prefer explicit invocation or confirm that the request needs Humanizer-style workflow support before applying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-humanizer-remove-workflow-helper-200354)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Humanizer](https://clawhub.ai/skills/humanizer)
- [Popular ClawHub skill demand: Nano Banana Pro](https://clawhub.ai/skills/nano-banana-pro)
- [OpenCLI streaming output feature issue](https://github.com/jackwener/OpenCLI/issues/2134)
- [nuget-license license generation issue](https://github.com/sensslen/nuget-license/issues/599)
- [kagent restricted Pod Security issue](https://github.com/kagent-dev/kagent/issues/2244)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, checklists, templates, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is shipped; outputs depend on the user's task and available inputs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
