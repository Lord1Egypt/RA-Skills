## Description:

Manage VK.com (Vkontakte) communities by posting text, photos, and videos and handling visitor messages through the VK API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruslanlanket](https://clawhub.ai/user/ruslanlanket)

### License/Terms of Use:


## Use Case:

Developers and community managers use this skill to automate VK community publishing, media uploads, message replies, conversation review, and Long Poll monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad, long-lived VK user tokens can expose account and community access if copied into shell history, logs, or shared terminals.

Mitigation: Use narrowly scoped VK credentials, prefer official VK developer flows and community-scoped credentials, avoid permanent offline user tokens unless necessary, and rotate any token used in examples.

Risk: Posting, messaging, mark-as-read, media upload, and Long Poll operations perform real actions on VK communities and conversations.

Mitigation: Review commands, token scopes, group IDs, owner IDs, file paths, and message text before execution, and test with a non-production community when possible.

## Reference(s):

- [VK API & CLI Guide](references/api.md)
- [VK Developers](https://dev.vk.com)
- [VK Host](https://vkhost.github.io/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit VK API JSON responses, attachment identifiers, and Long Poll message text when commands are run.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
