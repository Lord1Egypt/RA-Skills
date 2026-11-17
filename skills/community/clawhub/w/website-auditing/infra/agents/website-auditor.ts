import { defineAgent } from "@cargo-ai/cdk";

import { websiteAuditorPrompt } from "./website-auditor.prompt";
import { anthropic } from "../connectors/anthropic";
import { slack } from "../connectors/slack";
import { agentsFolder } from "../folders";
import { websiteAudits } from "../models/website-audits";

// The auditor: how well AI agents can find, read and use the website, every
// week, and the fixes the site's own source can make.
//
// A Claude Code harness agent, because the fix is a diff to the website's
// source and only a harness has a checkout to make it in and a pull request to
// put it up for review. Merging that pull request is what deploys the fix.
//
// Ora is reached through its MCP server, not a connector: Cargo has no Ora
// integration, and the server's reads need no key. The agent keeps three of
// its tools. scan_domain and get_score read a domain's audit, and get_skill
// fetches Ora's fix playbook fresh each run, since agent standards move faster
// than this file. Every other tool is disabled: the feedback tools write to
// Ora, run_checks and a forced scan spend the daily scan budget Ora gives each
// IP, and the rest are product discovery this pipeline has no use for.
// `disabledToolSlugs` is a deny list, so a tool Ora adds later is enabled
// until it is named here.
//
// History is the website_audits model, one row per domain per week, because
// Ora keeps only the latest scan.
export const websiteAuditor = defineAgent("website_auditor", {
  name: "Website auditor",
  description:
    "Weekly Ora agent-readiness score for our website and competitors, one pull request with the fixes the site's source can make, and one Slack digest.",
  color: "purple",
  harness: "claudeCode",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  // No `state`: deploy binds this project's connected state (cargo.state.json),
  // and the harness clones its repository at the state's directory and
  // production branch. The website's source is in that checkout; when it is
  // in another project, see `separate-site-repo` in SKILL.md.
  env: {
    // PLACEHOLDER: the domain the website is served on.
    AUDIT_DOMAIN: "www.example.com",
    // PLACEHOLDER: at most three competitor domains, comma separated, or
    // empty. Each is one scan a week.
    COMPETITOR_DOMAINS: "fabrikam.example,contoso.example",
    // The website's source, relative to the checkout root. This is where
    // `cargo-ai project add cookbook/website-building` puts it.
    WEBSITE_ROOT: "infra/website-building/apps/website",
  },
  mcpClients: [
    {
      kind: "custom",
      name: "ora",
      url: "https://ora.ai/api/mcp",
      authentication: null,
      disabledToolSlugs: [
        "submit_feedback",
        "submit_check_feedback",
        "get_verification_challenge",
        "run_checks",
        "get_feedback",
        "get_leaderboard",
        "discover_products",
        "search_capabilities",
        "list_skills",
        "list_checks",
      ],
    },
  ],
  uses: [
    { ref: websiteAudits, readOnly: false },
    {
      ref: slack.actions.postMessage,
      config: {
        // PLACEHOLDER: the channel the digest lands in, as a Slack id (C…)
        // read from the connector's channel autocomplete. Locked.
        channelId: "C0123456789",
        format: "markdown",
        disableUnfurling: true,
      },
    },
  ],
  triggers: [
    {
      type: "cron",
      name: "weekly",
      // 08:00 UTC Monday: a week of merged fixes deployed, and the digest in
      // the channel before the team plans the week.
      cron: "0 8 * * 1",
      text: "Run the weekly website audit. Follow your system prompt exactly: score each domain once, record it, open at most one fix pull request, post one digest.",
    },
  ],
  systemPrompt: websiteAuditorPrompt,
  evaluator: {
    rubric:
      "Was each configured domain scanned at most once this week, without force, and recorded? Does every fix in the pull request map to a failing check in Ora's result, taken from topFixes first and then by points lost, and touch only the website's source? Was at most one digest posted, with every score and check taken from Ora's result and no gain claimed as measured?",
    threshold: 0.8,
  },
  folder: agentsFolder,
});
