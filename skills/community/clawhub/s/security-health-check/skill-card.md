## Description:

Checks password strength, HIBP password exposure via k-anonymity, and SSL certificate health, then prints a security score report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security-conscious users use this skill to run local password strength checks, query HIBP for password exposure using a SHA-1 prefix, and inspect SSL certificate status from a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password checks send a SHA-1 prefix derived from the password to HIBP, while some CLI wording emphasizes local-only password analysis.

Mitigation: Disclose the HIBP prefix lookup before password checks and avoid using this mode in strict offline-only environments.

Risk: Passwords can be provided as CLI arguments, which may expose sensitive values through shell history or local process inspection.

Mitigation: Use only test or non-sensitive passwords in shared environments, clear shell history after use, or adapt the workflow to prompt for secrets securely.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/security-health-check)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [CLI text report and Markdown-style command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Password checks may contact HIBP with a SHA-1 prefix; SSL checks contact the target host.]

## Skill Version(s):

2.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
