## Description:

将本地技能发布到 ClawHub。触发场景：发布技能、上传技能到ClawHub、发布skill、ClawHub发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to publish a local skill folder to ClawHub through a guided browser and desktop upload workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete local backup files before upload.

Mitigation: Confirm the target folder contents before running the cleanup step, or remove that step when backup files must be preserved.

Risk: The workflow changes desktop input state and clipboard contents while interacting with a system file dialog.

Mitigation: Run it only in an intended interactive desktop session and verify the selected folder before continuing.

Risk: The workflow can publish a skill publicly under the MIT-0 license.

Mitigation: Manually verify the account, license selection, uploaded files, and final publish action before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infiniteask/skills/publish-agent-skill-infinite)
- [ClawHub publish skill page](https://clawhub.ai/publish-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with inline PowerShell and Python command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes manual confirmation steps for folder upload and final publishing.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
