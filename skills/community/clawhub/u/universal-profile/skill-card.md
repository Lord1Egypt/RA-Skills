## Description:

Manage LUKSO Universal Profiles, including identity, permissions, tokens, blockchain operations, and cross-chain support for Base and Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frozeman](https://clawhub.ai/user/frozeman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and operate LUKSO Universal Profiles, manage controller permissions, query assets, prepare profile and token operations, and execute direct or LUKSO relay transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or create controller keys used for signing profile actions.

Mitigation: Use dedicated controller keys, avoid plaintext private keys, do not pass keystore passwords on the command line, and keep credential files restricted.

Risk: The skill can initiate on-chain actions that may be irreversible.

Mitigation: Use a testnet first, verify the target chain and recipient before signing, and review transaction payloads before submission.

Risk: Broad controller permissions can expand the impact of a mistaken or compromised action.

Mitigation: Grant the narrowest practical permissions and restrict controller capabilities with allowed calls or data keys where possible.

## Reference(s):

- [ERC725.js Reference](references/ERC725-JS.md)
- [LUKSO Docs](https://docs.lukso.tech/)
- [LSP6 Key Manager](https://docs.lukso.tech/standards/access-control/lsp6-key-manager)
- [Universal Profile Authorization UI](https://openclaw.universalprofile.cloud)
- [ClawHub Skill Page](https://clawhub.ai/frozeman/skills/universal-profile)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, CLI commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction payloads, profile metadata, permission encodings, and on-chain operation guidance]

## Skill Version(s):

0.9.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
