## Description: <br>
测试-史新超 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roarday](https://clawhub.ai/user/roarday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to send user questions to the configured JointPilot chat API and return streamed answer text through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User questions may be sent to developer.jointpilot.com without clear per-use opt-in. <br>
Mitigation: Use only for questions suitable for that third-party service and avoid secrets, personal data, or confidential business content. <br>
Risk: The bundled script documents API_KEY usage but currently does not read API_KEY from the environment. <br>
Mitigation: Verify and fix credential handling before relying on the script in a deployed workflow. <br>


## Reference(s): <br>
- [API Interface Specification](references/api_spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/roarday/shixinchao) <br>
- [JointPilot chat completions API](https://developer.jointpilot.com/v1/api/async_chat/completions/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text responses with Markdown and inline bash examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key credential and network access to the external JointPilot API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
