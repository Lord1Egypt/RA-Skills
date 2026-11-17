## Description:

Self-evolving Polymarket trading bot. Design strategy with user, run paper trading, auto-improve until edge target met, then ask to switch to live.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and operate a Polymarket trading workflow: create user-confirmed market strategies, run dry-run signal scans, review performance, and activate live trading only after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet credentials for Polymarket automation.

Mitigation: Use a dedicated wallet with limited funds, keep credentials isolated per user, and do not share private keys or generated credential files.

Risk: Scheduled workflows can run repeated signal scans and may execute live trades after a strategy is activated.

Mitigation: Keep dry-run enabled until results are personally inspected, avoid cron setup unless removal is understood, and require explicit confirmation before activating live trading.

Risk: Untrusted USER_ID or strategy IDs can affect which local credential, strategy, and state files are used.

Mitigation: Use trusted, expected user and strategy identifiers only, and run the skill in an isolated environment with pinned dependencies.

Risk: Server security evidence reports unsafe scoping and persistence gaps for live-trading workflows.

Mitigation: Review the skill carefully before installing, limit wallet funds, and inspect state, strategy, and cron configuration before any live use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/patches429/skills/storyclaw-polymarket-trading)
- [Polymarket CLOB API endpoint](https://clob.polymarket.com)
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON credential, strategy, and performance state files when the user runs the bundled scripts.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
