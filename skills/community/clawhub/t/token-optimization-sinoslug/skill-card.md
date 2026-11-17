## Description:

Reduces unnecessary token usage with a current-state workflow for concise replies, trimmed logs, filtered tool outputs, and scripted token statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinoslug](https://clawhub.ai/user/sinoslug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to standardize current token-saving behavior across assistants while preserving answer quality. It is intended for requests to reduce prompt or context bloat, trim log and tool-output usage, and explain the active optimization workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow references an unbundled local token-show.py script path.

Mitigation: Verify the local script path and script contents before using the token statistics step, or use a release that bundles and verifies the script.

Risk: The workflow can write behavior changes into persistent memory files.

Mitigation: Require explicit user approval before updating memory files and review the proposed changes before persistence.

Risk: Aggressive token reduction can omit useful context or evidence.

Mitigation: Keep concise answers focused on the conclusion plus necessary evidence, and expand when the task requires detail or traceability.

## Reference(s):

- [Current Token Optimization Specification](references/current-spec.md)
- [ClawHub Skill Page](https://clawhub.ai/sinoslug/skills/token-optimization-sinoslug)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise prose and inline shell commands when token statistics are requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid redundant background, avoid full raw logs or large JSON dumps, and cite references/current-spec.md when explaining the optimization plan.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
