## Description: <br>
Test, debug, and inspect webhooks locally. Receive webhooks, inspect payloads, debug integrations, and replay requests. Essential for API development and third-party integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenxuyaun](https://clawhub.ai/user/chenxuyaun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to receive, inspect, replay, and forward webhook requests while debugging API integrations, third-party callbacks, and form submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook payloads and request history can contain sensitive data. <br>
Mitigation: Prefer test data, avoid unnecessary production traffic, and clear local request history after debugging sensitive integrations. <br>
Risk: Replay or forwarding commands can send webhook data to unintended or untrusted endpoints. <br>
Mitigation: Replay and forward requests only to trusted URLs that are appropriate for the data being handled. <br>
Risk: A local `webhook` command may resolve to an unexpected CLI on the user's machine. <br>
Mitigation: Confirm which `webhook` executable will run before using the skill's commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local listener, request inspection, replay, clear-history, and forwarding commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
