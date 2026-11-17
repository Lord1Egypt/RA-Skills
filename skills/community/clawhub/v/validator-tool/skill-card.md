## Description:

Validate common data values such as JSON, email addresses, URLs, IP addresses, phone numbers, UUIDs, hex strings, dates, and credit-card-like numbers with a local Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to run quick local validation checks for common input formats while building or testing data-processing workflows. Review the implemented script before relying on documented schema, batch, strict, or JSON-output behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release documentation overstates implemented validation features, including schema, batch, strict, and JSON-output behavior.

Mitigation: Verify behavior against the bundled script before using the skill in automation or CI workflows.

Risk: The script includes undocumented credit-card validation that may expose entered numbers through shell history, process arguments, or logs.

Mitigation: Do not pass real payment-card data or secrets to the script unless input handling and output redaction are changed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/validator-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text command-line validation results with optional guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local script output depends on the selected validator and input value.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
