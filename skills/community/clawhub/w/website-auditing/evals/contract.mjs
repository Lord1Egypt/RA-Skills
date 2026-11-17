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
await import(`../infra/agents/website-auditor.ts?contract=${stamp}`);
await import(`../infra/connectors/git.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const findOne = (nodes, predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};

assert.ok(byId.get("connector:github"), "defineConnector(github) must exist: the harness clones and opens the pull request through it");

const agent = byId.get("agent:website_auditor");
assert.ok(agent, "defineAgent(website_auditor) must exist");
assert.equal(
  agent.spec.harnessSlug,
  "claudeCode",
  "the auditor must be a Claude Code harness agent: its fix is a diff to the website's source",
);

// The harness runs against Cargo's LLM proxy, selected by the connector's
// integration: `claudeCode` with anything but `anthropic` deploys broken.
const llm = byId.get("connector:anthropic");
assert.ok(llm, "defineConnector(anthropic) must exist: the harness needs a model");
assert.equal(llm.spec.integrationSlug, "anthropic", "claudeCode is proxied to Anthropic");
assert.ok(agent.spec.connectorUuid, "the auditor must bind the LLM connector");
assert.equal(typeof agent.spec.languageModelSlug, "string", "the auditor must name a languageModel");

// Ora is the one MCP server, and it is read, never written.
const ora = findOne(
  agent.spec.mcpClients ?? [],
  (client) => client.kind === "custom" && client.url === "https://ora.ai/api/mcp",
  "the auditor must reach Ora through its MCP server",
);
assert.equal((agent.spec.mcpClients ?? []).length, 1, "Ora is the only MCP server on the auditor");
assert.equal(ora.authentication, null, "Ora's reads need no key: no credential on the MCP client");
for (const tool of ["submit_feedback", "submit_check_feedback", "get_verification_challenge"]) {
  assert.ok(ora.disabledToolSlugs.includes(tool), `${tool} writes to Ora: it must be disabled`);
}
assert.ok(
  ora.disabledToolSlugs.includes("run_checks"),
  "run_checks always scans live and spends the daily scan budget: it must be disabled",
);
for (const tool of ["scan_domain", "get_score", "get_skill"]) {
  assert.equal(ora.disabledToolSlugs.includes(tool), false, `${tool} is how the auditor reads Ora: keep it enabled`);
}

// The ledger is the auditor's only memory and its only model.
assert.ok(byId.get("model:website_audits"), "defineModel(website_audits) must exist");
const models = agent.spec.models ?? [];
assert.equal(models.length, 1, "website_audits is the only model on the auditor");
const ledger = findOne(
  models,
  (model) => model.uuid?.resourceId === "model:website_audits",
  "website_audits must be on the auditor's uses",
);
assert.equal(ledger.readOnly, false, "the auditor records each week's scans: the ledger must be writable");

const actions = agent.spec.connectorActions ?? [];
assert.equal(
  actions.filter((action) => action.integration !== "slack").length,
  0,
  "the only connector action on the auditor is slack.postMessage",
);
const post = findOne(
  actions,
  (action) => action.integration === "slack" && action.actionSlug === "postMessage",
  "the auditor must use slack.postMessage",
);
assert.equal(typeof post.config?.channelId, "string", "channelId must be locked on the postMessage use");
assert.notEqual(post.config.channelId, "", "channelId must not be empty");
assert.equal(post.config.format, "markdown", "format must be locked to markdown");
assert.equal((agent.spec.tools ?? []).length, 0, "no tool wraps an action the agent can call directly");

findOne(
  agent.spec.triggers ?? [],
  (trigger) => trigger.type === "cron" && typeof trigger.cron === "string",
  "the auditor must have one cron trigger",
);

const env = agent.spec.env ?? [];
const envByKey = new Map((Array.isArray(env) ? env : []).map((entry) => [entry.key, entry.value]));
for (const key of ["AUDIT_DOMAIN", "COMPETITOR_DOMAINS", "WEBSITE_ROOT"]) {
  assert.ok(envByKey.has(key), `env must carry ${key}`);
}
assert.notEqual(envByKey.get("AUDIT_DOMAIN"), "", "AUDIT_DOMAIN must name the website's domain");
assert.notEqual(envByKey.get("WEBSITE_ROOT"), "", "WEBSITE_ROOT must name the website's source");
const competitors = envByKey
  .get("COMPETITOR_DOMAINS")
  .split(",")
  .filter((domain) => domain.trim() !== "");
assert.ok(competitors.length <= 3, "at most three competitors: each one is a scan a week from a shared budget");

console.log("ok: website-auditing contract");
