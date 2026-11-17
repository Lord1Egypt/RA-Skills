## Description:

Security-first skill vetting for AI agents that checks external skills for red flags, dangerous patterns, permission scope, and suspicious code before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misscrx](https://clawhub.ai/user/misscrx)

### License/Terms of Use:


## Use Case:

Developers, agent operators, and external users use this skill to vet third-party skills before installation. It helps review source files, scripts, and documented behavior for malicious patterns, sensitive-file access, risky network use, and boundary-zone concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scanner can follow symlinks out of the scanned skill directory and may expose unrelated local file snippets in reports.

Mitigation: Run scans in a sandbox or on a copied skill tree, and avoid scanning untrusted archives that preserve symlinks unless path boundaries are enforced.

Risk: The server security verdict is suspicious, so automated use may create review or disclosure risk.

Mitigation: Review the skill before installing or using it in automation, and treat scanner reports as advisory until findings are manually confirmed.

## Reference(s):

- [Security Pattern Reference](artifact/references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown security review with shell command examples and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pass, caution, or block verdicts with critical, warning, and info findings.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
