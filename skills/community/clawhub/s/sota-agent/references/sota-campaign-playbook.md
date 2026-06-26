# SOTA Campaign Playbook

Use this reference when a user wants an agent to manage a CV or DS campaign toward a state-of-the-art result.

## Default campaign phases

1. Define the contract.
   - task
   - dataset
   - metric
   - split
   - baseline
   - target score
2. Scout the field.
   - shortlist relevant papers
   - check leaderboard rules
   - identify reproduced public baselines
3. Reproduce first.
   - trusted internal baseline
   - one strong public reference if possible
4. Run narrow ablations.
   - one question per serious change
5. Stress the winner.
   - seed or rerun check
   - failure-case review
   - compute sanity
6. Claim or hold.
   - no claim without evidence bundle

## Role split

- Scout: literature, benchmark rules, and repos
- Reproducer: baseline and reference runs
- Ablator: new hypotheses and controlled comparisons
- Reviewer: contamination, drift, and regression checks
- Promoter: claim wording and decision

## Stop conditions

- target metric definition is unclear
- benchmark split is contaminated or unstable
- no reproduced baseline exists
- current branch cannot plausibly clear the target inside the compute budget
- the candidate wins only by changing evaluation rules

## Evidence bundle

Keep at least:

- leaderboard snapshot
- paper triage file
- candidate card
- metrics tables
- failure-case notes
- claim summary
