## Description:

Soul Dreaming provides progressive memory management with categorized files, indexed retrieval, and survival-merge evolution to reduce context loss after compaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuexian1211](https://clawhub.ai/user/xuexian1211)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to preserve important decisions, discoveries, pending work, and workspace context across compaction or session boundaries through structured memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workspace memory can capture sensitive project history, personal preferences, security-sensitive configuration, or credential locations.

Mitigation: Require explicit opt-in before memory writes, keep memory files out of source control and broad search indexes, prohibit secrets and credential locations, and redact security-sensitive details.

Risk: Memory cleanup, merge, archive, or deletion cycles can remove useful context or preserve stale records that affect later agent behavior.

Mitigation: Review or back up memory files before cleanup, merge, archive, or deletion, and use the index and fitness metadata to check whether entries are current.

Risk: Incorrect or misleading memory entries can steer future work toward obsolete decisions or repeated mistakes.

Mitigation: Review memory content before relying on it for consequential work, and mark conflicts or superseded records clearly before future sessions consume them.

## Reference(s):

- [Memory Lifecycle](references/memory-lifecycle.md)
- [Anti-Amnesia Checklist](references/anti-amnesia-checklist.md)
- [Mount Strategy](references/mount-strategy.md)
- [Survival Merge Protocol](references/survival-merge.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions and templates for workspace memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured memory workflow with categorized files, journals, an index, and archive guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
