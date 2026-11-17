import { defineConnector } from "@cargo-ai/cdk";

// The identity and enrichment layer. Every company, whatever source found it,
// is resolved to its LinkedIn company page and read from there, so a row found
// by Exa carries exactly the columns of a row found by Sales Navigator.
export const linkedin = defineConnector("linkedin", {
  integration: "linkedin",
  default: true,
});
