-- Reconcile Anthropic billing CSV vs local ledger calls
-- Assumes provider_daily_usage table exists.

-- Local ledger (calls) aggregated by UTC day + model
WITH ledger AS (
  SELECT
    substr(ts,1,10) AS usage_date_utc,
    model AS model_version,
    SUM(input_tokens) AS input_no_cache,
    SUM(cache_write_tokens) AS cache_write_5m,
    SUM(cache_read_tokens) AS cache_read,
    SUM(output_tokens) AS output_tokens,
    SUM(cost_total) AS cost_total
  FROM calls
  WHERE provider='anthropic'
  GROUP BY 1,2
), prov AS (
  SELECT
    usage_date_utc,
    model_version,
    SUM(input_no_cache) AS input_no_cache,
    SUM(cache_write_5m) AS cache_write_5m,
    SUM(cache_read) AS cache_read,
    SUM(output_tokens) AS output_tokens
  FROM provider_daily_usage
  WHERE provider='anthropic'
  GROUP BY 1,2
)
SELECT
  prov.usage_date_utc,
  prov.model_version,

  prov.input_no_cache AS prov_input,
  ledger.input_no_cache AS ledger_input,
  (ledger.input_no_cache - prov.input_no_cache) AS diff_input,

  prov.cache_write_5m AS prov_cw,
  ledger.cache_write_5m AS ledger_cw,
  (ledger.cache_write_5m - prov.cache_write_5m) AS diff_cw,

  prov.cache_read AS prov_cr,
  ledger.cache_read AS ledger_cr,
  (ledger.cache_read - prov.cache_read) AS diff_cr,

  prov.output_tokens AS prov_out,
  ledger.output_tokens AS ledger_out,
  (ledger.output_tokens - prov.output_tokens) AS diff_out,

  ledger.cost_total AS ledger_cost
FROM prov
LEFT JOIN ledger
  ON ledger.usage_date_utc = prov.usage_date_utc
 AND ledger.model_version  = prov.model_version
ORDER BY prov.usage_date_utc, prov.model_version;
