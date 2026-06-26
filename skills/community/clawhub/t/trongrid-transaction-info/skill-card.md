## Description: <br>
Query and decode TRON transactions including status, confirmation, sender/receiver, resource costs, internal transactions, event logs, and failure analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greason](https://clawhub.ai/user/greason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and blockchain operations teams use this skill to inspect TRON transaction hashes, confirm finality, decode transfers or smart contract calls, and diagnose failed transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction hashes and addresses queried through the TronGrid MCP provider may be visible to that provider. <br>
Mitigation: Use the skill only when TronGrid is an acceptable provider for the investigation, and avoid querying sensitive wallet activity unless public-chain exposure is acceptable. <br>
Risk: Pending transactions, missing receipts, unavailable ABIs, or contract reverts can produce incomplete or uncertain decoded reports. <br>
Mitigation: Report uncertainty clearly, check pending and solidity-node data where available, and show raw method data when ABI-based decoding is unavailable. <br>


## Reference(s): <br>
- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api) <br>
- [ClawHub skill page](https://clawhub.ai/greason/trongrid-transaction-info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown transaction report with decoded fields, status, resources, events, and failure analysis when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TronGrid MCP transaction and block lookup tools; queried transaction hashes and addresses may be visible to the provider.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
