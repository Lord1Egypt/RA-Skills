## Description:

Security scanner for ClawHub skills. Analyze before you install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill reviewers use this skill to statically scan ClawHub or local skill directories before installation and review reported security findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can incorrectly mark risky skills as safe because of known allowlist matching and scoring gate issues.

Mitigation: Do not treat a SAFE result as the final security decision; manually review the scanned skill before installation.

Risk: The scanner can read outside a selected scan directory through symlinks.

Mitigation: Run scans of untrusted skill directories in a contained environment.

Risk: The release has a suspicious security verdict from ClawHub's security evidence.

Mitigation: Install only after review and inspect any downloaded or scanned skill before installation.

## Reference(s):

- [Skill Guard Pro on ClawHub](https://clawhub.ai/chloepark85/skills/skill-guard-pro)
- [Publisher profile: chloepark85](https://clawhub.ai/user/chloepark85)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable security report or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include risk level, risk score, files scanned, lines scanned, findings, URLs, and installation guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
