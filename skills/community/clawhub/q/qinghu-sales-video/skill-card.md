## Description:

Guides an agent to turn product images and selling points into short promotional videos with generated scripts, narration, and subtitles using Qinghu's video service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and marketing teams use this skill to create short product-promotion videos from product images and selling points for platforms such as TikTok and Douyin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or updating of unpinned Node and npm tools may change the user's environment.

Mitigation: Review installation steps and prefer an already installed, pinned qhkit version before running the skill.

Risk: Product media is uploaded to Qinghu and the service token may be stored for later use.

Mitigation: Obtain approval before uploading media and use a secure secret manager instead of entering tokens ad hoc or changing shell profiles.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-sales-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and video result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status, delivered video links, and credits charged when available.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
