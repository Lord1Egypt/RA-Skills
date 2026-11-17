import { defineFolder } from "@cargo-ai/cdk";

// One folder per pipeline, so "what put this agent here, and what came with
// it" is answered by looking, and removing the pipeline is a bounded job.
export const agentsFolder = defineFolder("website_auditing_agents", {
  kind: "agent",
  name: "Website auditing",
});

export const modelsFolder = defineFolder("website_auditing_models", {
  kind: "model",
  name: "Website auditing",
});
