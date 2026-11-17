import { defineModel } from "@cargo-ai/cdk";

import { apollo } from "../connectors/apollo";
import { modelsFolder } from "../folders";

// The second census: Apollo's own database, searched with the same brief as
// Sales Navigator. Two independent enumerations of one market are what the
// coverage estimate in references/run.md is computed from.
//
// Apollo has no industry taxonomy: industries are keyword tags, which over-
// and under-match. That is acceptable here because nothing is trusted from the
// source's label: every company is classified from its own description in the
// profile play. Size the pool with a small `limit` first; there is no free count.
//
// NO SCHEDULE, ON PURPOSE: every sync re-bills every returned record.
export const tamSourceApollo = defineModel("tam_source_apollo", {
  name: "TAM source: Apollo",
  connector: apollo,
  extractSlug: "fetchOrganizations",
  description:
    "TAM source 3 of 4: Apollo organizations for the same brief, the second census.",
  folder: modelsFolder,

  // Into Accounts on the domain, the LinkedIn page and the LinkedIn id,
  // declared for the same reason as AI Ark's. `linkedin_uid` is the numeric
  // LinkedIn company id (20 of 20 rows in the live run, each equal to the id
  // the profile read), so a company Apollo and Sales Navigator both found
  // merges directly, before any profile. Cargo's default unification for
  // Apollo leaves it out.
  unification: {
    source: "custom",
    type: "account",
    uniqueColumns: [
      { slug: "primary_domain", reference: "domain" },
      { slug: "linkedin_uid", reference: "linkedinId" },
      { slug: "linkedin_url", reference: "linkedinHandle" },
      // Only a URL that carries the numeric id (/company/12345) yields one.
      { slug: "linkedin_url", reference: "linkedinId" },
    ],
  },

  // PLACEHOLDER: the same brief in Apollo's filters. Employee ranges are
  // strings in Apollo's "min,max" form; locations are free text.
  config: {
    filters: {
      q_organization_keyword_tags: [
        "saas",
        "b2b software",
        "developer tools",
        "cybersecurity",
      ],
      organization_num_employees_ranges: ["51,200", "201,500", "501,1000"],
      organization_locations: [
        "United States",
        "United Kingdom",
        "France",
        "Germany",
      ],
    },
    // PLACEHOLDER: the budget. Billing is per returned record.
    limit: 1000,
  },
});
