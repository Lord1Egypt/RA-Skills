import { defineConnector } from "@cargo-ai/cdk";

// The Slack workspace the digest lands in. OAuth, so bound rather than created:
// a deploy cannot mint the grant. Authorize it once in the browser
// (`cargo-ai project add connector/slack`) and `default: true` binds to it.
//
// The agent posts through `slack.actions.postMessage` with the channel locked
// on the use. There is no SLACK_TOKEN and no wrapped tool.
export const slack = defineConnector("slack", {
  integration: "slack",
  default: true,
});
