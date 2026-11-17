## Description:

Runs a security review workflow for Codex or ClawHub skills before activation or publication, including inspection of skill files, scripts, permissions, network behavior, secret handling, dependency risks, and release-readiness gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to review Codex or ClawHub skill folders for security, dependency, activation, and publication-readiness risks before they trust or release a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Localized instructions and broad implicit activation metadata may cause the skill to activate in more situations than intended.

Mitigation: Review and narrow localized triggers and implicit invocation settings before relying on the skill as an activation or publication gate.

Risk: Inconsistent English and Chinese workflow descriptions may weaken confidence in the skill's security-gate behavior.

Mitigation: Align localized instructions and usage documentation with the English security review workflow before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-130902)
- [Requirement Plan](references/requirement-plan.md)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [AdMapix demand signal](https://clawhub.ai/skills/admapix)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown security scan report with findings, remediation checklist, pass or block recommendation, and optional validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should include severity, evidence, affected file, and recommended fix.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
