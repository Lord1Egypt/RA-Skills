## Description:

Generates storyboard keyframe images from shot prompts and character reference images, using references to maintain character consistency across shots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

Create one keyframe still for each storyboard shot from project prompts, using the matching character reference images for shots that include characters; the resulting images can serve as video first frames or references.

### Deployment Geography for Use:

Global; no geographic restrictions are specified in the release evidence.

## Known Risks and Mitigations:

Risk: Character reference images are provided to the selected image-generation service.

Mitigation: Use only reference images you are comfortable providing to that service.

Risk: This skill depends on project files and companion WBFlow skills, so installing it alone may not provide a runnable workflow.

Mitigation: Install and review the WBFlow controller and companion skills, and provide the expected project inputs.

## Reference(s):

- [WBFlow·第6环 关键帧 on ClawHub](https://clawhub.ai/junci003/skills/wbflow-image)

## Skill Output:

**Output Type(s):** [Images, Files]

**Output Format:** [PNG keyframe image files, one per shot]

**Output Parameters:** [One image for each prompt/shot; 16:9 or 9:16 dimensions]

**Other Properties Related to Output:** [Images may be used as video first frames or reference frames.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
