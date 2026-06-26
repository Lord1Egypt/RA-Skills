/**
 * SolidPod-Data — Core Pod Operations
 * Read datasets, list containers, write data, delete resources,
 * and provision new pods on Community Solid Server instances.
 *
 * All exported functions accept an optional `log` callback (default: console.log)
 * so callers can collect output without monkey-patching.
 */

import {
  getSolidDataset,
  getThingAll,
  getUrlAll,
  getStringNoLocaleAll,
  saveSolidDatasetAt,
  createSolidDataset,
  buildThing,
  setThing,
  createThing,
  deleteSolidDataset,
  getContainedResourceUrlAll,
  createContainerAt,
  getSourceUrl,
  getPodUrlAll,
} from "@inrupt/solid-client";

import { RDF } from "@inrupt/vocab-common-rdf";
import { getAuthFetch, getWebId } from "./auth.js";

// ─── Helpers ──────────────────────────────────────────────────────────────────

let _podUrlOverride = null;

/** Override the pod URL at runtime without mutating process.env. */
export function setPodUrl(url) {
  _podUrlOverride = url;
}

function defaultPodUrl() {
  const url = _podUrlOverride || process.env.SOLID_POD_URL;
  if (!url) throw new Error("SOLID_POD_URL is not set. Pass --pod-url or set the env var.");
  return url.endsWith("/") ? url : url + "/";
}

function ensureTrailingSlash(url) {
  return url.endsWith("/") ? url : url + "/";
}

function printThing(thing, log) {
  const predicates = Object.keys(thing.predicates || {});
  if (predicates.length === 0) {
    log("  (no predicates)");
    return;
  }
  for (const pred of predicates) {
    const values = [
      ...(getUrlAll(thing, pred) || []),
      ...(getStringNoLocaleAll(thing, pred) || []),
    ];
    for (const val of values) {
      log(`  ${pred}`);
      log(`    = ${val}`);
    }
  }
}

// ─── Read ──────────────────────────────────────────────────────────────────────

export async function readDataset(url, log = console.log) {
  const authFetch = await getAuthFetch();
  let dataset;
  try {
    dataset = await getSolidDataset(url, { fetch: authFetch });
  } catch (e) {
    throw new Error(`Could not read dataset at ${url}: ${e.message}`);
  }

  const things = getThingAll(dataset);
  if (things.length === 0) {
    log(`Dataset at ${url} is empty.`);
    return;
  }

  log(`\nDataset: ${url}\n${"─".repeat(60)}`);
  for (const thing of things) {
    log(`\nThing: ${getSourceUrl(thing) || thing.url || "(blank)"}`);
    printThing(thing, log);
  }
}

export async function readThing(datasetUrl, thingUrl, log = console.log) {
  const authFetch = await getAuthFetch();
  const dataset = await getSolidDataset(datasetUrl, { fetch: authFetch });
  const things = getThingAll(dataset);
  const thing = things.find(t => (getSourceUrl(t) || t.url) === thingUrl);
  if (!thing) {
    throw new Error(`Thing ${thingUrl} not found in dataset ${datasetUrl}`);
  }
  log(`\nThing: ${thingUrl}\n${"─".repeat(60)}`);
  printThing(thing, log);
}

export async function listContainer(url, log = console.log) {
  const authFetch = await getAuthFetch();
  url = ensureTrailingSlash(url);
  let dataset;
  try {
    dataset = await getSolidDataset(url, { fetch: authFetch });
  } catch (e) {
    throw new Error(`Could not list container at ${url}: ${e.message}`);
  }

  const contained = getContainedResourceUrlAll(dataset);
  log(`\nContainer: ${url}`);
  log(`${"─".repeat(60)}`);

  if (contained.length === 0) {
    log("  (empty)");
    return;
  }

  for (const resourceUrl of contained) {
    const isDir = resourceUrl.endsWith("/");
    log(`  ${isDir ? "[DIR] " : "[RES] "} ${resourceUrl}`);
  }
  log(`\n${contained.length} item(s)`);
}

