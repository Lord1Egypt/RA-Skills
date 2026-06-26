## Description: <br>
Generate and edit video with Runway Aleph through RunAPI. Use when the user asks an agent to create, edit, or transform video with Runway Aleph. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and content-production agents use this skill to route one-off Runway Aleph video generation or editing tasks through the RunAPI CLI, and to identify SDK options when integrating RunAPI into an application or backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video inputs, prompts, and request files may be sent to RunAPI and Runway cloud services. <br>
Mitigation: Review request.json before submission and confirm provider pricing, retention, and privacy terms before processing sensitive or proprietary media. <br>
Risk: The skill depends on the external runapi CLI and authentication state. <br>
Mitigation: Install the CLI from the documented RunAPI Homebrew tap, use runapi login or a scoped RUNAPI_API_KEY where possible, and avoid embedding credentials in request files or logs. <br>


## Reference(s): <br>
- [Runway Aleph model documentation](https://runapi.ai/models/runway-aleph.md) <br>
- [RunAPI Runway provider page](https://runapi.ai/providers/runway.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [Runway Aleph homepage](https://runapi.ai/models/runway-aleph) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References the runapi CLI, optional RUNAPI_API_KEY authentication, request.json inputs, asynchronous polling, and SDK package names.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
