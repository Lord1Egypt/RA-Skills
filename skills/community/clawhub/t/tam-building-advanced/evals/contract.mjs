// The boundaries schema validation cannot express, checked against the
// compiled registry. `cargo-ai project check` proves the resources are well
// formed; this proves they are still the pipeline this skill describes after
// an agent has adapted them.
//
// Run it from the skill folder after every adaptation:
//   node --import tsx evals/contract.mjs
import assert from "node:assert/strict";
import { resetRegistry, resources } from "@cargo-ai/cdk";

resetRegistry();
const stamp = Date.now();
// The play imports everything it reads, every source included.
await import(`../infra/plays/profile-company.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const get = (id) => {
  const resource = byId.get(id);
  assert.ok(resource, `${id} must exist`);
  return resource;
};

const integrationOf = (modelSpec) =>
  get(modelSpec.datasetUuid.resourceId).spec.integrationSlug;

// A TAM does not need to be fresher than a quarter, and every re-sync re-bills
// every record. A schedule is either absent (the default: built once,
// refreshed by hand) or a cron that fires at most once every three months: a
// fixed minute, hour and day, and a month field of `*/3` or rarer, or an
// explicit list of at most four months.
const atMostQuarterly = (schedule) => {
  if (schedule === undefined || schedule === null) return true;
  if (schedule.type !== "cron") return false;
  const [minute, hour, day, month, weekday] = schedule.cron
    .trim()
    .split(/\s+/);
  if (![minute, hour, day].every((field) => /^\d+$/.test(field))) return false;
  if (weekday !== "*") return false;
  const step = month.match(/^\*\/(\d+)$/);
  if (step) return Number(step[1]) >= 3;
  const months = month.split(",");
  return months.every((m) => /^\d+$/.test(m)) && months.length <= 4;
};

const valueAt = (config, path) =>
  path.reduce(
    (node, key) => (node === undefined || node === null ? node : node[key]),
    config,
  );

// ---------------------------------------------------------------------------
// The paid sources. Each one names its extractor and where industries, company
// size and countries live in its config: the three criteria every source
// carries, because a source without one bills for the whole dimension.
// ---------------------------------------------------------------------------
const PAID_SOURCES = {
  "model:tam_source_sales_navigator": {
    integration: "salesNavigator",
    extractor: "fetchAccountSearch",
  },
  "model:tam_source_ai_ark": {
    integration: "aiArk",
    extractor: "fetchCompanies",
    minimum: {
      industries: ["industry"],
      size: ["employeeSize"],
      countries: ["companyLocation"],
    },
  },
  "model:tam_source_apollo": {
    integration: "apolloio",
    extractor: "fetchOrganizations",
    minimum: {
      industries: ["filters", "q_organization_keyword_tags"],
      size: ["filters", "organization_num_employees_ranges"],
      countries: ["filters", "organization_locations"],
    },
  },
};

for (const [id, source] of Object.entries(PAID_SOURCES)) {
  const spec = get(id).spec;
  const config = spec.config ?? {};
  assert.equal(
    integrationOf(spec),
    source.integration,
    `${id} must source from ${source.integration}`,
  );
  assert.equal(
    spec.extractorSlug,
    source.extractor,
    `${id} must use ${source.integration}.${source.extractor}`,
  );
  assert.equal(
    typeof config.limit,
    "number",
    `${id} must set an explicit limit: it bills per returned record and this is the only cap`,
  );
  assert.ok(
    atMostQuarterly(spec.schedule),
    `${id}: no schedule, or a refresh at most once every three months. A sync re-runs the search and re-bills every returned record, including the companies already in the TAM`,
  );
  for (const [criterion, path] of Object.entries(source.minimum ?? {})) {
    const value = valueAt(config, path);
    assert.ok(
      value !== undefined && value !== null,
      `${id} must set ${criterion} (config.${path.join(".")}): without it the search has no edge in that dimension`,
    );
  }
}

// AI Ark filters are nested groups. A flat key is ignored silently and the
// sync sources the whole database up to limit.
const aiArkConfig = get("model:tam_source_ai_ark").spec.config;
for (const [key, value] of Object.entries(aiArkConfig)) {
  if (key === "limit" || key === "lookalikeDomains") continue;
  assert.ok(
    typeof value === "object" && value !== null && !Array.isArray(value),
    `tam_source_ai_ark config.${key} must be a nested filter group, not a flat value`,
  );
}

// Sales Navigator: every search carries the three criteria inside its URL, and
// no LinkedIn seat is attached.
const salesNavigatorConfig = get("model:tam_source_sales_navigator").spec
  .config;
assert.ok(
  Array.isArray(salesNavigatorConfig.urls) &&
    salesNavigatorConfig.urls.length > 0,
  "tam_source_sales_navigator must list at least one search URL",
);
for (const url of salesNavigatorConfig.urls) {
  for (const filterType of ["INDUSTRY", "COMPANY_HEADCOUNT", "REGION"]) {
    assert.ok(
      url.includes(`type:${filterType}`),
      `every Sales Navigator search must filter on ${filterType}: ${url.slice(0, 120)}…`,
    );
  }
}
assert.equal(
  salesNavigatorConfig.identityIds,
  undefined,
  "tam_source_sales_navigator must not attach identityIds: the search runs without a LinkedIn seat, and a seat puts that account at risk",
);

// Exa has no `limit`: its cap is the number of queries times `numResults`,
// and only company results carry the company's own domain.
const exaSource = get("model:tam_source_exa").spec;
assert.equal(integrationOf(exaSource), "exa", "tam_source_exa must source from exa");
assert.equal(
  exaSource.extractorSlug,
  "fetchSearch",
  "tam_source_exa must use exa.fetchSearch",
);
assert.ok(
  Array.isArray(exaSource.config.queries) &&
    exaSource.config.queries.length > 0,
  "tam_source_exa must run the queries in exaQueries (settings.ts)",
);
assert.equal(
  typeof exaSource.config.numResults,
  "number",
  "tam_source_exa must set numResults: with the number of queries, it is the only cap on what Exa bills",
);
assert.equal(
  exaSource.config.category,
  "company",
  "tam_source_exa must search companies: any other category returns publishers' pages, whose domains would become accounts",
);
assert.ok(
  atMostQuarterly(exaSource.schedule),
  "tam_source_exa: no schedule, or a refresh at most once every three months. A sync re-runs every query and re-bills every result",
);

// ---------------------------------------------------------------------------
// One account layer. Every source and the profile model unify into Unify
// Accounts with a declared (custom) unification, so Cargo does the merge and
// no workflow ever writes the TAM.
// ---------------------------------------------------------------------------
const UNIFIED = {
  "model:tam_source_sales_navigator": [
    ["sales_navigator_company_id", "linkedinId"],
  ],
  "model:tam_source_ai_ark": [
    ["domain", "domain"],
    ["linkedin_url", "linkedinHandle"],
    ["linkedin_url", "linkedinId"],
  ],
  "model:tam_source_apollo": [
    ["primary_domain", "domain"],
    // The numeric LinkedIn id: what joins Apollo to Sales Navigator directly.
    ["linkedin_uid", "linkedinId"],
    ["linkedin_url", "linkedinHandle"],
    ["linkedin_url", "linkedinId"],
  ],
  "model:tam_source_exa": [["domain", "domain"]],
  "model:tam_accounts": [
    ["linkedin_id", "linkedinId"],
    ["domain", "domain"],
    ["account_domain", "domain"],
    ["linkedin_url", "linkedinHandle"],
  ],
};
for (const [id, keys] of Object.entries(UNIFIED)) {
  const unification = get(id).spec.unification;
  assert.ok(
    unification && unification.source === "custom",
    `${id} must declare its unification (source "custom"): Sales Navigator's default is off, and a default can move`,
  );
  assert.equal(unification.type, "account", `${id} must unify as an account`);
  for (const [slug, reference] of keys) {
    assert.ok(
      unification.uniqueColumns.some(
        (column) => column.slug === slug && column.reference === reference,
      ),
      `${id} must unify ${slug} as ${reference}`,
    );
  }
}

