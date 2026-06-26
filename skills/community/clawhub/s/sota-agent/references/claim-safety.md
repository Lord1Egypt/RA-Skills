# Claim Safety

Use this reference before saying a candidate is state of the art.

## Claim checklist

- baseline rerun exists
- benchmark contract is fixed
- candidate score is recorded in a machine-readable artifact
- important regressions were checked
- compute context is known
- wording matches the actual evidence

## Hold the claim when

- the improvement is tiny and unstable
- the comparison uses a different split or metric
- the candidate depends on undisclosed private data
- the result only exists in one lucky seed or one notebook session
- failure cases got worse in a way that matters to the product

## Safe wording examples

- "beats the reproduced baseline by X on the agreed validation split"
- "best campaign result so far, not yet a public SOTA claim"
- "strong candidate, but claim blocked by benchmark integrity risk"

## Unsafe wording examples

- "SOTA" without public comparison logic
- "beats paper X" without reproducing or matching its benchmark contract
- "production-ready" when the result has only research-surface evidence
