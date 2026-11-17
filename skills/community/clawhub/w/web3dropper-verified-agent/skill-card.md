## Description:

Billions/Iden3 authentication and identity management tools for agents to create identities, link ownership, sign challenges, and verify signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3dropper](https://clawhub.ai/user/web3dropper)

### License/Terms of Use:

UNLICENSED

## Use Case:

External users, developers, and agents use this skill to manage decentralized identities on the Billions Network, link an agent DID to a human owner, and perform challenge-response identity verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity keys are created or imported and stored unencrypted under $HOME/.openclaw/billions.

Mitigation: Protect that directory like a wallet, restrict filesystem permissions, back it up carefully, and remove identities that are no longer needed.

Risk: Passing real private keys on the command line can expose them through shell history or process listings.

Mitigation: Prefer generated identities, avoid command-line private key import for sensitive keys, and use a patched release that removes or hardens key import.

Risk: Verification messages and signed artifacts are sent through external Billions/PolygonID and openclaw services.

Mitigation: Use trusted recipients, review messages before sharing them, and avoid signing challenges whose source or purpose is unclear.

Risk: Verification challenges may remain reusable if they are not expired or consumed.

Mitigation: Prefer deployments that expire or consume challenges after use and periodically clear stale challenge data.

## Reference(s):

- [Billions Network](https://billions.network/)
- [Web3Dropper Verified Agent on ClawHub](https://clawhub.ai/web3dropper/skills/web3dropper-verified-agent)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands plus script outputs as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce DID strings, identity lists, challenge strings, verification status, and verification URLs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
