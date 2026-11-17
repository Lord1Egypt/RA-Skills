import { defineModel } from "@cargo-ai/cdk";

import { crm } from "../connectors/crm";
import { modelsFolder } from "../folders";

// Every deal, every column, extracted as is. The model never filters: open
// deals, closed deals and every property land in storage, and the audit
// narrows with SQL (closed deals, the window, the columns each query needs).
// A filter here would be a second place the question is asked, invisible to
// anyone reading the queries, and changing it would mean a redeploy and a
// re-extraction instead of an edited query.
//
// Extraction bills no credits, and the agent reads it with SQL as
// `crm.crm_deals`. The deals carry amounts; no query selects one, and the
// contract fails if one does, so no amount reaches context/, which every
// agent reads, including the ones that talk to prospects.
//
// `hs_primary_associated_company` joins a deal to `crm_accounts`, and titles
// are read at the won accounts through `crm_contacts.associatedcompanyid`.
// Titles on the deal itself (its associated contacts) are the `deal_contacts`
// variation: add `associationObjectTypes: ["contacts"]` here and read the
// column it creates after the sync.
export const crmDeals = defineModel("crm_deals", {
  folder: modelsFolder,
  connector: crm,
  extractSlug: "fetchRecords",
  config: { objectType: "deals", columnSelectionMode: "all" },
  schedule: { type: "cron", cron: "0 * * * *" },
});
