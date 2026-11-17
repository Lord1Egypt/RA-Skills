## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixing, setup hardening, safety checks, reliability improvement, and adjacent skill design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent teams use this skill to turn SkillScan-style security and workflow needs into concise plans, checklists, analysis, code changes, or decision support. It emphasizes local-hardware-friendly workflows and explicit validation against the user's success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to run for general security, workflow, or gating requests where it is not the intended helper.

Mitigation: Invoke the skill explicitly for SkillScan-style workflow tasks and confirm the selected skill before relying on its output.

Risk: Generated security guidance may be incomplete or misleading if treated as an authoritative approval gate.

Mitigation: Review the guidance with the relevant maintainers and scan or test artifacts before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-100318)
- [SkillScan Demand Signal](https://clawhub.ai/skills/skillscan)
- [Skill Vetter Demand Signal](https://clawhub.ai/skills/skill-vetter)
- [Evaluation Depth and Statistical Rigor Demand Signal](https://github.com/openjny/copilot-eval/issues/74)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, prose, checklists, code snippets, shell commands, or configuration snippets depending on the user's request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, remaining risks, and follow-up work when helpful]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
