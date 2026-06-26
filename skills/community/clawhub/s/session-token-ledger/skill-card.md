## Description: <br>
Analyze local OpenClaw session token usage from a generated SQLite ledger and markdown summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgjq](https://clawhub.ai/user/zgjq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit local OpenClaw token usage, diagnose context bloat, inspect token-efficiency trends, and generate per-session or aggregate reports from a local ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads completed local OpenClaw session logs and creates local SQLite, JSON, and Markdown ledger files containing derived session metadata. <br>
Mitigation: Install only where local session analysis is intended, keep generated assets private, and avoid sharing ledger outputs unless session metadata has been reviewed. <br>
Risk: Optional hook setup can rebuild the ledger automatically after OpenClaw events. <br>
Mitigation: Enable the hook only when ongoing automatic ledger refreshes are desired; otherwise rebuild manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zgjq/session-token-ledger) <br>
- [Overview](references/overview.md) <br>
- [Hook setup](references/hook-setup.md) <br>
- [Query templates](references/queries.sql) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with SQLite queries, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports separate total tokens, input tokens, output tokens, and cache-read usage; generated ledger assets remain local.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
