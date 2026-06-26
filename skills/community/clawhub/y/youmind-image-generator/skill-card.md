## Description: <br>
Generate AI images from text prompts using YouMind's multi-model API with one API key for GPT Image, Gemini, Seedream, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DophinL](https://clawhub.ai/user/DophinL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images from natural-language prompts through YouMind and save the resulting image URLs to a YouMind board. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated images may be saved to the user's YouMind board. <br>
Mitigation: Avoid sensitive, proprietary, or confidential prompts and confirm that YouMind storage is appropriate for the use case. <br>
Risk: The workflow may install or depend on the global @youmind-ai/cli package. <br>
Mitigation: Verify the package source and installation command before use. <br>
Risk: Image generation requires a YouMind API key. <br>
Mitigation: Configure the API key outside chat and never paste the key into a conversation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DophinL/youmind-image-generator) <br>
- [YouMind](https://youmind.com?utm_source=youmind-image-generator) <br>
- [YouMind CLI](https://www.npmjs.com/package/@youmind-ai/cli) <br>
- [Setup](references/setup.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Long-Running Tasks](references/long-running-tasks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the YouMind CLI and YOUMIND_API_KEY; image generation is polled until completion or timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
