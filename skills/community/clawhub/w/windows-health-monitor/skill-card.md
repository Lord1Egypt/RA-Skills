## Description: <br>
Cross-platform diagnostics for OpenClaw gateways, including gateway health, event loop degradation, WhatsApp connectivity, service state, stuck background subagents, prewarm blocking, and diagnostic bundle generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jordan-thirkle](https://clawhub.ai/user/jordan-thirkle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose slow or unresponsive OpenClaw gateways, channel connectivity issues, delayed agent responses, and post-upgrade health problems across Windows, WSL2, Linux, and macOS environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic bundles and logs may contain system paths, identifiers, configuration structure, or log-derived details. <br>
Mitigation: Review exported bundles and logs before sharing them, and share diagnostics only with trusted recipients for troubleshooting. <br>
Risk: Some troubleshooting steps, including process termination, doctor fixes, and channel logout/login, can disrupt active OpenClaw sessions or unrelated local processes. <br>
Mitigation: Use disruptive commands only after understanding their impact, prefer targeted service restarts, and reserve broad process termination for last-resort recovery. <br>


## Reference(s): <br>
- [OpenClaw Health Monitor listing](https://clawhub.ai/jordan-thirkle/windows-health-monitor) <br>
- [OpenClaw WinHealth security disclosures](https://github.com/jordan-thirkle/openclaw-winhealth/blob/main/SECURITY.md) <br>
- [Diagnostic bundle privacy guidance](https://github.com/jordan-thirkle/openclaw-winhealth/blob/main/SECURITY.md#diagnostic-bundles) <br>
- [SkillSpector Security Audit](https://clawhub.ai/plugins/@jordan-thirkle/openclaw-winhealth/security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct users to generate diagnostic archives and review local logs before sharing.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
