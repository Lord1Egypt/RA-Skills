## Description:

Rune is a 67-skill mesh for AI coding assistants that routes coding, review, deployment, security, documentation, and project-state workflows through connected specialist skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhadaututtheky](https://clawhub.ai/user/nhadaututtheky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use Rune to coordinate AI-assisted software work across implementation, planning, review, testing, deployment, security checks, documentation, and session continuity. It is most relevant when a coding assistant needs structured routing among many task-specific workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill mesh can exert broad always-on influence over how an agent routes and performs coding sessions.

Mitigation: Review the routing skill and enable only the workflows needed for the repository before relying on it for sensitive work.

Risk: Auto-onboarding and session-continuity behavior can write persistent project files such as CLAUDE.md and .rune state.

Mitigation: Inspect generated project-state files, keep them under normal code review, and disable or remove persistence behavior where project policy does not allow it.

Risk: Memory and session capture can preserve project decisions, progress, or workflow preferences beyond a single interaction.

Mitigation: Avoid installing or invoking memory-related workflows on confidential repositories unless retention, access, and review expectations are clear.

Risk: The npm install path shown in artifact evidence uses npx without a pinned package version.

Mitigation: Pin package versions or install from a reviewed, checksummed release source before use in controlled environments.

## Reference(s):

- [ClawHub Rune Skill Page](https://clawhub.ai/nhadaututtheky/skills/rune-kit)
- [Artifact README](artifact/README.md)
- [Skill Index](artifact/skills/skill-index.json)
- [Rune Documentation](https://rune-kit.github.io/rune)
- [Rune Guides](https://rune-kit.github.io/rune/guides)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, command suggestions, file-change plans, and generated project-state or configuration files when invoked by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include routed workflow decisions, implementation steps, review findings, verification reports, and persistent project notes.]

## Skill Version(s):

2.32.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
