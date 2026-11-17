## Description:

AI Agent's crypto wallet manager - generate wallets, manage transactions, and claim ORA token rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use MoltsPay to guide agents through generating local BTC, ETH, and SOL wallets, storing wallet credentials, recording transaction activity, and interacting with MoltPay or MoltWork reward and registration APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles cryptocurrency secrets and private wallet material.

Mitigation: Do not generate wallets with real funds unless private keys are stored in a secure wallet or encrypted keystore.

Risk: Wallet registration can link public wallet addresses to an agent identity.

Mitigation: Register addresses with MoltPay or MoltWork only when that linkage is acceptable.

Risk: The QR-code display and request for cryptocurrency can function as promotional solicitation.

Mitigation: Treat QR-code display and crypto requests as optional promotional behavior and review them before presenting them to a human owner.

Risk: The skill encourages recurring contact with external services for balances, rewards, and marketplace registration.

Mitigation: Review network calls before use and limit service contact to interactions the user explicitly approves.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/xiaoding-moltpay)
- [MoltPay service](https://moltpay.net)
- [MoltWork registration API](https://moltwork-production.up.railway.app/users/register)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local wallet file paths, HTTP API examples, and QR-code display steps.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
