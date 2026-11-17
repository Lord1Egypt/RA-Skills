## Description:

RanchiMall Messenger lets an agent operate FLO messaging, contacts, mail, groups, public-key lookup, FLO and FLO-token transfers, Bitcoin queries, multisig workflows, and local key-value storage through Node.js CLI scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[void-57](https://clawhub.ai/user/void-57)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent manage decentralized FLO messenger workflows and blockchain operations from a local Node.js environment. It is intended for deliberate wallet, messaging, token, multisig, and local-cache tasks where the operator controls the private key environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle FLO private keys and related secrets through environment variables, command arguments, and command output.

Mitigation: Keep FLO_PRIVATE_KEY out of chat, avoid commands that pass --privkey, --privkeys, --pin, --secret, or --shares, and treat secure-privkey output as sensitive.

Risk: FLO, FLO-token, and multisig send operations can move funds or tokens irreversibly on-chain.

Mitigation: Install and run the skill only when the operator deliberately wants an agent to perform wallet or transfer actions, and review transaction commands before execution.

Risk: The skill writes local cache files and the security evidence flags JSON file access outside the stated storage area.

Mitigation: Restrict access to local cache files and review or fix IDB path handling before using the skill with untrusted database names.

Risk: On-chain memos and custom data are public once written.

Mitigation: Do not include private, regulated, or sensitive content in transaction memos or blockchain data payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/void-57/skills/ranchimall-messenger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also initiate network API calls, local cache updates, signed messages, and blockchain transactions when an agent executes the described commands.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