// The profile row is the one that carries the LinkedIn id, the page and the
// domain together: it is what joins a Sales Navigator row to an AI Ark row.
const profile = get("model:tam_accounts").spec;
assert.equal(profile.datasetUuid, "native");
const profileColumns = new Set([
  ...profile.config.columns.map((column) => column.slug),
  ...(profile.additionalColumns ?? []).map((column) => column.slug),
]);
for (const column of [
  "linkedin_id",
  "linkedin_url",
  "domain",
  "account_domain",
  "employee_count",
  "hq_country",
  "category",
  "subsidiary_probability",
  "status",
  "exclusion_reason",
]) {
  assert.ok(
    profileColumns.has(column),
    `tam_accounts must keep ${column}: the report and the ICP gates read it`,
  );
}
for (const slug of ["status", "exclusion_reason"]) {
  const column = profile.additionalColumns.find((c) => c.slug === slug);
  assert.equal(
    column.kind,
    "computed",
    `${slug} must be computed from settings.ts, so moving a gate re-gates every company`,
  );
}

// Unify Accounts is adopted, never created, and nothing else is declared on
// it: a declared column list or schedule would replace what other pipelines
// keep there.
const accounts = get("model:accounts").spec;
assert.equal(accounts.extractorSlug, "unifyAccounts");
assert.equal(
  accounts.additionalColumns,
  undefined,
  "accounts must not declare additionalColumns: the declaration would become the whole list and remove every other pipeline's columns",
);
assert.equal(
  accounts.schedule ?? undefined,
  undefined,
  "accounts must not declare a schedule: it is shared",
);

