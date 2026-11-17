import { defineFolder } from "@cargo-ai/cdk";

// Every resource this skill deploys is filed under folders named after it, so
// "what put this here, and what came with it" is answered by looking, and
// removing the skill is bounded rather than a hunt.
export const modelsFolder = defineFolder("tam_building_advanced_models", {
  kind: "model",
  name: "TAM building, advanced",
});

export const playsFolder = defineFolder("tam_building_advanced_plays", {
  kind: "play",
  name: "TAM building, advanced",
});
