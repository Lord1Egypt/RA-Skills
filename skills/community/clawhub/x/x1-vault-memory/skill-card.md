## Description: <br>
Backup and restore OpenClaw agent memory to IPFS with AES-256-GCM encryption and X1 blockchain CID anchoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lokoweb3](https://clawhub.ai/user/Lokoweb3) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External developers and OpenClaw agent operators use this skill to back up agent identity, memory, and workspace notes to encrypted IPFS storage, record backup CIDs on X1, and restore selected trusted backups when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full restore can overwrite workspace files too broadly without a preview or enforced allowlist. <br>
Mitigation: Prefer selective restore, keep a local copy before restoring, and restore only CIDs the user created and trusts. <br>
Risk: Wallet and Pinata credentials are required for backup and anchoring workflows. <br>
Mitigation: Use a dedicated low-balance wallet and a minimally scoped Pinata token; never use a primary wallet. <br>
Risk: Agent memory backups may contain secrets, private notes, or regulated data. <br>
Mitigation: Do not back up secrets or regulated data in agent memory, and review the backup scope before uploading. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Lokoweb3/x1-vault-memory) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>
- [Pinata](https://app.pinata.cloud) <br>
- [X1 Explorer](https://explorer.mainnet.x1.xyz) <br>
- [X1 Bridge](https://app.bridge.x1.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts produce encrypted backup uploads, CIDs, transaction URLs, and local log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PINATA_JWT and a dedicated X1 wallet file; restore operations should use trusted CIDs and selective restore where possible.] <br>

## Skill Version(s): <br>
0.1.10 (source: ClawHub release metadata; artifact metadata reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
