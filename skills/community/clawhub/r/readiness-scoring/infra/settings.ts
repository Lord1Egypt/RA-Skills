// The settings an operator changes without touching the graph. The score
// columns, the segments and the play are all generated from them, so edit here,
// run `cargo-ai project plan`, and read what moved.

// What each signal is worth on the day it lands, and how many days it takes to
// lose half of that. The key is the event's signal type: the `signal_type`
// Cargo Signals puts in the Account Events `properties` (`fundraising`,
// `job_offers`, …), or, for an event that carries none, the slug of the model
// it came from (a `demo_requests` model, a CRM's `meetings`). An event whose
// key is not listed here weighs nothing: a new feed must not move a score
// until someone has decided what it is worth.
//
// PLACEHOLDER: these two are the Cargo Signals feeds this example deploys.
// references/weights.md has defaults for the other signal types and for
// first-party events (demo requests, pricing-page visits), and the reasoning
// behind a half-life.
export const signals: Record<string, { weight: number; halfLifeDays: number }> =
  {
    fundraising: { weight: 10, halfLifeDays: 120 },
    job_offers: { weight: 4, halfLifeDays: 21 },
  };

// The score lines. A score at or above `readyThreshold` is `ready_now`, the
// segment the play routes from; at or above `warmingThreshold` it is
// `warming`. Both are in the same unit as the weights: with the weights above,
// a fresh round alone is ready, and two fresh job offers are warming.
//
// PLACEHOLDER until the pilot: set them from the score distribution the pilot
// query returns (references/run.md), not from a guess.
export const readyThreshold = 8;
export const warmingThreshold = 4;

// How far back an event counts. Older events contribute 0, which keeps a
// stale event from holding a score up by a rounding error. Three half-lives
// of the slowest signal leaves an event at an eighth of its weight, which no
// threshold above should hinge on.
export const horizonDays =
  3 * Math.max(...Object.values(signals).map((signal) => signal.halfLifeDays));
