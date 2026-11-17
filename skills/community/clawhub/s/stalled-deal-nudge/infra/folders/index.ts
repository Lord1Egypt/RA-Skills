import { defineFolder } from "@cargo-ai/cdk";

// One folder per pipeline, so "what put this agent here, and what came with
// it" is answered by looking, and removing the pipeline is a bounded job.
export const agentsFolder = defineFolder("stalled_deal_nudge_agents", {
  kind: "agent",
  name: "Stalled-deal nudge",
});

export const modelsFolder = defineFolder("stalled_deal_nudge_models", {
  kind: "model",
  name: "Stalled-deal nudge",
});
