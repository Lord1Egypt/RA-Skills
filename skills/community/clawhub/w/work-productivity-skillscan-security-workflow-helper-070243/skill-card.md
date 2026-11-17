## Description:

Helps agent users, skill authors, maintainers, and teams create SkillScan-style workflows for security review, setup hardening, reliability improvement, bug fixing, and adjacent skill design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn security, productivity, and reliability requests into actionable plans, checklists, scripts, templates, or decision support. It is aimed at AI-agent users, skill authors, maintainers, and teams adapting popular SkillScan-style workflows for local-hardware-friendly execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation rules could cause this skill to influence unrelated security, bug-fix, or workflow requests.

Mitigation: Prefer explicit invocation by skill name, tighten trigger keywords, or disable implicit invocation in environments with many installed skills.

Risk: Generated security or hardening guidance may be incomplete for a user's specific repository, workflow, or operational constraints.

Mitigation: Require users to review generated plans, checklists, scripts, and configuration changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-070243)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub skill demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Popular ClawHub skill demand: AdMapix](https://clawhub.ai/skills/admapix)
- [Popular ClawHub skill demand: PollyReach](https://clawhub.ai/skills/pollyreach)
- [GitHub's 2FA is to become mandatory on September 2, 2026](https://news.ycombinator.com/item?id=48976781)
- [Ask HN: I stopped fighting AI over-reliance and built a workflow around it](https://news.ycombinator.com/item?id=48979474)
- [A B2B marketing agency grew to $1.5M ARR in 6 months by betting on AI](https://news.ycombinator.com/item?id=48980665)
- [Ask HN: How are you doing threat modeling for Terraform/IaC?](https://news.ycombinator.com/item?id=48972048)
- [Coding Skills Development Report](https://news.ycombinator.com/item?id=48974093)
- [Feature request: skip or shrink the test-evidence agent pass when a deterministic commands.test exists and passes](https://github.com/kunchenguid/no-mistakes/issues/529)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional inline code blocks, shell commands, configuration snippets, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, validation notes, and remaining risks when helpful.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
