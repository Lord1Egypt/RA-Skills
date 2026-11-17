## Description:

Backup and restore OpenClaw agent memory to IPFS with AES-256-GCM encryption and X1 blockchain CID anchoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lokoweb3](https://clawhub.ai/user/lokoweb3)

### License/Terms of Use:

ISC

## Use Case:

External developers and OpenClaw agent operators use this skill to back up, list, and restore agent identity and memory files through encrypted IPFS storage with X1 chain CID anchoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dry-run command may be misleading and should not be treated as assurance that no upload, transaction, or state change will occur.

Mitigation: Do not rely on --dry-run until it is fixed; review the script behavior before running backup operations.

Risk: Backup and restore behavior can upload data, sign transactions, or overwrite agent state unexpectedly.

Mitigation: Use a dedicated low-balance wallet, a scoped Pinata token, and a reviewed workspace before running backup or restore commands.

Risk: Heartbeat automation can trigger unattended restores that overwrite agent files.

Mitigation: Enable heartbeat cron only when unattended restore behavior is explicitly accepted and monitored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lokoweb3/skills/x1-vault-memory)
- [Pinata](https://app.pinata.cloud)
- [X1 Explorer](https://explorer.mainnet.x1.xyz)
- [OpenClaw Docs](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes encrypted backup data, restore outputs, and local vault log entries when the scripts are run.]

## Skill Version(s):

0.1.10 (source: server release metadata; artifact frontmatter and package metadata report 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
