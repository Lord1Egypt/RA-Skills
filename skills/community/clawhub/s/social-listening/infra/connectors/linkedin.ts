import { defineConnector } from "@cargo-ai/cdk";

// LinkedIn: the post search the model syncs from, and the comment read the
// listener pulls for the few posts worth it. Bound to the workspace's
// connector; no seat, cookie or key of its own.
//
// Read-only by design. The integration also carries likePost, commentPost,
// connectProfile and messageProfile; none of them is on any `uses` in this
// pipeline, and the contract fails if one appears. A human decides whether to
// join a conversation.
export const linkedin = defineConnector("linkedin", {
  integration: "linkedin",
  default: true,
});
