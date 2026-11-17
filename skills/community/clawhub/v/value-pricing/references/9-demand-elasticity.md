# Bayesian demand price elasticity

This phase estimates how **observed transaction quantity** varies with realised unit price. It is distinct from `value_metric.py`, which estimates how competitors' listed prices vary with plan limits. Do not combine or rename those two elasticities.

## Input

Place a CSV at `demand/data/transactions.csv`, or pass `--csv`. Required columns:

| Column | Meaning |
|---|---|
| `date` | Transaction date, parseable as a date |
| `product` | Product identifier |
| `customer` | Stable customer identifier |
| `segment` | Customer segment |
| `realised_unit_price` | Positive realised price per unit, in one consistent currency and basis |
| `quantity` | Positive units on the transaction |

Optional controls are `promotion`, `channel`, and `contract_duration`. Promotion must be a binary flag or numeric value (such as discount percent); contract duration must be numeric in a consistent unit; channel may be categorical. Missing required values, invalid dates, non-positive prices, non-positive quantities, and fractional quantities are dropped and counted because the likelihood models unit counts. Missing optional values are imputed to the median for numeric fields and `unknown` for channel; this is reported. Realised prices must use the study currency per unit; the script performs no currency conversion.

Run `demand_elasticity.py --study S [--csv PATH]`. It fits one hierarchical zero-truncated negative-binomial log-link model per product. The likelihood conditions on positive transaction quantities; it does not pretend the transaction file contains no-purchase periods. Segment price slopes are partially pooled around a population slope. Customer intercepts account for repeated transactions, annual sine/cosine terms represent seasonality, and available promotion, channel, and contract-duration fields enter as controls. NUTS samples the posterior. The script flags convergence only when all R-hat values are finite and at most 1.05, minimum effective sample size is at least 100, and there are no divergent transitions. Inspect these diagnostics before using estimates.

The output also reports posterior predictive checks for transaction quantity, pairwise correlations between log price and each model control, highlights absolute correlations of 0.8 or higher, and gives a standardized predictor condition number. Predictive checks compare the observed mean, median, and 90th percentile with replicated positive transaction quantities. Correlations and condition number are checks for measured overlap and weak separation, not tests of price exogeneity; unmeasured confounding and endogenous price setting remain possible.

The summary reports each product and segment's posterior median price elasticity and 90% credible interval, plus expected transaction-quantity responses at 20% lower, baseline, and 20% higher prices. Scenario quantities are conditional predictions for a typical observed transaction, not estimates of total market demand.

## Identification and limitations

The minimum variation screen requires at least three distinct realised prices and a standard deviation of log price of at least 0.03. Segment-level variation is separately flagged; partial pooling can stabilize a weak segment estimate but cannot create identifying variation. A product failing the overall screen receives no elasticity estimate.

Transactions alone omit customers who did not purchase. Therefore, this model estimates quantity conditional on an observed transaction, not purchase incidence, customer-level demand, or market demand. To estimate incidence, supply a complete customer-period panel with zero-purchase periods and a defined exposure/availability measure, then use a model whose likelihood matches that data.

Price and quantity can be jointly determined: sellers may discount in response to expected demand, change prices for high-value customers, or bundle price with unobserved service. Promotions and other included controls do not establish exogeneity. Unless the study supplies a defensible randomized experiment, instrument, regression discontinuity, or other identification design, label the result **observational association**, not causal price elasticity. State the design, exclusions, and assumptions before any causal claim.

The price-scenario output holds controls and observed transaction composition fixed. It does not account for customer selection, competitor response, substitution, or changes in whether a transaction occurs. Small samples, sparse segments, seasonality beyond the annual cycle, and customer migration can also limit interpretation.

## Outputs and synthesis

The phase writes `demand/results/summary.json` with `demand_elasticity.products`. Synthesis copies the dedicated object to `synthesis/results/summary.json` and writes a separate `synthesis/data/demand_elasticity.json`. This remains separate evidence from the market meter elasticity in `market/results/summary.json`.

## Test fixture

The repository-level self-test creates synthetic repeated customer transactions with a planted negative price elasticity, checks posterior recovery and scenario direction, and covers missing rows and insufficient price variation. These synthetic checks verify code behavior; they do not validate causal identification in real observational data. It is kept outside the published skill folder because it launches analysis scripts for development checks.

The recovery fixture uses invented transaction data and generic segment labels for code checks only. It does not describe a real offering, audience, price, or customer record.
