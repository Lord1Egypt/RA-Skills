## Description: <br>
Revolut Business API CLI for accounts, balances, transactions, counterparties, payments, FX exchange, CSV export, and OAuth token refresh for business accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianhaberl](https://clawhub.ai/user/christianhaberl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and business operators use this skill to configure and run a Revolut Business CLI for account review, transaction export, counterparty lookup, payments, FX exchange, and internal transfers. It is intended for Revolut Business accounts, not Revolut Personal accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent high-impact banking authority for payments, FX exchange, transfers, and transaction export. <br>
Mitigation: Install only when agent-accessible Revolut Business operations are deliberate, avoid autonomous use for payments, FX, or transfers, and review destination, amount, currency, and export path before running commands. <br>
Risk: Refreshable Revolut credentials and private key material are stored locally under ~/.clawdbot/revolut/. <br>
Mitigation: Protect the credential directory, restrict Revolut API permissions and IP allowlists, and never share private keys, tokens, or client assertion JWTs. <br>
Risk: Some money-moving actions can execute without an additional confirmation step. <br>
Mitigation: Prefer draft payments where possible and require human review before direct payment, FX, or transfer execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/christianhaberl/revolut-business) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, CSV] <br>
**Output Format:** [Markdown guidance with shell commands, plus CLI text, JSON, or CSV output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and local Revolut Business OAuth credentials under ~/.clawdbot/revolut/.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
