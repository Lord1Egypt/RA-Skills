import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The accounts this skill watches: the shared native accounts model every
// pipeline declares under this slug (scripts/native-models.json). A project
// that already has it keeps one copy; rewire the imports to it and delete this
// file. One slug declared twice collides at deploy.
//
// It is also what gives every signal an account. `defineAccount` unifies into
// the workspace's Unify Accounts on the row's website, so an event whose
// company domain matches a row here lands in Account Events with that
// account's id. An event about a company no account model holds is dropped
// from Account Events, and so never scores.
export const gtmAccounts = defineModel("gtm_accounts", {
  name: "GTM accounts",
  kind: "native",
  extractSlug: "defineAccount",
  folder: modelsFolder,
});
