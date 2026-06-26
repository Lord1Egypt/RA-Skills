---
name: x-algo-claim-auditor
description: Review public claims about xai-org/x-algorithm, the X For You algorithm, Phoenix, Grox, Home Mixer, engagement weights, filters, ads blending, or viral algorithm narratives. Use when a user needs a cautious source-backed verdict without private account analysis, reach prediction, account operation, or script execution.
---

# X Algo Claim Auditor

Use this skill to review public claims against public X algorithm source evidence. The goal is a defensible verdict, not growth advice or live-platform prediction.

## Review Workflow

1. Extract the exact claim from the user, screenshot text, public post, or pasted text.
2. Identify which public repository, commit, file, or public citation is being used as evidence.
3. Classify the claim as `supported`, `misleading`, `unsupported`, or `not_public_repo`.
4. Cite the strongest public evidence and state what the evidence does not prove.
5. Flag overclaims about exact multipliers, production equivalence, private thresholds, account treatment, shadowbans, or draft-post reach prediction.
6. If the user wants a share card or public summary, keep it cautious and avoid implying that the public repo fully predicts live platform behavior.

## Verdict Meanings

- `supported`: public source directly supports the narrow claim.
- `misleading`: public source supports a weaker statement, but the claim overstates precision, production equivalence, or causality.
- `unsupported`: no public source evidence was found for the claim.
- `not_public_repo`: the claim depends on production configs, private thresholds, account state, or live ranking behavior absent from public source.

## Boundaries

- Do not claim that the public repo is the full live production system.
- Do not score draft posts, promise reach, or diagnose account-specific boosting or suppression.
- Do not request private account data, authenticated pages, non-public analytics, or account access.
- Do not upload, release, schedule, or operate authenticated sessions as part of this review.
- Do not execute local scripts or clone repositories unless the user separately asks for engineering work.

## Output Shape

Return:

- `Claim`: the exact claim being reviewed.
- `Verdict`: `supported`, `misleading`, `unsupported`, or `not_public_repo`.
- `Evidence`: source-backed points, with paths or public citations when available.
- `Boundary`: what the evidence does not prove.
- `Public wording`: a safer public-safe rewrite when useful.

Use `open-feed-recsys-lab` when the task is broader repository verification, Phoenix artifact readiness, or architecture mapping. Use `tinytroupe-feed-research-lab` when the task is draft comparison or synthetic audience reaction review.
