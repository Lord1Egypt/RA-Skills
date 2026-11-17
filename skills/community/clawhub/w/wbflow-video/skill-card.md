## Description:

This skill turns each prepared keyframe image into a short video clip, using the supplied video prompt to preserve shot continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

WBFlow users install this skill alongside the pipeline controller and companion stages to turn prepared shot keyframes and video prompts into per-shot video clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images may be processed by the selected video provider, and provider costs can vary.

Mitigation: Review the companion pipeline skills and confirm the provider and any associated costs before use.

## Reference(s):

- [WBFlow·第7环 图生视频 on ClawHub](https://clawhub.ai/junci003/skills/wbflow-video)

## Skill Output:

**Output Type(s):** [Video files]

**Output Format:** [MP4 video segment per shot]

**Output Parameters:** [One clip per input image; default 5 seconds, with a 5-second minimum.]

**Other Properties Related to Output:** [Uses each keyframe image as the first frame; does not generate still images or merge shots.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
