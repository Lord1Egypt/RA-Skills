## Description:

Security toolkit for AI workflows. Use when scanning code or repos for vulnerabilities, auditing third-party skills/MCPs/agent configs before installing, evaluating shell commands before running them, or generating secure design questions for new features. Provides `rafter run` (remote SAST + SCA, needs RAFTER_API_KEY), `rafter secrets` (offline secrets-only), `rafter agent exec --dry-run` (command-risk classification), and `rafter skill review`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafter](https://clawhub.ai/user/rafter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Rafter to scan code and repositories for vulnerabilities or secrets, review third-party skills and agent configurations, assess shell commands before execution, and get security design guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports credential access and transmission, command execution risks, and persistent configuration changes beyond the stated purpose. It marks the skill suspicious and notes incomplete scan coverage.

Mitigation: Follow the assessment's guidance to consider avoiding installation. If proceeding, review the source and limit credential access, outbound network access, and persistent configuration changes to actions you have explicitly reviewed.

## Reference(s):

- [Rafter website](https://rafter.so)
- [Rafter Security on ClawHub](https://clawhub.ai/rafter/skills/rafter-security)
- [Publisher profile: rafter](https://clawhub.ai/user/rafter)

## Skill Output:

**Output Type(s):** [Security analysis, Markdown reports, Shell commands, Configuration instructions, Security guidance]

**Output Format:** [Markdown guidance and audit reports with inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI behavior depends on the installed `rafter` binary. Remote scanning requires RAFTER_API_KEY; secrets-only scanning is described as offline.]

## Skill Version(s):

0.12.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
