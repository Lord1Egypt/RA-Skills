import { defineModel } from "@cargo-ai/cdk";

import { linkedin } from "../connectors/linkedin";
import { modelsFolder } from "../folders";

// The week's public LinkedIn posts about the problem you solve.
//
// A paid search source, so the query in `config` is what decides what you buy:
// `fetchPosts` bills per returned post. That is why the search lives here and
// not in SQL downstream, the one exception to "models pull all the data".
//
// PLACEHOLDER: `searchKeywords`. Derive it from the workspace context, never
// from memory: the pains the ICP names in its own words, the category term,
// and competitor names. LinkedIn reads OR between quoted phrases. Keep it to
// the phrases a buyer would write, not your positioning copy: nobody posts
// "revenue orchestration platform", people post "our lead routing broke again".
//
// Weekly and capped. `limit` is LinkedIn's page of 20 to 100; the schedule
// re-buys the search every Monday, and `datePosted: "Past week"` is what makes
// each sync a new week rather than a re-read of the last one.
//
// A sync REPLACES the rows: the extractor is not incremental. That is why
// "already surfaced" lives in `surfaced_posts`, not here.
export const linkedinPosts = defineModel("linkedin_posts", {
  connector: linkedin,
  extractSlug: "fetchPosts",
  description:
    "The week's public LinkedIn posts matching the buyer-language keywords. Read by the social listener; re-synced every Monday.",
  folder: modelsFolder,
  config: {
    searchKeywords:
      '"lead routing" OR "speed to lead" OR "revops stack" OR "Northwind Router"',
    sortBy: "Latest",
    datePosted: "Past week",
    limit: 40,
  },
  // 05:00 UTC Monday, two hours before the listener runs.
  schedule: { type: "cron", cron: "0 5 * * 1" },
});
