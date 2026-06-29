## Description: <br>
Control Wyze smart-home lights, plugs, and wall switches from an assistant using a local Node CLI backed by the unofficial wyze-node API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noelportugal](https://clawhub.ai/user/noelportugal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an assistant list and control Wyze lights, plugs, and wall switches after local Wyze credential and token setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands using 'all' or a broad name match can affect multiple Wyze devices at once. <br>
Mitigation: Confirm before broad actions, especially 'off all', and narrow commands by device kind or a specific nickname when possible. <br>
Risk: Plugs and switches may control doors, gates, garage openers, or important equipment. <br>
Mitigation: Act only on the user's named target and require confirmation for devices whose names imply door, garage, opener, gate, or safety-critical equipment. <br>
Risk: The skill reads Wyze API secrets and uses a cached local token. <br>
Mitigation: Keep the secrets file and token directory private, run login in a terminal, and avoid exposing Wyze credentials or token files in shared logs or workspaces. <br>
Risk: The underlying wyze-node integration is unofficial and may break if Wyze changes its API. <br>
Mitigation: Treat API failures as operational errors, re-run login or update wyze-node when authentication or device calls fail, and avoid relying on this skill for critical automation. <br>


## Reference(s): <br>
- [ClawHub Wyze skill page](https://clawhub.ai/noelportugal/wyze) <br>
- [wyze-node GitHub repository](https://github.com/noelportugal/wyze-node) <br>
- [wyze-node npm package](https://www.npmjs.com/package/wyze-node) <br>
- [Wyze Developer API Console](https://developer-api-console.wyze.com/#/apikey/view) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node, Wyze API credentials, and a local cached token; commands can change smart-home device state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
