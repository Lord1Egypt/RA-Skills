## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn skill-vetting, bug-fix, reliability, and safety-hardening requests into actionable workflows, checklists, analysis, code changes, or decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to structure practical skill-vetting workflows for bug fixes, setup hardening, safety review, reliability improvements, or adjacent skill creation. It produces local-hardware-friendly plans, templates, checklists, implementation support, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit activation keywords may cause the helper to run for unrelated requests.

Mitigation: Narrow or disable implicit activation so the skill runs only for explicit skill-vetting workflow requests.

Risk: Workflow outputs can affect skill safety, reliability, or setup choices if followed without review.

Mitigation: Review generated plans, checklists, code changes, and verification notes before applying them to installed or shared skills.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-102347)
- [Skill Vetter Demand Signal](https://clawhub.ai/skills/skill-vetter)
- [GitHub Skill Demand Signal](https://clawhub.ai/skills/github)
- [SkillScan Demand Signal](https://clawhub.ai/skills/skillscan)
- [V2EX Demand Signal](https://www.v2ex.com/t/1222295)
- [Hacker News Seeking Advice Signal](https://news.ycombinator.com/item?id=48621795)
- [Hacker News Threading Signal](https://news.ycombinator.com/item?id=48636078)
- [Hacker News Sandbox Signal](https://news.ycombinator.com/item?id=48632192)
- [Agent Gather GitHub Issue Signal](https://github.com/realproject7/agentgather/issues/78)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with optional code, shell-command, checklist, template, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, validation steps, remaining risks, and useful next steps when applicable.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
