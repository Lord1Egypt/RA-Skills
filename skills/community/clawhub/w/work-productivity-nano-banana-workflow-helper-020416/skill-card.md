## Description:

Helps agent users, skill authors, maintainers, and teams create practical Nano Banana Pro-style workflows for bug fixing, setup hardening, reliability improvement, and adjacent productivity skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn demand for Nano Banana Pro-style work-productivity workflows into concrete artifacts, checklists, analysis, code changes, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger keywords may cause accidental activation in unrelated work-productivity or image-generation conversations.

Mitigation: Tighten invocation triggers or review activations before relying on the workflow in shared agent environments.

Risk: Workflow outputs may include proposed code, shell commands, or configuration that are not automatically executed by the skill but could be copied into a project.

Mitigation: Review generated artifacts, commands, and configuration changes before deployment, and validate them against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-nano-banana-workflow-helper-020416)
- [Nano Banana Pro Demand Signal](https://clawhub.ai/skills/nano-banana-pro)
- [Nano PDF Demand Signal](https://clawhub.ai/skills/nano-pdf)
- [Ask HN Workflow Demand Signal](https://news.ycombinator.com/item?id=48979474)
- [Coding Skills Development Demand Signal](https://news.ycombinator.com/item?id=48974093)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, limits, validation notes, and remaining risks when helpful.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
