## Description: <br>
Generate videos using Seedance models from text prompts, images, videos, audio, or reference materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warm-wm](https://clawhub.ai/user/warm-wm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and creators use this skill to request Seedance video generation from text prompts or multimodal reference materials and receive generated video URLs and optional local file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist API keys in a workspace environment file. <br>
Mitigation: Use a dedicated, low-privilege API key, provide credentials only with explicit approval, and remove workspace environment entries after use. <br>
Risk: Prompts and referenced media URLs are sent to the video generation provider. <br>
Mitigation: Avoid private prompts or sensitive media URLs unless the provider and data handling are acceptable for the use case. <br>
Risk: Automatic retry after credential setup can repeat a generation request. <br>
Mitigation: Confirm the prompt, media inputs, and output expectations before retrying after credentials are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/warm-wm/video-generate) <br>
- [Skill documentation](SKILL.md) <br>
- [Video generation implementation](scripts/video_generate.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated video URLs, optional local file paths, and JSON status details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is returned by URL; long-running tasks may return pending task IDs for follow-up polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
