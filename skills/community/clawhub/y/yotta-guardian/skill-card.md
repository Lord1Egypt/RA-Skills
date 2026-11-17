## Description:

A cross-agent guard that evaluates tool calls for dangerous commands, sensitive-path writes, and system configuration changes, returning a verdict and audit details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to review agent tool calls for high-risk commands, sensitive-path writes, and system configuration changes, then inspect rule hits and audit records before deciding whether to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports confirmed detection bypasses, so some risky calls may pass the guard.

Mitigation: Keep independent host permissions and approval checks in force; do not rely on this guard as the sole enforcement layer.

Risk: A configured external checker may run even when --no-verifier is supplied.

Mitigation: Remove verifier settings from configuration instead of relying on --no-verifier.

Risk: Exit code 1 can represent a strict-policy denial.

Mitigation: Check the JSON allowed field and selected policy before interpreting a result.

Risk: Audit logs may contain command excerpts, and installation location affects which directory is modified.

Mitigation: Choose the intended installation directory and protect audit logs.

## Reference(s):

- [Rule reference](references/rules.md)
- [Policy and exit-code reference](references/policies.md)
- [Intent verifier protocol](references/intent-verifier.md)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-guardian)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Audit logs, Guidance]

**Output Format:** [JSON verdicts, JSONL audit records, and text or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts include matched rules and reasons.]

## Skill Version(s):

0.1.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
