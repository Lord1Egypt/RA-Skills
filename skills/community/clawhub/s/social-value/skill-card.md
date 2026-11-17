## Description:

Economic intelligence for AI agents via efficient micropayments using the Breez SDK with Liquid or Spark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to configure and operate a dedicated Bitcoin micropayments wallet for receiving, sending, batching, withdrawing, and estimating fees for sats transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to use mnemonic seed material that can authorize transactions with real funds.

Mitigation: Use only a new dedicated low-balance wallet, inject the mnemonic through a protected secret mechanism, start on testnet, and set SOCIAL_VALUE_MAX_BALANCE to a conservative nonzero cap.

Risk: Send, withdrawal, batch transfer, or drain operations can move real Bitcoin value.

Mitigation: Require explicit user approval for every value-moving operation and review fees and destinations before execution.

Risk: The security summary notes reliance on unpinned external wallet code.

Mitigation: Use a pinned, hashed, reviewed package version or an isolated runtime before using mainnet funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vveerrgg/skills/social-value)
- [Project homepage](https://github.com/HumanjavaEnterprises/huje.socialvalue.OC-python.src)
- [Breez SDK](https://breez.technology/sdk/)
- [NostrKey related skill](https://clawhub.ai/vveerrgg/nostrkey)
- [social-alignment related skill](https://clawhub.ai/vveerrgg/social-alignment)
- [sense-memory related skill](https://clawhub.ai/vveerrgg/sense-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline environment variable, shell, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can include wallet setup, transaction examples, fee estimation, and safety practices.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