// ---------------------------------------------------------------------------
// One play, on Unify Accounts. No play runs on a source model and no tool
// exists: sources only land rows, Cargo merges them.
// ---------------------------------------------------------------------------
const plays = [...byId.values()].filter((r) => r.id.startsWith("play:"));
assert.deepEqual(
  plays.map((play) => play.id),
  ["play:tam_profile_companies"],
  "the pipeline has exactly one play: the profile play on Unify Accounts",
);
const play = plays[0].spec;
assert.equal(
  play.modelUuid.resourceId,
  "model:accounts",
  "the profile play runs on Unify Accounts, after the merge, so a company several sources found is enriched once",
);
assert.deepEqual(play.changeKinds, ["added"]);
assert.ok(
  atMostQuarterly(play.schedule),
  "the profile play is a build step: no schedule (run as a batch after each source sync), or the quarterly refresh, the day after the sources",
);
assert.equal(
  play.runCreationRule,
  "once",
  "the profile play runs once per account: a re-run pays the LinkedIn enrich and the classification again",
);
assert.equal(
  play.isEnabled,
  Boolean(play.schedule),
  "the profile play is disabled with no schedule (it runs as a batch), and enabled only under the quarterly refresh",
);
const filterText = JSON.stringify(play.filter);
for (const modelId of [
  "model:tam_source_sales_navigator",
  "model:tam_source_ai_ark",
  "model:tam_source_apollo",
  "model:tam_source_exa",
  "model:tam_accounts",
]) {
  assert.ok(
    filterText.includes(modelId),
    `the profile play's filter must read ${modelId} on the account`,
  );
}
assert.equal(
  [...byId.values()].filter((r) => r.id.startsWith("tool:")).length,
  0,
  "no tool: the merge is Cargo's, not a workflow's",
);

// ---------------------------------------------------------------------------
// Read only outside Cargo. The connectors are the four sources and LinkedIn;
// a CRM connector, if the project declares one, only reads its companies,
// which unify into the same accounts.
// ---------------------------------------------------------------------------
const connectors = [...byId.values()]
  .filter((resource) => resource.id.startsWith("connector:"))
  .map((resource) => resource.spec.integrationSlug)
  .sort();
const CRM_INTEGRATIONS = ["hubspot", "salesforce", "attio"];
const expected = ["aiArk", "apolloio", "exa", "linkedin", "salesNavigator"];
assert.deepEqual(
  connectors.filter((slug) => !CRM_INTEGRATIONS.includes(slug)),
  expected,
  "the connectors are the four sources and LinkedIn: a fifth source is a recorded decision, edit this check in the same change",
);
for (const resource of byId.values()) {
  if (!resource.id.startsWith("model:")) continue;
  const spec = resource.spec;
  if (spec.datasetUuid === "native") continue;
  if (!CRM_INTEGRATIONS.includes(integrationOf(spec))) continue;
  assert.equal(
    spec.extractorSlug,
    "fetchRecords",
    `${resource.id}: a CRM is only read here, with fetchRecords and no filter`,
  );
}

console.log(
  "ok: four sources with their criteria and budgets, all unified into Accounts, one profile play, nothing written outside Cargo",
);
