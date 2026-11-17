## Description:

A coding-agent skill for tracing Python execution, diagnosing and repairing code, checking behavioral changes, automating AST edits, replaying selected I/O, synthesizing implementations from doctests, and updating affected callers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntrieuvi97](https://clawhub.ai/user/ntrieuvi97)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill with coding agents to inspect Python behavior, diagnose failures, propose or apply code changes, and update related callers across a repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chronos cassettes store unredacted call arguments and results, which may include credentials, tokens, or personal data.

Mitigation: Avoid production secrets and sensitive environments; add .thauthi/cassettes/ to .gitignore and do not commit or upload cassettes.

Risk: Chronos replays only intercepted boundaries, so other I/O and side effects may still run for real.

Mitigation: Do not replay functions with real side effects against production systems.

Risk: The security scan found no reported issues in inspected Markdown, but missing local references left the review incomplete.

Mitigation: Review referenced files before installing the skill.

## Reference(s):

- [Thauthi on ClawHub](https://clawhub.ai/ntrieuvi97/skills/thauthi)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Code and file edits, shell commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May apply code changes when invoked with apply options.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
