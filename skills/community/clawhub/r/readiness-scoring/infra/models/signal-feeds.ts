import { defineModel, type ModelUnificationSpec } from "@cargo-ai/cdk";

import { cargoSignals } from "../connectors/cargo-signals";
import { modelsFolder } from "../folders";
import { gtmAccounts } from "./gtm-accounts";

// Two Cargo Signals feeds on the accounts in `gtm_accounts`: rounds raised and
// jobs posted. Each is an ingest model: Cargo Signals pushes an event when it
// detects one, and the model never re-buys what it already holds.
//
// WATCHLIST, NOT MARKET. Both feeds watch only the accounts in `gtm_accounts`,
// matched on their website. Market scope would deliver, and bill, every round
// and every job posting in the market, most of them about companies no account
// model holds, which Account Events then drops.
//
// One feed per signal type, rather than the single account watchlist feed,
// because the score weighs by `signal_type`. The account watchlist feed tags
// every event `account_watchlist`, whatever happened, so a round and a job
// posting would weigh the same.
//
// The unification is declared, not left to the integration's default: an
// event lands in Account Events by the company's website or LinkedIn page, and
// `last_signal_date` is when it happened. That is the integration default for
// company signals today; declaring it keeps the score's input fixed if the
// default ever moves.
const watched = {
  kind: "watchlist",
  entities: {
    source: "model",
    modelUuid: gtmAccounts.uuid,
    domainColumnSlug: gtmAccounts.columns.website,
  },
};

// The spend ceiling. Cargo Signals bills per event delivered, and the first
// delivery on a new watchlist looks back months, so a cap per day is what
// keeps the first week from costing more than the rest of the quarter.
const advancedSettings = { dailyLeadLimit: 50 };

const accountEventUnification: ModelUnificationSpec = {
  source: "custom",
  type: "accountEvent",
  uniqueColumns: [
    { slug: "company.website", reference: "domain" },
    { slug: "company.linkedin_url", reference: "linkedinHandle" },
  ],
  timeColumnSlug: "last_signal_date",
};

export const fundraisingSignals = defineModel("readiness_fundraising_signals", {
  connector: cargoSignals,
  extractSlug: "listenFundraising",
  description:
    "Rounds raised by the accounts in gtm_accounts, from Cargo Signals. Each event lands in Account Events and moves the readiness score.",
  folder: modelsFolder,
  // One lead per company. Cargo Signals delivers a company event once per
  // contact it attaches, and bills each one: without this, one round arrives
  // as several events, each counted in the score and each billed.
  config: {
    scope: { ...watched, filters: { maxLeadsPerCompany: 1 } },
    advancedSettings,
  },
  unification: accountEventUnification,
});

export const jobOfferSignals = defineModel("readiness_job_offer_signals", {
  connector: cargoSignals,
  extractSlug: "listenJobOffers",
  description:
    "Jobs posted by the accounts in gtm_accounts, from Cargo Signals. Each event lands in Account Events and moves the readiness score.",
  folder: modelsFolder,
  // PLACEHOLDER: the titles that mean they are building the team you sell to.
  // Without a title filter every posting counts, and a company hiring
  // warehouse staff scores like one hiring a RevOps lead.
  config: {
    scope: {
      ...watched,
      filters: {
        job: {
          jobTitleInclude: ["Revenue Operations", "Sales Operations", "GTM"],
        },
      },
    },
    advancedSettings,
  },
  unification: accountEventUnification,
});
