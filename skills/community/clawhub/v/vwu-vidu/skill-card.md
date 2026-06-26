## Description: <br>
Vidu helps agents use vwu.ai-hosted Vidu video-generation models for text-to-video, image-to-video, task status checks, and video downloads through command-line helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure a vwu.ai API key, create Vidu video-generation jobs from text prompts or reference images, poll asynchronous task status, and download generated MP4 videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: vwu.ai API keys could be exposed if committed to files, shared in logs, or stored permanently in shell startup files. <br>
Mitigation: Use a dedicated, revocable API key, keep it out of source control, and prefer a secret manager or session-scoped environment variable. <br>
Risk: Prompts and reference images are sent to vwu.ai for generation and may contain sensitive content. <br>
Mitigation: Avoid sending sensitive images or prompts and review provider terms and data-handling expectations before use. <br>
Risk: Video generation consumes API quota and asynchronous jobs may take several minutes or fail. <br>
Mitigation: Monitor account quota, use short test jobs first, and check task status before retrying or creating additional jobs. <br>


## Reference(s): <br>
- [ClawHub Vidu Skill](https://clawhub.ai/a3273283/vwu-vidu) <br>
- [vwu.ai Console](https://vwu.ai) <br>
- [Vidu Image-to-Video Documentation](https://platform.vidu.cn/docs/image-to-video) <br>
- [New API Documentation](https://docs.newapi.ai/en) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands; helper scripts return CLI text and can download MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VWU_API_KEY and sends user-provided prompts or images to vwu.ai.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
