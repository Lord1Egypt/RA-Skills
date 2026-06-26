## Description: <br>
Build payment flows for Pump Tokenized Agents using @pump-fun/agent-payments-sdk. Use when accepting payments, building accept-payment transactions, integrating Solana wallets, or verifying that a user has paid an invoice on-chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sushant-baton](https://clawhub.ai/user/sushant-baton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building Pump Tokenized Agent services use this skill to create Solana wallet payment flows, construct unsigned payment transactions for user signing, and verify invoices on-chain before delivering paid functionality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may approve a wallet transaction with the wrong amount, currency, network, or payment context. <br>
Mitigation: Show the intended payment details before wallet approval and rely on user-signed transactions; never request or handle private keys or seed phrases. <br>
Risk: Untrusted or mismatched npm packages and RPC providers can undermine payment flow reliability. <br>
Mitigation: Verify package names and versions before installation, align Solana dependency versions with the payment SDK, and choose a trusted RPC provider. <br>
Risk: A client may report payment before the invoice is actually confirmed. <br>
Mitigation: Verify each invoice server-side with the same amount, memo, start time, end time, currency, and user wallet before delivering the paid service. <br>


## Reference(s): <br>
- [Scenario Tests](references/SCENARIOS.md) <br>
- [Wallet Integration (Frontend)](references/WALLET_INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, TSX, environment configuration, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes user-signed wallet transactions, server-side payment verification, trusted RPC selection, and dependency version compatibility.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
