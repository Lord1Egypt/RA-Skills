# Synthesis and pricing hypotheses

Synthesis compares the evidence collected for the chosen decision. It does not require a numeric price corridor or multiple packages when the evidence does not support them.

## Compare the evidence

Bring together only the relevant inputs: market references, customer value, delivery economics, buyer research, constraints, and current commercial terms. Put estimates on a common currency, unit, scope, and period before comparing. Explain what cannot be normalized.

Where inputs conflict, show the disagreement and the assumptions that drive it. Use ranges or scenarios where uncertainty matters. Do not fill a missing evidence side with invented values or an automatic capture percentage.

## Evaluate candidate structures

If the decision concerns packaging or pricing structure, define candidate options from the user's business model. They may involve scope, access, quality, service level, capacity, outcome, billing unit, timing, or another custom dimension. Assess buyer clarity, operational enforceability, fairness, cost exposure, and consistency with the evidence.

Use `proposals.yaml` and `optimize_packages.py` only when their configured inputs match the study. Their package scoring is conditional on the supplied value, conjoint, and cost models. A model-selected candidate is not an optimized or guaranteed price.

## Report

Present the studied decision, evidence by source, candidate hypotheses if supported, uncertainty, trade-offs, and what would change the conclusion. Include unresolved gaps and a practical validation plan. Do not state a recommendation more precise than its evidence allows.
