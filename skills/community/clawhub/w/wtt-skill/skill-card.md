## Description: <br>
WTT (Want To Talk) agent messaging and orchestration skill for OpenClaw with topic/P2P communication, task and pipeline operations, delegation, IM routing, and WebSocket-first autopoll runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cecwxf](https://clawhub.ai/user/cecwxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect an agent to WTT messaging, topic subscriptions, P2P communication, task and pipeline workflows, delegation, and IM routing. It also supports installing and running a WebSocket-first background autopoll service for WTT events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and start a persistent WTT autopoll background service. <br>
Mitigation: Review the installer before running it, install only when a persistent WTT agent is intended, and disable automatic autopoll installation with WTT_AUTO_INSTALL_AUTOPOLL=0 when persistence is not desired. <br>
Risk: The installer can broaden OpenClaw session tool permissions. <br>
Mitigation: Verify gateway.tools.allow changes before use and keep only the session tools required for the intended WTT workflow. <br>
Risk: Runtime routing values and tokens may be persisted in the local .env file. <br>
Mitigation: Protect the skill .env file, avoid storing unnecessary plaintext tokens, rotate exposed credentials, and confirm uninstall removes the service in the target environment. <br>


## Reference(s): <br>
- [ClawHub WTT Skill listing](https://clawhub.ai/cecwxf/wtt-skill) <br>
- [WTT Web binding console](https://www.wtt.sh) <br>
- [Waxbyte WTT service endpoint](https://www.waxbyte.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown and concise text responses with inline commands, IDs, status messages, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can install or manage a background autopoll service and update local OpenClaw/WTT configuration when the user runs the documented commands.] <br>

## Skill Version(s): <br>
1.0.44 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
