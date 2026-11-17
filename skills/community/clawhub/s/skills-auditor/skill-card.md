## Description:

Security audit + append-only logging + monitoring for OpenClaw skills (file-level diff, baseline approval, SHA-256 integrity). Requires Python >=3.9 and git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucloud-security](https://clawhub.ai/user/ucloud-security)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw skill directories, record append-only local scan logs, monitor skill changes, and prepare summarized notifications for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the implementation can persist unintended sensitive files and can miss or suppress important security findings.

Mitigation: Review before installing, run in a contained workspace or after fixing symlink rejection and containment checks, and do not rely on its risk score alone until SKILL.md scanning and metadata-based finding suppression are corrected.

Risk: Diffs, snapshots, and notifications can contain sensitive workspace content.

Mitigation: Keep notification targets local or trusted, send concise summaries by default, and require explicit review before sharing raw diffs externally.

## Reference(s):

- [Skill Auditor on ClawHub](https://clawhub.ai/ucloud-security/skills/skills-auditor)
- [SKILL.md](artifact/SKILL.md)
- [scripts/README.md](artifact/scripts/README.md)
- [templates/README.md](artifact/templates/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command examples, NDJSON logs, JSON scan records, and notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files, git snapshots, and configurable risk rules; notification output is summarized by default.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
