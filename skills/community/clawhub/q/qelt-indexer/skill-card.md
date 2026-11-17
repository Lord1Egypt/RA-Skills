## Description:

Qelt Indexer lets agents query indexed QELT blockchain data via the Mainnet Indexer REST API, including blocks, transactions, address history, token balances, and sync health, without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prqelt](https://clawhub.ai/user/prqelt)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to look up QELT blocks, transactions, wallet activity, token balances, and indexer sync state through documented QELT indexer endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QELT block, transaction, and wallet lookup queries are sent to the documented QELT indexer domains.

Mitigation: Use the skill only when the user is comfortable sending those lookup queries to the listed QELT indexer services.

Risk: Indexer lag can make recently reported blockchain data stale.

Mitigation: Check the documented health endpoint before reporting latest data and warn when the lag value indicates stale indexing.

Risk: Rate limits can interrupt repeated or broad lookup workflows.

Mitigation: Keep requests bounded with documented pagination and apply backoff when rate-limit errors occur.

Risk: The bundled API reference includes contract-verification endpoints outside the primary read-only lookup workflows.

Mitigation: Keep use to documented read-only lookup workflows unless the contract-verification endpoints receive separate review.

## Reference(s):

- [QELT Mainnet Indexer](https://mnindexer.qelt.ai)
- [QELT Testnet Indexer](https://tnindexer.qelt.ai)
- [QELT Indexer API Quick Reference](references/api-endpoints.md)
- [ClawHub skill page](https://clawhub.ai/prqelt/skills/qelt-indexer)
- [Publisher profile](https://clawhub.ai/user/prqelt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and summarized API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be grounded in live API responses and should note sync lag when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
