import { defineAgent } from "@cargo-ai/cdk";

import { listenerPrompt } from "./listener.prompt";
import { anthropic } from "../connectors/anthropic";
import { linkedin } from "../connectors/linkedin";
import { slack } from "../connectors/slack";
import { agentsFolder } from "../folders";
import { linkedinPosts } from "../models/linkedin-posts";
import { surfacedPosts } from "../models/surfaced-posts";

// The listener: once a week, which public conversations are worth joining and
// who in them looks like a buyer.
//
// The model does the buying (one capped keyword search, synced Monday at 05:00
// UTC); the agent does the judging. It reads the week's posts, drops the ones
// already surfaced, picks at most five against the ICP and pains in the
// workspace context, reads comments only on those, and posts one digest.
//
// Comments, not reactions. A comment is a person saying something in public
// about the problem; a reaction is a click. `searchPostReactions` bills per
// reactor and returns no words to quote, so it is left off `uses` (the
// `with-reactions` variation in SKILL.md adds it back).
//
// No engagement action, ever. likePost, commentPost, connectProfile and
// messageProfile live on the same connector; none is on `uses`, and the
// contract fails if one is added. The digest is for a human who decides.
//
// The engagers are not stored. They appear in that week's digest, quoted from
// a public comment, and the ledger keeps only the post. A standing list of
// people who commented is a list nobody gave a basis for.
export const listener = defineAgent("social_listener", {
  name: "Social listener",
  description:
    "Weekly digest of the LinkedIn conversations worth joining, and the commenters in them who match the ICP.",
  color: "yellow",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  // Context and post reads, at most five comment pulls, one post and a few
  // ledger rows, with room left over so the post always fits.
  maxSteps: 40,
  capabilities: [
    // Read-only: the ICP, the pains in the buyer's words, competitors. The
    // rubric for "worth joining" and "looks like a buyer".
    { slug: "context", config: { isReadOnly: true } },
  ],
  uses: [
    { ref: linkedinPosts, readOnly: true },
    // The ledger is the one model the agent writes.
    { ref: surfacedPosts, readOnly: false },
    linkedin.actions.searchPostComments,
    {
      ref: slack.actions.postMessage,
      config: {
        // PLACEHOLDER: the channel the digest lands in, as a Slack id (C…)
        // read from the connector's channel autocomplete. Locked so the
        // digest, which names people, never lands in a shared channel.
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
      // 07:00 UTC Monday: two hours after the posts model syncs. Move both
      // together.
      cron: "0 7 * * 1",
      text: "Write this week's social listening digest. Follow your system prompt exactly: read the context, skip what is already in surfaced_posts, pick at most five posts, read comments only on those, post one digest, record it.",
    },
  ],
  systemPrompt: listenerPrompt,
  evaluator: {
    rubric:
      "Was exactly one digest posted, with no post already in surfaced_posts? Is every pick tied to a named line of the ICP or pains? Is every engager quoted from a comment that was read, with no employer or URL invented? Did it avoid every engagement action?",
    threshold: 0.8,
  },
  folder: agentsFolder,
});
