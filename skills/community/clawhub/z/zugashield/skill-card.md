## Description: <br>
ZugaShield Security Scanner scans OpenClaw messages, tool calls, model outputs, and recalled memory to help block prompt injection, SSRF, command injection, data leakage, and memory poisoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zuga-luga](https://clawhub.ai/user/Zuga-luga) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this plugin to add security scanning to OpenClaw deployments across connected channels and to inspect scanner status and threat reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin relies on a separate Python scanner that can inspect broad OpenClaw traffic, including messages, tool arguments, model outputs, and recalled memory. <br>
Mitigation: Review the plugin and the zugashield Python package before installing, and deploy only where that traffic inspection is approved. <br>
Risk: The security evidence notes package and source ambiguity around the OpenClaw plugin and Python MCP package. <br>
Mitigation: Verify package names, publisher identity, and repository provenance before installation, and consider pinning package versions. <br>
Risk: Fail-closed behavior can block activity when the scanner is unavailable. <br>
Mitigation: Test the scanner in the target environment, monitor scanner status, tune timeouts, and choose fail-closed settings deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zuga-luga/zugashield) <br>
- [Publisher profile](https://clawhub.ai/user/Zuga-luga) <br>
- [Project homepage](https://github.com/Zuga-luga/ZugaShield) <br>
- [npm package](https://www.npmjs.com/package/zugashield-openclaw-plugin) <br>
- [PyPI package](https://pypi.org/project/zugashield/) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text command responses and JSON-compatible plugin configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May block OpenClaw requests or tool executions when scans detect threats or when fail-closed scanner availability rules apply.] <br>

## Skill Version(s): <br>
0.1.1 (source: package.json, openclaw.plugin.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
