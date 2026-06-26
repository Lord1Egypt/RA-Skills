# SKILL: reality-check

## Purpose
Prevent bad strategic decisions by forcing assumptions into the open, testing them, and ranking feasibility before commitment.

## When to Use
- A plan sounds good but may be fragile or unrealistic
- The user is optimistic without evidence
- A decision has meaningful downside risk

## Inputs
- `idea` (required): the proposed plan/decision
- `assumptions` (optional): stated assumptions; if missing, Morpheus must extract them

## Steps
1. List assumptions (explicit + implicit).
2. For each assumption:
   - define what would make it true/false
   - define the cheapest test/experiment
   - define failure impact if wrong
3. Identify the weakest links (highest impact × lowest evidence).
4. Evaluate feasibility:
   - resources/time
   - constraints/governance
   - reversibility
5. Produce:
   - viability score (0–100)
   - critical flaws
   - recommendation (proceed / revise / stop)
6. Provide the next 1–3 validation steps.

## Validation
- Assumptions are explicit and testable.
- Claims are labeled as evidence vs hypothesis.
- Recommendation follows the evidence, not optimism.

## Output
- `viability_score` (0–100)
- `critical_flaws`
- `recommendation`
- `next_steps`

## Safety Rules
- Prioritize truth over optimism.
- No financial guarantees or claims of certainty without evidence.

## Example
Idea: “Launch a new token feature in 48h.”
Output: viability 35/100; critical flaw: no governance approval + no test coverage; next steps: scope reduction + emergency review + paper validation.

