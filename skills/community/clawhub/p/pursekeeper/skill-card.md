## Description:

Helps agents find and use Nano (XNO) payment services, operate a node-free wallet, sell services over HTTP 402, and fund a wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pursekeeper](https://clawhub.ai/user/pursekeeper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set up and manage a Nano wallet, find services that accept Nano, make capped HTTP 402 payments, and accept Nano payments for their own services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags possible exposure of redeemable payment recovery tokens through the proxy state endpoint.

Mitigation: Keep the proxy on loopback, require its access key, protect the state file, and treat recovery tokens as sensitive; review the state endpoint before installation.

## Reference(s):

- [Node-free Nano wallet guide](references/no-node.md)
- [Nano inference proxy guide](references/inference-proxy.md)
- [Nano-accepting services directory](references/sellers.md)
- [Buying inference from NanoGPT](references/buy-from-nanogpt.md)
- [Pursekeeper website](https://pursekeeper.dev)
- [ClawHub skill page](https://clawhub.ai/pursekeeper/skills/pursekeeper)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet and payment instructions; Nano payments are irreversible once confirmed.]

## Skill Version(s):

0.3.20 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
