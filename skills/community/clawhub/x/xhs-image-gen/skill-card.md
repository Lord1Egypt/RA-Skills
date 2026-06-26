## Description: <br>
Creates Xiaohongshu note materials by drafting post copy, generating cover and content card images from Markdown, and optionally publishing the note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limoxt](https://clawhub.ai/user/limoxt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to prepare Xiaohongshu posts, render 1080x1440 card images in multiple themes, and optionally publish reviewed content to Xiaohongshu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing path uses a live Xiaohongshu browser session cookie and can send it to a configurable API service. <br>
Mitigation: Prefer rendering without publishing when possible, keep .env out of sync, sharing, and version control, and avoid --api-mode with non-local API URLs. <br>
Risk: Generated posts can be made public after rendering. <br>
Mitigation: Review posts before making them public and use the default private publishing behavior for preview. <br>


## Reference(s): <br>
- [XHS Image Gen on ClawHub](https://clawhub.ai/limoxt/xhs-image-gen) <br>
- [Parameter Reference](artifact/references/params.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, render-ready Markdown content, CLI commands, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rendering supports multiple themes and pagination modes; publishing requires an XHS_COOKIE when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
