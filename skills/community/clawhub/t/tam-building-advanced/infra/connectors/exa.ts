import { defineConnector } from "@cargo-ai/cdk";

// Exa: search by meaning. It finds companies by what their website says they
// do, which is how it reaches the ones filed under an industry nobody would
// filter on. tam_source_exa syncs the queries in settings.ts through it.
export const exa = defineConnector("exa", {
  integration: "exa",
  default: true,
});
