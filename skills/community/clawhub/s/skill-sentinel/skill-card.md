## Description:

Scan OpenClaw skill directories for high-signal security risks such as download-and-execute chains, obfuscated execution, and suspicious callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to statically scan OpenClaw skill directories before installation, publishing, or CI release gates. It helps surface risky shell patterns, suspicious callbacks, obfuscated execution, and social-engineering content without executing the target skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner output can include short snippets from text-like files under the target path.

Mitigation: Point the scanner only at intended skill directories and avoid broad private folders unless that disclosure is acceptable.

Risk: The fixture directory includes intentionally unsafe sample commands for detection tests.

Mitigation: Do not execute sample files under fixtures/malicious-skill; use them only as static scanner test inputs.

Risk: The rule set is narrow and may not identify every security issue in a skill.

Mitigation: Treat scanner results as a high-signal first pass and keep human review or additional security checks in the release process.

## Reference(s):

- [Skill Sentinel on ClawHub](https://clawhub.ai/mike007jd/skills/skill-sentinel)

## Skill Output:

**Output Type(s):** [Text, JSON, SARIF, Shell commands, Guidance]

**Output Format:** [Plain text, JSON, or SARIF scanner results with risk levels and findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include short matching snippets from scanned text-like files and CI-oriented exit codes when fail-on thresholds are configured.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
