## Description: <br>
YYClaw helps agents check account balance and usage, list available models, and call AI models through the YYClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GeniusTimee](https://clawhub.ai/user/GeniusTimee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route model requests through YYClaw, inspect available models and pricing, and monitor balance or usage tied to a YYClaw API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model calls send prompts and related request data to a paid third-party service. <br>
Mitigation: Use the skill only when YYClaw is an intended provider, and avoid sending secrets, credentials, private documents, or sensitive business data unless the service is trusted for that data. <br>
Risk: Requests can consume paid balance tied to the configured API key. <br>
Mitigation: Check balance and usage before and after use, and monitor account activity for unexpected charges. <br>


## Reference(s): <br>
- [YYClaw ClawHub listing](https://clawhub.ai/GeniusTimee/yyclaw) <br>
- [YYClaw API service](https://crypto.yyclaw.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and Python or JavaScript code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include API request examples and model, balance, usage, or chat-completion responses from YYClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
