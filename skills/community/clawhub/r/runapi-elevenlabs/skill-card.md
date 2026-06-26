## Description: <br>
Generate speech, dialogue, sound effects, transcriptions, and audio isolation with ElevenLabs through RunAPI, using the CLI for one-off tasks and SDKs for app or backend integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to create speech, dialogue, and sound effects, transcribe audio, or isolate audio through ElevenLabs on RunAPI. It supports one-off CLI workflows and SDK-based application integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to cloud services through RunAPI and ElevenLabs and may use sensitive RunAPI credentials. <br>
Mitigation: Use this skill only for approved cloud audio tasks, review request files before execution, and protect RUNAPI_API_KEY or saved runapi login state as sensitive credentials. <br>
Risk: Audio prompts or source files could contain secrets, regulated data, or confidential personal or business information. <br>
Mitigation: Avoid submitting secrets or regulated data unless the use case and provider handling are approved. <br>


## Reference(s): <br>
- [RunAPI ElevenLabs model homepage](https://runapi.ai/models/elevenlabs) <br>
- [RunAPI ElevenLabs model overview, pricing, and rate limits](https://runapi.ai/models/elevenlabs.md) <br>
- [RunAPI ElevenLabs provider comparison](https://runapi.ai/providers/elevenlabs.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-elevenlabs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, request-file guidance, and SDK package references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference RUNAPI_API_KEY or saved runapi login state for authentication.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
