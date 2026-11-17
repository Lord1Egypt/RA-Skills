## Description:

Fertilizer ordering and customer or supplier management skill that uses the xyfcli CLI to place orders, query product, price, inventory, customer, and dealer information, and parse order images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayafans](https://clawhub.ai/user/mayafans)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations users use this skill to collect and validate fertilizer order details, query customer, product, inventory, and address data, and submit confirmed order drafts through xyfcli. It can also guide image-based order extraction before user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit order drafts and modify customer addresses.

Mitigation: Review before production use, require explicit user confirmation for orders and address changes, and use a least-privilege or test token during validation.

Risk: Authentication tokens may be exposed in logs, transcripts, or configuration output.

Mitigation: Avoid running config show --json, limit token visibility, and rotate any token that appears in logs or transcripts.

Risk: Unsafe address reuse or insufficient validation could create orders for the wrong customer, product, inventory level, or payment mode.

Mitigation: Confirm backend enforcement of dealer product authorization, inventory, address ownership, and payment-mode validation before trusting the skill for real orders.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mayafans/skills/xyfcli-order-guide)
- [XYFCLI Command Quick Reference](references/cli_quickref_chinese.md)
- [Interactive Ordering Workflow](references/workflow_guide.md)
- [Image Processing Reference](references/image_processing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with xyfcli shell commands and human-readable or JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the xyfcli binary and configured API base URL and bearer token.]

## Skill Version(s):

1.4.4 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
