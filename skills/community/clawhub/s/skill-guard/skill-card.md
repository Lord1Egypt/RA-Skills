## Description:

Stage, scan, and install a ClawHub skill when the user requests a guarded ClawHub installation. Blocks installation on security findings or incomplete scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesouttake](https://clawhub.ai/user/jamesouttake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install requested ClawHub skills through a guarded workflow that stages downloads, requires complete clean Snyk Agent Scan results, and blocks installation when scans are incomplete or report findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guarded installer downloads a requested skill, uploads staged text content to Snyk for analysis, and can modify the local OpenClaw workspace after a clean scan.

Mitigation: Use it only where external Snyk analysis and workspace modification are acceptable, and provide SNYK_TOKEN through an environment variable or secret manager.

Risk: A clean scanner result is not a guarantee that a downloaded skill is safe.

Mitigation: Review retained quarantine and backup directories as data when a scan or replacement fails, and do not execute staged skill content.

Risk: The scanner package is pinned, but its transitive dependencies are not fully locked and uvx may download dependencies on first use.

Mitigation: Use trusted clawhub and uvx binaries from approved package sources and run the installer in an environment where first-use downloads are acceptable.

Risk: Replacing an existing skill can require manual recovery if the machine crashes or the process is forcibly terminated.

Mitigation: Use --force only for intentional replacement, preserve the printed run directory, and recover from the previous-skill backup if automatic rollback cannot complete.

## Reference(s):

- [Snyk Agent Scan](https://github.com/snyk/agent-scan)
- [ClawHub skill page](https://clawhub.ai/jamesouttake/skills/skill-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print exit status, a private staging directory, and backup location information.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
