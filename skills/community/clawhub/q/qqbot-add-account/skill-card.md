## Description: <br>
Add new QQ Bot accounts to an existing OpenClaw Gateway instance when a user provides a QQ Bot appId and clientSecret or app token, covering both CLI and direct configuration edit approaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homer212416](https://clawhub.ai/user/homer212416) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to add additional QQ Bot accounts to an existing Gateway and optionally route a bot to its own agent workspace with separate memory and persona. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QQ Bot appId and clientSecret values may be exposed if stored directly in openclaw.json. <br>
Mitigation: Protect credential values, back up openclaw.json before editing, and prefer the OpenClaw credentials store or SecretRef for production use. <br>
Risk: Gateway configuration edits can persistently change bot account behavior or routing. <br>
Mitigation: Validate JSON syntax after edits and enable a separate agent workspace only when independent memory and persona are intended. <br>
Risk: Incorrect account bindings can route messages to the wrong agent workspace. <br>
Mitigation: Check the qqbot account alias, channel, accountId, and agentId bindings before relying on the new route. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/homer212416/qqbot-add-account) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON5 and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential handling notes, gateway configuration steps, and optional multi-agent routing guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
