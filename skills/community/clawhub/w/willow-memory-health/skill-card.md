## Description:

Audits OpenClaw memory files for stale, dead, redundant, dark, and contradictory records and guides confirmed cleanup actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudi193-cmd](https://clawhub.ai/user/rudi193-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to diagnose memory quality issues and decide whether to archive, merge, re-index, or review memory files. It is useful when an agent appears to forget information or when memory folders need periodic maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the memory directory selected by the user, which may contain sensitive agent memory content.

Mitigation: Run it only on memory folders you intend to audit, and review the reported file list before approving any follow-up action.

Risk: Cleanup actions can move memory files, merge records, update qmd indexing, or append audit summaries.

Mitigation: Require explicit user confirmation for each change and show the exact files or actions before proceeding.

Risk: DARK record detection depends on qmd availability and index state.

Mitigation: Treat DARK findings as retrieval-index health signals, update or re-index qmd when approved, and re-run diagnostics to confirm results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rudi193-cmd/skills/willow-memory-health)
- [Publisher Profile](https://clawhub.ai/user/rudi193-cmd)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Memory Health Script](artifact/scripts/memory_health.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports memory-health buckets and flags; optional qmd-based DARK detection requires qmd.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
