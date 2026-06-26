---
name: stablecoin-use-check
description: A decision guide that helps users evaluate whether a stablecoin use case makes sense for them. Use when the user is considering holding or using a stablecoin. Prompt-only.
---

# stablecoin-use-check

A decision guide that helps users evaluate whether a stablecoin use case makes sense for them.

## Workflow

1. Ask what the user wants to do with the stablecoin: hold, send, earn, convert, or use as a buffer.
2. Ask about the specific stablecoin, platform, or protocol being considered.
3. Assess the use case against alternatives: keeping cash, using a bank, holding ETH instead.
4. Identify risks: depeg risk, platform risk, regulatory risk, counterparty risk.
5. Give a fit decision: recommended, conditional, or not recommended for their situation.

## Output Format

- Use case summary
- Fit assessment
- Top risks to watch
- Alternatives to consider
- Questions to ask before committing

## Quality Bar

- Grounded in the user's actual goal, not abstract pros/cons.
- Honest about stablecoin risks that are often glossed over.
- Does not recommend any specific platform or product.

## Edge Cases

- If the user wants to use a stablecoin as a long-term store of value, flag the difference between holding and earning.
- If the use case is sending money across borders, also flag KYC and regulatory considerations.

## Compatibility

- Prompt-only, no platform integration.
- Works with user-provided descriptions of what they want to do.
