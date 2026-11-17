## Description:

Guides agents through generating two-person promotional videos from an authorized reference video and optional character image using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use this skill to guide an agent in producing two-person product or livestream-style videos with synchronized movements from a reference video. The agent checks inputs and pricing, submits the job, and shares the resulting video link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a CLI and storing a Qinghu API token may expose credentials or introduce dependency risk.

Mitigation: Review the installation and token storage approach, and prefer a pinned or already-reviewed qhkit version.

Risk: Submitted videos and images are uploaded to Qinghu and may contain others' likenesses, including minors.

Mitigation: Use only owned or authorized materials and obtain guardian consent for minors before upload.

Risk: Generating videos spends Qinghu credits and may require a paid subscription.

Mitigation: Check the live credit estimate and subscription eligibility, then obtain user confirmation before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-duo-viral-video)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Video links]

**Output Format:** [Markdown with commands and a generated video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports estimated credits before submission and actual credits after completion.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
