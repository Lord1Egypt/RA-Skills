---
name: yield-offer-sanity-check
description: A checklist skill that evaluates whether a yield, staking, or earn offer is reasonable or suspicious. Use when the user encounters a yield promotion. Prompt-only.
---

# yield-offer-sanity-check

A checklist skill that evaluates whether a yield, staking, or earn offer is reasonable or suspicious.

## Workflow

1. Take the yield offer details: platform, APY, token, lock period, and conditions.
2. Run a sanity check: compare APY to risk-free rate, flag inconsistency.
3. Check for red flags: guaranteed returns, complex mechanics hidden behind jargon, token inflation to pay yield.
4. Assess the protocol's track record, team, and audit status.
5. Give a verdict: reasonable, suspicious, or needs more information.

## Output Format

- Offer summary
- Sanity check verdict
- Red flags found
- What makes sense and what does not
- Recommended next step

## Quality Bar

- Uses math and evidence, not vague skepticism.
- Distinguishes between high APY due to inflation versus real yield.
- Does not declare any platform safe, only flags clear warning signs.

## Edge Cases

- New protocols with no track record should be flagged even if the offer looks clean.
- If the user does not share the token name or platform, say what is unknown.

## Compatibility

- Prompt-only, no on-chain data required.
- Best with specific offer details typed or pasted by the user.
