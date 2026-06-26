## Description: <br>
Zz Chat helps an agent set up a phone-accessible OpenClaw chat bridge using a user-deployed Cloudflare Worker and local bridge process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[badxtdss](https://clawhub.ai/user/badxtdss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to deploy and connect a mobile chat interface that forwards messages to a local OpenClaw agent. It is intended for users who understand Cloudflare Worker deployment, local persistent processes, and the privacy implications of forwarding chat through remote services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill deploys public Cloudflare Worker infrastructure and stores a stable local chat identifier. <br>
Mitigation: Review the deployment target before installing, understand where chat traffic flows, and remove local ~/.zz state when retiring the setup. <br>
Risk: The skill runs a persistent local bridge that forwards remote messages into the local OpenClaw agent. <br>
Mitigation: Enable persistence only when needed, keep the bridge under user control, and know how to stop the watchdog or remove the LaunchAgent. <br>
Risk: Security evidence warns that chat data may pass through weakly protected remote services with incomplete disclosure. <br>
Mitigation: Avoid sharing sensitive data through the bridge and review the service endpoints and Worker code before use. <br>
Risk: Security guidance specifically advises avoiding the Node bridge as written. <br>
Mitigation: Prefer the Python bridge unless the Node bridge has been reviewed and remediated for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/badxtdss/zz-chat) <br>
- [Publisher profile](https://clawhub.ai/user/badxtdss) <br>
- [Developer profile](https://b23.tv/rEEYnVF) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands, configuration steps, and generated chat-link guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce deployment commands, local service setup steps, a phone chat URL, and QR-code presentation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
