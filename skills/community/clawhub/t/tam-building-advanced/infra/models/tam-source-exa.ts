import { defineModel } from "@cargo-ai/cdk";

import { exa } from "../connectors/exa";
import { modelsFolder } from "../folders";
import { exaQueries, exaResultsPerQuery } from "../settings";

// The search by meaning: companies found by what their website says they do,
// which reaches the ones filed under an industry nobody would filter on. The
// queries live in settings.ts; a sync runs each one once and keeps one row per
// company, with the firmographics Exa returns (name, headcount, headquarters,
// founding year).
//
// NO SCHEDULE, ON PURPOSE: every sync re-runs every query and re-bills every
// returned result.
export const tamSourceExa = defineModel("tam_source_exa", {
  name: "TAM source: Exa",
  connector: exa,
  extractSlug: "fetchSearch",
  description:
    "TAM source 4 of 4: companies Exa found for the written queries in settings.ts, one row each.",
  folder: modelsFolder,

  // Into Accounts on the domain, the only key Exa returns. Declared rather
  // than left to the integration's default, so the TAM does not move if the
  // default ever does.
  unification: {
    source: "custom",
    type: "account",
    uniqueColumns: [{ slug: "domain", reference: "domain" }],
  },

  config: {
    queries: exaQueries,
    // One result per company. Any other category returns pages on
    // publishers' domains, which must never become accounts.
    category: "company",
    // The budget: queries × results per query, billed per returned result.
    numResults: exaResultsPerQuery,
  },
});
