## Description: <br>
AI-powered avatar accessory synthesis that analyzes art style, lighting, and angle to add matching hats and headwear to avatar images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ls569333469](https://clawhub.ai/user/ls569333469) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add hats, headwear, or other accessories to avatar images through an MCP tool or FastAPI endpoint while preserving the source avatar's style, lighting, and composition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input avatar images may be sent to Google Gemini and, when using the public demo, to the demo operator. <br>
Mitigation: Use only images approved for those services, and prefer running the skill locally with a limited Gemini API key. <br>
Risk: The web mode can expose an unauthenticated image-editing endpoint if deployed broadly. <br>
Mitigation: Bind web mode to localhost, add authentication, restrict CORS, and avoid exposing port 8000 publicly. <br>
Risk: image_url fetching can retrieve remote content supplied by a caller. <br>
Mitigation: Disable image_url input or tightly validate allowed URLs before enabling web access. <br>
Risk: Face, body, and background preservation is prompt-based and may fail in generated outputs. <br>
Mitigation: Manually inspect generated images before relying on or publishing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ls569333469/the-clawcap) <br>
- [The-ClawCap repository](https://github.com/ls569333469/The-ClawCap) <br>
- [Gemini image generation documentation](https://ai.google.dev/gemini-api/docs/image-generation#image-editing) <br>
- [Google AI Studio API key setup](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Images, JSON, API responses, Configuration guidance] <br>
**Output Format:** [PNG image bytes or base64-encoded PNG with JSON metadata; setup guidance is Markdown with inline shell and JSON snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY; accepts a base64 avatar image or image URL plus accessory and optional negative prompts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
