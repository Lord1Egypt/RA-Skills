import { defineConnector } from "@cargo-ai/cdk";

// AI Ark: the company source. Bound with `default: true`, and it runs on
// Cargo's managed connection, so there is no key, no seat, and no cookie to
// configure. Every action bills in credits.
//
// Two of its actions matter here and they are deliberately split across the
// two things this skill does:
//
//   - `countCompanies` is FREE and takes exactly the same filter groups as the
//     search. It is a design-time CLI call, not a deployed resource: you run it
//     while shaping the ICP filter, and a resource that only ever wraps one
//     connector action is ceremony. See the count-first gate in the skill.
//   - `fetchCompanies` is the extractor on ../models/tam-companies.ts. It bills
//     PER RETURNED RECORD, which is why `limit` in that file is a budget rather
//     than a preference, and why the model carries no schedule.
export const aiArk = defineConnector("ai_ark", {
  integration: "aiArk",
  default: true,
});
