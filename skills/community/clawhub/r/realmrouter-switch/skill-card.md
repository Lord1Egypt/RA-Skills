## Description:

Zero-friction RealmRouter model manager for OpenClaw. Chat-first workflow for setting API key, guided model picking, switching with availability check, rollback, connectivity testing, and short rr commands on both Unix and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vegetable1bird](https://clawhub.ai/user/vegetable1bird)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure RealmRouter credentials, choose or switch default models, test connectivity, and roll back OpenClaw configuration changes across macOS, Linux, and Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a RealmRouter API key in OpenClaw configuration and backup files.

Mitigation: Use a dedicated RealmRouter key, keep OpenClaw configuration and backup files access-controlled, and rotate or revoke the key if it may have been exposed.

Risk: The skill can change the default OpenClaw model and restart the OpenClaw gateway.

Mitigation: Review the selected model and current configuration before switching, keep the generated backups, and use rollback if behavior is not as expected.

Risk: Installer commands add local rr wrappers and the Windows workflow may request elevated execution.

Mitigation: Install from a pinned, trusted ClawHub release where possible and avoid running Windows installation with administrator privileges unless it is required.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vegetable1bird/skills/realmrouter-switch)
- [RealmRouter API endpoint](https://realmrouter.cn/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw configuration, create backups, and restart the OpenClaw gateway when the user executes the skill's commands.]

## Skill Version(s):

2.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
