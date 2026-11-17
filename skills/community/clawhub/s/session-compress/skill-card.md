## Description:

Compress OpenClaw session .jsonl files by trimming old messages while preserving system messages, recent turns, and task-relevant context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzqsama066](https://clawhub.ai/user/zzqsama066)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to identify and compress large main-agent session files while preserving system messages, recent turns, and task-relevant context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow invokes a relative scripts/compress.ps1 file that is not included in the artifact.

Mitigation: Use the skill only after supplying and inspecting the intended compress.ps1 implementation.

Risk: In-place compression can permanently overwrite OpenClaw session history.

Mitigation: Run the documented dry run first and prefer OutputPath or a backup before modifying the original .jsonl file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzqsama066/skills/session-compress)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to run a dry run before compression and optionally write compressed output to a separate file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
