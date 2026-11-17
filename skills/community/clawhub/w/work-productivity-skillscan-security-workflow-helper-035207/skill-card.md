## Description:

Helps AI-agent users, skill authors, maintainers, and teams create SkillScan-style workflows for bug fixing, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent users use this skill to turn security, reliability, and SkillScan-style workflow requests into actionable plans, checklists, code changes, or decision support. It is intended for practical local-friendly workflows that make assumptions, success criteria, validation, and follow-up risks visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation may cause the skill to appear in ordinary security, productivity, or planning conversations where the user did not intend to use it.

Mitigation: Narrow the activation metadata and prefer explicit invocation before installing it in environments that auto-load skills.

Risk: Generated workflows, checklists, or code changes may be incomplete or mismatched to a specific project context.

Mitigation: Review outputs against the stated success criteria, verify assumptions, and test or scan changes before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-035207)
- [SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [Self-improving Agent demand signal](https://clawhub.ai/skills/self-improving-agent)
- [Ask HN: Line by Line Agentic Coding](https://news.ycombinator.com/item?id=48754327)
- [Ask HN: End Every Work Session with One Note](https://news.ycombinator.com/item?id=48743102)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code, shell command, checklist, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's immediate workflow and should include validation notes when helpful.]

## Skill Version(s):

0.20260702.35207 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