export async function readPodResource(url, log = console.log) {
  const authFetch = await getAuthFetch();
  let response;
  try {
    response = await authFetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status} ${response.statusText}`);
  } catch (e) {
    throw new Error(`Could not fetch resource at ${url}: ${e.message}`);
  }

  const text = await response.text();
  log(`\nResource: ${url}`);
  log(`Content-Type: ${response.headers.get("content-type") || "unknown"}`);
  log(`${"─".repeat(60)}`);
  log(text);
}

export async function podInfo(url, log = console.log) {
  url = url || defaultPodUrl();
  const authFetch = await getAuthFetch();

  let dataset;
  try {
    dataset = await getSolidDataset(url, { fetch: authFetch });
  } catch (e) {
    throw new Error(`Could not fetch pod info at ${url}: ${e.message}`);
  }

  const webId = await getWebId();
  const things = getThingAll(dataset);

  log(`\nPod: ${url}`);
  log(`Authenticated as: ${webId}`);
  log(`${"─".repeat(60)}`);

  const storages = getPodUrlAll(dataset);
  if (storages.length > 0) {
    log("Storage roots:");
    for (const s of storages) log(`  ${s}`);
  } else {
    log("Storage roots: (none advertised in dataset)");
  }

  log(`Things in root: ${things.length}`);
}

// ─── Write ─────────────────────────────────────────────────────────────────────

export async function createContainer(url, log = console.log) {
  const authFetch = await getAuthFetch();
  url = ensureTrailingSlash(url);
  try {
    await createContainerAt(url, { fetch: authFetch });
    log(`Created container: ${url}`);
  } catch (e) {
    throw new Error(`Could not create container at ${url}: ${e.message}`);
  }
}

export async function writeDataset(datasetUrl, predicate, object, log = console.log) {
  const authFetch = await getAuthFetch();

  let dataset;
  let exists = true;
  try {
    dataset = await getSolidDataset(datasetUrl, { fetch: authFetch });
  } catch (e) {
    if (process.env.SOLIDPOD_DATA_DEBUG) console.error(`[debug] Dataset not found at ${datasetUrl}, will create: ${e.message}`);
    dataset = createSolidDataset();
    exists = false;
  }

  const thingUrl = datasetUrl + "#data";
  const isUrl = /^https?:\/\//.test(object);
  const thing = isUrl
    ? buildThing(createThing({ url: thingUrl })).addUrl(predicate, object).build()
    : buildThing(createThing({ url: thingUrl })).addStringNoLocale(predicate, object).build();

  dataset = setThing(dataset, thing);
  await saveSolidDatasetAt(datasetUrl, dataset, { fetch: authFetch });
  log(`${exists ? "Updated" : "Created"} dataset: ${datasetUrl}`);
  log(`  <${thingUrl}> <${predicate}> "${object}"`);
}


export async function deleteResource(url, log = console.log) {
  const authFetch = await getAuthFetch();
  try {
    if (url.endsWith("/")) {
      await deleteSolidDataset(url, { fetch: authFetch });
    } else {
      const res = await authFetch(url, { method: "DELETE" });
      if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
    }
    log(`Deleted: ${url}`);
  } catch (e) {
    throw new Error(`Could not delete ${url}: ${e.message}`);
  }
}

// ─── Area / Topic Management ───────────────────────────────────────────────────

const SOLIDPOD_DATA_NS = "https://solidpod-data.example/ns#";
const AREA_TYPE = `${SOLIDPOD_DATA_NS}Area`;
const AREA_INDEX = "solidpod-data-areas.ttl";

function areaIndexUrl(basePodUrl) {
  return ensureTrailingSlash(basePodUrl) + AREA_INDEX;
}

export async function listAreas(basePodUrl, log = console.log) {
  basePodUrl = basePodUrl || defaultPodUrl();
  const authFetch = await getAuthFetch();
  const indexUrl = areaIndexUrl(basePodUrl);

  let dataset;
  try {
    dataset = await getSolidDataset(indexUrl, { fetch: authFetch });
  } catch (e) {
    if (process.env.SOLIDPOD_DATA_DEBUG) console.error(`[debug] Area index not found at ${indexUrl}: ${e.message}`);
    log("No areas registered yet. Use: /solidpod-data area create <name>");
    return;
  }

  const things = getThingAll(dataset);
  const areas = things.filter(t => getUrlAll(t, RDF.type).includes(AREA_TYPE));

  if (areas.length === 0) {
    log("No areas found.");
    return;
  }

  log(`\nSolidPod-Data Areas in ${basePodUrl}\n${"─".repeat(60)}`);
  for (const area of areas) {
    const url = getSourceUrl(area) || area.url;
    const names = getStringNoLocaleAll(area, `${SOLIDPOD_DATA_NS}name`);
    const descs = getStringNoLocaleAll(area, `${SOLIDPOD_DATA_NS}description`);
    log(`\n  Area: ${names[0] || "(unnamed)"}`);
    log(`  URL:  ${url}`);
    if (descs[0]) log(`  Desc: ${descs[0]}`);
  }
}

export async function createArea(name, description, basePodUrl, log = console.log) {
  basePodUrl = basePodUrl || defaultPodUrl();
  const authFetch = await getAuthFetch();
  const areaContainerUrl = ensureTrailingSlash(basePodUrl) + name + "/";
  const indexUrl = areaIndexUrl(basePodUrl);

  await createContainerAt(areaContainerUrl, { fetch: authFetch });
  log(`Created area container: ${areaContainerUrl}`);

  let indexDataset;
  try {
    indexDataset = await getSolidDataset(indexUrl, { fetch: authFetch });
  } catch (e) {
    if (process.env.SOLIDPOD_DATA_DEBUG) console.error(`[debug] Area index not found at ${indexUrl}, will create: ${e.message}`);
    indexDataset = createSolidDataset();
  }

  let thing = buildThing(createThing({ url: areaContainerUrl }))
    .addUrl(RDF.type, AREA_TYPE)
    .addStringNoLocale(`${SOLIDPOD_DATA_NS}name`, name);

  if (description) {
    thing = thing.addStringNoLocale(`${SOLIDPOD_DATA_NS}description`, description);
  }

  indexDataset = setThing(indexDataset, thing.build());
  await saveSolidDatasetAt(indexUrl, indexDataset, { fetch: authFetch });
  log(`Registered area "${name}" in ${indexUrl}`);
}

// ─── Pod Provisioning (Community Solid Server) ────────────────────────────────

/**
 * Print step-by-step instructions for creating a new SOLID Pod on a
 * Community Solid Server (CSS) instance.
 *
 * We output the registration command rather than executing it directly,
 * so the user retains full control over credentials and the registration
 * request is made from their own shell session.
 */
export async function createPod(username, cssBaseUrl, log = console.log) {
  const parsed = new URL(cssBaseUrl);
  if (!["https:", "http:"].includes(parsed.protocol)) {
    throw new Error("cssBaseUrl must be an http or https URL.");
  }

  const registrationUrl = ensureTrailingSlash(cssBaseUrl) + "idp/register/";
  const email = `${username}@solidpod-data.local`;

  log(`\nTo create a SOLID Pod for "${username}" on ${cssBaseUrl}:`);
  log(`\n${"─".repeat(60)}`);
  log(`Option 1 — Web UI (recommended):`);
  log(`  Open ${cssBaseUrl} in your browser and complete registration.`);
  log(`  Use pod name: ${username}`);
  log(`  Use email:    ${email}`);
  log(`\nOption 2 — CSS HTTP registration endpoint:`);
  log(`  POST to: ${registrationUrl}`);
  log(`  See Community Solid Server docs for the required JSON fields:`);
  log(`  https://communitysolidserver.github.io/CommunitySolidServer/`);
  log(`\n${"─".repeat(60)}`);
  log(`After registration, set these env vars to use the pod with SolidPod-Data:`);
  log(`  SOLID_IDP=${cssBaseUrl}`);
  log(`  SOLID_POD_URL=${ensureTrailingSlash(cssBaseUrl)}${username}/`);
}
