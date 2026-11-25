import { defineModel } from "@cargo-ai/cdk";

import { horizonDays, signals } from "../settings";

const weights = Object.fromEntries(
  Object.entries(signals).map(([key, signal]) => [key, signal.weight]),
);
const halfLives = Object.fromEntries(
  Object.entries(signals).map(([key, signal]) => [key, signal.halfLifeDays]),
);

// Unify Account Events: one row per event on an account, from every model that
// unifies as an account event (the Cargo Signals feeds, a CRM's activities, a
// product's usage events). A new feed reaches the score by unifying here, with
// no edit to the score.
//
// ADOPTED, NOT CREATED. Every workspace has this model; a deploy finds it by
// its extractor and takes it over. It sets two things on it:
//
//   - `readiness_contribution`, the column below.
//   - The schedule. A sync of Account Events first syncs the models that feed
//     it, then rebuilds it and recomputes the column, so this hourly cron is
//     what moves a delivered signal into the score, and what ages the ones
//     already there. It runs at :00; Unify Accounts sums the column at :10 and
//     the play reads the stage at :20.
//
// `additionalColumns` IS THE WHOLE LIST. A deploy removes every additional
// column of this model that is not declared here, values included. Before the
// first deploy, read the live ones (`cargo-ai storage column list` on this
// model) and copy every one the workspace keeps into this list. A project
// declares this model once: another pipeline that adds columns to it adds them
// here.
export const accountEvents = defineModel("account_events", {
  kind: "native",
  extractSlug: "unifyAccountEvents",
  schedule: { type: "cron", cron: "0 * * * *" },
  additionalColumns: [
    {
      kind: "computed",
      slug: "readiness_contribution",
      type: "number",
      label: "Readiness contribution",
      description:
        "What this event adds to its account's readiness score today: weight × 0.5 ^ (age / half-life), from readiness-scoring's settings.ts.",
      // What one event adds to its account's score today, keyed by the Cargo
      // Signals `signal_type` in `properties`, or the source model's slug for
      // an event that has none. An unweighed key, an event with no date, or
      // one older than the horizon contributes 0. The clock is read when the
      // column is computed, which is every rebuild of this model, so the value
      // falls on its own between signals.
      //
      // The function runs in the warehouse, not here: only `imports` reach it.
      imports: { weights, halfLives, horizonDays },
      expression: (record) => {
        const key =
          record.properties && record.properties.signal_type
            ? record.properties.signal_type
            : record.model_slug;
        const weight = weights[key];
        if (
          weight === undefined ||
          record.occurred_at === null ||
          record.occurred_at === undefined
        ) {
          return 0;
        }
        const ageDays =
          (Date.now() - new Date(record.occurred_at).getTime()) / 86400000;
        if (ageDays > horizonDays) {
          return 0;
        }
        return weight * Math.pow(0.5, ageDays / halfLives[key]);
      },
    },
  ],
});
