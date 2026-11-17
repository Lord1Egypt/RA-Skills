import { defineAgent } from "@cargo-ai/cdk";

import { webScribePrompt } from "./web-scribe.prompt";
import { anthropic } from "../connectors/anthropic";
import { agentsFolder } from "../folders";

// The web scribe: a Claude Code harness agent on a weekly cron.
//
// `harness: "claudeCode"` swaps the LLM loop for the coding runtime, and that
// is what makes this cookbook possible. The output of a week is not a column
// value; it is a diff across markdown files under context/, plus the page and
// news files it wrote under cadence/, delivered as one pull request. Only an
// agent with a working tree can produce that diff, and only a pull request
// makes it reviewable before it becomes what every other agent believes.
//
// `connector` and `languageModel` are required even here. The harness does not
// bring its own model: it runs against Cargo's LLM proxy, which bills this
// connector and meters usage against this slug. Any Anthropic model works with
// `claudeCode`; see `../connectors/anthropic.ts`.
//
// The first run seeds whatever context/ domain is empty; every run after adds
// what changed that week. Run the first one by hand rather than waiting for
// Monday:
//
//   cargo-ai ai message create --agent-uuid <uuid> \
//     --parts '[{"type":"text","text":"Run the web capture. Follow your system prompt exactly."}]'
//
// No `state`, and nothing to put in one. Deploy binds this project's
// connected state (cargo.state.json) and the harness clones its repository at
// the state's directory and production branch, which is the correct binding:
// the repository holding context/ IS this project's. `cargo-ai project check`
// prints the binding; the state's directory must be where the agent's
// `npx tsx` resolves node_modules from, and a project whose state is not
// connected deploys this agent unbound.
//
// No `env` either, and no script. The domain and the pages are constants in
// ./web-scribe.prompt.ts, next to the exact commands the agent runs, so the
// harness picks up an edit on its next clone. The page read and the news
// search go through `cargo-ai`, which the sandbox is signed in to, so there is
// no credential anywhere in this cookbook.
//
// No `uses` and no `capabilities`. It reads the web with two `cargo-ai`
// commands, and the one thing it must never do is write the workspace context directly: a
// `context` capability here would be a second write path that skips the pull
// request.
export const webScribe = defineAgent("web_scribe", {
  name: "Web scribe",
  description:
    "Weekly: reads the company's website and the week's news, seeds any empty context/ domain, adds what changed as dated files, and opens one pull request.",
  color: "blue",
  harness: "claudeCode",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  triggers: [
    {
      type: "cron",
      name: "weekly",
      // 06:00 UTC every Monday, before anyone reads the repository. The news
      // window runs from the last merged baseline, so a quiet week that opened
      // no pull request is covered by the next one, not skipped.
      cron: "0 6 * * 1",
      text: "Run the weekly web capture. Follow your system prompt exactly: read the web, add what changed to context/, and open one pull request, or none when nothing changed.",
    },
  ],
  systemPrompt: webScribePrompt,
  folder: agentsFolder,
});
