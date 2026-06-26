## Description: <br>
Creates Seedance 2.0 image and video prompts, and can help run Dreamina CLI workflows for text-to-image, text-to-video, image-to-image, image-to-video, video extension, task lookup, and history checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chencore](https://clawhub.ai/user/chencore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative developers use this skill to draft structured Chinese Seedance 2.0 prompts and, when the local Dreamina CLI is installed and authenticated, run media generation workflows. It supports image generation, video generation, image edits, image-to-video, video extension, and result retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke Dreamina CLI generation workflows that upload local image or video files to an external service. <br>
Mitigation: Only provide media files intended for upload, avoid sensitive local files, and confirm generation commands before running them. <br>
Risk: Broad activation wording could cause surprise use when a request only mentions related Seedance or video-generation terms. <br>
Mitigation: Prefer explicit Seedance requests or a dedicated command before executing CLI actions; use prompt-only mode when CLI use is not intended. <br>
Risk: The skill depends on a locally installed and browser-authenticated Dreamina CLI. <br>
Mitigation: Verify the CLI with `dreamina --version` and confirm login or credits before attempting generation. <br>


## Reference(s): <br>
- [Dreamina CLI download](https://jimeng.jianying.com/cli) <br>
- [ClawHub skill page](https://clawhub.ai/chencore/seedance-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Chinese prompt text, inline bash command examples, generation result links, and task status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Dreamina submit IDs, image or video URLs, dimensions, durations, and the prompt used for generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
