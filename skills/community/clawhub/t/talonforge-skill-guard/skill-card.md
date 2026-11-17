## Description:

Scan ClawHub skills for security vulnerabilities before installing, including prompt injections, malware payloads, hardcoded secrets, and other threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to stage ClawHub skills, scan them before installation, and block or quarantine skills when scanner output indicates security issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can delete or move unintended files if paths are not strictly contained.

Mitigation: Validate skill slugs against a strict allowlist and canonicalize every delete or move path before execution.

Risk: The scanner is invoked as unpinned remote code.

Mitigation: Pin mcp-scan to a reviewed version before relying on the scan result.

Risk: The --skip-scan option can bypass the skill's primary security control.

Mitigation: Remove or strongly gate --skip-scan and require explicit review when scanning is bypassed.

Risk: Dependency setup guidance includes curl-to-shell installation.

Mitigation: Use a trusted package installation path and avoid curl-to-shell setup on important workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/casperzinou/skills/talonforge-skill-guard)
- [Publisher profile](https://clawhub.ai/user/casperzinou)
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Terminal output and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installer exits with status codes for clean installs, errors, and quarantined threats.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
