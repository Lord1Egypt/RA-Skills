import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The ledger: one row per post already put in front of the team. It is the
// idempotency key.
//
// `linkedin_posts` is replaced on every sync, and a post from last Sunday can
// match two Mondays in a row. Without this the same thread headlines two
// digests and the channel learns to skim. The listener reads it before it
// spends anything on comments, and appends only after the digest posted.
//
// It stores the post, never the people: who engaged is in the digest, for a
// human to read that week, and is not kept as a list.
export const surfacedPosts = defineModel("surfaced_posts", {
  kind: "native",
  extractSlug: "defineCustom",
  config: {
    columns: [
      // The LinkedIn post urn. The ledger key: one row per post.
      { slug: "post_urn", type: "string" },
      { slug: "post_url", type: "string" },
      { slug: "surfaced_at", type: "string" },
      // Why it made the digest, in one line, so a reader of the ledger sees
      // the judgment without the Slack thread.
      { slug: "reason", type: "string" },
      // The Slack ts of the digest it appeared in.
      { slug: "slack_ts", type: "string" },
    ],
  },
  folder: modelsFolder,
});
