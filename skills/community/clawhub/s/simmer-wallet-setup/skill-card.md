## Description:

Self-custody wallet setup for Simmer agents. Bring your own key, import a funded Polymarket wallet, or connect an existing dashboard-registered agent to your local runtime. Skip this skill if you use a managed wallet because managed setup is a one-time dashboard flow, not an agent task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure self-custody wallet signing for Simmer agents that trade on Polymarket or Kalshi, including external keys, imported Polymarket wallets, and existing dashboard-registered agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime may hold real wallet private keys or API keys for a real-money trading workflow.

Mitigation: Use an isolated environment, prefer a local key store over bare environment variables, avoid shared surfaces for keys, and keep wallet keys unset during package installation.

Risk: The setup asks users to install mutable third-party code.

Mitigation: Install pinned and verified SDK versions where possible and avoid curl-to-bash installers unless the source and contents have been reviewed.

Risk: Some SDK calls can sign approvals or trigger configured exit trades.

Mitigation: Review commands before execution, confirm the intended wallet and venue, and verify auto risk monitor settings before running the agent.

## Reference(s):

- [Simmer Skill Page](https://clawhub.ai/simmer/skills/simmer-wallet-setup)
- [Simmer Dashboard](https://simmer.markets/dashboard?ref=sdk-skill&utm_campaign=sdk-skill)
- [Polymarket Wallet Import](https://docs.simmer.markets/polymarket-import)
- [Simmer Wallet Docs](https://docs.simmer.markets/wallets)
- [V2 Migration Guide](https://docs.simmer.markets/v2-migration)
- [Open Wallet Standard](https://openwallet.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment-variable setup guidance for SIMMER_API_KEY, optional wallet key handling, package installation, wallet linking, approvals, and verification.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
