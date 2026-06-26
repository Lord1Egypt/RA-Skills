## Description: <br>
Connect to WoClaw Hub for shared memory and multi-agent topic messaging between AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingp14](https://clawhub.ai/user/xingp14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use WoClaw to connect OpenClaw agents to a self-hosted WoClaw Hub for topic messaging, member discovery, and shared key/value memory during multi-agent coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends agent IDs, topic messages, and shared memory content to a user-configured WoClaw Hub. <br>
Mitigation: Use only trusted hubs, avoid storing secrets or regulated data in topics or shared memory, and deploy over WSS/HTTPS or trusted private networks. <br>
Risk: WoClaw Hub authentication depends on a token supplied through configuration or environment variables. <br>
Mitigation: Keep WOCLAW_TOKEN out of committed config, logs, screenshots, and shell history, and rotate or scope tokens where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xingp14/woclaw) <br>
- [Project homepage](https://github.com/XingP14/woclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions and command guidance for connecting to a configured WoClaw Hub.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
