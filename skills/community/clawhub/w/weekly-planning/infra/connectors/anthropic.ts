import { defineConnector } from "@cargo-ai/cdk";

// The model the planner runs on.
//
// A harness agent does not bring its own model. Claude Code runs inside the
// sandbox with `ANTHROPIC_BASE_URL` pointed at Cargo's proxy and a minted
// session token as its key, so every token it spends is billed to this
// connector and metered against the `languageModel` slug on the agent. Omit
// either and the release has no runtime to deploy.
//
// The connector's integration is also what selects the proxy: `anthropic` for
// `claudeCode`, `openCode` and `deepAgents`, `openAi` for `codex`. Pairing a
// harness with the wrong integration typechecks green and fails at deploy.
//
// `default: true` binds the workspace's existing Anthropic connector — the one
// authenticated once in the UI — rather than creating one, so this cookbook
// deploys with no env var of its own. It resolves the integration's default
// connector first and falls back to a slug match.
export const anthropic = defineConnector("anthropic", {
  integration: "anthropic",
  default: true,
});
