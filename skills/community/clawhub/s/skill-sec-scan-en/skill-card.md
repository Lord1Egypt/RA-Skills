## Description:

Skill Security Scanner scans ClawHub, GitHub, and local skill packages for security risks across JavaScript, TypeScript, Python, and shell files and reports categorized findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to triage skill packages before installation or release. It helps identify suspicious patterns, summarize affected files, and produce reports for follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can run unintended shell commands and may handle remote archives unsafely.

Mitigation: Run it only in a disposable or sandboxed environment and avoid scanning untrusted remote URLs with this version.

Risk: Attacker-controlled target strings may affect the Node or shell entrypoints.

Mitigation: Do not pass untrusted target strings directly to the scanner; review and constrain targets before execution.

Risk: The scanner may incorrectly mark unsafe skills as safe.

Mitigation: Treat scores as triage signals and perform independent code and security review before installing or approving a scanned skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/torchesfrms/skills/skill-sec-scan-en)
- [Detection rules reference](references/rules.md)
- [Dangerous commands reference](references/dangerous-commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown security reports, optional JSON or JSONL issue records, and shell commands for scans and whitelist operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include scanned file counts, score, risk level, category, rule, severity, affected file, and conclusion; static scan results require independent review.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
