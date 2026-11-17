## Description:

Automatically crawls new local chat logs, chunks conversation text, and appends structured memory entries to Space2-OS hippocampus storage for agent memory evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate ingestion of local chat logs into a Space2-OS memory buffer. It is intended for environments where recurring local memory capture is deliberate and controlled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring chat-log ingestion can persist sensitive conversation content into S2 memory.

Mitigation: Use the skill only with intentional approval, redact secrets before storage, and define retention and deletion controls for hippocampus_logs.json.

Risk: Weak log-directory scoping can ingest unintended files from shared or writable-by-others locations.

Mitigation: Restrict the log directory, avoid shared writable folders, add an explicit extension allowlist, and check symlinks before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-memory-hook)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [text, configuration, JSON files]

**Output Format:** [Console status text plus JSON memory and cursor files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends timestamped memory records to hippocampus_logs.json and updates s2_hook_cursor.json for delta-sync tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
