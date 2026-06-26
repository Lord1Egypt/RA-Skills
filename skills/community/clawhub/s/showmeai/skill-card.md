## Description: <br>
Generate images, videos, and 3D models through the Showmeai API, using OpenAI-compatible image generation, Seedance video generation, and image-to-3D conversion models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hulebaji](https://clawhub.ai/user/hulebaji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to ask an agent to create or edit images, generate videos, and convert 2D images into 3D model files through Showmeai services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded images, video frames, and generation metadata are sent to Showmeai services. <br>
Mitigation: Use the skill only when Showmeai is trusted for the requested content, and avoid confidential media or private internal URLs. <br>
Risk: An unintended Showmeai_BASE_URL could send requests to the wrong provider endpoint. <br>
Mitigation: Keep Showmeai_BASE_URL pointed at the intended provider and review configuration before use. <br>
Risk: Saved generated media and 3D model files can persist locally after the task completes. <br>
Mitigation: Use explicit output directories where appropriate and remove saved media when it is no longer needed. <br>
Risk: The API key grants access to Showmeai generation services. <br>
Mitigation: Use a scoped API key where possible and keep Showmeai_API_KEY out of shared logs, prompts, and committed files. <br>


## Reference(s): <br>
- [Showmeai API](https://api.showmeai.art) <br>
- [Showmeai ClawHub Skill Page](https://clawhub.ai/hulebaji/showmeai) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text, JSON task responses, MEDIA URLs, and saved media or model files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Showmeai_API_KEY and Showmeai_BASE_URL; images may be URL-only unless saving is requested, while videos and 3D models may return async task IDs before files are available.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
