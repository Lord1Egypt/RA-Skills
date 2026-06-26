## Description: <br>
Call Gemini models through RunAPI using OpenAI-compatible or Gemini contents clients for chat, streaming, multimodal vision, Google Search grounding, structured output, and reasoning effort. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to call Gemini models through RunAPI from OpenAI-compatible clients, Gemini contents clients, curl, or Gemini CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media, and generated requests are routed through an external API service. <br>
Mitigation: Review RunAPI and upstream provider data-handling terms before sending secrets, regulated data, confidential documents, or private images. <br>
Risk: Long non-streaming Gemini responses can hold an agent workflow open longer than needed. <br>
Mitigation: Use streaming for responses longer than a few hundred tokens, as recommended by the artifact. <br>


## Reference(s): <br>
- [RunAPI Gemini model documentation](https://runapi.ai/models/gemini.md) <br>
- [RunAPI Gemini model page](https://runapi.ai/models/gemini) <br>
- [RunAPI Google provider page](https://runapi.ai/providers/google.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-gemini) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, API request examples, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RUNAPI_TOKEN; may optionally use GOOGLE_API_KEY and GOOGLE_GENAI_BASE_URL for Gemini contents clients.] <br>

## Skill Version(s): <br>
0.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
