## Description:

Helps developers adapt Solana programs to Light SDK patterns for rent-free PDAs, token accounts, mints, DeFi integrations, router cold-account loading, and tests with Anchor or Pinocchio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilo-14](https://clawhub.ai/user/tilo-14)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for Solana program development when adding Light SDK rent-free account patterns, integrating Anchor or Pinocchio examples, handling hot and cold account flows, and preparing router or test code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable external install paths and dynamically loaded external skills or MCP access can introduce unreviewed content during agent work.

Mitigation: Review the skill before installing and prefer a pinned commit or signed release instead of an unpinned `npx` command.

Risk: Broad subagent or DeepWiki MCP access could expose wallet files, tokens, or unrelated private repositories.

Mitigation: Limit subagents to the intended project directory and avoid exposing wallet files, tokens, or unrelated private repositories.

Risk: The Jito bundle example is a third-party transaction submission path.

Mitigation: Review transaction routing, endpoint choice, and signing behavior before using that example in a production workflow.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/tilo-14/skills/solana-light-sdk)
- [ZK Compression Documentation](https://www.zkcompression.com)
- [Anchor Pattern](references/anchor.md)
- [Pinocchio Pattern](references/pinocchio.md)
- [Client SDK](references/client-sdk.md)
- [Router Integration](references/router.md)
- [CPI Pattern](references/instructions.md)
- [Testing](references/testing.md)
- [FAQ](references/faq.md)
- [Light SDK API Reference](https://docs.rs/light-sdk/latest/light_sdk/)
- [Light Token API Reference](https://docs.rs/light-token/latest/light_token/)
- [Light Client API Reference](https://docs.rs/light-client/latest/light_client/)
- [Light Protocol Audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Rust, TypeScript, TOML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference node, cargo, and anchor tooling for builds and tests.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
