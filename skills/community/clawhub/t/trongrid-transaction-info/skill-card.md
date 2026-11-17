## Description:

Query and decode TRON transactions for status, confirmation, participants, resource costs, internal transactions, event logs, and failure analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greason](https://clawhub.ai/user/greason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and support teams use this skill to investigate TRON transaction hashes, verify success and finality, decode contract actions and logs, and diagnose failed or pending transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction hashes and related public-chain queries are sent to TronGrid MCP.

Mitigation: Use public transaction data only, and do not provide wallet seed phrases, private keys, or other secrets.

Risk: Transaction interpretation can be incomplete when receipt data is pending or a contract ABI is unavailable.

Mitigation: Label pending results clearly, show raw data when decoding is unavailable, and avoid presenting unresolved analysis as final.

## Reference(s):

- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)
- [Check transfer status example](artifact/examples/check-transfer-status.md)
- [Decode a contract call example](artifact/examples/decode-contract-call.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown transaction report with decoded fields, tables, and failure analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public-chain lookup workflow using transaction hashes and related TRON transaction data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
