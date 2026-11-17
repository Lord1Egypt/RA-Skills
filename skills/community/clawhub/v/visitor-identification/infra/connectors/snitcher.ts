import { defineConnector } from "@cargo-ai/cdk";

// Snitcher on Cargo's credits. `default: true` binds the workspace's default
// Snitcher connection instead of creating one, so there is no Snitcher account
// or API key to manage: creating the companies model provisions a Snitcher
// workspace for the site, and Cargo bills the identified companies.
//
// A workspace on its own Snitcher key selects an existing Snitcher workspace
// instead, and provisions nothing; this skill is written for the managed path.
export const snitcher = defineConnector("snitcher", {
  integration: "snitcher",
  default: true,
});
