## Description: <br>
Controlled Windows package management workflow based on winget that guides an agent to safely search, inspect, download, install, upgrade, uninstall, and list upgradeable applications on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiapeng](https://clawhub.ai/user/hongjiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and Windows users use this skill to guide an agent through controlled package search, inspection, download, install, upgrade, uninstall, and upgrade-listing workflows with winget. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide installs, upgrades, and removals of Windows applications through winget. <br>
Mitigation: Review exact package IDs before approving package operations, and approve elevation or installer dialogs only when they match the requested action. <br>
Risk: Ambiguous package names can cause the agent to target the wrong package. <br>
Mitigation: Require disambiguation and prefer exact package IDs before install, upgrade, download, or uninstall actions. <br>
Risk: Uninstall operations are higher risk and may report success even when the application remains installed. <br>
Mitigation: Treat uninstall as high risk, avoid automatic retries, and perform a post-check when the host environment allows it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongjiapeng/winget-package-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command examples and JSON-like result schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only workflow; requires a Windows host with winget 1.6+ for full operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
