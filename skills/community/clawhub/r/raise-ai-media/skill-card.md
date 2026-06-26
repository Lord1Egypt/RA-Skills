## Description: <br>
RaiseAI Media helps agents generate and analyze images, videos, video scripts, and prompts through the RaiseAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacobluxj](https://clawhub.ai/user/jacobluxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent create or analyze media through RaiseAI, including image generation, video generation, video script generation, and prompt extraction from images or videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to share and persist a RaiseAI API key through chat. <br>
Mitigation: Configure RAISE_AI_API_KEY through a protected local settings or secrets mechanism where possible, use a dedicated low-privilege key if available, and rotate or revoke the key if it may have been exposed. <br>
Risk: Prompts, public media URLs, generated outputs, and API usage are sent to RaiseAI. <br>
Mitigation: Install only if the user trusts RaiseAI and the agent environment with that information, and avoid sending sensitive or private media unless approved. <br>
Risk: Media generation can consume RaiseAI API credits or quota. <br>
Mitigation: Monitor API usage and credit consumption, and use a dedicated key or account controls where available. <br>
Risk: Generated media results may be returned as temporary signed links. <br>
Mitigation: Share result links only with the intended recipient and download needed outputs before the links expire. <br>


## Reference(s): <br>
- [RaiseAI homepage](https://ai.micrease.com) <br>
- [ClawHub release page](https://clawhub.ai/jacobluxj/raise-ai-media) <br>
- [API setup](references/api-setup.md) <br>
- [Image generation](references/image-generation.md) <br>
- [Video generation](references/video-generation.md) <br>
- [Script generation](references/script-generation.md) <br>
- [Prompt extraction](references/prompt-extraction.md) <br>
- [Polling and errors](references/polling-and-errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, configuration snippets, generated script text, and media result links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill submits asynchronous RaiseAI tasks and returns generated media links or extracted/generated script content when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
