## Description:

Security checks for external content, including downloads, fetched documents, attachments, and newly imported resources, before an agent trusts or acts on them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-hussein](https://clawhub.ai/user/z-hussein)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to guide agents when inspecting untrusted external content, verifying downloads, and running scoped security audits before taking action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled checksum may be mistaken for proof of publisher authenticity.

Mitigation: Treat the checksum as a convenience integrity check and verify publisher identity and release provenance separately before relying on the skill.

Risk: Broad local audits can inspect files, services, logs, and configuration outside the user's intended scope.

Mitigation: Require explicit, bounded audit scope and user approval before host-wide enumeration, and exclude secrets and sensitive paths by default.

Risk: Quarantine, deletion, memory logging, or other write actions can modify local state.

Mitigation: Require direct user approval for each write or destructive action and keep temporary inspection writes inside an isolated workspace.

## Reference(s):

- [Attack Patterns Reference](references/attack-patterns.md)
- [Security Audit Checklist](references/audit-checklist.md)
- [Cryptography & Security Examples](references/crypto-examples.md)
- [Modern Security Tools Reference](references/modern-tools.md)
- [Security Best Practices Reference](references/security-best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, findings, recommendations, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should avoid raw secrets and sensitive configuration values.]

## Skill Version(s):

2.2.2 (source: server release metadata and changelog, released 2026-09-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
