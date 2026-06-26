## Description: <br>
Seedance 2.0 Video Gen helps agents turn text, image, video, or audio briefs into Seedance/EvoLink video generation prompts, JSON request bodies, and call examples for text-to-video, image-to-video, and reference-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xk103295870-alt](https://clawhub.ai/user/xk103295870-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to prepare Seedance/EvoLink video-generation requests, choose an appropriate model mode, structure prompts with @asset references, and review example API calls before submitting jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated request JSON can be used for paid third-party API calls. <br>
Mitigation: Review the generated JSON, selected model, duration, quality, and media URLs before executing any API request. <br>
Risk: Prompts and referenced media may be shared with the third-party video generation provider. <br>
Mitigation: Avoid submitting private images, videos, audio, or sensitive prompts unless the user is comfortable sharing them with the provider. <br>
Risk: The skill relies on SEEDANCE_API_KEY for EvoLink authentication. <br>
Mitigation: Store SEEDANCE_API_KEY in a secure environment variable and avoid pasting credentials into prompts, examples, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xk103295870-alt/seedance2-video-gen) <br>
- [Seedance 2.0 API documentation](https://seedance2api.app) <br>
- [EvoLink API key signup](https://evolink.ai/signup) <br>
- [Official cases](cases/official-cases.md) <br>
- [Prompt templates](prompts/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and curl, JavaScript, or Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Seedance model names, prompt text, media URL lists, duration, quality, aspect ratio, and audio settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
