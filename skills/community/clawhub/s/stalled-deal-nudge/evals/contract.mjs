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
await import(`../infra/agents/nudger.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const findOne = (nodes, predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};

const agent = byId.get("agent:stalled_deal_nudger");
assert.ok(agent, "defineAgent(stalled_deal_nudger) must exist");
assert.ok(agent.spec.connectorUuid, "the nudger must bind an LLM connector");

// The worked example runs on Cargo native models: no CRM connector, no key.
// A CRM-backed adaptation swaps the models (SKILL.md, `crm-backed`) and drops
// this assertion with a line under ## Decisions.
assert.equal(
  byId.has("connector:hubspot"),
  false,
  "the example needs no CRM connector: deals and activities are native models",
);
for (const slug of ["gtm_opportunities", "gtm_accounts", "gtm_activities"]) {
  const model = byId.get(`model:${slug}`);
  assert.ok(model, `defineModel(${slug}) must exist`);
}

const modelUse = (slug) =>
  findOne(
    agent.spec.models ?? [],
    (model) => model.uuid?.resourceId === `model:${slug}`,
    `${slug} must be on the nudger's uses`,
  );
for (const slug of ["gtm_opportunities", "gtm_accounts", "gtm_activities"]) {
  assert.equal(
    modelUse(slug).readOnly,
    true,
    `${slug} must be read-only to the agent: a nudge never changes a deal`,
  );
}
assert.ok(byId.get("model:deal_nudges"), "defineModel(deal_nudges) must exist");
assert.equal(
  modelUse("deal_nudges").readOnly,
  false,
  "the nudger appends to deal_nudges after each post: it must be writable",
);

const actions = agent.spec.connectorActions ?? [];
const nonSlack = actions.filter((action) => action.integration !== "slack");
assert.equal(
  nonSlack.length,
  0,
  `the nudger reads models, not connectors; found ${nonSlack.map((a) => `${a.integration}.${a.actionSlug}`).join(", ")}`,
);

const post = findOne(
  actions,
  (action) =>
    action.integration === "slack" && action.actionSlug === "postMessage",
  "the nudger must use slack.postMessage",
);
assert.equal(
  typeof post.config?.channelId,
  "string",
  "channelId must be locked on the postMessage use, not left for the agent to pick",
);
assert.notEqual(post.config.channelId, "", "channelId must not be empty");
assert.equal(
  actions.filter(
    (action) =>
      action.integration === "slack" && action.actionSlug !== "postMessage",
  ).length,
  0,
  "the ledger is the dedupe: no Slack history read on uses",
);

const capabilities = JSON.stringify(agent.spec.capabilities ?? []);
assert.ok(
  /"isReadOnly":\s*true/.test(capabilities),
  "the context capability must be read-only",
);

const cron = findOne(
  agent.spec.triggers ?? [],
  (trigger) => trigger.type === "cron" && typeof trigger.cron === "string",
  "the nudger must have one cron trigger",
);
assert.match(
  cron.cron,
  /\s1$/,
  "the nudger runs once a week: the ledger keys on the ISO week",
);

console.log("ok: stalled-deal-nudge contract");
