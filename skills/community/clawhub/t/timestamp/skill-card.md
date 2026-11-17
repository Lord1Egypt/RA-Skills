## Description:

Create cryptographic proofs anchoring files' exact content and timestamp to the Bitcoin blockchain for immutable, verifiable history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axhoff](https://clawhub.ai/user/axhoff)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to timestamp workspace files with OpenTimestamps, archive changed proofs, and verify .ots proof files for file-history integrity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hash and timing metadata for timestamped files may be sent to third-party OpenTimestamps infrastructure.

Mitigation: Review the target file list before stamping and avoid highly sensitive or easily guessable files unless that metadata exposure is acceptable.

Risk: Auto-memory mode can include USER.md, MEMORY.md, SOUL.md, AGENTS.md, and memory/*.md from the workspace.

Mitigation: Inspect the auto-memory target set before running it manually, on commits, or on a schedule.

Risk: The scripts depend on the external OpenTimestamps client and timestamp infrastructure.

Mitigation: Install the OpenTimestamps client in an isolated, preferably pinned environment and verify proofs after Bitcoin confirmation.

## Reference(s):

- [Timestamp ClawHub release](https://clawhub.ai/axhoff/skills/timestamp)
- [Publisher profile](https://clawhub.ai/user/axhoff)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates .ots proof files beside target files and archives older proofs under .ots-archive when files change.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
