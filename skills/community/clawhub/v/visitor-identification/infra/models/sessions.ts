import { defineModel } from "@cargo-ai/cdk";

import { snitcher } from "../connectors/snitcher";
import { modelsFolder } from "../folders";
import { visitingCompanies } from "./companies";

// Every visit by an identified company: the organisation, when it started,
// the referrer and the pages viewed. Join it to the companies model on
// `organisation_uuid = uuid`. Sessions cost nothing beyond the companies.
//
// `workspaceUuid` is the Snitcher workspace the companies model provisioned.
// It is a token, so this model deploys after that one, in the same deploy.
export const visitorSessions = defineModel("website_visitor_sessions", {
  connector: snitcher,
  extractSlug: "fetchSessions",
  description:
    "Website sessions of the identified visiting companies, from Snitcher.",
  folder: modelsFolder,
  config: { workspaceUuid: visitingCompanies.config._workspaceUuid },
});
