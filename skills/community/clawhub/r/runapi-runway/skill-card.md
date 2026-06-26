## Description: <br>
Generate and edit video with Runway through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to generate, edit, extend, or transform video with Runway through the RunAPI CLI for one-off tasks, or through RunAPI SDKs when integrating video generation into an application or backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use RUNAPI_API_KEY or a saved runapi login session as credentials. <br>
Mitigation: Treat the API key and saved CLI session as secrets, avoid exposing them in logs or shared files, and revoke or rotate them if disclosed. <br>
Risk: Prompts, media, and task data may be sent to RunAPI/Runway and may incur provider costs. <br>
Mitigation: Use the skill only when the user accepts RunAPI/Runway processing and any applicable pricing, rate limits, and provider terms. <br>
Risk: The runtime depends on installing the runapi binary from the RunAPI Homebrew tap. <br>
Mitigation: Verify the Homebrew tap and binary source before installation and keep the CLI updated through the documented package manager. <br>


## Reference(s): <br>
- [RunAPI Runway model overview](https://runapi.ai/models/runway.md) <br>
- [RunAPI Runway provider comparison](https://runapi.ai/providers/runway.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [RunAPI Runway homepage](https://runapi.ai/models/runway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, SDK package names, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include RunAPI CLI commands, request-file guidance, asynchronous polling commands, and SDK selection guidance.] <br>

## Skill Version(s): <br>
0.2.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
