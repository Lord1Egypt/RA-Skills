import { defineFolder } from "@cargo-ai/cdk";

// Every resource this skill deploys is filed under a folder named after the
// skill. A workspace accumulates resources from several skills plus whatever
// the team wrote by hand, and the folder is what answers "what put this here,
// and what else came with it" by looking. It is also what makes removing a
// skill bounded rather than a hunt.
//
// Folders are per-kind. This skill deploys two models and nothing else.
export const modelsFolder = defineFolder("visitor_identification_models", {
  kind: "model",
  name: "Visitor identification",
});
