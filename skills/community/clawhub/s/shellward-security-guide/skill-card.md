## Description:

OpenClaw security deployment guide that helps users harden an OpenClaw installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jnmetacode](https://clawhub.ai/user/jnmetacode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review an OpenClaw deployment for network exposure, container isolation, credential handling, audit logging, plugin security, and patch status, then receive prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential scans can expose sensitive values if broad files or environment variables are printed or retained.

Mitigation: Limit scans to OpenClaw-specific paths, redact secret values, and avoid storing credential-bearing output.

Risk: A blanket SSH permission command can change files beyond the intended target.

Mitigation: Inspect affected paths individually and apply permission changes only after confirming the exact files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jnmetacode/skills/shellward-security-guide)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown checklist with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese guidance; destructive operations should require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
