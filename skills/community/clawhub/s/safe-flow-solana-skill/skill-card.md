## Description:

Use when running SafeFlow against a deployed Solana program. Trigger for tasks such as generating an agent keypair, asking the owner to fund gas and create wallet/session via the web dashboard, saving walletPda/sessionPda for autonomous payments, and executing rate-limited payments on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwangzil](https://clawhub.ai/user/fwangzil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure an AI agent for SafeFlow-controlled Solana payments, hand off wallet/session setup to the owner, and execute or query rate-limited payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment and wallet inputs may be handled unsafely, creating risk of local code execution or unintended transfers.

Mitigation: Replace inline node -e and ts-node -e usage with checked-in scripts that parse arguments safely and validate recipient and amount before loading the keypair.

Risk: The local agent keypair may be exposed or misused if stored without strong controls.

Mitigation: Protect the keypair with restrictive file permissions or a safer signer, and add dry-run, confirmation, and spending-policy controls before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fwangzil/skills/safe-flow-solana-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may create a local Solana keypair and .safeflow/config.json when run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
