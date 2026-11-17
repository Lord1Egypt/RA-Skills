## Description:

人民币大写转换工具，将数字金额转换为人民币大写金额字符串。

This skill is ready for commercial/non-commercial use.

## Publisher:

[q342998378](https://clawhub.ai/user/q342998378)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert numeric amount strings into uppercase Chinese RMB financial text for invoices, receipts, ledgers, or other Chinese-language money workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The interface and output are specific to Chinese RMB uppercase amount formatting.

Mitigation: Use this skill only for RMB workflows and verify the generated amount text against the target financial document requirements.

Risk: Decimal input is converted to cents before formatting, so callers should avoid passing ambiguous or over-precise amount strings.

Mitigation: Normalize amounts to the expected currency precision before calling the tool and review outputs for financial records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/q342998378/skills/rmb-upper-skill)
- [Publisher profile](https://clawhub.ai/user/q342998378)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object containing a success flag and either an RMB uppercase result string or an error string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input is a single numeric amount string; output text is Chinese/RMB-specific and may include a negative prefix.]

## Skill Version(s):

1.0.0 (source: manifest.yaml and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
