## Description: <br>
Streams real-time Solana SPL stablecoin transfers for USDT and USDC over the Bitquery GraphQL WebSocket API, excluding swap transactions and returning transfer, block, transaction, fee, and program-method details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[divyn](https://clawhub.ai/user/divyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and treasury analysts use this skill to monitor Solana USDC and USDT payment activity in real time, build dashboards or alerts, and reconcile transfers by sender, receiver, amount, signature, slot, and fees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Bitquery API token is passed in the WebSocket URL and could be exposed through logs, shell history, or proxy traces. <br>
Mitigation: Use a dedicated Bitquery API key from an environment variable, avoid printing the full WebSocket URL, and rotate the key if exposure is suspected. <br>
Risk: The stream can continue running indefinitely and consume local or API resources. <br>
Mitigation: Run in a virtual environment or container when practical, and use the optional timeout for bounded monitoring sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/divyn/solana-stablecoin-payments-tracking) <br>
- [Solana stablecoin transfers GraphQL reference](references/graphql-fields.md) <br>
- [Bitquery documentation](https://docs.bitquery.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and bash snippets; the streaming script emits formatted text transfer summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and may run as a long-lived WebSocket stream unless the optional timeout is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
