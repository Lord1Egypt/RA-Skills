## Description:

SiliconFlow API helps agents generate images, videos, and Chinese speech through SiliconFlow after the user configures an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-j-j](https://clawhub.ai/user/mr-j-j)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call SiliconFlow for text-to-image, image-to-image, text-to-video, image-to-video, video status checks, text-to-speech, and model listing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts, images, and text are sent to a third-party SiliconFlow API for processing.

Mitigation: Use only with non-sensitive prompts, images, and text, and review data-handling requirements before deployment.

Risk: The authoritative security review reports unsafe scripting that can execute injected Python from crafted prompts in image-to-image or image-to-video flows.

Mitigation: Do not pass untrusted prompt content to image-to-image or image-to-video commands until the Python construction is fixed and reviewed.

Risk: The skill stores a SiliconFlow API key locally and generated media can incur SiliconFlow billing.

Mitigation: Store the API key with restrictive file permissions, monitor usage, and confirm billing impact before running generation commands.

## Reference(s):

- [SiliconFlow](https://siliconflow.cn)
- [SiliconFlow API base URL](https://api.siliconflow.cn/v1)
- [ClawHub skill page](https://clawhub.ai/mr-j-j/skills/siliconflow-api)
- [Publisher profile](https://clawhub.ai/user/mr-j-j)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, Files, Text, Guidance]

**Output Format:** [Markdown with inline bash commands; generated media is saved as PNG, MP4, or MP3 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a locally stored SiliconFlow API key, sends prompts and input media to a third-party API, and may consume account balance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
