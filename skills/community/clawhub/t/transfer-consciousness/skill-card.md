## Description:

Prepare and verify a checkpoint-based handoff of agent work to another host or session while preserving context, permissions and single-writer ownership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to prepare a durable continuation brief, verify transferred files, and coordinate a single-owner handoff between sessions or hosts without treating it as live process migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned install command may fetch different skill contents than the version reviewed.

Mitigation: Prefer a pinned or manually reviewed copy before installation.

Risk: A handoff bundle could expose secrets, private transcripts, session material, or unrelated project files.

Mitigation: Transfer only explicitly relevant files and inspect the bundle for secrets before sharing it.

Risk: Two agents may write to the same work if readiness is mistaken for ownership transfer.

Mitigation: Require a clear cutover through an existing lock or lease mechanism, or disclose and supervise the procedural handoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antreasantoniou/skills/transfer-consciousness)
- [Maintainer skills page](https://antreas.io/skills/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include handoff identifiers, file inventories, hashes, watch inventories, and ownership status checkpoints.]

## Skill Version(s):

1.0.0 (source: CHANGELOG.md and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
