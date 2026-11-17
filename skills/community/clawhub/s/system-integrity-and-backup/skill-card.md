## Description:

Encrypted backups, integrity verification, and data retention enforcement for Greek legal requirements (5-20 year retention). AES-256.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

Developers and operators of OpenClaw Greek accounting deployments use this skill to maintain encrypted backups, verify local data integrity, enforce retention review workflows, and prepare audit-ready status reports.

### Deployment Geography for Use:

Greece

## Known Risks and Mitigations:

Risk: The skill handles sensitive accounting data with broad local access and inconsistent encryption-key guidance.

Mitigation: Require one documented encryption-key model before use and restrict permissions on backup, auth, and log paths.

Risk: Event snapshots and permanent logs may capture sensitive client data.

Mitigation: Define who or what may trigger snapshots and review permanent logs for sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/system-integrity-and-backup)
- [OpenClaw Greek Accounting homepage](https://github.com/satoshistackalotto/openclaw-greek-accounting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with OpenClaw command examples and JSON/PDF report descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local jq, openssl, tar, OPENCLAW_DATA_DIR, and OPENCLAW_ENCRYPTION_KEY configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
