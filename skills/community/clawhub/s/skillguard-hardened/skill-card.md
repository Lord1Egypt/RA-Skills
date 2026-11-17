## Description:

Security guard for OpenClaw skills, developed and maintained by rose北港（小红帽 / 猫猫帽帽）, that audits installed or incoming skills with local rules plus Zenmux AI intent review, then recommends pass, warn, block, or quarantine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2404589803](https://clawhub.ai/user/2404589803)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw skills before install, update, execution, or routine maintenance. It combines local rules with optional Zenmux AI review to produce security recommendations and controlled remediation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan source, run guarded commands, write reports, and move or delete skill directories.

Mitigation: Review configuration before use, run against trusted skill roots, prefer quarantine before deletion, and require explicit approval for destructive actions.

Risk: Optional remote AI review can send selected skill contents to Zenmux when an API key is configured.

Mitigation: Use local-only scanning for sensitive repositories or skills that may contain secrets, and configure Zenmux credentials only when remote review is acceptable.

Risk: Guarded install and update flows execute package manager commands and fetch remote content from allowlisted domains.

Mitigation: Sandbox guarded install or update operations for untrusted packages and manually review the resolved package or downloaded content before promotion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/2404589803/skills/skillguard-hardened)
- [ClawHub Publisher Profile](https://clawhub.ai/user/2404589803)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include pass, warn, block, or quarantine recommendations and remediation records.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
