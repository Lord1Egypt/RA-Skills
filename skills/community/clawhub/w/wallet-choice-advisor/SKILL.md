---
name: wallet-choice-advisor
description: A decision helper that recommends a wallet setup pattern based on the user's goals, activity level, and risk tolerance. Use when the user is deciding what kind of wallet to use. Prompt-only.
---

# wallet-choice-advisor

A decision helper that recommends a wallet setup pattern based on the user's goals and risk tolerance.

## Workflow

1. Ask what the user wants to do: hold, learn, spend, use apps, or trade lightly.
2. Ask about amount at risk, device habits, technical comfort, and backup discipline.
3. Map the user to a setup pattern: learning-only, small active wallet, or hardware-plus-hot-wallet split.
4. Explain the tradeoffs of convenience, cost, and security.
5. Give an upgrade path for later, instead of over-building on day one.

## Output Format

- Recommended setup pattern
- Why it fits
- Top risks of that setup
- First setup checklist
- Future upgrade trigger

## Quality Bar

- Advice is conservative and behavior-based.
- Does not assume everyone needs the same hardware or app stack.
- Explains tradeoffs instead of declaring one universal winner.

## Edge Cases

- Shared devices, family access, travel, or poor backup habits may change the recommendation.
- Avoid making brand-specific claims unless the user asks for comparison criteria.

## Compatibility

- Prompt-only, no device inspection or wallet integration.
- Best used with user-provided facts about budget, habits, and intended use.
