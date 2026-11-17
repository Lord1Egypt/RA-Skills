## Description:

Diagnose, fix, and prevent agent skill trigger failures across AI agent skill ecosystems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skill Compass to diagnose why skills do not trigger, audit skill descriptions, identify discovery and token-budget issues, and guide remediation for more reliable agent routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional auto-fix behavior can persistently edit installed skill files.

Mitigation: Run audit mode read-only first, pass an explicit --skills-dir, review affected SKILL.md files, and use --fix only after backups or version control are in place.

Risk: Weak scoping or misleading side-effect documentation may cause broader changes than expected during remediation.

Mitigation: Constrain the skills directory before remediation and review proposed changes before allowing an agent to apply fixes automatically.

## Reference(s):

- [Failure Pattern Reference](references/failure-patterns.md)
- [Skill Compass on ClawHub](https://clawhub.ai/thomaszhou22/skills/skill-compass-guardian)
- [650-Trial Activation Study](https://medium.com/@ivan.seleznov1)
- [agentskills.io Description Optimization](https://agentskills.io/skill-creation/optimizing-descriptions)
- [SkillRouter Paper](https://arxiv.org/abs/2603.22455)
- [Agent Skills Survey](https://arxiv.org/html/2602.12430v3)
- [Skill Triggering Guide](https://dev.to/lizechengnet/why-claude-code-skills-dont-trigger-and-how-to-fix-them-in-2026-o7h)
- [BSWEN Skill Triggering](https://docs.bswen.com/blog/2026-03-24-skill-triggering/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run an audit script; optional auto-fix mode can edit SKILL.md files when explicitly used.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
