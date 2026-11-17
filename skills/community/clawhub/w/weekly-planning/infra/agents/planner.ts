import { defineAgent } from "@cargo-ai/cdk";

import { plannerPrompt } from "./planner.prompt";
import { anthropic } from "../connectors/anthropic";
import { agentsFolder } from "../folders";

// The planner: a Claude Code harness agent, not a streamText agent.
//
// `harness: "claudeCode"` swaps the LLM loop for the coding runtime, and that
// is what makes this skill possible. The output of a week is not a column
// value; it is one or more diffs — a raw dump plus one recommendation file
// per active initiative (or one workspace file when there are none). Only an
// agent with a working tree can produce those diffs, and only a pull request
// makes a recommendation reviewable before it is next week's work.
//
// `connector` and `languageModel` are required even here. The harness does not
// bring its own model: it runs against Cargo's LLM proxy, which bills this
// connector and meters usage against this slug. Any Anthropic model works with
// `claudeCode`; see `../connectors/anthropic.ts`.
//
// No `capabilities`, on purpose. The workspace half of the week — whoami, the
// week's runs, credits, what is even deployed — is read with Cargo's own CLI,
// which the harness already has: it clones a Cargo project, so `cargo-ai` (or
// its `npx @cargo-ai/cli` form) is right there next to the toolchain that
// project pins, and the plugin's own approval hook already treats those reads
// as the safe class. A capability would be a second path to the same data,
// wired in the release rather than in the prompt, and only the prompt can say
// "read, never execute" — which is the whole point here, because a
// recommendation is markdown a human merges, not a deploy. The commands are
// listed in `planner.prompt.ts` §1b.
export const planner = defineAgent("weekly_planning", {
  name: "Weekly planning",
  description:
    "Ranks last week's GTM work against active initiatives, declared infra, and live runs, and opens one reviewable pull request per initiative (or one workspace pull request when there are none).",
  color: "blue",
  harness: "claudeCode",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER — your model of choice
  // No `state`: deploy binds this project's connected state (cargo.state.json),
  // and the harness clones its repository at the state's directory and
  // production branch. That directory must hold the package.json declaring
  // `@cargo-ai/cdk`, where node_modules is and therefore the only place the
  // agent's `npx tsx …/collect/week.ts` resolves. In the scaffolded layout
  // that is the repository root, which is also where cadence/ and
  // initiatives/ live. `cargo-ai project check` prints the binding; a project
  // whose state is not connected deploys this agent unbound, with an empty
  // sandbox.
  env: {
    // IANA timezone the recapped ISO week is computed in. Public, so a
    // plain string rather than a secret. The cron is Monday 15:00 UTC,
    // which is 8am here during PDT; change both together if you move it.
    PLANNING_TIMEZONE: "America/Los_Angeles",
  },
  triggers: [
    {
      type: "cron",
      name: "weekly",
      // 15:00 UTC Monday: 8am PT during PDT, 7am PT during PST. Recaps the
      // ISO week that just ended. A Sunday run recaps an incomplete week;
      // keep the cron on Monday.
      cron: "0 15 * * 1",
      text: "Run weekly planning. Follow your system prompt exactly: write the dump, then open one pull request per active initiative, or one workspace pull request if there are none.",
    },
  ],
  systemPrompt: plannerPrompt,
  folder: agentsFolder,
});
