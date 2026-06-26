## Description: <br>
Install or upgrade VT Sentinel security plugin for OpenClaw when users ask to set up, enable, update, or upgrade VirusTotal scanning, malware protection, or file security scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[king-tero](https://clawhub.ai/user/king-tero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install or upgrade the VT Sentinel security plugin through approved OpenClaw CLI commands, then restart and verify the gateway so the plugin becomes active. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or updating the plugin changes the user's OpenClaw extension state and restarts the user-scope gateway. <br>
Mitigation: Review the OpenClaw commands before approving and verify the plugin state with `openclaw plugins list` after the operation. <br>
Risk: The installed plugin performs VirusTotal/VTAI security scanning and may have privacy implications for files submitted or inspected. <br>
Mitigation: Inspect the external plugin package first if privacy behavior, automatic scanning, blocking, VirusTotal/VTAI use, or audit logging requires additional assurance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/king-tero/vt-sentinel-installer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/king-tero) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openclaw CLI and user approval before making install, update, uninstall, or gateway restart changes.] <br>

## Skill Version(s): <br>
1.10.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
