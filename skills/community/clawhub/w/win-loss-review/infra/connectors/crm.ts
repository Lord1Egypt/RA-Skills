import { defineConnector } from "@cargo-ai/cdk";

// The CRM the deals live in, and the source of all three models. HubSpot is
// the checked example; Salesforce and Attio change the integration here and
// the models' config (references/crm-audit.md).
//
// Same slug as crm-enrichment's and crm-deduplication's connector, so a
// project running either shares one connection: drop this copy and import
// theirs. Bound, not created: authorize HubSpot once
// (`cargo-ai project add connector/hubspot`) and `default: true` resolves to it.
export const crm = defineConnector("crm", {
  integration: "hubspot",
  default: true,
});
