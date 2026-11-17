## Description:

Use this skill when the user wants to put a Solana wallet on trial, identify the action most likely to cause regret tomorrow, return a verdict, and only then preview execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a Solana wallet use this skill to request a pre-trade court-style review that identifies one likely regrettable action, returns one verdict, and previews execution only after the verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a Solana wallet address to an external Court API endpoint.

Mitigation: Review the skill before installing and use it only when users accept sending the wallet address to the listed endpoint.

Risk: The skill can rely on an external API's transaction plan before wallet execution.

Mitigation: Before signing or broadcasting, require the wallet-connected client to decode the full transaction, verify programs, accounts, amounts, fees, slippage, and recipients, and show a trusted approval screen generated from the decoded transaction.

## Reference(s):

- [Wallet Twin Court API](https://todays-orders.vercel.app/api/todays-orders)
- [ClawHub Skill Page](https://clawhub.ai/richard7463/skills/wallet-twin-court)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown with fixed courtroom sections and inline shell commands when showing the API call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses wallet, market, quote, route, and receipt data from the court workflow; labels execution previews clearly until execution is confirmed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
