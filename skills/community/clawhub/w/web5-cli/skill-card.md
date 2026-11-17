## Description:

Supports Web5 CLI work for decentralized identity, CKB wallet operations, DID management, PDS data operations, account creation, posting, and profile updates.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[rink1969](https://clawhub.ai/user/rink1969)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to plan and run Web5 CLI workflows for DID, wallet, and PDS account tasks. The included helper scripts cover account creation and destruction workflows for validation environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallets, private keys, bearer tokens, and irreversible account or DID destruction.

Mitigation: Use disposable test identities and low-value testnet funds, avoid production keys, and require manual confirmation before delete, destroy, import, export, write, or send-tx operations.

Risk: Private keys and account information may be stored locally in plaintext under ~/.web5-cli.

Mitigation: Do not keep plaintext private keys, bearer tokens, or account files in shared, backed-up, or logged environments.

Risk: The artifact describes itself as a proof-of-concept technical validation tool and warns against production use.

Mitigation: Limit use to validation or demonstration environments until the package, scripts, and operational safeguards are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rink1969/skills/web5-cli)
- [Publisher profile](https://clawhub.ai/user/rink1969)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Web5 CLI commands are expected to emit JSON for agent and script parsing.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
