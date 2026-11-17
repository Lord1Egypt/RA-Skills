## Description:

Scans an authorized project directory for common credential patterns and reports masked findings for remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check directories they are authorized to inspect for common leaked credentials before committing code and to prepare a rotation-focused remediation summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning directories without permission may expose sensitive project information.

Mitigation: Scan only directories the user owns or is authorized to inspect.

Risk: A reported credential may remain usable or exposed in commit history.

Mitigation: Treat findings as sensitive and rotate or revoke credentials rather than relying on deletion alone.

Risk: Limited patterns and skipped files can leave leaked credentials undetected.

Mitigation: Review skipped-file notes and do not treat zero findings as proof that the directory is secret-free.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nenadzivotic/skills/secret-leak-scan-lite)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON scan report and human-readable remediation summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include credential type, file, line, and masked fingerprint; raw secret values are not reported.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
