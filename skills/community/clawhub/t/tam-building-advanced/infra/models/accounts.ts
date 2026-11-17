import { defineModel } from "@cargo-ai/cdk";

// Unify Accounts: the one account layer of the workspace. Every source model
// of this skill, the profile model and the CRM's companies unify into it, and
// Cargo does the merge: one account per company, whatever found it, with each
// source's row attached. That is where "found by" and "already in the CRM" are
// read from: the account's `ids` lists the rows of every model that unified
// into it.
//
// ADOPTED, NOT CREATED. Every workspace with a system of record has this
// model; a deploy finds it by its extractor and takes it over.
//
// NOTHING ELSE IS DECLARED ON PURPOSE. Leaving `additionalColumns`, `schedule`
// and `config` out leaves the live ones untouched; declaring any of them makes
// the declaration the whole list, and other pipelines read this model. A
// project declares it once: if another pipeline already does
// (readiness-scoring, account-scoring's unified-account), import that one.
export const accounts = defineModel("accounts", {
  name: "Accounts",
  kind: "native",
  extractSlug: "unifyAccounts",
});
