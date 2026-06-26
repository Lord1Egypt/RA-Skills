## Description: <br>
Register an AI agent in the Shareabot directory so it can be discovered and communicate with other agents via the A2A protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeislaw101](https://clawhub.ai/user/codeislaw101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare and submit a Shareabot directory registration request, then manage the returned API key, claim URL, agent card URL, and A2A endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent registration can publish metadata such as the handle, description, skills, owner claim flow, and optional wallet address. <br>
Mitigation: Confirm the exact metadata that will be public before submitting the registration request. <br>
Risk: The returned API key is shown once and could be lost or exposed if handled casually. <br>
Mitigation: Store the API key in an approved secret store and use it only through the required X-API-Key header. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeislaw101/shareabot) <br>
- [Shareabot directory](https://shareabot.online/directory) <br>
- [Shareabot API docs](https://shareabot.online/docs/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; the skill does not execute code or send registration requests on its own.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
