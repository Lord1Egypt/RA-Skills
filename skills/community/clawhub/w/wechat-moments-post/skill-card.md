## Description:

Automates posting an image and caption to WeChat Moments on Windows desktop by opening Moments, selecting an image, pasting caption text, publishing, and checking the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zch-danny](https://clawhub.ai/user/zch-danny)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate a Windows desktop WeChat Moments posting workflow when they need to publish a configured image and caption through the WeChat UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically click through the WeChat desktop UI and publish a post without a final built-in confirmation.

Mitigation: Review the configured image and caption before running the publish step, and run it only when the WeChat session is ready for posting.

Risk: The skill captures broad desktop and WeChat screenshots into a temporary directory.

Mitigation: Close or hide sensitive desktop content before execution and clean the configured temporary screenshot directory afterward.

Risk: OCR or GUI targeting can misread the compose window or fail to paste the caption accurately.

Mitigation: Use explicit verification keywords when possible and manually check the compose window before relying on the published result.

## Reference(s):

- [WeChat Moments workflow reference](references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/zch-danny/skills/wechat-moments-post)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with Python script execution steps and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Windows desktop WeChat session and user-provided image and caption values.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
