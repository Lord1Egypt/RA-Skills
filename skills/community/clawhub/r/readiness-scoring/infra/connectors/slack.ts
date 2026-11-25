import { defineConnector } from "@cargo-ai/cdk";

// Where the team hears that an account is ready. One message per account that
// crosses the line, in one channel the operator named. Binds the workspace's
// DEFAULT Slack connector rather than creating one: authorize it once
// (`cargo-ai project add connector/slack`) and this declaration resolves to it.
export const slack = defineConnector("slack", {
  integration: "slack",
  default: true,
});
