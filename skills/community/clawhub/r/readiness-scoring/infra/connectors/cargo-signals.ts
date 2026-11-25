import { defineConnector } from "@cargo-ai/cdk";

// Cargo Signals: the feeds that land fundraising rounds and job offers on the
// accounts this skill watches. Billed per event delivered, in Cargo credits,
// with no key of its own, so `default: true` binds the workspace's connector
// the same way the AI Ark one binds in tam-building.
export const cargoSignals = defineConnector("cargo_signals", {
  integration: "cargoSignals",
  default: true,
});
