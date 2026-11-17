## Description:

Summarize what is open, what changed, and what is due soon from a Campus Copilot snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local agent users use this skill to turn imported Campus Copilot snapshots into a concise brief covering open work, recent changes, upcoming due items, and current site workload. The skill is intended for read-only analysis of provided snapshot or contract data, with live browser validation only when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Summaries may be incomplete or stale if the provided snapshot is outdated or partial.

Mitigation: Ground conclusions in the supplied snapshot fields and call out missing or uncertain data instead of filling gaps from live sources.

Risk: Live browser automation could move the workflow outside the skill's read-only posture.

Mitigation: Use imported snapshot or contract data by default and perform live validation only when the user explicitly requests it.

Risk: The skill references companion example files that are not packaged with this artifact.

Mitigation: Do not rely on those examples unless the user or release package provides them separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaojiou176/skills/read-only-workspace-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise plain-language summary, typically in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should stay grounded in the provided Campus Copilot snapshot or contract data and should not perform live browser automation unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
