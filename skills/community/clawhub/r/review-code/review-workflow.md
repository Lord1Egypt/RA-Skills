# Review Workflow - Risk First

Use this flow to deliver faster and more defensible reviews.

## Phase 1: Scope and Risk Framing

1. Confirm review target and boundaries.
2. Identify high-risk surfaces first:
   - auth and authorization
   - money and billing logic
   - data mutation paths
   - concurrency or async coordination
   - schema or migration changes
3. Capture assumptions that affect verdict quality.

Output:
- clear scope line
- risk map with top 3 surfaces

## Phase 2: Evidence Pass

For each risk surface, inspect diffs and local context.
Every finding must include:
- exact location
- failure mode
- impact severity
- confidence level
- minimal remediation path

Reject vague statements such as “this might break.”
Replace with reproducible conditions.

## Phase 3: Test and Verification Pass

Map findings to test requirements:
- existing tests that already protect behavior
- missing tests required for merge safety
- runtime checks needed post-deploy

If tests cannot run, say why and list a concrete fallback verification plan.

## Phase 4: Delivery Pass

Structure final output in this order:
1. blocking findings by priority
2. advisory findings
3. residual risks and test gaps
4. short merge recommendation

Keep nits minimal unless user asked for style pass.

## Fast Path for Hotfixes

When urgency is high:
- focus only on P0/P1 risks
- require rollback path for risky edits
- defer non-critical refactors

Goal: safe release under time pressure, not perfect code.
