## Description:

Researches a token, analyzes Uniswap liquidity and risk, and executes a trade only after risk assessment approval and explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run a research-to-trade workflow for Uniswap tokens: inspect token and pool conditions, assess risk, request confirmation, and execute only approved trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An approved run can lead to a real Uniswap trade from a configured wallet, including gas costs and irreversible on-chain settlement.

Mitigation: Install only a trusted, pinned version and require explicit user confirmation after research, pool analysis, and risk assessment before execution.

Risk: A trade request without a specific amount could lead to unsafe assumptions about position size.

Mitigation: Ask for the trade amount and do not proceed until the user provides one.

Risk: Low liquidity, high slippage, unverified tokens, or unsafe pools can make a proposed trade unsuitable.

Mitigation: Use the skill's risk gate to stop on VETO or HARD_VETO decisions and report the reason instead of executing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wpank/skills/research-and-trade)
- [Skill Specification](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown-style progress summaries, risk assessment reports, confirmation prompts, and final trade execution or veto reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include transaction details and explorer links when an approved trade is executed.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
