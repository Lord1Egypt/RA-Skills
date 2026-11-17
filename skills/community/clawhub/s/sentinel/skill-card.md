## Description:

Automated backup, integrity monitoring, and self-healing for AI agent workspaces. Detects unexpected changes, creates automatic backups, self-heals from corruption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI agent operators, and workspace maintainers use Sentinel to monitor critical local workspace files, create backups, compare file manifests, and restore known-good state after corruption or accidental changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, back up, and overwrite configured workspace files, and evidence.security flags restore safeguards as too weak for overwrite authority.

Mitigation: Run it unprivileged, test on non-critical workspaces first, disable automatic restore until behavior is verified, and review restore targets before allowing overwrite operations.

Risk: Monitoring traversal-prone patterns, untrusted symlinks, or shared backup locations can increase the chance of restoring or exposing unintended files.

Mitigation: Constrain monitored paths to trusted workspace files, avoid untrusted symlinks and traversal-prone patterns, and keep backups outside shared locations with appropriate filesystem permissions.

Risk: The artifact documents local-only backups, plain-file backup storage, limited corruption detection, and delayed scheduled checks.

Mitigation: Use Sentinel as a local recovery aid only, add separate off-site backup or version control where needed, and pair it with application-level validation for semantic correctness.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/sentinel)
- [README.md](artifact/README.md)
- [LIMITATIONS.md](artifact/LIMITATIONS.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local configuration guidance, monitoring and restore commands, manifest workflows, and operational cautions for workspace backup and recovery.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
