## Description:

Provides cross-platform diagnostic guidance for OpenClaw gateways, including health checks, event loop degradation, WhatsApp connectivity, service state, stuck background subagents, prewarm blocking, and diagnostic bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordan-thirkle](https://clawhub.ai/user/jordan-thirkle)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw developers and operators use this skill to diagnose slow or unresponsive gateways, delayed agent responses, WhatsApp channel issues, service state problems, and post-upgrade regressions across Windows, WSL2, Linux, and macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic bundles and log inspection can expose system metadata, file paths, identifiers, and configuration shape.

Mitigation: Review exported bundles and log excerpts before sharing them, and share them only with trusted recipients for troubleshooting.

Risk: `pkill -9 node` can terminate unrelated Node.js processes and cause data loss.

Mitigation: Use targeted OpenClaw gateway restart commands first, and reserve `pkill -9 node` for last-resort recovery when the gateway is completely unresponsive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jordan-thirkle/skills/windows-health-monitor)
- [OpenClaw WinHealth SECURITY.md](https://github.com/jordan-thirkle/openclaw-winhealth/blob/main/SECURITY.md)
- [Diagnostic Bundle Privacy Disclosure](https://github.com/jordan-thirkle/openclaw-winhealth/blob/main/SECURITY.md#diagnostic-bundles)
- [SkillSpector Security Audit](https://clawhub.ai/plugins/@jordan-thirkle/openclaw-winhealth/security-audit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific diagnostic steps and cautionary notes for sensitive diagnostic data.]

## Skill Version(s):

1.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
