## Description: <br>
Use PoYo AI Veo 3.1 for frame-conditioned video generation through the PoYo submit endpoint, including fast and quality model modes, start-frame and end-frame guidance, reference images, and resolution choices up to 4K. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and submit PoYo Veo 3.1 video-generation requests, choose between fast and quality modes, include optional reference or frame images, and track returned task IDs for polling or callbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and callback URLs are sent to PoYo's external video-generation API. <br>
Mitigation: Review requests before submission and avoid sensitive, proprietary, internal-only, or secret-bearing content. <br>
Risk: API keys may be exposed if passed through command-line arguments or shared payloads. <br>
Mitigation: Set POYO_API_KEY in the environment and avoid embedding credentials in commands, files, or prompts. <br>


## Reference(s): <br>
- [PoYo Veo 3.1 API Documentation](https://docs.poyo.ai/api-manual/video-series/veo-3-1) <br>
- [PoYo Veo 3.1 OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/veo-3-1.json) <br>
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [Local API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/veo-3-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a chosen model id, final payload or parameter summary, reference-image status, returned task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
