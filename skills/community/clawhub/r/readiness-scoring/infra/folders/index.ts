import { defineFolder } from "@cargo-ai/cdk";

// Every resource this skill deploys is filed under folders named after the
// skill, not under a shared "GTM" one. A workspace accumulates resources from
// several skills plus whatever the team wrote by hand, and the folder is what
// answers "what put this here, and what else came with it" by looking. It is
// also what makes removing a skill bounded rather than a hunt.
//
// Folders are per-kind, which is why there are two: this skill deploys models
// and a play, and no agent. Account Events is the workspace's own model and is
// not filed here.
export const modelsFolder = defineFolder("readiness_scoring_models", {
  kind: "model",
  name: "Readiness scoring",
});

export const playsFolder = defineFolder("readiness_scoring_plays", {
  kind: "play",
  name: "Readiness scoring",
});
