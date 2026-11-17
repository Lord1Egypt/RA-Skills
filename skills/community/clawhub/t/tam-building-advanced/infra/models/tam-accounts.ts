import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";
import {
  countries,
  inScopeCategories,
  maxEmployees,
  minEmployees,
  subsidiaryThreshold,
  unknownCategory,
} from "../settings";

// One profile per company: what the profile play read from its LinkedIn page
// and how it classified it. Same columns whatever source found the company.
//
// It is also what makes the sources one market. Sales Navigator knows a
// company by its LinkedIn id, AI Ark by its domain and LinkedIn page name,
// Exa by its website; only Apollo carries the id and the domain together, and
// only for what it found. This row carries all three, and it unifies into
// Accounts too, so every source's row for the same company lands on one
// account.
//
// `status` and `exclusion_reason` are computed from settings.ts: the
// classifier labels the company, these columns decide what the label means.
// Nothing is deleted; read the TAM as `status = 'in_scope'`.

// The row the computed columns read. Native columns are typed only after
// `cargo-ai project types` has seen the model, so they are spelled out here.
type Row = {
  category?: string | null;
  subsidiary_probability?: number | null;
  employee_count?: number | null;
  hq_country?: string | null;
};

export const tamAccounts = defineModel("tam_accounts", {
  name: "TAM accounts",
  kind: "native",
  extractSlug: "defineCustom",
  description:
    "One row per company in the TAM: its LinkedIn page, your category, and whether it is in scope.",
  config: {
    columns: [
      { slug: "linkedin_id", type: "string" },
      { slug: "linkedin_url", type: "string" },
      { slug: "name", type: "string" },
      { slug: "domain", type: "string" },
      { slug: "account_domain", type: "string" },
      { slug: "website", type: "string" },
      { slug: "hq_country", type: "string" },
      { slug: "hq_city", type: "string" },
      { slug: "employee_count", type: "number" },
      { slug: "linkedin_industry", type: "string" },
      { slug: "description", type: "string" },
      { slug: "category", type: "string" },
      { slug: "subsidiary_probability", type: "number" },
      { slug: "profiled_at", type: "date" },
    ],
  },
  additionalColumns: [
    {
      kind: "computed",
      slug: "status",
      type: "string",
      label: "Status",
      description:
        "in_scope, out_of_scope or needs_review, from the category, the subsidiary probability, the headcount and the country against settings.ts.",
      imports: {
        inScopeCategories,
        unknownCategory,
        subsidiaryThreshold,
        minEmployees,
        maxEmployees,
        countries,
      },
      // A thin page, a missing headcount or a missing country is a gap in the
      // data, never a reason to drop the company: needs_review.
      expression: (record: Row) => {
        if (!record.category || record.category === unknownCategory) {
          return "needs_review";
        }
        if (
          record.employee_count === null ||
          record.employee_count === undefined ||
          !record.hq_country
        ) {
          return "needs_review";
        }
        if (
          !inScopeCategories.includes(record.category) ||
          (record.subsidiary_probability || 0) >= subsidiaryThreshold ||
          record.employee_count < minEmployees ||
          record.employee_count > maxEmployees ||
          !countries.includes(record.hq_country)
        ) {
          return "out_of_scope";
        }
        return "in_scope";
      },
    },
    {
      kind: "computed",
      slug: "exclusion_reason",
      type: "string",
      label: "Exclusion reason",
      description:
        "Why a company is not in scope: the first gate it failed. Empty when in scope.",
      imports: {
        inScopeCategories,
        unknownCategory,
        subsidiaryThreshold,
        minEmployees,
        maxEmployees,
        countries,
      },
      expression: (record: Row) => {
        if (!record.category || record.category === unknownCategory) {
          return "not_enough_information";
        }
        if (
          record.employee_count === null ||
          record.employee_count === undefined ||
          !record.hq_country
        ) {
          return "missing_size_or_country";
        }
        if (!inScopeCategories.includes(record.category)) {
          return "category: " + record.category;
        }
        if ((record.subsidiary_probability || 0) >= subsidiaryThreshold) {
          return "subsidiary_or_country_page";
        }
        if (
          record.employee_count < minEmployees ||
          record.employee_count > maxEmployees
        ) {
          return "size: " + record.employee_count;
        }
        if (!countries.includes(record.hq_country)) {
          return "country: " + record.hq_country;
        }
        return "";
      },
    },
  ],
  unification: {
    source: "custom",
    type: "account",
    // Two domains, both strong: the one LinkedIn gives and the one the
    // account already had. They differ more often than you would think
    // (`corporate.acme.example` on LinkedIn, `acme.example` at the source):
    // with only LinkedIn's, the profile becomes an account of its own and the
    // source account is never profiled (live, 2026-11-11).
    uniqueColumns: [
      { slug: "linkedin_id", reference: "linkedinId" },
      { slug: "domain", reference: "domain" },
      { slug: "account_domain", reference: "domain" },
      { slug: "linkedin_url", reference: "linkedinHandle" },
    ],
  },
  folder: modelsFolder,
});
