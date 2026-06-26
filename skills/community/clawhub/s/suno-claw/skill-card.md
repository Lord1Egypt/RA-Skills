## Description: <br>
Suno Claw is a multi-agent creative workflow that turns a user's music idea into Suno/kie.ai-ready lyrics, style tags, titles, and generated audio links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonzhang-zzx](https://clawhub.ai/user/jasonzhang-zzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Music creators, developers, and agent users use this skill to convert a brief music idea into structured lyrics, style tags, Suno prompts, and progressive kie.ai music generations. It supports both lyrical songs and instrumental requests, then stores liked outputs as local preference memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creative prompts, lyrics, titles, and style tags are sent to the kie.ai API for music generation. <br>
Mitigation: Avoid sensitive unpublished material and use the skill only when external API processing is acceptable. <br>
Risk: The skill keeps liked generations and preference signals in local memory files. <br>
Mitigation: Delete memory/history.json and memory/patterns.log when retained preferences or generation history should be cleared. <br>
Risk: A configured callback URL can receive generation content or status information. <br>
Mitigation: Leave CALLBACK_URL empty unless the endpoint is controlled and trusted. <br>
Risk: The kie.ai API key authorizes paid or quota-limited generation calls. <br>
Mitigation: Use a dedicated API key and rotate it if it is exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jasonzhang-zzx/suno-claw) <br>
- [Suno AI](https://suno.ai) <br>
- [kie.ai documentation](https://docs.kie.ai/) <br>
- [kie.ai Suno API documentation](https://docs.kie.ai/suno-api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, api calls, guidance] <br>
**Output Format:** [Markdown progress and result summaries with JSON prompt payloads, shell command invocations, and generated audio URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KIEAI_API_KEY; may use CALLBACK_URL when the user controls the endpoint; stores liked generation history and preference patterns in local memory files.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
