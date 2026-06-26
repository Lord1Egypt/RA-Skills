## Description: <br>
Encrypted backups, integrity verification, and data retention enforcement for Greek legal requirements (5-20 year retention). AES-256. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and operators use this skill to manage local backup, integrity, retention, restore-test, and schema migration workflows for Greek accounting data. It is suited to environments that can tightly control the intended data tree and require human review for retention and destructive actions. <br>

### Deployment Geography for Use: <br>
Greece <br>

## Known Risks and Mitigations: <br>
Risk: The skill is documented for broad backup, decryption, retention, and cleanup actions over local accounting data. <br>
Mitigation: Install only where access to the intended data tree can be restricted, and require explicit operator approval before decryption, snapshot creation, cleanup, deletion, or retention actions. <br>
Risk: Security evidence notes conflicting documentation about encryption-key storage. <br>
Mitigation: Define and review key handling before deployment; keep backup decryption keys separate from backups and avoid storing plaintext keys on disk. <br>
Risk: Retention behavior is jurisdiction-specific and may affect regulated records. <br>
Mitigation: Treat retention outputs as guidance for human review, and confirm Greek legal retention requirements before archiving or deleting records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/satoshistackalotto/system-integrity-and-backup) <br>
- [Publisher Profile](https://clawhub.ai/user/satoshistackalotto) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>
- [Artifact Evaluation Prompts](artifact/EVALS.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON or YAML-style operational examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, openssl, tar, OPENCLAW_DATA_DIR, and OPENCLAW_ENCRYPTION_KEY; documented operations are local to OPENCLAW_DATA_DIR.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
