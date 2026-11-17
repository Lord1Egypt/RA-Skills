## Description:

Reviews shell commands, scripts, or directories before execution to identify dangerous patterns such as pipe-to-shell, destructive deletion, risky redirection, and obfuscated execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and release engineers use this skill to review proposed shell commands or scripts before execution and produce audit-friendly findings, safer alternatives, manual review points, and final recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review verdict is suspicious because the implementation is narrower than advertised and has file-boundary and output-handling risks.

Mitigation: Treat results as lightweight advisory review, scan trusted directories, and review findings before using them as a command-safety gate.

Risk: The output path can affect important files if users point --output at sensitive locations.

Mitigation: Prefer dry-run or stdout use, and avoid writing to important paths unless overwrite behavior is explicitly controlled.

Risk: Directory scans may include untrusted filesystem content such as symlinks.

Mitigation: Use the skill on trusted directories and inspect inputs before scanning broad or shared paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/run-command-safety-check)
- [README](artifact/README.md)
- [Specification](artifact/resources/spec.json)
- [Smoke test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local input only; supports dry-run/stdout use and does not require third-party Python packages.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
