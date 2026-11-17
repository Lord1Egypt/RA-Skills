import { defineModel } from "@cargo-ai/cdk";

import { crm } from "../connectors/crm";
import { modelsFolder } from "../folders";

// The accounts behind the deals: industry, size and geography are what won
// versus lost is cut by. Declared exactly as crm-enrichment and
// crm-deduplication declare it, so a project running either keeps one model:
// drop this copy and import theirs.
export const crmAccounts = defineModel("crm_accounts", {
  folder: modelsFolder,
  connector: crm,
  extractSlug: "fetchRecords",
  config: { objectType: "companies", columnSelectionMode: "all" },
  schedule: { type: "cron", cron: "0 * * * *" },
});
