## Description:

Provides audit checklists, configuration guidance, and incident-response steps for hardening OpenClaw and Aegis deployments against exposure, credential leakage, unsafe skill installation, unauthorized gateway access, and compromise recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebrierfox](https://clawhub.ai/user/thebrierfox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw and Aegis deployments, tighten gateway and credential handling, vet third-party skills before installation, and follow containment and recovery procedures after suspected compromise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some command snippets can reveal gateway tokens or other credentials in terminal output.

Mitigation: Replace secret-printing checks with redacted or boolean checks before use.

Risk: Incident-response copy commands can create additional copies of logs and configuration files containing sensitive data.

Mitigation: Create incident evidence directories with restrictive permissions before copying logs or configuration files.

Risk: Broad process termination commands can stop unrelated sessions or services.

Mitigation: Preview matching process IDs and scopes before terminating processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thebrierfox/skills/security-hardening-toolkit-v1-0)
- [Publisher profile](https://clawhub.ai/user/thebrierfox)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with checklists, command snippets, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides operator-facing recommendations; command snippets should be reviewed and adapted before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
