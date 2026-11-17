## Description:

Automates WeChat for Windows to open the desktop client and send messages, images, and files to specified contacts, and can be called by other skills for automated delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgfuying](https://clawhub.ai/user/wgfuying)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and automation agents use this skill on Windows machines with WeChat Desktop installed to send confirmed messages, images, and files to named contacts or groups from command-line invocations or batch manifests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can send WeChat messages, images, and files from the logged-in account without recipient verification or confirmation.

Mitigation: Require explicit confirmation of the recipient, content, and attachments before execution, and review batch manifests carefully.

Risk: Local files can be sent as WeChat attachments.

Mitigation: Avoid sensitive files and constrain command or manifest file paths to the intended attachments.

Risk: The automation depends on a visible WeChat Windows UI and exact contact selection.

Mitigation: Use structured result markers and screenshot output to verify outcomes without closing or minimizing WeChat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wgfuying/skills/wechat-desktop-claw-automatic-control)
- [Source repository](https://github.com/WGfuying/wechat-desktop-claw-automatic-control)
- [SkillHub homepage](https://skillhub.cn/skills/wechat-desktop-claw-automatic-control)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime emits structured text markers and optional PNG screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit [SENT_OK], [SENT_FAIL], and [RESULT] markers for agent parsing; optional screenshot output supports post-send verification.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter declares 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
