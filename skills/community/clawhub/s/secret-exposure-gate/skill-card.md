## Description:

Checks a release directory for possible secrets, tokens, private URLs, certificate fragments, and credential files before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and release engineers use this skill as a pre-publication review gate to scan local directories for likely credential exposure and produce remediation-oriented review notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could treat the skill as a complete secret scanner even though server security evidence says its gate is under-scoped.

Mitigation: Use it as a lightweight preflight review and run a dedicated secret-scanning tool before publishing important repositories or packages.

Risk: Scan results may miss sensitive files or patterns outside the bundled heuristic coverage.

Mitigation: Review high-risk files manually and keep repository or package release checks in place before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/secret-exposure-gate)
- [README](artifact/README.md)
- [Specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)
- [Smoke test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review reports with optional JSON output from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize scan overview, suspected secrets, high-risk files, false-positive notes, remediation advice, and recheck guidance without displaying full secret values.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
