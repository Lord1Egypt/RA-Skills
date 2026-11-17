## Description:

Operate ClawVault services, configuration, vault presets, scanning, and OpenClaw plugin acceptance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martin2877](https://clawhub.ai/user/martin2877)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage an installed ClawVault environment from OpenClaw agents, including service lifecycle, local configuration, vault presets, threat scanning, and plugin acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start and stop local ClawVault processes.

Mitigation: Install it only where the operator is allowed to manage those local services, and avoid use on shared systems unless process-control effects are acceptable.

Risk: The skill can read files supplied to scan-file or plugin-acceptance.

Mitigation: Provide only files intended for inspection, and avoid custom --path values for plugin-acceptance unless the target file is safe to read.

Risk: The skill can write persistent ClawVault configuration.

Mitigation: Review configuration backups and intended changes before using config-set or vault-apply.

Risk: The skill can contact dashboard URLs for status checks, hot-patching, and plugin verification.

Mitigation: Prefer the default local dashboard address and avoid custom --clawvault-url values unless the endpoint is trusted.

## Reference(s):

- [ClawVault Repository](https://github.com/tophant-ai/ClawVault)
- [OpenClaw Skill Guide](https://github.com/tophant-ai/ClawVault/blob/main/doc/OPENCLAW_SKILL.md)
- [Tophant Clawvault Operator on ClawHub](https://clawhub.ai/martin2877/skills/tophant-clawvault-operator)
- [Publisher Profile](https://clawhub.ai/user/martin2877)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [Plain text or JSON command results, with configuration changes written locally when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands start or stop local processes, scan user-supplied text or files, or update ClawVault configuration.]

## Skill Version(s):

0.2.6 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
