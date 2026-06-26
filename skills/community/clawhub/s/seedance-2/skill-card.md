## Description: <br>
Use PoYo AI Seedance 1.5 Pro for higher-end image-to-video generation through the PoYo submit endpoint when a user needs longer clips, optional audio, fixed-lens control, broad aspect-ratio support, or custom Seedance payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to prepare, submit, and track PoYo Seedance 1.5 Pro image-to-video generation jobs. It helps choose the model, build request payloads, submit authenticated API calls, preserve returned task IDs, and plan polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, job settings, task IDs, and optional webhook notifications are sent to PoYo. <br>
Mitigation: Avoid sensitive prompts or private image URLs unless PoYo privacy and retention terms fit the intended use. <br>
Risk: The skill requires a PoYo API key for authenticated submissions. <br>
Mitigation: Set POYO_API_KEY as an environment variable and avoid passing credentials on the command line or storing them in payload files. <br>


## Reference(s): <br>
- [Artifact API Reference](references/api.md) <br>
- [PoYo Seedance 1.5 Pro Documentation](https://docs.poyo.ai/api-manual/video-series/seedance-1-5-pro) <br>
- [PoYo Seedance 1.5 Pro OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/seedance-1-5-pro.json) <br>
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/seedance-2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a returned task_id when a PoYo request is submitted; live submission requires POYO_API_KEY and curl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
