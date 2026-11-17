## Description:

Diagnoses and repairs WeCom channel configuration issues in OpenClaw, including connection failures, missing bot credentials, plugin ID mismatches, and unsupported multi-account configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fclwtt](https://clawhub.ai/user/fclwtt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw WeCom integrations use this skill to diagnose channel failures and prepare repair guidance, shell commands, and configuration snippets for restoring single-account operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeCom bot credentials may be exposed if users paste real secrets into chat or run commands that print secret-bearing configuration.

Mitigation: Avoid sharing real secrets in chat, redact command output before review, and enter credentials through safer mechanisms when available.

Risk: The provided configuration template uses open group access, which can broaden who may interact with the WeCom integration.

Mitigation: Replace open group policy with explicit trusted senders or groups unless broad group access is intentional.

Risk: Repair guidance may change live OpenClaw configuration and restart the gateway.

Mitigation: Back up openclaw.json before edits, review proposed changes, and verify channel and gateway status after restart.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fclwtt/skills/skills-5)
- [WeCom OpenClaw plugin](https://github.com/openclaw/wecom-openclaw-plugin)
- [WeCom AI Bot documentation](https://open.work.weixin.qq.com/help?doc_id=21657)
- [OpenClaw channel configuration documentation](https://docs.openclaw.ai/channels)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
