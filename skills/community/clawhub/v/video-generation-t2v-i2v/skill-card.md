## Description: <br>
AI video generation toolkit that generates videos from text prompts or input images using multiple video models, including Veo 3.1, Veo 3, Seedance 1.5 Pro, Wan 2.5, Grok Imagine Video, and OmniHuman. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gentleyo](https://clawhub.ai/user/gentleyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate short videos from text prompts or animate an input image through supported third-party video generation services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images may be sent to third-party video generation or image hosting services. <br>
Mitigation: Use only content approved for third-party processing and avoid private, regulated, or proprietary images unless public hosting is acceptable. <br>
Risk: Local environment files may expose more secrets than this workflow needs. <br>
Mitigation: Run the skill from a dedicated folder with a minimal .env containing only the API keys required for the selected workflow. <br>


## Reference(s): <br>
- [inference.sh](https://inference.sh) <br>
- [ImgBB API](https://api.imgbb.com/) <br>
- [SM.MS Upload API](https://sm.ms/api/v2/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [JSON status objects and local video file paths, with supporting Markdown or shell commands when configuring or dry-running the workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated videos are saved locally, normally under outputs/videos, and the skill reports absolute file paths for rendering.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
