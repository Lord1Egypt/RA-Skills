## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixes, hardening, reliability improvements, and adjacent skill ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn SkillScan-style demand into actionable workflows, checklists, analysis, code changes, and verification notes. It emphasizes local-hardware-friendly implementation and visible assumptions, limits, and follow-up risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation triggers may route ordinary security or productivity requests to this skill unintentionally.

Mitigation: Tighten or disable implicit invocation and invoke the skill only for clearly scoped SkillScan-style workflow tasks.

Risk: Workflow guidance could introduce incorrect or misleading changes if applied without review.

Mitigation: Review generated artifacts, scan skill changes before deployment, and verify outputs against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-140500)
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub skill demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Popular ClawHub skill demand: AdMapix](https://clawhub.ai/skills/admapix)
- [Tell HN: We need an accounting system for cognitive debt](https://news.ycombinator.com/item?id=48760460)
- [What I had to unlearn as a perfectionist before I could ship](https://news.ycombinator.com/item?id=48774284)
- [A B2B marketing agency grew to $1.5M ARR in 6 months by betting on AI](https://news.ycombinator.com/item?id=48772872)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, text]

**Output Format:** [Markdown responses with checklists, plans, code snippets, shell commands, and verification notes as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be directly actionable, local-hardware friendly, and explicit about assumptions, limits, and remaining risks.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
