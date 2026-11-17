// The boundaries CDK schema validation cannot express, checked against the
// compiled registry. `cargo-cdk check` proves the resources are well formed;
// this proves they are still the pipeline this skill describes after an agent
// has adapted them.
//
// Run it from the skill folder after every adaptation:
//   node --import tsx evals/contract.mjs
import assert from "node:assert/strict";
import { resetRegistry, resources } from "@cargo-ai/cdk";

resetRegistry();
const stamp = Date.now();
await import(`../infra/models/tam-companies.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const get = (id) => {
  const resource = byId.get(id);
  assert.ok(resource, `${id} must exist`);
  return resource;
};

// ---------------------------------------------------------------------------
// The source is the model, and its filter is the TAM. Each supported source
// names its extractor and where industries, company size and countries live
// in its config. A source missing from this table is not a supported swap:
// add it here, with its three paths, in the same change that adopts it.
// ---------------------------------------------------------------------------
const SOURCES = {
  aiArk: {
    extractor: "fetchCompanies",
    nested: true,
    minimum: {
      industries: ["industry"],
      size: ["employeeSize"],
      countries: ["companyLocation"],
    },
  },
  FullEnrich: {
    extractor: "fetchCompanies",
    nested: true,
    // Free per returned record, so a schedule re-runs the search at no
    // charge. Re-read the price before relying on this: if it stops being
    // free, drop the flag.
    freeToRefresh: true,
    minimum: {
      industries: ["industry"],
      size: ["headcount"],
      countries: ["headquarters"],
    },
  },
  apolloio: {
    extractor: "fetchOrganizations",
    nested: false,
    minimum: {
      industries: ["filters", "q_organization_keyword_tags"],
      size: ["filters", "organization_num_employees_ranges"],
      countries: ["filters", "organization_locations"],
    },
  },
  salesNavigator: {
    extractor: "fetchAccounts",
    nested: false,
    minimum: {
      industries: ["industryCodes"],
      size: ["companyHeadcounts"],
      countries: ["headquarterLocationIds"],
    },
  },
};

const sourceSpec = get("model:tam_companies").spec;
const sourceConnector = get(sourceSpec.datasetUuid.resourceId).spec;
const source = SOURCES[sourceConnector.integrationSlug];
assert.ok(
  source,
  `${sourceConnector.integrationSlug} is not a supported TAM source: references/sources.md lists the ones this contract knows, with the extractor and the three minimum paths for each`,
);

assert.equal(
  sourceSpec.extractorSlug,
  source.extractor,
  `the company universe must be ${sourceConnector.integrationSlug}.${source.extractor} on the model`,
);

const config = sourceSpec.config ?? {};
const filterGroups = Object.entries(config).filter(([key]) => key !== "limit");
assert.ok(
  filterGroups.length > 0,
  "the model config must carry at least one ICP filter: an unfiltered search sources the whole database up to limit",
);
if (source.nested) {
  for (const [key, value] of filterGroups) {
    assert.equal(
      typeof value === "object" && value !== null && !Array.isArray(value),
      true,
      `config.${key} must be a nested filter group, not a flat value: a flat map is ignored silently and you pay for the whole database`,
    );
  }
}

for (const [criterion, path] of Object.entries(source.minimum)) {
  const value = path.reduce((node, key) => node?.[key], config);
  assert.ok(
    value !== undefined && value !== null,
    `the model config must set ${criterion} (config.${path.join(".")}): industries, company size and countries are the minimum of every TAM, and without one the search bills for the whole dimension`,
  );
}

assert.equal(
  typeof config.limit,
  "number",
  "the model config must set an explicit limit: the search bills per returned record and this is the only cap",
);

if (!source.freeToRefresh) {
  assert.equal(
    sourceSpec.schedule ?? null,
    null,
    `the ${sourceConnector.integrationSlug} model must not carry a schedule: a cron re-runs the search and re-bills every returned record, including the rows already sourced. A paid refresh-cadence is a recorded decision: edit this check in the same change`,
  );
}

// ---------------------------------------------------------------------------
// Atomic: one connector, one model, one folder. Nothing judges, nothing writes.
// ---------------------------------------------------------------------------
for (const id of byId.keys()) {
  const kind = id.split(":")[0];
  assert.ok(
    ["model", "connector", "folder"].includes(kind),
    `${id} is a ${kind}: this skill sources a TAM and deploys no play, agent, tool or segment`,
  );
}
const connectors = [...byId.values()].filter(
  (resource) => resource.id.startsWith("connector:"),
);
assert.deepEqual(
  connectors.map((resource) => resource.spec.integrationSlug),
  [sourceConnector.integrationSlug],
  "the only connector is the company source: a CRM or an LLM is a dependency of a next step, not of building the TAM, and a swapped source replaces AI Ark rather than sitting beside it",
);
const models = [...byId.keys()].filter((id) => id.startsWith("model:"));
assert.deepEqual(
  models,
  ["model:tam_companies"],
  "the only model is the sourced universe: CRM extracts and the unified accounts model belong to the next steps that need them",
);

console.log(
  `ok: one ${sourceConnector.integrationSlug} connector, one model, and the ICP filter carries industries, company size and countries`,
);
