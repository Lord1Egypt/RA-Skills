## Description:

Collect local runtime metadata (OS build, Node/Electron versions, workspace paths) for support diagnostics and environment drift detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bsyv7](https://clawhub.ai/user/bsyv7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use the probe to collect local operating system, architecture, runtime, workspace, and free-space details in a Markdown report for support tickets, comparisons between machines, and post-upgrade checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious because it could not fully interpret the hook file, leaving installation behavior partly unreviewed.

Mitigation: Review the hook file and its behavior before installing; the available scan results do not establish that the skill is safe.

Risk: The supplied SessionStart hook writes a marker file under the user's profile, while the skill text describes the probe as read-only.

Mitigation: Confirm that this profile-file write is expected before enabling the hook.

## Reference(s):

- [WB Verify Probe on ClawHub](https://clawhub.ai/bsyv7/skills/wb-verify-probe)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown environment report file (wb-env-report.md)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One report file written to the workspace root; values reflect the machine where the probe runs.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
