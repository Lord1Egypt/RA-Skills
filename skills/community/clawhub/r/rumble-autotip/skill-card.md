## Description:

Autonomous AI agent that tips Rumble.com creators in cryptocurrency based on watch time, with smart splits, community pools, event-triggered tipping, and conversational AI setup powered by Tether WDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dev-me4](https://clawhub.ai/user/dev-me4)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent to configure cryptocurrency tips for Rumble creators, manage tipping rules and budgets, and review wallet, balance, tip history, smart split, community pool, and event-triggered tipping workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous tips are real, irreversible cryptocurrency payments.

Mitigation: Use small spending limits, review rules before enabling automation, and treat every autonomous tip as a final on-chain transfer.

Risk: The skill requests real wallet and payment authority with under-scoped natural-language controls.

Mitigation: Set strict daily and per-session caps and confirm how transaction approval works before connecting a funded wallet.

Risk: Wallet dependencies are reported as unpinned in the security evidence.

Mitigation: Prefer a release with pinned dependency versions or a lockfile before installation.

Risk: Seed storage and wallet handling need careful review before use.

Mitigation: Confirm the actual extension's seed storage, encryption, and recovery behavior before importing an existing seed phrase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dev-me4/skills/rumble-autotip)
- [Project homepage from ClawHub metadata](https://github.com/kalxe/rumble-ai-extension)

## Skill Output:

**Output Type(s):** [text, configuration, guidance, API calls]

**Output Format:** [Markdown and conversational text with structured tipping-rule parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe wallet setup, budgets, rules, supported tokens, transaction history, and autonomous tipping decisions.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter says 2.1.0 and skill.json says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
