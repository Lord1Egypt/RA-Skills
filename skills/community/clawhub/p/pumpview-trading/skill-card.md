## Description:

Connects an agent to PumpView for locally signed Solana swaps, confirmed receipts, trading volume, and live trade data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grinchdev](https://clawhub.ai/user/grinchdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and traders using PumpView can prepare and submit user-authorized Solana swaps with local wallet signing, inspect confirmed trades and volume, and access paid live trade data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed swap submissions and invoice payments can spend funds or incur fees.

Mitigation: Review the wallet, trade amounts, slippage, destination, fees, tips, and invoice before authorized local signing; do not infer purchase approval from a data request.

Risk: API keys, wallet signatures, signed transaction bytes, invoice IDs, and trade details are sensitive.

Mitigation: Use the runtime secret store and authorized wallet integration; keep sensitive values out of prompts, logs, and repositories.

Risk: Retries after an uncertain response can duplicate a trade or payment.

Mitigation: Recover using the existing request, swap, or invoice ID and check its status before authorizing another transaction.

## Reference(s):

- [PumpView integration reference](references/workflow.md)
- [PumpView API schema](https://api.pumpview.fun/v1/openapi.json)
- [PumpView developer quickstart](https://pumpview.fun/developers/quickstart.md)
- [ClawHub skill listing](https://clawhub.ai/grinchdev/skills/pumpview-trading)

## Skill Output:

**Output Type(s):** [Text, Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with code or API examples as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Swap and payment actions require an authorized local wallet; live trade data requires a paid package.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
