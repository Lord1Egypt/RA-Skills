# SKILL: signal-vs-noise

## Purpose
Filter relevant information from noise while preserving evidence and decision-impact.

## When to Use
- Many messages/news/items arrive at once
- A decision must be made and inputs are overwhelming
- You need a ranked list of what matters

## Inputs
- `dataset` (required): list of items (news, messages, metrics, notes)
- `decision_context` (optional): what decision this supports
- `time_window` (optional): timeframe considered relevant

## Steps
1. Normalize the dataset into items with `source`, `timestamp` (if present), and `content`.
2. Extract key claims per item (1–3 claims max).
3. Remove redundancy:
   - merge duplicates
   - group near-duplicates by same claim
4. Identify high-impact signals:
   - changes in constraints (governance, deadlines, outages)
   - verified facts that shift probability
   - actionable next steps
5. Rank signals by:
   - impact on the decision
   - credibility/verifiability
   - urgency (only if real)
6. Output:
   - ranked signals with evidence
   - discarded noise (with brief reason)

## Validation
- No duplicated signals in the ranked list.
- Each signal includes at least one evidence pointer (source/item id).
- Novelty is not treated as importance by default.

## Output
- `ranked_signals`: ordered list with `claim`, `why_it_matters`, `evidence`
- `discarded_noise`: list with `item` + `reason`

## Safety Rules
- Avoid bias toward novelty: “new” is not automatically “important”.
- Do not delete dissent; label it as low-confidence when evidence is weak.

## Example
Input: 30 chat messages + 5 news headlines about a protocol.
Output: top 5 signals (governance vote date, confirmed exploit, liquidity change) + noise bucket (memes, repeated hype).

