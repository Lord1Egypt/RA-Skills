## Description: <br>
Generate Werydance 2.0 videos through WeryAI for text-to-video, image-to-video, multi-image video, first-frame/last-frame transitions, and mixed-reference video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwwdn](https://clawhub.ai/user/fwwdn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to prepare, submit, and monitor WeryAI Werydance 2.0 video-generation jobs from text prompts, image references, ordered frames, or mixed image/video/audio references. It helps expand short briefs into generation-ready prompts, validate supported parameters, and return task status or playable video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, and explicitly selected local media files are sent to WeryAI for generation. <br>
Mitigation: Use public HTTPS media URLs where possible, avoid sensitive private files, and review the full prompt and parameters before confirming a paid run. <br>
Risk: Local media paths can be uploaded to WeryAI when selected for generation. <br>
Mitigation: Run dry-run first to inspect uploadPreview and confirm exactly which local files would be uploaded. <br>
Risk: The WERYAI_API_KEY secret is required for runtime access. <br>
Mitigation: Provide WERYAI_API_KEY through the environment and do not commit or store the secret value in repository files. <br>


## Reference(s): <br>
- [Seedance Prompt Optimization](references/seedance-prompt-optimization.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fwwdn/seedance-2-video-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/fwwdn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include expanded prompts, confirmation tables, dry-run previews, task IDs, batch IDs, error codes, and generated video URLs.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
