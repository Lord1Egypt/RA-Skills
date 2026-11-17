## Description:

Reliable Feishu file sending workflow for delivering attachments separately from explanatory text and avoiding mediaLocalRoots path issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujunyanyanya](https://clawhub.ai/user/yujunyanyanya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when sending generated or edited files to Feishu users, especially when diagnosing missing attachments or file delivery failures. It guides the agent to keep explanatory text and attachments in separate outbound messages and to use paths allowed by mediaLocalRoots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad persistent upload allowlist such as the entire /tmp directory could expose unintended local files.

Mitigation: Use a dedicated outbound directory with restrictive permissions instead of broadly whitelisting temporary directories.

Risk: Gateway configuration changes and local file sends may disclose files without enough user intent checking.

Mitigation: Require explicit user approval before changing Feishu gateway configuration or sending local files.

## Reference(s):

- [Feishu file sending notes](references/feishu-file-sending-notes.md)
- [ClawHub skill page](https://clawhub.ai/yujunyanyanya/skills/yujunyanyanya-feishu-file-send)
- [Publisher profile](https://clawhub.ai/user/yujunyanyanya)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English operational guidance for Feishu attachment delivery.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
