## Description:

Pre-install safety check for ClawHub skills that scans for the three highest-risk signals before anything lands on disk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordo-tech](https://clawhub.ai/user/ordo-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check a ClawHub community skill before installation, review LOW / MEDIUM / HIGH risk findings, and decide whether to proceed, confirm, or block the install.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan reports include recurring commercial promotion.

Mitigation: Review generated reports before relying on them in formal install workflows, and confirm that promotional links do not distract from the actual risk decision.

Risk: The skill evaluates untrusted manifests without clearly documented isolation.

Mitigation: Use it as a pre-install advisory gate and manually scrutinize results for adversarial or unknown skills before installing anything.

Risk: The free release checks only three risk signals.

Mitigation: Treat clean results as limited assurance and use additional review for permissions, provenance, suspicious exec chains, and data exfiltration behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ordo-tech/skills/skill-pre-install-scanner)
- [Publisher profile](https://clawhub.ai/user/ordo-tech)
- [ClawHub Security Pack](https://theagentgordo.gumroad.com/l/clawhub-security-pack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style risk report with a LOW / MEDIUM / HIGH rating, flagged findings, and install guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The free release reports three risk signals and may advise confirmation or blocking for higher-risk installs.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
