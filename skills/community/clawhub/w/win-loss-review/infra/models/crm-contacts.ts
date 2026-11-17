import { defineModel } from "@cargo-ai/cdk";

import { crm } from "../connectors/crm";
import { modelsFolder } from "../folders";

// The people on the deals, for the titles the personas are reconciled
// against. Declared exactly as crm-enrichment and crm-deduplication declare
// it, so a project running either keeps one model: drop this copy and import
// theirs. The audit reads titles and ids only, never an email.
export const crmContacts = defineModel("crm_contacts", {
  folder: modelsFolder,
  connector: crm,
  extractSlug: "fetchRecords",
  config: { objectType: "contacts", columnSelectionMode: "all" },
  schedule: { type: "cron", cron: "0 * * * *" },
});
