## Description:

Use this skill when auditing or operating the Trinity/OpenClaw self-evolution loop: checking version status, preflight health, capability validation gates, direction radar output, failure-repair fallback, and user-facing progress reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw self-evolution readiness, verify validation gates, and produce plain-language reports about practical capability changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could rely on incorrect local status or preflight commands when making readiness claims.

Mitigation: Confirm the official OpenClaw status and preflight commands for the local setup before using the skill's audit results.

Risk: Public reports could expose private operational records or machine-specific paths.

Mitigation: Review generated reports before publication and remove sensitive local data, private records, and machine-specific details.

## Reference(s):

- [v16.0 Audit Baseline](references/v16-audit.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with status checks, validation summaries, and user-facing progress reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included; outputs should avoid private operational records and machine-specific paths.]

## Skill Version(s):

16.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
