import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The companies the deals belong to, for the name the digest prints. A Cargo
// native account model (`defineAccount`: id, name, website, industry, ...),
// joined on `gtm_opportunities.account_id`.
//
// `gtm_accounts` is a shared native model (scripts/native-models.json): every
// pipeline that needs accounts declares it under this slug, so a project that
// installs several keeps one, with each pipeline's added columns merged.
export const gtmAccounts = defineModel("gtm_accounts", {
  name: "GTM accounts",
  kind: "native",
  extractSlug: "defineAccount",
  folder: modelsFolder,
});
