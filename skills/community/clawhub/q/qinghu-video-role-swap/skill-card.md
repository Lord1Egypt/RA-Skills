## Description:

Guides an agent through replacing a person in a video using an original video, a replacement portrait, and the video's duration while retaining the original motion and lip movements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use this skill to replace people in existing videos, including adapting model footage for different audiences, after confirming rights to the person's likeness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs or updates a third-party CLI and uploads selected videos and images to a third-party service.

Mitigation: Use an approved or pinned qhkit version when reproducibility matters, and share only media and API credentials you trust the package and service to handle.

Risk: Replacing a person's likeness without permission can enable misuse.

Mitigation: Confirm the user has rights to the person's likeness; decline unauthorized face replacement.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-video-role-swap)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Video links]

**Output Format:** [Markdown with command examples and a generated video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation is asynchronous; responses may include a task ID, completion status, and charged credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
