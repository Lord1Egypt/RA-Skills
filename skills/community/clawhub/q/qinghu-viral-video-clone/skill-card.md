## Description:

Analyzes a short-video link, adapts its script for the user's product, and guides generation of a similarly styled marketing video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and creators use a Douyin or TikTok video link to draft a product-specific script and generate a similar short marketing video after reviewing the script and cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install or upgrade Node and qhkit or change shell configuration.

Mitigation: Approve setup steps explicitly and avoid persistent shell changes unless requested.

Risk: The service token grants access to the video-generation account.

Mitigation: Use a scoped token and keep it out of shared output.

Risk: Video generation and reference videos can consume credits.

Mitigation: Review the adapted script and estimate charges before submitting a generation task.

Risk: Closely copying source video material or dialogue may infringe rights.

Mitigation: Adapt the creative structure without reusing original footage or dialogue.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-viral-video-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Video links]

**Output Format:** [Markdown with script comparisons, generation status, and a video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation is asynchronous; reports task ID and applicable credit costs.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
