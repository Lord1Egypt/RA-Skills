## Description:

A CLI for searching and invoking services on the UnifAI network across DeFi, token data, social media, web search, news, travel, sports, and utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yilunzhang](https://clawhub.ai/user/yilunzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use UnifAI to discover available UnifAI network services, inspect action payload schemas, invoke service actions, manage CLI configuration, and optionally sign supported blockchain transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs unpinned npm package code through the unifai CLI.

Mitigation: Pin and verify the unifai-sdk package version before installation or deployment.

Risk: The CLI can sign real cryptocurrency transactions using local private keys.

Mitigation: Avoid high-value wallet keys, prefer restricted or test wallets, and manually review every transaction before using --sign.

Risk: Different services require exact payload field names, and guessing fields can cause failures or unintended service calls.

Mitigation: Run unifai search first, inspect the returned payload schema, and invoke actions only with the exact field names and required values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yilunzhang/skills/unifai)
- [UnifAI SDK homepage](https://github.com/unifai-network/unifai-sdk-js)
- [UnifAI CLI source](https://github.com/unifai-network/unifai-sdk-js/tree/main/src/cli)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the unifai CLI and UNIFAI_AGENT_API_KEY; transaction signing also requires local wallet private key environment variables.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
