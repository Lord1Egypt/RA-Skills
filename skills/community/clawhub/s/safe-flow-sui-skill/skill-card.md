## Description: <br>
Use when running SafeFlow against the shared Sui package with owner-assisted provisioning. Trigger for tasks such as creating an agent execution address with local Sui CLI, asking owner to fund gas and finish web-side wallet/session setup, saving walletId/sessionCapId for autonomous payments, syncing package id to SQL, and running Publish API plus Walrus end-to-end tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FWangZil](https://clawhub.ai/user/FWangZil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to coordinate owner-assisted SafeFlow setup on Sui, persist wallet and session capability identifiers, run controlled payment tests, and exercise Publish API plus Walrus end-to-end flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute real Sui payment test flows and stores delegated wallet/session capability data. <br>
Mitigation: Use testnet or tightly capped funds, verify recipient addresses and payment amounts before execution, keep generated .safeflow files private and out of version control, and rotate or revoke session capabilities after testing. <br>
Risk: The Publish API and Walrus end-to-end flow depends on surrounding agent scripts and package dependencies. <br>
Mitigation: Inspect the surrounding agent_scripts and package dependencies before running the end-to-end flow, and use explicit operator-provided API URLs and credentials. <br>


## Reference(s): <br>
- [Owner-Handoff Flow](references/owner-handoff-flow.md) <br>
- [Publish API Test Flow](references/publish-api-test-flow.md) <br>
- [Package ID SQL Sync](references/sql-sync.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Sui CLI install guide](https://docs.sui.io/guides/developer/getting-started/sui-install) <br>
- [Sui CLI reference](https://docs.sui.io/references/cli) <br>
- [SafeFlow producer endpoint](https://producer.safeflow.space) <br>
- [SafeFlow dashboard](https://dash.safeflow.space) <br>
- [Walrus testnet publisher](https://publisher.walrus-testnet.walrus.space) <br>
- [Walrus testnet aggregator](https://aggregator.walrus-testnet.walrus.space) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces owner handoff JSON, SafeFlow runtime configuration, environment exports, payment test results, SQL package-id sync entries, and Publish API status output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
