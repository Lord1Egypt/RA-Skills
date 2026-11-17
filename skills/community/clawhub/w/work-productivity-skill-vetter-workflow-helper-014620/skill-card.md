## Description:

Helps agent users, skill authors, maintainers, and teams create practical Skill Vetter-style workflows for bug fixing, setup hardening, reliability improvement, and adjacent skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn Skill Vetter-style demand into actionable workflows, checklists, analysis, code changes, or decision support. It is aimed at practical local-hardware-friendly planning and validation rather than model training or cloud-only automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may trigger the skill on unrelated security, GitHub, or bug-fix requests.

Mitigation: Confirm the user's requested outcome and constraints before applying the workflow; prefer explicit invocation when precise routing matters.

Risk: The skill can generate vetting, hardening, or reliability guidance that may be incomplete for a specific environment.

Mitigation: Review outputs against local security, reliability, and deployment criteria before applying generated changes.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-014620)
- [Requirement Plan](references/requirement-plan.md)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [Deferred maintenance discussion](https://news.ycombinator.com/item?id=48680354)
- [Responsible disclosure discussion](https://news.ycombinator.com/item?id=48688932)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Analysis]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local-hardware-friendly artifacts and includes a short verification or next-step note when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
