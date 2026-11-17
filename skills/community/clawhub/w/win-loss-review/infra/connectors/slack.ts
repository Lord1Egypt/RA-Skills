import { defineConnector } from "@cargo-ai/cdk";

// The Slack workspace the monthly digest is posted into.
//
// The agent posts its five-line digest through `slack.actions.postMessage`,
// with the channel locked on the use (see ../agents/win-loss-analyst.ts): a
// channel the agent could pick is a channel it can get wrong, and a digest
// about lost deals in a customer shared channel is the one failure here
// nobody can undo.
//
// OAuth, so bound rather than created: authorize it once in the browser
// (`cargo-ai project add connector/slack`) and `default: true` binds to it. A
// deploy cannot mint the grant.
export const slack = defineConnector("slack", {
  integration: "slack",
  default: true,
});
