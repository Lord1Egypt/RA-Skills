## Description:

SOLO is a third-party OpenClaw meta-agent framework for coordinating a kernel, audit layer, and execution skills under a separation-of-powers operating model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use SOLO to define governance boundaries, audit scheduled agent work, capture operational learnings, and coordinate related OpenClaw skills. It is intended for persistent agent-fleet oversight where policy, audit, and execution responsibilities need to remain separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary characterizes the skill as asking for broad persistent control over memory and policy files.

Mitigation: Review proposed memory, audit, and policy changes before applying them, and install only in workspaces where persistent governance behavior is intended.

Risk: The security guidance flags remote uploads and external notifications with unclear user control.

Mitigation: Disable or remove upload and notification paths unless they are explicitly approved for the workspace and the credentials are scoped to the intended destination.

Risk: The artifact includes an IMA upload helper that reads Markdown or text files and sends their contents through an external helper using environment credentials.

Mitigation: Audit the external IMA helper, require explicit approval before upload commands, and use least-privilege IMA credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meta-evo-creator/skills/solo)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [SOLO audit agent](artifact/agent-audit.md)
- [MEV Five-Layer Engine](artifact/SOUL.mev.md)
- [Eval Loop for Self-Improvement](artifact/references/eval-loop.md)
- [Promotion Guide](artifact/references/promotion-guide.md)
- [Learning Schema](artifact/references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON audit records, learning entries, configuration paths, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent memory, audit archive, policy, and upload-related actions that should be reviewed before use.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
