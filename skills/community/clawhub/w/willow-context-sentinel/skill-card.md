## Description:

Checks Willow/OpenClaw session state on Linux and tells an agent whether to continue, compact context, hand off work, or pause for Postgres recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudi193-cmd](https://clawhub.ai/user/rudi193-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators running Willow/OpenClaw use this skill to monitor context pressure and choose the next operational step before response quality degrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script embeds file paths into generated Python source, which can execute injected Python in a manipulated environment.

Mitigation: Use only in a trusted local Willow/OpenClaw environment and patch the script to pass paths to Python as command-line arguments before routine use.

Risk: The runtime metadata declares bash, but the script also depends on python3.

Mitigation: Declare and verify python3 as a runtime dependency before installation or automated execution.

Risk: Heartbeat integration can cause the script to run repeatedly and automatically.

Mitigation: Review the automation cadence and run it with the least privileges needed to read local Willow state files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rudi193-cmd/skills/willow-context-sentinel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text status lines with Markdown guidance and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The sentinel script emits one of STATUS_OK, COMPACT_NOW, HANDOFF_NOW, or POSTGRES_DOWN.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
