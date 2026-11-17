import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The open pipeline, as a Cargo native deal model: no connector, no key, so
// this example deploys in an empty workspace. The `defineDeal` extractor gives
// the standard deal schema (id, name, account_id, amount, stage_name,
// close_date, probability, next_step, is_closed, is_won, owner_id, ...).
//
// Nothing here decides what "stalled" means. That is a question, and it is
// asked in the agent's SQL in `../agents/nudger.prompt.ts`.
//
// Deals live in a CRM? Swap this for a connector-backed model that extracts
// every deal and every column (`fetchRecords`, `columnSelectionMode: "all"`)
// and adapt the column names in the prompt's SQL. SKILL.md, `crm-backed`.
//
// `gtm_opportunities` is a shared native model (scripts/native-models.json): every
// pipeline that needs opportunities declares it under this slug, so a project that
// installs several keeps one, with each pipeline's added columns merged.
export const gtmOpportunities = defineModel("gtm_opportunities", {
  name: "GTM opportunities",
  kind: "native",
  extractSlug: "defineDeal",
  folder: modelsFolder,
});
