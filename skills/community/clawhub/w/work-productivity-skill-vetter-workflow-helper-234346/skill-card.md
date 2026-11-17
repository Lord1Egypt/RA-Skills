## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical Skill Vetter-style workflows for bug fixing, setup hardening, safety review, reliability improvement, and adjacent skill planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, skill authors, maintainers, and teams use this skill to turn skill-vetting demand into actionable workflows, checklists, analysis, code-change support, and validation notes. It is suited for practical review and hardening work around ClawHub skill setup, safety, reliability, and related workflow design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate the skill on ordinary GitHub, security, or bug-fix requests where the user did not intend a Skill Vetter-style workflow.

Mitigation: Confirm the requested outcome and narrow invocation triggers or routing policy before relying on the skill for unrelated GitHub, security, or bug-fix work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-234346)
- [Requirement Plan](references/requirement-plan.md)
- [Skill Vetter Demand Signal](https://clawhub.ai/skills/skill-vetter)
- [GitHub Demand Signal](https://clawhub.ai/skills/github)
- [SkillScan Demand Signal](https://clawhub.ai/skills/skillscan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code, shell-command, checklist, template, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tailored artifacts and validation notes for the user's immediate workflow; no executable code is bundled in the release artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
