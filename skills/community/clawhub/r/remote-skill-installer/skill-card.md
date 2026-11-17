## Description:

Installs, manages, and updates OpenClaw skills from remote URLs or an official hub for selected agents, with batch import, retry behavior, and basic validation safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysy88092144](https://clawhub.ai/user/ysy88092144)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add, update, remove, list, and batch import remote OpenClaw skills across local agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installation or update can persistently overwrite active agent skill instructions from untrusted or mutable sources.

Mitigation: Use trusted, pinned, reviewed source URLs and inspect changes before updating installed skills.

Risk: Custom hub configuration or mirror fallback can redirect official imports to content that has not been independently verified.

Mitigation: Keep OPENCLAW_SKILLS_HUB_BASE and ~/.openclaw/skills-hub-url pointed at trusted locations, and avoid mirror fallback unless the mirrored content is verified.

Risk: Validation and checksum records do not establish publisher identity or whether downloaded instructions are appropriate to run.

Mitigation: Treat checksums as integrity records only, and review the downloaded skill and its security posture before enabling it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ysy88092144/skills/remote-skill-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local skill files and source metadata in OpenClaw workspaces when its commands are executed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
