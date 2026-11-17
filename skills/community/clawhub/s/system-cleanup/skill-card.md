## Description:

Maintains OpenClaw installations by inspecting system status, analyzing disk usage, and cleaning old backup, temporary, swap, and session files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mickey3721](https://clawhub.ai/user/mickey3721)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to perform routine OpenClaw maintenance, recover disk space, and review cleanup candidates before removing stale files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup script can delete editor swap files automatically.

Mitigation: Inspect listed files before deletion and avoid unattended scheduled runs unless automatic cleanup behavior is acceptable.

Risk: The cleanup script handles filenames unsafely in some paths.

Mitigation: Fix the script to use null-delimited filename handling before routine use.

Risk: The skill is marked suspicious by the authoritative security evidence.

Mitigation: Review the artifact files before installing or running and use the skill only for OpenClaw-specific maintenance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mickey3721/skills/system-cleanup)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and maintenance instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that inspect or delete OpenClaw-related files; users should review deletion candidates before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
