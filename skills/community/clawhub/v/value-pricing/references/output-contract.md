# Output contract

The structures below document the current script outputs. Example values are schema placeholders, not
study findings. Several scripts implement a specific feature-based, monthly analysis and should only be
used when those assumptions match the configured study. For other pricing bases, preserve the relevant
fields and explicitly document the study's own currency, unit, period, and tax basis.

Synthesis can only combine what lands in a known shape. Each phase writes `<phase>/results/summary.json`
with the keys below; extra keys are fine, missing ones are not. A value a phase could not produce is
`null`, with the reason under `gaps`. Never a guess. Script-generated monetary values use the basis
assumed by that script (currently commonly monthly); document currency, unit, period, and tax basis
explicitly. Do not use a script where its assumptions do not fit. Intervals are 90% `[p05, p95]` where
implemented; feature and segment identifiers are configurable study identifiers. When a phase is done
by hand, write its applicable outputs and document the method.

## Common header

```json
{"phase": "market|cost|value|panel|demand|synthesis", "run_date": "YYYY-MM-DD", "currency": "EUR",
 "fx": {"USD": 0.0, "date": "YYYY-MM-DD"}, "git_sha": "... or null",
 "assumptions": ["each one a sentence a reviewer can disagree with"],
 "gaps": [{"what": "...", "why": "...", "blocked_on": "owner | data | null"}]}
```

## market

```json
{"corpus": {"n_vendors": 0, "n_priced": 0, "price_visibility": {"priced": 0, "free_only": 0, "quote_only": 0, "undisclosed": 0}},
 "reference_price_rule": "recommended > middle paid tier; usage plans at each segment's reference_volume",
 "fit": {"r2_oos": 0.0, "mape_oos": 0.0, "n_train": 0, "n_test": 0},
 "kappa": {"dropped": ["feature_id"]},
 "feature_values": [{"feature_id": "...", "coef": 0.0, "ci90": [0, 0], "pct_price_effect": 0.0, "prevalence": 0.0, "ours": "yes|partial|no", "ci_excludes_zero": true}],
 "implied_price": {"<segment>": {"ols": {"point": 0, "ci90": [0, 0]}, "lasso": {"point": 0, "ci90": [0, 0]}, "neighbours": {"point": 0, "p10_p90": [0, 0]}}},
 "support": {"our_feature_count": 0, "share_priced_at_or_above_us": 0.0},
 "nearest_competitors": [{"vendor": "...", "coverage": 0.0, "ref_main": 0, "missing_our_features": "a;b"}],
 "out_of_sample_features": ["..."],
 "meters": [{"axis": "...", "share_all": 0.0, "share_direct": 0.0, "elasticity": 0.0, "ci90": [0, 0], "r2_within": 0.0, "co_moves": {"<axis>": 0.0}}],
 "unit_multipliers": {"<axis>": {"1": 1.0, "2": 0.0}}}
```

## cost

```json
{"lines": [], "variable_per_customer": {"<segment>": {"point": 0, "ci90": [0, 0]}},
 "people_per_customer": {"<segment>": {"hours": 0, "eur": 0, "eur_range": [0, 0]}},
 "channel_share_of_price": 0.0, "fixed_platform": 0,
 "floor_price": [{"segment": "...", "target_margin": 0.8, "floor_with_people": 0}],
 "carry": [{"price": 0, "segment": "...", "customers_to_carry_fixed": 0}],
 "support_minutes_afforded": [{"segment": "...", "price": 0, "target_margin": 0.8, "minutes": 0}]}
```

## value

```json
{"design": {"n_scenarios": 0, "seed": 0},
 "value_by_segment": {"<segment>": {"value": {"p10": 0, "p50": 0, "p90": 0}, "evc": {"p50": 0}, "by_type_share": {"hours": 0.0}}},
 "wtp_band_evc": {"<segment>": {"capture_10": 0, "capture_20": 0, "capture_30": 0}},
 "feature_value": [{"feature_id": "...", "share_of_scenarios_valued": 0.0, "median_eur_when_valued": 0, "shapley_share": 0.0, "leave_one_out_eur_mean": 0, "is_gate": false}],
 "sensitivity": [{"parameter": "...", "S1": 0.0, "ST": 0.0}]}
```

## panel

```json
{"preregistration": {"sha": "...", "date": "..."},
 "method": "HB-MNL ...", "convergence": {"rhat_max": 0.0, "ess_min": 0, "divergences": 0},
 "reservation_price": {"<segment>": {"median": 0, "ci90": [0, 0], "p25": 0, "p75": 0, "never_buy_share": 0.0}},
 "wtp_per_level": [{"attribute": "...", "level": "...", "pooled": {"mean": 0, "ci90": [0, 0]}, "by_segment": {"<segment>": 0}}],
 "holdout_hit_rate": 0.0, "arm_effects": {"anchor": {}, "paraphrase": {}},
 "calibration": {"ratio_range": [0, 0], "benchmark": "...", "applied": false},
 "hypotheses": [{"id": "H1", "supported": true, "statistic": "..."}],
 "deviations": ["..."]}
```

`preregistration`, `calibration`, `hypotheses` and `deviations` are written by hand after the scripts run;
VW and Gabor-Granger live in `panel/results/{psm,gabor_granger,gabor_granger_binary}.csv`.

## demand

`demand_elasticity.py` writes transaction-based price response as a separate evidence source. This is not the competitor listed-price meter elasticity in `market.meters`.

```json
{"demand_elasticity": {
  "status": "observational", "input_validation": {"rows_received": 0, "rows_used": 0},
  "model": "hierarchical negative-binomial ...", "interval": "90% posterior credible interval",
  "identification": {"causal": false, "statement": "..."},
  "products": {"<product>": {
    "status": "ok|insufficient_price_variation", "n_rows": 0,
    "price_variation": {"n_unique_prices": 0, "log_price_sd": 0.0, "by_segment": {}},
    "diagnostics": {"rhat_max": 0.0, "ess_min": 0.0, "divergences": 0, "converged": true},
    "estimates": [{"segment": "...", "elasticity": 0.0, "ci90": [0, 0],
      "scenarios": [{"price_factor": 0.8, "expected_quantity": 0, "expected_quantity_ci90": [0, 0]}]}]
  }}}
}}
```

Only observed transaction rows are modelled. Unless zero-purchase periods and exposure are available, estimates describe transaction quantity conditional on purchase, not purchase incidence or total demand. Observational price associations are not causal absent a defensible identification design.

## synthesis

`synthesis/data/corridor.csv`, `feature_value.csv`, `proposals_eval.csv`, `synthesis/results/packages.json`,
and `synthesis/PROPOSALS.md`. When the demand phase ran, synthesis carries its dedicated
`demand_elasticity` object and writes `synthesis/data/demand_elasticity.json`; this remains separate from
the market meter results.
