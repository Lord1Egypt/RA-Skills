## Description:

AI video generation toolkit that helps agents generate videos from text prompts or input images using multiple AI models, including Veo 3.1, Veo 3, Seedance 1.5 Pro, Wan 2.5, and Grok Imagine Video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gentleyo](https://clawhub.ai/user/gentleyo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create short AI-generated videos from English text prompts or to animate images into videos through supported video generation services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images may be sent to external video generation and image hosting services.

Mitigation: Use the skill only with content that is acceptable to share with those services, and review generated outputs before use.

Risk: Environment-file loading may expose unrelated secrets if the skill is run from a private project root.

Mitigation: Run the skill from a dedicated directory without unrelated .env secrets, and use narrowly scoped API keys.

Risk: Image-to-video generation may upload local images to public or third-party image hosting before video generation.

Mitigation: Use publicly shareable images or a reviewed upload service configuration, and supply only the specific API token needed for the selected upload service.

Risk: The skill depends on the separately installed inference.sh CLI.

Mitigation: Pin, review, or locally vendor the CLI before deployment in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gentleyo/skills/video-generation-t2v-i2v)
- [ClawHub publisher profile](https://clawhub.ai/user/gentleyo)
- [inference.sh](https://inference.sh)
- [ImgBB API](https://api.imgbb.com/)
- [SM.MS upload API](https://sm.ms/api/v2/upload)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions and JSON command results containing generated video file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated video files are saved locally, and successful script output includes absolute paths for downloaded MP4 files.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
