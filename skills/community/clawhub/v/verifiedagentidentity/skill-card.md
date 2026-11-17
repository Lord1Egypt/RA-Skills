## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nopalempl](https://clawhub.ai/user/nopalempl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external agent users use this skill to create and manage decentralized agent identities, link an agent DID to a human owner, sign challenges, and verify DID ownership proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent private keys may be persisted in plaintext when `BILLIONS_NETWORK_MASTER_KMS_KEY` is not configured.

Mitigation: Configure `BILLIONS_NETWORK_MASTER_KMS_KEY` before identity creation or import, and restrict access to `$HOME/.openclaw/billions`.

Risk: Passing private keys directly on the command line can expose them through shell history or process inspection.

Mitigation: Avoid command-line private-key arguments and prefer generating or importing identities through a protected runtime environment.

Risk: Signed challenge tokens should be treated as reusable until expiration and consumption controls are confirmed.

Mitigation: Limit token sharing, use short-lived challenge workflows, and require review before relying on signed challenges for high-trust authentication.

## Reference(s):

- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)
- [ClawHub skill page](https://clawhub.ai/nopalempl/skills/verifiedagentidentity)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or string command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Node.js scripts and may persist identity data under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
