# Billing and Cost Control

Read the capability's `billing` object before submitting. Price and availability come from the live Capability Registry and can change without a Skill update.

- `mode: fixed`: use `credits` as the request price.
- `mode: input_count`: combine `base_credits`, `unit_credits`, and `unit_size` for submitted inputs.
- `mode: base_plus_result`: combine the base price with the per-result rate; the final charge depends on returned records.
- `dynamic: true`: do not interpret a zero base price as a free request.

Before a large job:

1. Call `socq_account` or `socq account`.
2. Inspect the endpoint's credits and billing unit.
3. Reduce `results_limit` or platform count when the user has not authorized a large spend.
4. Submit one representative platform first when input quality is uncertain.

API keys may have hourly and daily credit ceilings in addition to the account balance. A rate/credit limit response is not a provider failure; wait for the indicated reset or ask the user to adjust scope.
