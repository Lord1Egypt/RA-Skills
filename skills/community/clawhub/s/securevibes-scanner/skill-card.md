## Description:

Run AI-powered application security scans on codebases, including vulnerability scanning, threat modeling, code review, incremental scans, and optional DAST.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anshumanbh](https://clawhub.ai/user/anshumanbh)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to run SecureVibes scans, generate threat models, review code for vulnerabilities, summarize findings, and configure recurring incremental scans for authorized repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run security scans and optional DAST against codebases or URLs.

Mitigation: Use it only for repositories and targets you own or are explicitly authorized to test.

Risk: Incremental monitoring can create recurring background scans and persistent .securevibes artifacts.

Mitigation: Enable scheduled monitoring only after reviewing retention, access, and operational monitoring for the target repository.

Risk: The scanner depends on networked and credential-backed SecureVibes and Anthropic tooling.

Mitigation: Install the CLI with pipx or uv, pin and verify the installed version, and protect API keys or OAuth sessions used by the scanning process.

Risk: Security evidence identifies a Git argument-handling flaw around remote and branch inputs.

Mitigation: Do not pass untrusted values to --remote or --branch; use known repository remotes and branch names controlled by the operator.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anshumanbh/skills/securevibes-scanner)
- [SecureVibes Website](https://securevibes.ai)
- [SecureVibes PyPI Project](https://pypi.org/project/securevibes/)
- [SecureVibes GitHub Project](https://github.com/anshumanbh/securevibes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and references to generated SecureVibes Markdown and JSON artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan results are written under the target repository's .securevibes directory when the SecureVibes CLI runs successfully.]

## Skill Version(s):

0.5.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
