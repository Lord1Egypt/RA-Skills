## Description:

Installs or upgrades the VT Sentinel OpenClaw security plugin for VirusTotal malware and file security scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[king-tero](https://clawhub.ai/user/king-tero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install or update VT Sentinel, restart the gateway, and verify that VirusTotal-backed file scanning and blocking hooks are active.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or upgrades a persistent security plugin and restarts the OpenClaw gateway.

Mitigation: Confirm the install or update before running commands, inspect the package with openclaw plugins inspect when provenance matters, and verify the plugin after restart.

Risk: The activated plugin can scan new or downloaded files and block risky execution patterns.

Mitigation: Review VT Sentinel behavior and configuration before enabling it, especially on systems where file scanning or blocking could interrupt normal workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/king-tero/skills/vt-sentinel-installer)
- [king-tero Publisher Profile](https://clawhub.ai/user/king-tero)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw CLI; proposes install, update, restart, and verification commands for user approval.]

## Skill Version(s):

1.10.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
