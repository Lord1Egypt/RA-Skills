## Description:

Deterministic TRACE+ quality scorer for Agent Skill packages that audits SKILL.md inputs across six dimensions and produces JSON and Markdown findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris1wang3](https://clawhub.ai/user/chris1wang3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to score, audit, compare, and improve Agent Skill packages before release. It is intended for single-skill, comparison, and batch quality reviews using the TRACE+ rubric.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch mode or broad target paths can inspect more local skill-package files than intended.

Mitigation: Provide specific skill directories or SKILL.md files, and avoid broad personal or project roots unless those files are intended to be reviewed.

Risk: Static quality scoring can miss behavior that only appears during live agent use.

Mitigation: Treat static_proxy effectiveness results as review guidance and supplement them with behavioral evaluation before relying on release readiness decisions.

## Reference(s):

- [Scoring Engine Deterministic](references/scoring-engine-deterministic.md)
- [Audit Playbook](references/audit-playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/chris1wang3/skills/skill-quality-scorer)
- [Project Homepage](https://github.com/Chris1Wang3/HammerRoom-Skills/tree/master/skill-quality-scorer)
- [Support Issues](https://github.com/Chris1Wang3/HammerRoom-Skills/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON and Markdown audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include score breakdowns, trigger tests, recommendations, and static-audit findings.]

## Skill Version(s):

1.1.9 (source: server release evidence and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
