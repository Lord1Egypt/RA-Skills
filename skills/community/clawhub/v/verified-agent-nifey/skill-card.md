## Description:

Billions decentralized identity for agents that links agents to human identities using Billions ERC-8004 and Attestation Registries, and supports authentication proof generation and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mangfiksi](https://clawhub.ai/user/mangfiksi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage decentralized agent identities, link an agent DID to a human owner, sign identity challenges, and verify DID ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private keys may be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not configured.

Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, and protect the master key separately from the agent workspace.

Risk: Identity data is persisted outside the workspace under $HOME/.openclaw/billions.

Mitigation: Restrict filesystem permissions for that directory and include it in local secret-handling and backup policies.

Risk: Passing existing private keys on the command line can expose them through shell history or process listings.

Mitigation: Avoid command-line private key import for valuable identities; use freshly generated identities or a protected execution environment when import is unavoidable.

Risk: The skill depends on external network endpoints and a Node dependency lockfile.

Mitigation: Review the listed Billions and resolver endpoints and inspect the dependency lockfile before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mangfiksi/skills/verified-agent-nifey)
- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command outputs may include DID strings, JSON identity records, verification URLs, signed tokens, challenges, or signature verification status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
