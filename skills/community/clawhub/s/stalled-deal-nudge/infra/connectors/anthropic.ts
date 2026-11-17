import { defineConnector } from "@cargo-ai/cdk";

// The model the nudger runs on. Every token a Monday's digest spends is billed
// to this connector and metered against the agent's `languageModel` slug.
//
// `default: true` binds the workspace's existing Anthropic connector rather
// than creating one, so this pipeline deploys with no env var of its own.
export const anthropic = defineConnector("anthropic", {
  integration: "anthropic",
  default: true,
});
