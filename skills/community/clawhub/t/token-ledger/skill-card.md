## Description: <br>
Token Ledger (SQLite) records OpenClaw model usage and costs into SQLite, manages an optional watcher, and provides SQL-first reports for daily usage and billing reconciliation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonathanJing](https://clawhub.ai/user/JonathanJing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install or run a local OpenClaw token ledger, query model usage and cost history, and produce deterministic daily finance reports without rescanning session JSONL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional watcher continuously monitors local OpenClaw session JSONL files and writes model usage and cost history to a local SQLite database. <br>
Mitigation: Use one-shot backfill for occasional reporting, install the LaunchAgent only when continuous monitoring is needed, and inspect the rendered plist before loading it. <br>
Risk: The local ledger can reveal model usage patterns, session identifiers, and cost history. <br>
Mitigation: Treat ~/.openclaw/ledger.db and the checkpoint file as sensitive local data and restrict filesystem access accordingly. <br>
Risk: Ledger totals may differ from provider billing when retries, timeouts, streaming interruptions, or unknown pricing entries occur. <br>
Mitigation: Use the ledger as an auditable reconciliation aid, keep pricing versions explicit, and compare anomalous totals with provider billing records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JonathanJing/token-ledger) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, SQL, and command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce SQLite queries, daily cost summaries, LaunchAgent setup guidance, and local ledger maintenance commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
