## Description:

Fetch token swap quotes and executable calldata from the spanDEX API so users can compare routes and prepare wallet-ready EVM transaction payloads, with execution requiring Privy and strongly recommended calldata verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougalcantara](https://clawhub.ai/user/dougalcantara)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch spanDEX swap quotes, inspect best-price or fastest routes, dry-run transaction steps, and execute Base swaps through Privy-managed wallets when execution prerequisites are satisfied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare and send real onchain transactions from remotely supplied calldata without requiring full independent verification.

Mitigation: Use quote-only or dry-run by default, install and trust an onchain transaction verification skill before execution, and avoid executing if full verification is unavailable.

Risk: A wrong wallet, token, recipient, chain, approval amount, destination contract, or calldata value could cause unintended asset movement.

Mitigation: Verify wallet, token, recipient, chain, approval amount, destination contract, and calldata before signing, and keep strict Privy spending policies.

Risk: A mutable spanDEX API endpoint could change the source of quotes and executable calldata.

Mitigation: Pin SPANDEX_URL in the environment when possible and change it only on direct user instruction.

## Reference(s):

- [spanDEX](https://spandex.sh)
- [spanDEX docs](https://docs.spandex.sh)
- [Privy](https://privy.io)
- [Privy Interop Notes](references/privy.md)
- [Token Reference - Base](references/tokens.md)
- [ClawHub Skill Page](https://clawhub.ai/dougalcantara/skills/spandex-agentic-swap)
- [Publisher Profile](https://clawhub.ai/user/dougalcantara)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and human-readable summaries of JSON quote responses and EVM transaction payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Base, supports quote-only, dry-run, and execute modes, and requires Privy for execution.]

## Skill Version(s):

0.4.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
