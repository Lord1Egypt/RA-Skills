## Description:

小爱音箱语音播报。一句话让小爱说话，无需编写代码，支持定时提醒、远程喊话、家庭传话。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkfan](https://clawhub.ai/user/zkfan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send short voice announcements to Xiaomi Xiaoai speakers for home reminders, family messages, work alerts, and scheduled notifications. It can list linked devices, test account connectivity, and target a specific speaker by name or device ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Xiaomi account credentials and can remotely control linked speakers.

Mitigation: Install only when this account access and speaker control are acceptable, and restrict use to trusted local environments.

Risk: MI_PASS may be exposed if stored in shell startup files, cron entries, command strings, or shared logs.

Mitigation: Use a secret manager or tightly permissioned local secret file, and avoid placing the password directly in persistent shell or scheduler commands.

Risk: Executable dependencies loaded from /tmp/MiService can be replaced or modified outside the skill.

Mitigation: Use a private virtual environment with pinned, verified dependency versions and avoid importing dependencies from /tmp/MiService.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zkfan/skills/xiaoai-speaker)
- [xiaoai-speaker GitHub Repository](https://github.com/zkfan/xiaoai-speaker)
- [MiService Xiaomi Service API](https://github.com/Yonsm/MiService)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text/status output, setup guidance, and speaker voice announcements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Xiaomi account credentials through MI_USER and MI_PASS, with optional MI_DEVICE_NAME or MI_DEVICE_ID speaker targeting.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
