## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical Gog-style Google Workspace workflows, checklists, analyses, code changes, and decision support for bug fixes, setup hardening, reliability improvements, or adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, skill authors, maintainers, and teams use this skill to turn Gog-style Google Workspace productivity needs into practical workflows, templates, checklists, analysis, code changes, or decision support. It is intended for local-hardware-friendly guidance rather than cloud-only automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Google, workspace, productivity, CLI, and bug-fix triggers may activate the skill for requests where a narrower specialist skill would be more appropriate.

Mitigation: Review the invocation context before relying on outputs, and narrow or disable implicit invocation when precise routing matters.

Risk: Guidance, workflow, code, shell command, or configuration suggestions may be incorrect for a user's environment.

Mitigation: Validate generated artifacts against stated success criteria and review commands or configuration changes before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-070243)
- [Requirement Plan](artifact/references/requirement-plan.md)
- [Popular ClawHub skill demand: Gog](https://clawhub.ai/skills/gog)
- [New mandatory Gmail, your Android backup storage needs may increase](https://news.ycombinator.com/item?id=48969253)
- [Coding Skills Development Report](https://news.ycombinator.com/item?id=48974093)
- [Termany Agent-Native Terminal](https://www.v2ex.com/t/1228797)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code, shell command, checklist, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, remaining risks, and next steps when helpful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
