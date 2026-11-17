## Description:

Framework-only skill trigger reference. Runtime matching implementation has been removed from the published artifact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill as a reference for skill-trigger declarations, dependency expectations, and OpenClaw-style intent routing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release describes the package as documentation-only, but server security evidence reports active routing code, setup scripts, workspace writes, and agent-routing instructions.

Mitigation: Review and scan the package before deployment; run it only in controlled environments and require explicit approval before routing decisions affect agent behavior.

Risk: The included code can read OpenClaw workspace routing data and write workspace configuration or state files.

Mitigation: Audit the skill index and workspace paths, pin dependencies, back up configuration, and limit filesystem permissions during evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/skill-trigger-v2)
- [ClawHub publisher profile](https://clawhub.ai/user/halfmoon82)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include routing declarations and configuration guidance; executable use requires review due to the suspicious security verdict.]

## Skill Version(s):

2.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
