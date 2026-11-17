# Supported input formats

Accept JSON exported from OpenAI's organization Usage or Costs endpoints. A Costs export supplies the actual amount charged; an optional Usage export adds token and caching signals. Analyze both files together when both are available.

Files may be passed positionally in any order or with explicit `--costs` and `--usage` flags. Date-range or request-ID mismatches produce warnings; they do not abort analysis.

The analyzer recursively recognizes:

- Monetary values in `amount.value`, `cost`, `total_cost`, `cost_usd`, or `amount_usd`.
- Usage fields such as `input_tokens`, `output_tokens`, `input_cached_tokens`, and `num_model_requests`.
- Breakdown labels such as `model`, `line_item`, `project_name`, or `project_id`.

Usage records do not contain the amount charged. When token usage exists without cost data, request a Costs JSON export rather than estimating from a stale model-price table. Costs results use `amount.value` and can be grouped by `project_id`, `line_item`, or `api_key_id`.

Do not accept CSV, screenshots, invoices, or non-OpenAI provider exports in the MVP.
