## Description:

Forces high-agency exhaustive problem-solving with corporate PUA pressure, triggering on user frustration, repeated failures, passive behavior, or quality complaints across task types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rorschachachxd](https://clawhub.ai/user/rorschachachxd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to push an agent into a forceful problem-solving posture for debugging, implementation, code review, research, and ambiguous tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate on broad user-frustration phrases rather than only on an explicit command.

Mitigation: Remove or disable the automatic trigger list and require explicit user approval before activating this work mode.

Risk: The skill describes a persistent ~/.pua/evolution.md mechanism that can carry behavior rules across sessions.

Mitigation: Disable or remove the persistence mechanism before use unless persistent behavior baselines are intentionally desired.

Risk: The skill encourages broad searches, repository scans, endpoint calls, and extra work outside the immediate request.

Mitigation: Require explicit user approval before broad searches, repository-wide scans, endpoint calls, or work outside the requested task.

## Reference(s):

- [Project homepage](https://github.com/tanweai/pua)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown responses with optional code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce validation evidence, task plans, review findings, and explicit status markers during agent work.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter; artifact/_meta.json lists 2.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
