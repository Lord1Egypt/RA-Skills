import assert from "node:assert/strict";
import { resetRegistry, resources } from "@cargo-ai/cdk";

// The boundaries schema validation cannot express, checked against the
// compiled registry. `cargo-ai project check` proves the resources are well formed;
// this proves they are still the pipeline this skill describes after an agent
// has adapted them.
//
// Run it from the skill folder after every adaptation:
//   node --import tsx evals/contract.mjs
resetRegistry();
const stamp = Date.now();
await import(`../infra/agents/listener.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const findOne = (nodes, predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};

// The paid search: capped, weekly, and a week wide.
const posts = byId.get("model:linkedin_posts");
assert.ok(posts, "defineModel(linkedin_posts) must exist");
const configText = JSON.stringify(posts.spec);
assert.ok(
  /"searchKeywords":\s*"[^"]/.test(configText),
  "linkedin_posts must carry a searchKeywords query: the search is what you buy",
);
const limit = Number((configText.match(/"limit":\s*(\d+)/) ?? [])[1]);
assert.ok(
  limit >= 20 && limit <= 100,
  `linkedin_posts limit must be LinkedIn's page of 20 to 100, got ${limit}`,
);
assert.ok(
  configText.includes('"Past week"'),
  'linkedin_posts must search "Past week": a wider window re-buys last week',
);
assert.ok(configText.includes('"cron"'), "linkedin_posts must sync on a schedule");

const ledger = byId.get("model:surfaced_posts");
assert.ok(ledger, "defineModel(surfaced_posts) must exist: it is the dedupe");
const ledgerColumns = JSON.stringify(ledger.spec);
for (const forbidden of ["linkedin_url", "commenter", "engager", "email"]) {
  assert.equal(
    ledgerColumns.includes(forbidden),
    false,
    `surfaced_posts stores posts, never people: found "${forbidden}"`,
  );
}

const agent = byId.get("agent:social_listener");
assert.ok(agent, "defineAgent(social_listener) must exist");
assert.ok(agent.spec.connectorUuid, "the listener must bind an LLM connector");

const modelUse = (resourceId) =>
  findOne(
    agent.spec.models ?? [],
    (model) => model.uuid?.resourceId === resourceId,
    `${resourceId} must be on the listener's uses`,
  );
assert.equal(
  modelUse("model:linkedin_posts").readOnly,
  true,
  "the listener reads linkedin_posts; the sync owns it",
);
assert.equal(
  modelUse("model:surfaced_posts").readOnly,
  false,
  "the listener appends to surfaced_posts after the digest: it must be writable",
);

// Read-only on LinkedIn. An engagement action here is automated outreach.
const actions = agent.spec.connectorActions ?? [];
const engaging = [
  "likePost",
  "commentPost",
  "commentPostComment",
  "connectProfile",
  "messageProfile",
  "followProfile",
  "visitProfile",
];
const found = actions.filter(
  (action) =>
    action.integration === "linkedin" && engaging.includes(action.actionSlug),
);
assert.equal(
  found.length,
  0,
  `the listener never engages; found ${found.map((a) => a.actionSlug).join(", ")}`,
);
const linkedinActions = actions
  .filter((action) => action.integration === "linkedin")
  .map((action) => action.actionSlug);
assert.deepEqual(
  linkedinActions,
  ["searchPostComments"],
  "the only LinkedIn action is the comment read on picked posts",
);

const post = findOne(
  actions,
  (action) =>
    action.integration === "slack" && action.actionSlug === "postMessage",
  "the listener must use slack.postMessage",
);
assert.equal(
  typeof post.config?.channelId,
  "string",
  "channelId must be locked on the postMessage use",
);
assert.notEqual(post.config.channelId, "", "channelId must not be empty");

const capabilities = JSON.stringify(agent.spec.capabilities ?? []);
assert.ok(
  capabilities.includes("context") && /"isReadOnly":\s*true/.test(capabilities),
  "the context capability must be on and read-only: it is the rubric",
);

findOne(
  agent.spec.triggers ?? [],
  (trigger) => trigger.type === "cron" && typeof trigger.cron === "string",
  "the listener must have one cron trigger",
);

console.log("ok: social-listening contract");
