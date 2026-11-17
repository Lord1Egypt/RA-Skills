## Description:

TuleBank helps an agent check wallet balances, send ARS to CVU or ALIAS destinations, swap USDC and wARS, manage beneficiaries, and move funds through ARS off-ramp and on-ramp flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aromeoes](https://clawhub.ai/user/aromeoes)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate the TuleBank CLI for wallet setup, balance checks, beneficiary management, ARS bank transfers, token swaps, and ARS on-ramp or off-ramp workflows. It is intended for conversational assistance around real wallet, KYC, beneficiary, and transaction actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real financial transfers and swaps through wallet, beneficiary, KYC, and transaction workflows.

Mitigation: Require explicit human confirmation of amount, recipient, destination identifier, token, and action before execution, and prefer manual send mode for fund movement.

Risk: Conversational recipient names or descriptions can resolve to the wrong beneficiary.

Mitigation: Search beneficiaries first, ask the user to clarify multiple matches, and confirm exact CVU or ALIAS and holder details before sending.

Risk: Token swaps and ARS-denominated sends can produce unintended amounts if an agent manually converts values.

Mitigation: Use the CLI amount semantics directly, avoid manual USDC conversion for ARS amounts, and run transaction history after sends, swaps, or on-ramp creation.

## Reference(s):

- [ClawHub Tulebank Skill Page](https://clawhub.ai/aromeoes/skills/tulebank)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and human-readable summaries of JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the tulebank CLI binary and human confirmation for fund movement.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
