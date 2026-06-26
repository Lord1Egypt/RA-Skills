## Description: <br>
Self-evolving Polymarket trading bot. Design strategy with user, run paper trading, auto-improve until edge target met, then ask to switch to live. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, run, and review Polymarket trading strategies with paper trading first and live trading only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores wallet secrets locally and can use configured credentials for Polymarket trading if the host is compromised. <br>
Mitigation: Use only a dedicated low-balance wallet, protect local credential files, and avoid sharing hosts with untrusted users. <br>
Risk: Persistent cron jobs can run automated trades, including real-money trades after dry-run is disabled. <br>
Mitigation: Keep dry_run enabled until live-trading risk is intentionally accepted, inspect crontab entries before adding them, and require explicit user confirmation before enabling live trading. <br>
Risk: Untrusted or path-like USER_ID values could affect where local credential and state files are read or written. <br>
Mitigation: Use simple trusted user identifiers and avoid path separators or externally supplied USER_ID values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patches429/storyclaw-polymarket-trading) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and POLYMARKET_PRIVATE_KEY or per-user credential JSON for authenticated trading operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
