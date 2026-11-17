## Description:

Run an executable X Layer pre-execution guard for autonomous agents: OnchainOS DEX route judgment, honeypot and price-impact checks, proof-mode evidence, and optional Agentic Wallet execution via onchainos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to evaluate X Layer swap intents before execution, produce guard decisions, and capture proof-mode or live-wallet execution evidence. It helps agents block, resize, retry, or execute swaps based on route quality, token safety, price impact, and wallet readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use OnchainOS API credentials and a logged-in Agentic Wallet for live swap execution.

Mitigation: Use proof mode or --no-execute by default, and enable agentic-wallet mode only after independent confirmation of the token pair, amount, wallet, chain, and slippage.

Risk: Mock output is produced when API credentials are unavailable and should not be treated as live trading proof.

Mitigation: Check credential configuration and preserve a clear distinction between mock, proof-mode, and live Agentic Wallet results.

Risk: Running in a project directory with sensitive .env files may expose credentials to the skill runtime.

Mitigation: Avoid running the skill from projects containing sensitive .env files and provide only the credentials required for the intended guard run.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Pin and review dependencies before deployment in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard7463/skills/xlayer-execution-guard)
- [OKX Web3 / OnchainOS API base](https://web3.okx.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON guard/proof files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guard output can include pre-execution verdicts, route checks, execution status, proof identifiers, and closed-loop validation.]

## Skill Version(s):

1.0.1 (source: server release evidence and plugin.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
