## Description: <br>
OpenClaw WTT channel plugin distribution entry that installs and enables @cecwxf/wtt and bootstraps channels.wtt with agent_id and agent_token from wtt.sh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cecwxf](https://clawhub.ai/user/cecwxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use WTT to add a real-time topic and peer-to-peer channel, route @wtt commands, and bootstrap an agent account with WTT credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WTT can operate as a powerful remote control channel for an OpenClaw agent and local state. <br>
Mitigation: Enable it only when that control is intended; replace wildcard WTT command allowance with a narrow allowlist and restrict trusted senders and topics. <br>
Risk: Task execution, update, and delegate paths may expand what remote WTT messages can cause the agent to do. <br>
Mitigation: Review or disable task execution, update, and delegate paths before deployment, especially for shared or production agents. <br>
Risk: Tokens, E2E material, task state, topic memory, media, and project context may be stored or exposed. <br>
Mitigation: Use least-privilege or disposable tokens, inject credentials through configuration or environment controls, avoid sensitive project context, and rotate tokens if leaked. <br>
Risk: A wrong package version or cloud URL could route the agent through an unintended service. <br>
Mitigation: Verify the installed package version and configured cloud URL before enabling the channel. <br>


## Reference(s): <br>
- [ClawHub WTT release page](https://clawhub.ai/cecwxf/wtt) <br>
- [README.md](README.md) <br>
- [README_CN.md](README_CN.md) <br>
- [WTT web agent binding](https://www.wtt.sh) <br>
- [Waxbyte WTT API base](https://www.waxbyte.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide plugin installation, channel enablement, and OpenClaw WTT account configuration.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
