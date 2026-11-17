import { defineAgent } from "@cargo-ai/cdk";

import { nudgerPrompt } from "./nudger.prompt";
import { anthropic } from "../connectors/anthropic";
import { slack } from "../connectors/slack";
import { agentsFolder } from "../folders";
import { gtmAccounts } from "../models/gtm-accounts";
import { gtmActivities } from "../models/gtm-activities";
import { gtmOpportunities } from "../models/gtm-opportunities";
import { dealNudges } from "../models/deal-nudges";

// The nudger: every Monday, one Slack digest per owner listing the open deals
// that went quiet, why each is worth a touch now, and a draft follow-up.
//
// One agent on a cron, not a play plus a per-deal workflow. The output is a
// digest grouped by owner, and grouping is a judgment over the whole list: a
// play enrolls deals one by one and would need a second step to gather them
// back into one post per owner. The agent selects the stalled deals itself, in
// SQL over the deal and activity models, so the "quiet for N days" rule is a
// query anyone can read in `nudger.prompt.ts`, not a segment filter.
//
// The example runs on Cargo native models and needs no CRM connector. With
// deals in HubSpot, Salesforce or Attio, swap `gtm_opportunities` and `gtm_activities` for
// connector-backed models (SKILL.md, `crm-backed`); this file does not change.
//
// What it may touch:
//   - `gtm_opportunities`, `gtm_accounts`, `gtm_activities`, read-only.
//   - `deal_nudges`, writable: the weekly ledger, the only thing it writes.
//   - `slack.postMessage` with the channel locked.
// A nudge that could move a stage would change the forecast from a guess.
export const nudger = defineAgent("stalled_deal_nudger", {
  name: "Stalled-deal nudger",
  description:
    "Each Monday, posts one Slack digest per owner of the open deals that went quiet, with why each matters now and a draft follow-up.",
  color: "yellow",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  // Per-run ceiling. A Monday of twenty stalled deals at a read or two each
  // plus one post per owner fits; a backlog bigger than that posts what it has, and
  // the ledger lets the next run pick up the rest.
  maxSteps: 80,
  capabilities: [
    // Read-only: positioning, objections, competitors. What makes a draft
    // specific to us.
    { slug: "context", config: { isReadOnly: true } },
  ],
  uses: [
    { ref: gtmOpportunities, readOnly: true },
    { ref: gtmAccounts, readOnly: true },
    { ref: gtmActivities, readOnly: true },
    { ref: dealNudges, readOnly: false },
    {
      ref: slack.actions.postMessage,
      config: {
        // PLACEHOLDER: the channel the digests land in, as a Slack id (C…)
        // read from the connector's channel autocomplete. Locked so a digest
        // that quotes deal amounts never lands in a customer shared channel.
        channelId: "C0123456789",
        format: "markdown",
        disableUnfurling: true,
      },
    },
  ],
  triggers: [
    {
      type: "cron",
      name: "monday_morning",
      // 15:00 UTC on Mondays: 8am PT during PDT, 7am PT during PST. Before the
      // pipeline meeting. Move it and the timezone
      // in `text` together.
      cron: "0 15 * * 1",
      text: "Post this week's stalled-deal digests. Today is the current date in America/Los_Angeles. Follow your system prompt exactly: select in SQL, dedupe against deal_nudges for this ISO week, research, post one digest per owner, record each post.",
    },
  ],
  systemPrompt: nudgerPrompt,
  // The QA gate on every run.
  evaluator: {
    rubric:
      "Was there at most one digest per owner, none repeating a deal already in deal_nudges for this week? Is every quoted line and date traceable to a row in activities? Does each draft pick up from the deal's own last activity rather than a generic check-in?",
    threshold: 0.8,
  },
  folder: agentsFolder,
});
