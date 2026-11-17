## Description:

Codex Account Switcher helps agents query OpenAI Codex OAuth quotas in OpenClaw, switch the preferred account by email or profile id, and optionally auto-switch when the 5-hour quota falls below a threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unknown-shu](https://clawhub.ai/user/unknown-shu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect Codex OAuth account quota status, reorder the preferred OpenClaw openai-codex profile, sync a Codex CLI login into OpenClaw, and automate quota-aware account failover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw and Codex OAuth credential files and can persist OAuth credentials into OpenClaw profiles.

Mitigation: Install only in environments where that credential access is acceptable, verify auth directory file permissions, and use dry-run modes before writing changes.

Risk: Quota checks send OAuth access tokens to ChatGPT's usage endpoint.

Mitigation: Run the quota and auto-switch scripts only with accounts and network paths approved for ChatGPT usage queries.

Risk: Account switching changes the OpenClaw openai-codex account order and may affect which account the agent uses.

Mitigation: Preview switches with --dry-run, confirm the target email or profile id, and review the OpenClaw auth-state file after changes when operating shared agents.

Risk: The sync command creates local credential backups that may retain sensitive OAuth material.

Mitigation: Remove stale .bak credential files when they are no longer needed and avoid committing auth files, logs, screenshots, or account emails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unknown-shu/skills/unknownshu-codex-account-switcher)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled scripts emit human-readable text or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and openclaw; some commands read local OpenClaw/Codex OAuth state and may write OpenClaw auth profile or account order files.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
