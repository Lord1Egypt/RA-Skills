import { defineConnector } from "@cargo-ai/cdk";

// Apollo: the second census. A different database searched with the same
// brief, which is what makes the Sales Navigator × Apollo overlap usable for
// the coverage estimate in references/run.md.
export const apollo = defineConnector("apollo", {
  integration: "apolloio",
  default: true,
});
