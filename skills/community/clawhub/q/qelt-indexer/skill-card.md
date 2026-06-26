## Description: <br>
Query QELT blockchain data--blocks, transactions, address history, ERC-20 token balances, and indexer sync status--via the Mainnet Indexer REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PRQELT](https://clawhub.ai/user/PRQELT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to query public QELT blockchain blocks, transactions, wallet history, token balances, and indexer sync status without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QELT lookup targets such as wallet addresses and transaction hashes are sent to the qelt.ai indexer and may be logged by that external service. <br>
Mitigation: Query only public blockchain data that the user is comfortable sending to qelt.ai, and avoid using the skill for sensitive correlation workflows. <br>
Risk: Contract-verification POST endpoints can submit source or verification data to qelt.ai. <br>
Mitigation: Use POST verification endpoints only when the user explicitly intends to submit that data; use the read-only GET lookup endpoints for normal blockchain queries. <br>


## Reference(s): <br>
- [QELT Mainnet Indexer](https://mnindexer.qelt.ai) <br>
- [QELT Indexer API Quick Reference](references/api-endpoints.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/PRQELT/qelt-indexer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live public QELT blockchain data returned by qelt.ai indexer endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
