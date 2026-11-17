import { definePlay, defineWorkflow } from "@cargo-ai/cdk";
import { z } from "zod";

import { linkedin } from "../connectors/linkedin";
import { playsFolder } from "../folders";
import { accounts } from "../models/accounts";
import { tamAccounts } from "../models/tam-accounts";
import { tamSourceAiArk } from "../models/tam-source-ai-ark";
import { tamSourceApollo } from "../models/tam-source-apollo";
import { tamSourceExa } from "../models/tam-source-exa";
import { tamSourceSalesNavigator } from "../models/tam-source-sales-navigator";
import { companyDomain } from "../scripts/company-domain";
import {
  inScopeCategories,
  outOfScopeCategories,
  unknownCategory,
} from "../settings";

// The options the classifier picks from: your categories, then what a company
// can be instead. Built here because a workflow body cannot map an array.
const categoryOptions = [
  ...inScopeCategories,
  ...outOfScopeCategories,
  unknownCategory,
].map((option) => ({ option }));

// The two questions put to every company.
const classifyQuestions = [
  {
    type: "choice",
    id: "category",
    instructions:
      "Which category describes what this company sells and to whom? Judge from the description, not from the industry label. If the description is too thin to tell, pick Not enough information.",
    options: categoryOptions,
  },
  {
    type: "noul",
    id: "subsidiary",
    instructions:
      "Is this page a subsidiary, a regional or country page, or an acquired brand of a larger company, rather than an independent company?",
  },
] as const;

// One account in, one profile out. Runs once per company, after Cargo has
// merged what every source found, so a company four sources found is read and
// classified once.
//
// 1. LinkedIn company enrich. The account's LinkedIn page when a source gave
//    one (Sales Navigator's id, AI Ark's or Apollo's URL), else its domain
//    (Exa). The enrich returns the LinkedIn id, the page and the domain: the
//    same identity, the same columns, whatever source found the company.
// 2. Classification into your categories, from the company's own description,
//    and the subsidiary question, in one call.
// 3. One row in tam_accounts. It unifies back into the same account, which is
//    what joins a Sales Navigator row and an AI Ark row for the same company.
const profileCompany = defineWorkflow(
  "tam_profile_company_workflow",
  {
    // Unify Accounts' own golden columns, already normalised by Cargo: a
    // numeric LinkedIn id, a LinkedIn page name, a bare domain.
    input: z.object({
      id: z.string(),
      domain: z.string().optional(),
      linkedin_id: z.string().optional(),
      linkedin_handle: z.string().optional(),
    }),
    output: z.object({
      result: z.enum(["profiled", "unresolved"]),
    }),
    uses: { linkedin },
    imports: {
      tamAccounts,
      classifyQuestions,
      companyDomain,
    },
  },
  ({ input, uses, model, classify }) => {
    const page = input.linkedin_id || input.linkedin_handle;
    if (!page && !input.domain) {
      return { result: "unresolved" as const };
    }

    // The account's LinkedIn page when a source gave one, else its domain
    // (Exa). Only the taken lookup runs.
    const company = page
      ? uses.linkedin.enrichCompany({
          linkedinUrl: `https://www.linkedin.com/company/${page}`,
        })
      : uses.linkedin.enrichCompanyFromDomain({ domain: input.domain || "" });
    if (!company.company_id) {
      return { result: "unresolved" as const };
    }

    const judged = classify({
      state: {
        name: company.company_name,
        website: company.website,
        linkedin_industry: company.industries[0],
        description: company.description,
      },
      questions: classifyQuestions,
    });
    model.upsert({
      modelUuid: tamAccounts.uuid,
      matchingColumnSlug: "linkedin_id",
      matchingValue: company.company_id,
      mappings: [
        { columnSlug: "linkedin_id", value: company.company_id },
        { columnSlug: "linkedin_url", value: company.linkedin_url },
        { columnSlug: "name", value: company.company_name },
        {
          columnSlug: "domain",
          // Never blank, never a short link: LinkedIn's domain when it is
          // real, else the account's, else where LinkedIn's short link lands.
          value: companyDomain({
            linkedinDomain: company.domain,
            linkedinWebsite: company.website,
            sourceDomain: input.domain || "",
          }),
        },
        { columnSlug: "account_domain", value: input.domain || "" },
        { columnSlug: "website", value: company.website },
        { columnSlug: "hq_country", value: company.hq_country },
        { columnSlug: "hq_city", value: company.hq_city },
        { columnSlug: "employee_count", value: company.employee_count },
        { columnSlug: "linkedin_industry", value: company.industries[0] },
        { columnSlug: "description", value: company.description },
        { columnSlug: "category", value: judged.answers.category.choice },
        {
          columnSlug: "subsidiary_probability",
          value: judged.answers.subsidiary.noul,
        },
        { columnSlug: "profiled_at", value: new Date() },
      ],
    });
    return { result: "profiled" as const };
  },
);

// The only play, and a build step, not an always-on automation. The sources
// carry no schedule, so new companies only arrive when you re-source; the play
// runs once, as a batch, after each source sync (references/run.md). No
// schedule and never enabled: a play with no schedule never runs on its own.
// `once` means a re-run after a refresh pays only for the companies that are
// new.
//
// Its filter is what the batch runs over: the accounts at least one TAM
// source found and no profile covers yet. A related-model condition reads the
// source's row on the account, NULL when that source did not find it.
export const profileCompanies = definePlay("tam_profile_companies", {
  name: "TAM: profile company",
  description:
    "For every account a TAM source found and no profile covers: LinkedIn company enrich, classify into your categories, write one row in tam_accounts.",
  folder: playsFolder,
  model: accounts,
  workflow: profileCompany,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "or",
        conditions: [
          {
            kind: "string",
            relatedModelUuid: tamSourceSalesNavigator.uuid,
            columnSlug: "sales_navigator_company_id",
            operator: "isNotEmpty",
          },
          {
            kind: "string",
            relatedModelUuid: tamSourceAiArk.uuid,
            columnSlug: "id",
            operator: "isNotEmpty",
          },
          {
            kind: "string",
            relatedModelUuid: tamSourceApollo.uuid,
            columnSlug: "id",
            operator: "isNotEmpty",
          },
          {
            kind: "string",
            relatedModelUuid: tamSourceExa.uuid,
            columnSlug: "domain",
            operator: "isNotEmpty",
          },
        ],
      },
      {
        conjonction: "and",
        conditions: [
          {
            kind: "string",
            relatedModelUuid: tamAccounts.uuid,
            columnSlug: "linkedin_id",
            // isNull, not isEmpty: an account no profile covers has no
            // tam_accounts row, so the joined column is NULL, and isEmpty
            // only matches an empty string (0 accounts, live 2026-11-11).
            operator: "isNull",
          },
        ],
      },
    ],
  },
  isEnabled: false,
  runCreationRule: "once",
  changeKinds: ["added"],
});
