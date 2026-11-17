import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// Logged activity: one row per meeting, call, email, note or task, against an
// account and, when there is one, an opportunity and a contact. Read-only for
// every agent that uses it.
//
// `gtm_activities` is a shared native model: every pipeline that reads
// activity declares it with this exact slug and these columns
// (scripts/native-models.json), so a project that installs several keeps one.
// Whatever logs your activity fills it: call-capture's scribe, a sequencer or
// recorder webhook, a play, a CSV, or `cargo-ai storage record create-bulk`.
// On a CRM, swap it for a connector-backed model of the CRM's engagements and
// map their columns onto these (`crm-backed` in SKILL.md).
export const gtmActivities = defineModel("gtm_activities", {
  name: "GTM activities",
  kind: "native",
  extractSlug: "defineCustom",
  config: {
    columns: [
      // gtm_accounts.id
      { slug: "account_id", type: "string" },
      // gtm_opportunities.id, or empty when not tied to one.
      { slug: "opportunity_id", type: "string" },
      // gtm_contacts.id, or empty when not tied to one.
      { slug: "contact_id", type: "string" },
      { slug: "occurred_at", type: "date" },
      // meeting | call | email | note | task
      { slug: "kind", type: "string" },
      { slug: "subject", type: "string" },
      { slug: "body", type: "string" },
      // Who on our side did it.
      { slug: "owner_email", type: "string" },
    ],
  },
  folder: modelsFolder,
});
