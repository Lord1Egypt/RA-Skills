## Description:

Compare two queue or state snapshots and explain what changed between them. Use when Codex needs to analyze drift between JSON/JSONL snapshots, detect newly stuck jobs, missing queue references, changed counters, or state regressions across two points in time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare before-and-after JSON or JSONL-derived queue and state snapshots, then interpret added, removed, and changed fields as operational regressions, recoveries, or noise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can create or overwrite the path passed with --out.

Mitigation: Set --out only to an approved local report path you are comfortable creating or overwriting.

Risk: The generated Markdown report may include values copied from the input snapshots.

Mitigation: Review the before and after files for sensitive data before generating or sharing the report.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands]

**Output Format:** [Markdown diff report with a JSON command status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper reads local JSON inputs, writes a local Markdown report, and limits listed changed, added, and removed entries in the report.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
