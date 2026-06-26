## Description: <br>
Compare two queue or state snapshots and explain what changed between them. Use when Codex needs to analyze drift between JSON/JSONL snapshots, detect newly stuck jobs, missing queue references, changed counters, or state regressions across two points in time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to compare before and after JSON or JSONL-derived snapshots and summarize operational drift, regressions, recoveries, missing references, and changed counters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diff reports can include changed values from the input snapshots, which may expose secrets or sensitive operational data if those snapshots contain them. <br>
Mitigation: Use snapshots that have been reviewed or redacted for sensitive values, and store generated Markdown reports only in locations appropriate for the data they contain. <br>


## Reference(s): <br>
- [Queue State Diff on ClawHub](https://clawhub.ai/neo1307/queue-state-diff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with a JSON command summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script compares flattened JSON keys, reports counts for added, removed, and changed keys, and limits detailed changed, added, and removed entries in the Markdown report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
