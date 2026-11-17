import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The ledger: one row per deal nudged per week. `week` plus `opportunity_id` is the
// idempotency key.
//
// The agent leaves out any deal that already has a row for this ISO week, and
// appends rows only after the owner's digest was posted. A re-run on the same
// Monday therefore posts nothing new, and a failed post is retried by the next
// run rather than recorded as sent.
//
// It is also the memory a nudge needs: how many weeks running a deal has been
// flagged. A deal on its third Monday reads differently from one on its first,
// and only the ledger knows.
export const dealNudges = defineModel("deal_nudges", {
  kind: "native",
  extractSlug: "defineCustom",
  config: {
    columns: [
      // The deal id (gtm_opportunities.id).
      { slug: "opportunity_id", type: "string" },
      // ISO week the nudge belongs to, e.g. 2026-W41.
      { slug: "week", type: "string" },
      { slug: "nudged_at", type: "string" },
      { slug: "owner_id", type: "string" },
      { slug: "deal_name", type: "string" },
      { slug: "days_quiet", type: "number" },
      // The Slack ts of the digest the deal appeared in.
      { slug: "slack_ts", type: "string" },
    ],
  },
  folder: modelsFolder,
});
