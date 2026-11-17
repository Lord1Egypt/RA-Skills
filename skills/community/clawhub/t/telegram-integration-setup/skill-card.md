## Description:

Configure and troubleshoot OpenClaw Telegram integrations for new bots, DMs, groups, and topic-enabled supergroups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastiangansca](https://clawhub.ai/user/sebastiangansca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and troubleshoot OpenClaw Telegram routing for DMs, groups, and topic-enabled supergroups. It helps validate account-scoped policy, allowlists, mention-gating, chat IDs, thread IDs, and gateway restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram setup work may involve bot tokens, chat IDs, logs, gateway restarts, and group permissions.

Mitigation: Keep secrets out of shared prompts and logs, review sensitive configuration before use, and apply the skill's safer defaults for allowlists, mention-gating, narrow sender rules, and single active polling or webhook paths.

Risk: Incorrect account scope, allowlist, mention-gating, or topic thread settings can cause missed replies or unintended group responses.

Mitigation: Validate the active account policy, chat target, sender allowlist, mention requirement, thread ID, and gateway reload with fresh Telegram test messages.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, configuration-oriented steps, and troubleshooting notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; does not ship executable code or background services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
