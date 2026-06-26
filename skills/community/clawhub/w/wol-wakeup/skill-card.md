## Description: <br>
WoL Wakeup helps an OpenClaw agent manage saved Wake-on-LAN devices, guide users through adding or removing devices, and send wake packets by device name or number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xunone11](https://clawhub.ai/user/xunone11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to keep a local list of Wake-on-LAN devices, trigger wake requests from chat messages, and run guided workflows for adding or deleting saved devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persistent OpenClaw hook can inspect inbound messages and may log local message data. <br>
Mitigation: Enable the hook service only when that visibility is acceptable, keep it bound to localhost, and review local logs and retention settings. <br>
Risk: Hardcoded or reused hook tokens can allow unauthorized local hook requests. <br>
Mitigation: Generate a unique hook token for each installation, avoid example tokens, and pass secrets through environment variables or protected configuration. <br>
Risk: OpenClaw configuration and WoL state files may expose device MAC addresses or hook credentials. <br>
Mitigation: Restrict filesystem permissions on OpenClaw config files and the WoL state directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xunone11/wol-wakeup) <br>
- [Publisher profile](https://clawhub.ai/user/xunone11) <br>
- [OpenClaw hook endpoint](http://127.0.0.1:8765/hook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Wake-on-LAN workflow responses and local setup guidance; runtime behavior depends on OpenClaw hooks, Python 3, and the wakeonlan package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, frontmatter, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
