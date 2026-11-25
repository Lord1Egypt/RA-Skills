// The boundaries schema validation cannot express, checked against the
// compiled registry. `cargo-ai project check` proves the resources are well formed;
// this proves they are still the pipeline this skill describes after an agent
// has adapted them.
//
// Run it from the skill folder after every adaptation:
//   node --import tsx evals/contract.mjs
import assert from "node:assert/strict";
import { resetRegistry, resources } from "@cargo-ai/cdk";

resetRegistry();
const stamp = Date.now();
const { signals, readyThreshold, warmingThreshold, horizonDays } = await import(
  `../infra/settings.ts?contract=${stamp}`
);
await import(`../infra/models/signal-feeds.ts?contract=${stamp}`);
await import(`../infra/models/account-events.ts?contract=${stamp}`);
await import(`../infra/models/accounts.ts?contract=${stamp}`);
await import(`../infra/plays/route-ready-accounts.ts?contract=${stamp}`);
await import(`../infra/segments/readiness.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const get = (id) => {
  const resource = byId.get(id);
  assert.ok(resource, `${id} must exist`);
  return resource;
};

const cronMinute = (schedule, what) => {
  assert.equal(schedule?.type, "cron", `${what} must run on a cron`);
  const minute = Number(schedule.cron.split(" ")[0]);
  assert.ok(
    Number.isInteger(minute),
    `${what} must run at a fixed minute so the three steps stay in order`,
  );
  return minute;
};

// ---------------------------------------------------------------------------
// Settings: the weights decide, and the lines are in their unit.
// ---------------------------------------------------------------------------
const signalTypes = Object.keys(signals);
assert.ok(signalTypes.length > 0, "settings.ts must weigh at least one signal");
for (const [type, signal] of Object.entries(signals)) {
  assert.match(
    type,
    /^[a-z0-9_]+$/,
    `signal "${type}" must be a bare signal type or model slug: it is inlined into the query as a string literal`,
  );
  assert.ok(
    signal.weight > 0,
    `signal "${type}" must weigh more than 0: a type that should not count is deleted from signals, where unknown types already weigh 0`,
  );
  assert.ok(
    signal.halfLifeDays > 0,
    `signal "${type}" must have a positive half-life: the decay divides by it`,
  );
}
assert.ok(
  readyThreshold > warmingThreshold && warmingThreshold > 0,
  "readyThreshold must be above warmingThreshold, and both above 0: otherwise a stage is empty or every account is in it",
);

// ---------------------------------------------------------------------------
// The score is two columns computed on rebuild: what each event adds today on
// Account Events, and their sum on Unify Accounts. Nothing writes a score.
// ---------------------------------------------------------------------------
const accountEvents = get("model:account_events").spec;
assert.equal(
  accountEvents.extractorSlug,
  "unifyAccountEvents",
  "account_events must be the workspace's Unify Account Events, adopted: any other extractor under that slug collides with it",
);
const contribution = (accountEvents.additionalColumns ?? []).find(
  (column) => column.slug === "readiness_contribution",
);
assert.ok(
  contribution !== undefined && contribution.kind === "computed",
  "account_events must carry the computed readiness_contribution column: a score written onto rows by a play stops decaying between signals",
);
// The compiled column, run the way the warehouse runs it: `record` bound, the
// expression returned. Checking what it computes rather than how it is spelled
// is what survives an adaptation that rewrites the function.
const runInWarehouse = (column, record) =>
  new Function("record", `return ${column.expression.expression}`)(record);
const daysAgo = (days) => new Date(Date.now() - days * 86400000).toISOString();

for (const [type, signal] of Object.entries(signals)) {
  const fresh = runInWarehouse(contribution, {
    properties: { signal_type: type },
    model_slug: "feed",
    occurred_at: daysAgo(0),
  });
  assert.ok(
    Math.abs(fresh - signal.weight) < 0.01,
    `a fresh "${type}" event must contribute its weight from settings.ts (${signal.weight}), not ${fresh}`,
  );
  const halfLife = runInWarehouse(contribution, {
    properties: { signal_type: type },
    model_slug: "feed",
    occurred_at: daysAgo(signal.halfLifeDays),
  });
  assert.ok(
    Math.abs(halfLife - signal.weight / 2) < 0.01,
    `a "${type}" event one half-life old must contribute half its weight: the contribution must decay by half-life, read from the clock when it is computed`,
  );
}
const [firstType] = Object.keys(signals);
assert.equal(
  runInWarehouse(contribution, {
    properties: {},
    model_slug: "a_model_nobody_weighed",
    occurred_at: daysAgo(0),
  }),
  0,
  "an event whose type settings.ts does not weigh must contribute 0: otherwise a new feed moves every score before anyone decided what it is worth",
);
assert.equal(
  runInWarehouse(contribution, {
    properties: { signal_type: firstType },
    model_slug: "feed",
    occurred_at: daysAgo(horizonDays + 1),
  }),
  0,
  "an event older than horizonDays from settings.ts must contribute 0",
);
assert.equal(
  runInWarehouse(contribution, {
    properties: { signal_type: firstType },
    model_slug: "feed",
    occurred_at: null,
  }),
  0,
  "an event with no date must contribute 0",
);

const accounts = get("model:accounts").spec;
assert.equal(
  accounts.extractorSlug,
  "unifyAccounts",
  "accounts must be the workspace's Unify Accounts, adopted: the score lives on the account row everyone reads",
);
const accountColumns = new Map(
  (accounts.additionalColumns ?? []).map((column) => [column.slug, column]),
);
const score = accountColumns.get("readiness_score");
assert.ok(
  score !== undefined && score.kind === "metric",
  "accounts must carry the readiness_score metric",
);
assert.deepEqual(
  score.aggregation,
  { function: "SUM", columnSlug: "computed__readiness_contribution" },
  "the score must be the SUM of the events' readiness_contribution",
);
assert.equal(
  score.relationshipUuid?.resourceId,
  "model:account_events",
  "the score must aggregate over the relationship Account Events generates (accountEvents.relationships.account_id): it cannot be declared, and a literal uuid ties the code to one workspace",
);
assert.equal(score.relationshipUuid.field, "relationships.account_id");

const stage = accountColumns.get("readiness_stage");
assert.ok(
  stage !== undefined && stage.kind === "computed",
  "accounts must carry the computed readiness_stage column",
);
for (const [score, expected] of [
  [readyThreshold, "ready_now"],
  [warmingThreshold, "warming"],
  [warmingThreshold / 2, "cold"],
]) {
  assert.equal(
    runInWarehouse(stage, { metric__readiness_score: score }),
    expected,
    `a score of ${score} must be ${expected}: the stage comes from the thresholds in settings.ts`,
  );
}
assert.equal(
  [...byId.values()].some(
    (resource) => resource.spec.extractorSlug === "defineQuery",
  ),
  false,
  "the score must not be a query model: the columns put it on the account row, on any warehouse",
);

// ---------------------------------------------------------------------------
// Feeds: company signals, on a watchlist, into Account Events.
// ---------------------------------------------------------------------------
const feeds = [...byId.values()].filter(
  (resource) =>
    resource.id.startsWith("model:") &&
    typeof resource.spec.extractorSlug === "string" &&
    resource.spec.extractorSlug.startsWith("listen"),
);
assert.ok(feeds.length > 0, "the skill must carry at least one signal feed");
for (const feed of feeds) {
  assert.equal(
    feed.spec.config?.scope?.kind,
    "watchlist",
    `${feed.id} must watch a list of accounts: market scope bills for every event in the market, most of them on companies no account model holds`,
  );
  assert.equal(
    feed.spec.unification?.type,
    "accountEvent",
    `${feed.id} must unify as an account event: an event that lands in Contact Events never reaches the score`,
  );
  if (feed.spec.extractorSlug === "listenFundraising") {
    assert.equal(
      feed.spec.config.scope.filters?.maxLeadsPerCompany,
      1,
      `${feed.id} must deliver one lead per company: a round otherwise arrives once per contact, counted and billed each time`,
    );
  }
  assert.ok(
    feed.spec.config?.advancedSettings?.dailyLeadLimit > 0,
    `${feed.id} must cap deliveries per day: the first delivery on a new watchlist looks back months`,
  );
}

// ---------------------------------------------------------------------------
// The play posts once per climb, after the score it reads.
// ---------------------------------------------------------------------------
const play = get("play:route_ready_accounts").spec;
assert.equal(
  play.modelUuid?.resourceId,
  "model:accounts",
  "the play must run on Unify Accounts, where the stage is",
);
assert.deepEqual(
  play.changeKinds,
  ["added"],
  "the play must create runs only for accounts entering ready_now: without it every ready account is posted every hour",
);
assert.equal(
  play.isEnabled,
  false,
  "the first plan must ship the play disabled",
);
const playConditions = play.filter.groups.flatMap((group) => group.conditions);
assert.ok(
  playConditions.length === 1 &&
    playConditions[0].columnSlug === "computed__readiness_stage" &&
    playConditions[0].values?.join() === "ready_now",
  "the play must filter on readiness_stage = ready_now, never on the raw score: the threshold lives in settings.ts and only reaches the play through the stage",
);

const eventsMinute = cronMinute(accountEvents.schedule, "account_events");
const scoresMinute = cronMinute(accounts.schedule, "accounts");
const playMinute = cronMinute(play.schedule, "the play");
assert.ok(
  eventsMinute < scoresMinute && scoresMinute < playMinute,
  "Account Events must rebuild before Unify Accounts sums it, and Unify Accounts before the play reads the stage: out of order, each tick acts on the previous hour",
);

const connectorNodes = play.nodes.filter((node) => node.kind === "connector");
assert.equal(
  connectorNodes.length,
  1,
  "the play must contain exactly one connector node, the Slack post: anything else is a per-account action nobody approved",
);
assert.equal(connectorNodes[0].integrationSlug, "slack");

// ---------------------------------------------------------------------------
// Segments view the stages the query emits.
// ---------------------------------------------------------------------------
const segments = [...byId.values()].filter((resource) =>
  resource.id.startsWith("segment:"),
);
const segmentStages = new Set();
for (const segment of segments) {
  const conditions = segment.spec.filter.groups.flatMap(
    (group) => group.conditions,
  );
  assert.equal(
    conditions.every(
      (condition) => condition.columnSlug === "computed__readiness_stage",
    ),
    true,
    `${segment.id} filters on something other than readiness_stage: a threshold restated in a segment drifts from settings.ts`,
  );
  for (const condition of conditions) {
    for (const value of condition.values ?? []) segmentStages.add(value);
  }
}
assert.deepEqual(
  [...segmentStages].sort(),
  ["ready_now", "warming"],
  "there must be one segment for ready_now and one for warming",
);

assert.equal(
  [...byId.keys()].some((id) => id.startsWith("agent:")),
  false,
  "this skill must declare no agent: the score is arithmetic, and an LLM per account per hour is a bill with no judgment in it",
);

console.log(
  "ok: each event's contribution decays on rebuild, Unify Accounts sums it, the feeds watch a list, and the play posts once per climb after the score it reads",
);
