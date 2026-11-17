## Description:

Complete Superpowers methodology for OpenClaw, a 12-skill collection that guides design-before-code, test-first development, systematic debugging, verification, and structured code review for rigorous AI-assisted development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fenccerece](https://clawhub.ai/user/fenccerece)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this OpenClaw skill collection to guide AI-assisted development through design approval, implementation planning, test-first coding, systematic debugging, completion verification, and code review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill globally changes agent behavior through a strongly opinionated development workflow.

Mitigation: Install it only in workspaces where that workflow is wanted, and require agents to preserve system and developer instruction priority.

Risk: The workflow can lead agents toward dependency installation, build, test, commit, push, merge, or delete/discard actions without a clear consent gate.

Mitigation: Require explicit user approval before dependency setup, builds, tests, commits, pushes, merges, or destructive cleanup actions, especially in untrusted repositories.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review and scan the skill before deployment, and apply the security guidance as operating policy.

## Reference(s):

- [Superpowers-Openclaw ClawHub page](https://clawhub.ai/fenccerece/skills/superpowers-openclaw)
- [Project homepage](https://github.com/superpowers-open/superpowers-open)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, checklists, and workflow gates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces process guidance for agent behavior; no structured API output is declared.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
