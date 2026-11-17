## Description:

Scans Python skill directories for security risks such as dangerous code patterns, hardcoded secrets, risky file or network usage, and optional file reputation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub maintainers use this skill to scan Python-based skills before release, generating findings and risk scores that support security review and publishing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML reports may expose untrusted scan contents or unsafe markup when scanning untrusted skills.

Mitigation: Prefer JSON output or review and fix report generation before enabling HTML reports for untrusted inputs.

Risk: Reports can include snippets from .env or configuration files that contain sensitive values.

Mitigation: Avoid scanning directories with secrets unless reports are protected, access-controlled, and cleaned after review.

Risk: The installer creates a symlink under ~/.local/bin.

Mitigation: Install in an isolated environment and verify the symlink target before placing it on PATH.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/skills/skill-secure-checker)
- [ClawHub Publisher Profile](https://clawhub.ai/user/utopiabenben)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JSON security report with optional HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes finding counts, risk score, risk level, issue details, and optional nonzero exit for high or critical findings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
