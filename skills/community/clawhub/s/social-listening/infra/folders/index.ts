import { defineFolder } from "@cargo-ai/cdk";

// One folder per pipeline, so "what put this here, and what came with it" is
// answered by looking, and removing the pipeline is a bounded job.
export const agentsFolder = defineFolder("social_listening_agents", {
  kind: "agent",
  name: "Social listening",
});

export const modelsFolder = defineFolder("social_listening_models", {
  kind: "model",
  name: "Social listening",
});
