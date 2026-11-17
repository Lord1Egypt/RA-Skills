import { defineModel } from "@cargo-ai/cdk";

import { snitcher } from "../connectors/snitcher";
import { modelsFolder } from "../folders";

// The companies whose people visit the site: one row per organisation
// Snitcher resolves from a visit's IP address, with its website, industry and
// first and last visit. Company-level only: no person is identified.
//
// Creating it provisions a Snitcher workspace for `url` and writes two values
// into the model's config: `_workspaceUuid`, which the sessions model reads,
// and `_trackingScript`, the public installation snippet the site loads its
// tracker from. Both resolve in the same deploy through `visitingCompanies.config`.
//
// NO SCHEDULE. The extractor fetches incrementally on Cargo's own interval and
// refuses a cron. Each identified company is billed when it first lands here,
// so spend follows traffic: read the live price before deploying.
export const visitingCompanies = defineModel("website_visiting_companies", {
  connector: snitcher,
  extractSlug: "fetchOrganisations",
  description:
    "Companies identified visiting the website, from Snitcher. Company-level only.",
  folder: modelsFolder,
  config: {
    // PLACEHOLDER: the site's public HTTPS origin, the same value as its
    // `site.json` `canonicalUrl`. Changing it later provisions a new Snitcher
    // workspace, with a new tracker and none of the history.
    url: "https://www.example.com/",
  },
});
