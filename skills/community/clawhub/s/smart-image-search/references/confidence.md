# Confidence policy

Use confidence to decide whether to send one image or multiple candidates.

## Confidence bands

### high
Conditions usually include:
- top score clearly exceeds the rest
- semantic match is strong
- intent match is strong
- result is not a tiny thumbnail or obvious site asset

Action:
- send 1 best image directly

### medium
Conditions usually include:
- top score is decent but not dominant
- multiple candidates are similarly plausible
- source quality is mixed

Action:
- prefer sending 2-3 candidates
- or send 1 image with a brief note if the user asked for speed over precision

### low
Conditions usually include:
- weak score spread
- query drift is visible
- results are noisy, duplicated, or low quality
- engines disagree heavily or only bad sources are available

Action:
- do not pretend there is a reliable best match
- send search links plus 2-3 candidate links or images

## Simple practical rule

- If top score >= 12 and beats second place by >= 4: high
- Else if top score >= 7: medium
- Else: low

Adjust downward if:
- the result is obviously a thumbnail or site asset
- the chosen source is low quality
- intent-specific cues are weak
