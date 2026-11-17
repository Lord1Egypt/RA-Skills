## Description:

SVM helps agents explain Solana architecture and protocol internals across execution, accounts, consensus, transactions, validator economics, data, development, and token extensions using Helius and Solana references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xichigo](https://clawhub.ai/user/0xichigo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, protocol engineers, and technical reviewers use this skill to get sourced explanations of Solana protocol architecture, including the SVM execution engine, account model, consensus, transactions, validator economics, and related development concepts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to register an unpinned third-party Helius MCP package, which may later run different package code in Claude sessions.

Mitigation: Review the Helius MCP package provenance before installing, and prefer a pinned version or vetted local install method before registering the MCP server.

Risk: Some Solana topics in the artifact are proposals or have source-fetching limits, which can lead to overconfident or incomplete protocol explanations.

Mitigation: Follow the artifact guidance to label proposals clearly, cite Helius blog posts, SIMDs, or source paths, and state when a requested source is outside the MCP tool scope.

## Reference(s):

- [Account Model & Programming Model](references/accounts.md)
- [Compilation Pipeline](references/compilation.md)
- [Consensus](references/consensus.md)
- [Data Layer](references/data.md)
- [Program Development](references/development.md)
- [Execution Engine](references/execution.md)
- [Program Deployment](references/programs.md)
- [Token Extensions & DeFi Primitives](references/tokens.md)
- [Transactions & Local Fee Markets](references/transactions.md)
- [Validator Economics](references/validators.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with citations and occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [In-conversation responses; the skill instructs the agent not to write local files with fetched content.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
