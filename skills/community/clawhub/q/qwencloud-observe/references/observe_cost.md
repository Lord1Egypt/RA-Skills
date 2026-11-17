# Observe Cost

Show **actual billed cost only** — never an estimate. Cost comes from BSS OpenAPI
`QueryInstanceBill` (per-instance settled/real amounts). Currency is USD (international site).

## Inputs from state

From `.qwencloud-deploy`: `outputs.ecs_instance_ids[]`, `outputs.db_instance_id`, `region_id`,
`created_at`. Use the instance IDs to pick this app's rows out of the account bill.

## Query real bill

Query per-instance bill for the target cycle(s) (`YYYY-MM`, last 18 months supported). Default to
the current cycle; when the user asks for a range, query each cycle.

```bash
aliyun bssopenapi QueryInstanceBill --BillingCycle <YYYY-MM> --IsBillingItem false --PageSize 300
```

For a specific day, add `--Granularity DAILY --BillingDate <YYYY-MM-DD>`.

`QueryInstanceBill` returns the whole account cycle. From `Data.Items.Item[]`, keep only rows whose
`InstanceID` matches this app's ECS/RDS IDs. Read `PretaxAmount` (payable), `Currency`,
`ProductCode` (e.g. `ecs`, `rds`), `SubscriptionType`, `BillingCycle`. Sum the matched rows for
this app's real cost, and report the ECS / RDS breakdown by `ProductCode`.

Reference: https://help.aliyun.com/en/user-center/developer-reference/call-api-operations-to-manage-resources-and-costs

## Month-end projection (optional)

When the user asks "roughly how much this month", project linearly from the current cycle's settled
amount:

```bash
aliyun bssopenapi QueryBill --BillingCycle <YYYY-MM> --Type PayAsYouGo --PageSize 300
```

Extrapolate the current-cycle paid amount by elapsed days
(`projected month-end = amount so far / elapsed days * days in month`). Label it clearly as a
**projection from the settled bill, not a billed amount**; still report the actual cost separately.

## No bill yet

- If no matching row exists for the cycle (e.g. just deployed, or the cycle has not been billed
  yet) → mark cost `unknown` with the reason "no actual bill for this cycle yet". Never fall back
  to an estimate and never fabricate a price.
- `QueryInstanceBill` permission failure → mark cost `unknown` with the missing permission.

## Result

Cost-layer summary: actual billed amount for this app in the cycle, ECS / RDS breakdown by
`ProductCode`, currency, and the billing cycle. All values are real billed amounts; never labeled
"estimate".
