## Description:

Skill Security Guard scans third-party AI skills for malicious code, sensitive data exposure, risky file operations, and suspicious network behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sukimgit](https://clawhub.ai/user/sukimgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill users, and administrators use this skill to statically scan Python-based skills before installation, release, or periodic audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled network checker modules are broader than the stated static skill-scanning purpose and could expose local network or firewall details if imported or invoked.

Mitigation: Review or remove the network checker modules before installation, and run the skill only in a restricted environment unless those modules are needed and trusted.

Risk: Static scan reports can include false positives or incomplete findings.

Mitigation: Treat results as review prompts and manually inspect flagged code before approving or rejecting a skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sukimgit/skills/skill-security-guard-publish)
- [Publisher profile](https://clawhub.ai/user/sukimgit)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text report with risk scores, findings, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static analysis only; scans target Python skill files without executing them.]

## Skill Version(s):

1.0.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
