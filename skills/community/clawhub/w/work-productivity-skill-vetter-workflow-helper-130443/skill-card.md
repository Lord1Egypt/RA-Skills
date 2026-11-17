## Description:

Helps agent users, skill authors, maintainers, and teams create practical workflows, artifacts, checklists, analyses, and implementation support for Skill Vetter-style review and adaptation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, skill authors, maintainers, and teams use this skill to turn Skill Vetter-style demand into a practical review, planning, hardening, or implementation workflow. It produces concise artifacts that clarify goals, assumptions, validation criteria, and remaining risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation keywords and implicit invocation may cause the skill to appear during unrelated security, GitHub, or bug-fix requests.

Mitigation: Narrow trigger wording or confirm intent before applying the workflow when precise routing matters.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [ClawHub Github Skill](https://clawhub.ai/skills/github)
- [ClawHub SkillScan](https://clawhub.ai/skills/skillscan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's task and should include assumptions, validation notes, and follow-up risks when useful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
