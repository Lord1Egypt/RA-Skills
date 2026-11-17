import { defineConnector } from "@cargo-ai/cdk";

// The model the win-loss review agent runs on.
//
// A harness agent does not bring its own model: it runs inside the sandbox
// with `ANTHROPIC_BASE_URL` pointed at Cargo's proxy and a minted session
// token as its key, so every token it spends is billed to this connector and
// metered against the `languageModel` slug on the agent.
//
// The connector's integration is also what selects the proxy: `anthropic` for
// `claudeCode`, `openCode` and `deepAgents`, `openAi` for `codex`. Pairing a
// harness with the wrong integration typechecks green and fails at deploy.
//
// `default: true` binds the workspace's existing Anthropic connector, the one
// authenticated once in the UI, rather than creating one, so this cookbook
// deploys with no env var of its own.
export const anthropic = defineConnector("anthropic", {
  integration: "anthropic",
  default: true,
});
