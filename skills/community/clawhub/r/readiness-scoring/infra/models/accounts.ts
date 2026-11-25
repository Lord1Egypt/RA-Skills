import { defineModel } from "@cargo-ai/cdk";

import { readyThreshold, warmingThreshold } from "../settings";
import { accountEvents } from "./account-events";

// Unify Accounts: the account row reps and every other pipeline already read.
// The score lives here, on the account, as two columns:
//
//   - `readiness_score`, a metric: the sum of `readiness_contribution` over
//     the account's Account Events.
//   - `readiness_stage`, computed from the score and the two thresholds:
//     `ready_now`, `warming` or `cold`. The segments and the play read this,
//     never the score, so moving a threshold moves every account at the next
//     rebuild with no other edit.
//
// The metric aggregates over the relationship Account Events generates
// (`account_id` → `id`), read as `accountEvents.relationships.account_id`. It
// cannot be declared, and its uuid differs per workspace, so the adopt of
// Account Events publishes it. A workspace whose Account Events has never
// synced has no relationship yet: the deploy says so, and the fix is one sync
// of Account Events.
//
// ADOPTED, NOT CREATED, and on its own schedule: hourly at :10, after Account
// Events at :00, so the sum reads contributions computed the same hour.
//
// `additionalColumns` IS THE WHOLE LIST. A deploy removes every additional
// column of Unify Accounts that is not declared here, values included, and
// every pipeline and person in the workspace reads this model. Before the
// first deploy, read the live ones (`cargo-ai storage column list` on this
// model) and copy every one the workspace keeps into this list. A project
// declares this model once.
export const accounts = defineModel("accounts", {
  kind: "native",
  extractSlug: "unifyAccounts",
  schedule: { type: "cron", cron: "10 * * * *" },
  additionalColumns: [
    {
      kind: "metric",
      slug: "readiness_score",
      type: "number",
      label: "Readiness score",
      description:
        "Sum of the account's event contributions: rises with each fresh signal, falls as they age.",
      relationship: accountEvents.relationships.account_id,
      aggregation: {
        function: "SUM",
        columnSlug: "computed__readiness_contribution",
      },
    },
    {
      kind: "computed",
      slug: "readiness_stage",
      type: "string",
      label: "Readiness stage",
      description: `ready_now at ${readyThreshold} or more, warming at ${warmingThreshold} or more, cold below.`,
      imports: { readyThreshold, warmingThreshold },
      expression: (record) =>
        record.metric__readiness_score >= readyThreshold
          ? "ready_now"
          : record.metric__readiness_score >= warmingThreshold
            ? "warming"
            : "cold",
    },
  ],
});
