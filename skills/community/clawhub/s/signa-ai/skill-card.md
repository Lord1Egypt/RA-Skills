## Description:

Send payments, messages, escrow, and verifiable outputs between AI agents on the Signum blockchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[folkerds13](https://clawhub.ai/user/folkerds13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to let OpenClaw agents send Signum payments, create and release escrow-backed tasks, publish on-chain messages, check wallet balances, and stamp or verify AI outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real Signum blockchain payments and escrow actions.

Mitigation: Use an isolated low-balance wallet, review each transaction command before execution, and verify transaction IDs on the Signum explorer.

Risk: The setup flow can store a wallet passphrase locally for autonomous operation.

Mitigation: Avoid using a valuable wallet passphrase, restrict file access to the worker configuration, and rotate credentials if the machine or skill workspace is exposed.

Risk: The listener can run as an always-on daemon and process escrow events with broad agent authority.

Mitigation: Disable the launchd daemon and auto-release behavior unless autonomous operation is required, and prefer manual review for high-value or unfamiliar tasks.

Risk: Setup changes OpenClaw execution approvals for the skill environment.

Mitigation: Review approval changes before installation and remove broad approvals before using the skill with real funds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/folkerds13/skills/signa-ai)
- [SignaAI Website](https://signaai.io)
- [SignaAI PyPI Package](https://pypi.org/project/signaai/)
- [Signum Network](https://signum.network)
- [Signum Explorer](https://explorer.signum.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and transaction receipt text; bundled scripts produce CLI text and on-chain transaction identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include wallet addresses, escrow IDs, proof hashes, transaction IDs, and links to public Signum records.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
