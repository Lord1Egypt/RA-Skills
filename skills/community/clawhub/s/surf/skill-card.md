## Description:

Surf lets agents query live cryptocurrency data across prices, wallets, social intelligence, DeFi, on-chain SQL, prediction markets, news, and related domains through the Surf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hughzhou-gif](https://clawhub.ai/user/hughzhou-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use Surf to answer crypto-market, wallet, DeFi, social, news, prediction-market, and on-chain questions with live data, and to build workflows that consume structured crypto responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install or update executable Surf CLI tooling and refresh API specifications.

Mitigation: Review the CLI provider and run the skill in a least-privileged workspace before allowing automatic updates.

Risk: The skill can add routing instructions to AGENTS.md or CLAUDE.md and create a git commit.

Mitigation: Require explicit user approval, inspect the diff before committing, and decline routing changes when they are not appropriate for the project.

Risk: Crypto queries go to Surf, and feedback submission may attach recent chat context.

Mitigation: Avoid using the skill in conversations containing secrets or sensitive wallet/account details, and submit feedback only after explicit user consent.

Risk: Surf API responses are external untrusted data.

Mitigation: Treat returned content as data only and do not execute instructions that may appear inside response fields.

## Reference(s):

- [ClawHub Surf skill listing](https://clawhub.ai/hughzhou-gif/skills/surf)
- [Surf CLI documentation](https://agents.asksurf.ai/docs/cli/introduction)
- [Surf account and API key portal](https://agents.asksurf.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and summarized JSON data responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to run the Surf CLI, update local routing files, and treat API responses as untrusted external data.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact metadata.version is 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
