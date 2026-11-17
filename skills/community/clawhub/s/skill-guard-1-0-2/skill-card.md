## Description:

Scan ClawHub skills for security vulnerabilities before installing, including prompt injections, malware payloads, hardcoded secrets, and other threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to stage, scan, and install ClawHub skills with a pre-install security gate. It is intended for users who want security feedback before adding third-party skills to an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports path-safety weaknesses in the installer.

Mitigation: Use only simple trusted skill slugs and review the staged path before installation.

Risk: The security evidence reports supply-chain weaknesses.

Mitigation: Prefer a version that pins scanner dependencies and avoids curl-piped shell setup instructions.

Risk: Scan-bypass or overwrite flags can reduce the protection provided by the skill.

Mitigation: Avoid --skip-scan and --force unless their effects have been reviewed and accepted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenswj/skills/skill-guard-1-0-2)
- [kenswj ClawHub Profile](https://clawhub.ai/user/kenswj)
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI usage, exit codes, dependency notes, and threat-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
