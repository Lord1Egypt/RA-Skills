## Description:

Zhiliao helps an agent create natural-language news tracking topics, retrieve aggregated articles, manage subscriptions, and schedule recurring topic updates through shell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfeng03-dev](https://clawhub.ai/user/jfeng03-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to track news topics, browse aggregated articles, manage topic subscriptions, and automate periodic article checks after configuring a ZHILIAO_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe credential handling may expose or send the ZHILIAO_API_KEY in ways the user does not expect.

Mitigation: Remove bundled local agent settings, rotate any exposed key, configure a fresh key through a trusted local mechanism, and only send it to the official HTTPS Zhiliao endpoint.

Risk: The included local agent-permission file is overbroad for normal use.

Mitigation: Review and remove .claude/settings.local.json before installation or restrict permissions to only the commands needed for this skill.

Risk: Default HTTP endpoints and configurable API origins can send credentials to an insecure or unexpected service.

Mitigation: Switch defaults and configuration to HTTPS and validate the API origin before running commands that include credentials.

Risk: Temporary file and topic-id handling may create avoidable local-file safety issues.

Mitigation: Harden temporary-file cleanup and validate topic identifiers before using the scripts in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jfeng03-dev/skills/zhiliao)
- [Zhiliao website](https://zhiliao.news/)
- [Zhiliao API key page](https://open.zhiliao.news/)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON-backed local cache files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ZHILIAO_API_KEY and writes local configuration, topic, session, and article cache data under ~/.zhiliao.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
