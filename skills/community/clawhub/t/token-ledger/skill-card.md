## Description:

Audit-grade token and cost ledger for OpenClaw. Use when you need to (1) record every model call's usage (input/output/cache read/cache write/cost) into SQLite, (2) install/manage the ledger watcher LaunchAgent, (3) query ledger.db for daily usage/cost, fixed overhead, or historical billing reconciliation, or (4) generate low-token financial reports from SQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain an auditable local SQLite ledger of OpenClaw model usage, token counts, and cost estimates. It supports one-shot backfills, a persistent watcher, Spark token synchronization, SQL queries, and deterministic daily finance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watcher can run persistently and records sensitive local usage metadata, including session and cron-derived usage details.

Mitigation: Install it only when a local usage ledger is intended, review what it records, and restrict permissions on ~/.openclaw and the generated SQLite database.

Risk: Spark synchronization can contact a loopback API configured through LOCAL_API_HUB_URL.

Mitigation: Keep LOCAL_API_HUB_URL pointed only at a trusted local service and avoid routing it to untrusted hosts.

Risk: The LaunchAgent installation path should be verified before daemon use.

Mitigation: Review the generated LaunchAgent plist/template behavior before loading the watcher with launchctl.

## Reference(s):

- [ClawHub Token Ledger Homepage](https://clawhub.ai/jonathanjing/token-ledger)
- [ClawHub Token Ledger Skill Page](https://clawhub.ai/jonathanjing/skills/token-ledger)
- [Anthropic Claude Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [OpenAI Model Documentation](https://developers.openai.com/api/docs/models)
- [Google Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, SQL, guidance]

**Output Format:** [Markdown guidance with shell command blocks, SQL snippets, configuration steps, and deterministic text reports from SQLite.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill writes and queries a local SQLite ledger and can run as a persistent watcher when installed by the user.]

## Skill Version(s):

0.1.2 (source: server release metadata and skill metadata.openclaw.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
