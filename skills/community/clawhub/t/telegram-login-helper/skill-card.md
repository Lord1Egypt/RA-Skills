## Description:

Consolidate practical Telegram personal-account login workflows for tdl/TDLib: reuse an existing namespace, complete QR login, batch-login multiple namespaces, copy working TDLib state, and escalate honestly when human auth or API credentials are required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevewu422](https://clawhub.ai/user/stevewu422)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when Telegram personal-account access is blocked at login, when a reusable TDLib namespace or copied session state may resolve the issue, or when another agent needs a concise local login runbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated TDLib session state may expose a Telegram personal account if copied, stored, or reused without adequate protection.

Mitigation: Use the skill only for accounts you own or are authorized to administer, protect any session-state transfer and storage, and avoid copying state between machines unless that handling is secured.

Risk: The artifact includes hardcoded local paths and the steve namespace, which may be inappropriate in shared or different environments.

Mitigation: Review the paths and namespaces before use, then remove or adapt hardcoded local values for the target environment.

Risk: Telegram API credentials and TDLib data directories are sensitive and can enable account access.

Mitigation: Treat TELEGRAM_API_ID, TELEGRAM_API_HASH, and TDLib data directories as secrets and keep them out of logs, shared workspaces, and unprotected artifacts.

## Reference(s):

- [Telegram Login Runbook](references/runbook.md)
- [ClawHub Skill Page](https://clawhub.ai/stevewu422/skills/telegram-login-helper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive login guidance that may require QR scanning, reusable TDLib session state, or TELEGRAM_API_ID and TELEGRAM_API_HASH.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
