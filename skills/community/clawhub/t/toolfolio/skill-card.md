## Description:

Analyzes video shot cuts and camera movement, then generates English AI video prompts and motion data for each detected shot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winme99998](https://clawhub.ai/user/winme99998)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to inspect a video, identify shot boundaries and camera movement, and draft English AI-video prompts for each shot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis JSON can include representative video frames as base64 thumbnails, which may expose sensitive visual content from user-provided videos.

Mitigation: Avoid running the skill on sensitive videos unless local thumbnail copies in the analysis output are acceptable.

Risk: Unpinned Python dependencies can make analysis behavior less reproducible across environments.

Mitigation: Install dependencies in a virtual environment and pin package versions when reproducible results are required.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Console text plus a local JSON analysis file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-shot time ranges, movement labels, confidence scores, English AI prompts, motion details, and base64 JPEG thumbnails.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
