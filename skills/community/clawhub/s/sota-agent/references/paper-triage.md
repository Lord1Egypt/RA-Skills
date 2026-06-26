# Paper Triage

Use this reference when the agent needs to decide which papers or repos matter.

## Keep only decision-relevant fields

For each paper or repo, extract:

- task and dataset
- metric and split
- model family
- training recipe highlights
- data or augmentation assumptions
- compute or runtime notes
- what is actually novel
- what seems reproducible versus fragile

## Triage buckets

- `must-read`: directly targets the same benchmark contract
- `worth-stealing`: transferable trick or training pattern
- `baseline-only`: strong reference but not directly competitive
- `skip`: mismatched task, metric, split, or unrealistic compute

## Questions worth answering

- What gap does this work close?
- Which pieces are likely causal?
- Which pieces are likely stack-specific noise?
- What is the cheapest experiment that would falsify the paper-inspired hypothesis?

## Anti-pattern

Do not build a campaign around paper-count vanity.
Five weakly related papers usually add less value than one reproduced strong baseline and one well-tested hypothesis.
