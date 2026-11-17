import { defineConnector } from "@cargo-ai/cdk";

// AI Ark: the lookalike source. It also searches by filter, but here its job
// is the one the other three cannot do well: find companies that look like
// the customers you name (`lookalikeDomains`). `countCompanies` is free and
// takes the same groups, so size it before you sync.
export const aiArk = defineConnector("ai_ark", {
  integration: "aiArk",
  default: true,
});
