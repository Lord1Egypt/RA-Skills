## Description:

Execute limit orders on Polymarket markets by specifying market slug, outcome, price, and order size via a Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zakkycrypt01](https://clawhub.ai/user/zakkycrypt01)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to submit Polymarket limit orders from an agent workflow after providing a market slug, outcome direction, price, and size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent live wallet-backed Polymarket trading authority.

Mitigation: Use a minimally funded dedicated wallet and review each requested trade before execution.

Risk: Security evidence reports weak validation and an unsafe shell command wrapper.

Mitigation: Avoid untrusted market_slug or direction inputs until shell invocation, local order validation, explicit confirmation, and order-size limits are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zakkycrypt01/skills/zakkycrypt01-polymarket-trader)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls]

**Output Format:** [Plain text trade status and Python dictionary-style response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place live wallet-backed Polymarket limit orders through the Polymarket CLOB API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
