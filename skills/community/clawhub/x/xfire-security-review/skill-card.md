## Description:

Multi-agent adversarial security review: three AI agents independently review code and debate findings so only supported vulnerabilities appear in the final report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[har1sh-k](https://clawhub.ai/user/har1sh-k)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to review pull requests, diffs, and repositories for security vulnerabilities and receive reports in human-readable or CI-friendly formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send repository code to selected external AI providers during analysis.

Mitigation: Use it only for repositories where sharing code with the configured providers is acceptable.

Risk: API keys and GitHub tokens are required for common workflows.

Mitigation: Use narrowly scoped, preferably short-lived credentials and avoid exposing unnecessary provider keys.

Risk: Cache, debug, or result files may contain sensitive code or findings.

Mitigation: Keep generated cache, debug, and result files out of commits and CI artifacts.

Risk: Installing the referenced package can execute third-party code in the user's environment.

Mitigation: Pin or verify the xfire package version before installing and running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/har1sh-k/skills/xfire-security-review)
- [xfire project homepage](https://github.com/Har1sh-k/xfire)

## Skill Output:

**Output Type(s):** [text, markdown, json, sarif, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, or SARIF reports with optional shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can post pull request comments, emit CI-oriented SARIF, and write debug traces or cached context when configured.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
