## Description:

Detect API keys, tokens, and credentials in code with 50+ patterns, entropy analysis, and multiple report formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, maintainers, and CI pipeline owners use this skill to scan project files for leaked credentials, list detection patterns, filter by severity, and emit JSON or SARIF reports for review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation documentation uses an unpinned remote Python download.

Mitigation: Prefer the bundled reviewed artifact, or pin and verify any remote download before execution.

Risk: Generated reports can reveal raw secrets in context lines.

Mitigation: Do not publish CI logs, JSON, or SARIF output from this version until context redaction is confirmed; rotate any real credentials exposed in reports.

Risk: Broad scans or auxiliary verification on untrusted packages can expose sensitive files or execute checks outside the intended target.

Mitigation: Limit scans to intended project paths and run auxiliary package verification only in a sandbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/secret-scanner)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, SARIF, shell commands, guidance]

**Output Format:** [CLI text reports, JSON arrays, SARIF 2.1.0 files, and exit codes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scans local paths; can filter by severity, disable entropy detection, and respect .gitignore.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
