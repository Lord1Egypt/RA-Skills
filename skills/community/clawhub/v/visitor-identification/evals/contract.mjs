import assert from "node:assert/strict";
import { readdirSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { resetRegistry, resources } from "@cargo-ai/cdk";

import { snitcherSettings } from "../site/lib/snitcher.ts";

// The boundaries schema validation cannot express, checked against the
// compiled registry and the site's snippet parser. `cargo-ai project check` proves
// the resources are well formed; this proves they are still the visitor
// pipeline this skill describes after an agent has adapted them.
//
// Run it from the skill folder after every adaptation:
//   node --import tsx evals/contract.mjs
const resourceFiles = (dir) =>
  readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return resourceFiles(path);
    return entry.name.endsWith(".ts") ? [path] : [];
  });

resetRegistry();
const stamp = Date.now();
for (const file of resourceFiles(fileURLToPath(new URL("../infra", import.meta.url))))
  await import(`${pathToFileURL(file).href}?contract=${stamp}`);

const all = resources();
const byId = (id) => all.find((resource) => resource.id === id);

const folder = byId("folder:visitor_identification_models");
assert.ok(folder, "defineFolder(visitor_identification_models) must exist");
assert.equal(folder.spec.folderKind, "model", "the folder must be a model folder");

const connector = all.find(
  (resource) => resource.kind === "connector" && resource.spec.integrationSlug === "snitcher",
);
assert.ok(connector, "a Snitcher connector must be declared");

const companies = byId("model:website_visiting_companies");
assert.ok(companies, "defineModel(website_visiting_companies) must exist");
assert.equal(
  companies.spec.extractorSlug,
  "fetchOrganisations",
  "the companies model extracts fetchOrganisations: it is what provisions the tracker",
);
assert.match(
  companies.spec.config?.url ?? "",
  /^https:\/\/[a-z0-9.-]+\/?$/i,
  "the companies model's url is the site's HTTPS origin, the canonicalUrl the gate runs on",
);
assert.equal(
  companies.spec.schedule,
  undefined,
  "no schedule: the extractor fetches on Cargo's interval and refuses a cron",
);

const sessions = byId("model:website_visitor_sessions");
assert.ok(sessions, "defineModel(website_visitor_sessions) must exist");
assert.equal(sessions.spec.extractorSlug, "fetchSessions");
const workspace = sessions.spec.config?.workspaceUuid;
assert.equal(
  workspace?.resourceId,
  companies.id,
  "sessions read the Snitcher workspace the companies model provisioned",
);
assert.equal(workspace?.field, "config._workspaceUuid");

for (const model of [companies, sessions])
  assert.equal(
    model.spec.folderUuid?.resourceId,
    folder.id,
    `${model.id} must be filed in the visitor_identification_models folder`,
  );

// The site keeps only the snippet's profile ID and loads its own settings.
const snippet = (settings) =>
  `<script>\n!function(e){"use strict";var t=e&&e.namespace;}(${JSON.stringify(settings, null, 2)});\n</script>`;
const documented = {
  apiEndpoint: "radar.snitcher.com",
  cdn: "cdn.snitcher.com",
  namespace: "Snitcher",
  profileId: "Ab3_x-9Z",
};

const settings = snitcherSettings(snippet(documented));
assert.equal(settings.profileId, "Ab3_x-9Z");
assert.equal(settings.waitForConsent, true);
assert.deepEqual(
  Object.values(settings.features),
  [false, false, false, false, false],
  "form, click, download, error and recording capture stay off",
);
assert.equal(
  snitcherSettings(snippet({ ...documented, features: { formTracking: true } })).features
    .formTracking,
  false,
  "a snippet that turns form capture on is overridden",
);
for (const [label, bad] of [
  ["another API endpoint", { ...documented, apiEndpoint: "collector.example.com" }],
  ["another CDN", { ...documented, cdn: "cdn.example.com" }],
  ["another namespace", { ...documented, namespace: "Tracker" }],
  ["a profile ID carrying code", { ...documented, profileId: 'x"); alert(1); //' }],
])
  assert.throws(() => snitcherSettings(snippet(bad)), /Unrecognised Snitcher snippet/, label);
assert.throws(
  () => snitcherSettings("<script>console.log(1)</script>"),
  /Unrecognised Snitcher snippet/,
  "a snippet with no settings call",
);

console.log("ok: visitor-identification contract");
