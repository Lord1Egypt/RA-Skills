# Customer value and scenarios

Use value modelling when the buyer's relevant outcomes and a credible counterfactual can be described. Economic Value to the Customer compares the buyer's next-best alternative with the differentiated outcomes of the offer. It is a structured estimate, not an observed willingness-to-pay figure.

## Define value drivers

For each material driver, record:

- the buyer outcome and who receives it;
- the unit and time period;
- the counterfactual or alternative;
- the evidence for quantity, probability, and outcome size;
- dependencies, overlap with other drivers, and possible double counting;
- assumptions, uncertainty ranges, and limits to realization.

Include direct outcomes and enabling conditions where relevant. Model whether an outcome requires adoption, use, buyer action, operational capacity, or other conditions. Do not assume that a measured operational improvement becomes financial value without a supported conversion path.

## Scenario design

Define scenarios around the actual decision, population, and relevant units. Use supplied data where available. Label distributions and formulas as assumptions, cite their basis, and keep unsupported values unset. Computational scenario count and seed are not respondent sample size or empirical evidence.

## Analysis and safeguards

Prevent overlap across lines with a documented rule. Vary the assumptions that materially affect conclusions and report sensitivity or intervals. Explain which drivers dominate the result and whether the conclusion changes under plausible alternatives.

The included `value_mc.py` supports a specific Monte Carlo and feature-attribution workflow. It requires configured variables, formulas, and dependencies. Use it only when feature or attribute attribution is meaningful; otherwise report the value analysis at the outcome or offering level without forcing a feature split.

## Report

Describe the counterfactual, units, sources, assumptions, uncertainty, and sensitivity. Call the result a modelled value estimate. Do not describe it as price, willingness to pay, or realized customer benefit without appropriate evidence.
