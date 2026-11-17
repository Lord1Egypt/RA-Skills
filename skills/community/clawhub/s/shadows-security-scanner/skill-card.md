## Description:

7-phase security audit pipeline: reconnaissance, dependency scan, application tests, API security, hardening check, OWASP verification, and report generation for use before production deployments or after incidents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nakedoshadow](https://clawhub.ai/user/nakedoshadow)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to run a structured repository security audit, inspect dependencies and application risks, verify hardening, check for exposed secrets, and produce an actionable Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan reads source files and git history, and reports may display discovered secret-like values.

Mitigation: Run reports in a private terminal and redact sensitive findings before sharing output.

Risk: Dependency audit tools and the optional HTTP header check can make outbound network requests.

Mitigation: Run those checks only where network access is approved, and provide a target URL only for systems you intend to check.

Risk: Pattern-based checks can miss vulnerabilities or flag harmless examples.

Mitigation: Treat results as review input and confirm findings with focused manual review or dedicated SAST, SCA, DAST, and secrets-scanning tools.

## Reference(s):

- [Shadows Security Scanner on ClawHub](https://clawhub.ai/nakedoshadow/skills/shadows-security-scanner)
- [NakedoShadow publisher profile](https://clawhub.ai/user/nakedoshadow)
- [ClawHub metadata homepage](https://clawhub.ai/NakedoShadow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown security audit report with command output summaries, findings, vulnerability tables, hardening status, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit flow; dependency scanners and optional HTTP header checks may make outbound requests when those phases are run.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
