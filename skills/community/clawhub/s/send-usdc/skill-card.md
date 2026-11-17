## Description:

Send USDC to an Ethereum address or ENS name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrag](https://clawhub.ai/user/0xrag)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to prepare wallet-status, balance, and USDC transfer commands for paying, tipping, donating, or otherwise sending funds to an Ethereum address or ENS name on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke a mutable external wallet package that may move funds.

Mitigation: Use a reviewed, version-pinned `awal` package or run the command in a restricted execution environment before allowing transfers.

Risk: Incorrect recipient, ENS resolution, amount, or chain selection could send funds to the wrong destination.

Mitigation: Verify the recipient, resolved ENS address, transfer amount, wallet authentication, balance, and Base chain before executing any send command.

Risk: The artifact does not provide enough built-in transfer confirmation guidance.

Mitigation: Require an explicit user confirmation step for the final amount, recipient, resolved address, and chain before running the transfer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xrag/skills/send-usdc)
- [Publisher profile](https://clawhub.ai/user/0xrag)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may transfer funds; users should verify wallet authentication, recipient, resolved ENS address, amount, and chain before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
