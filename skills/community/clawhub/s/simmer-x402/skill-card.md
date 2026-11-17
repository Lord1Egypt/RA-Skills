## Description:

Make x402 payments to access paid APIs and gated content when an agent needs to fetch data from x402-gated endpoints, including Kaito, Simmer premium endpoints, and other x402 providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to access x402-gated HTTP APIs, check Base wallet balances, and make Quicknode JSON-RPC calls through x402 payment flows. It is intended for operators who can set wallet funding, endpoint allowlists, and per-call spending policies before enabling real payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real x402 calls can spend USDC from the configured wallet, and on-chain payments are irreversible.

Mitigation: Use a dedicated, minimally funded hot wallet, preview requests with dry-run mode, and set a strict per-call limit before enabling payment execution.

Risk: Configuration controls are not strong enough for autonomous use without review, including reliance on environment variables for lower spending limits.

Mitigation: Review config precedence before deployment, pass explicit per-call limits where possible, and enforce budgets or confirmations at the calling agent layer.

Risk: Untrusted URLs, POST bodies, or imported helper calls may trigger payment flows.

Mitigation: Restrict callers to reviewed endpoints and request shapes, add explicit allowlists, and rate-limit calls that can reach x402-gated services.

Risk: Broad dependency ranges can change payment behavior after installation.

Mitigation: Pin and review exact dependency versions before production or unattended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/simmer-x402)
- [Kaito x402 API documentation](https://github.com/MetaSearch-IO/KaitoX402APIDocs)
- [Quicknode x402 documentation](https://x402.quicknode.com/llms.txt)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON API responses, and Markdown instructions with bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make real x402 payments and return paid API or JSON-RPC results when configured with a funded wallet.]

## Skill Version(s):

1.0.9 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
