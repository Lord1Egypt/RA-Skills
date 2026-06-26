/**
 * SolidPod-Data — Access Control Operations
 * Supports both WAC (Web Access Control) and ACP (Access Control Policies).
 * Detects which scheme the server uses automatically.
 *
 * All exported functions accept an optional `log` callback (default: console.log)
 * so callers can collect output without monkey-patching.
 */

import {
  getAgentAccess,
  getAgentAccessAll,
  setAgentAccess,
  getSolidDataset,
  saveSolidDatasetAt,
  createSolidDataset,
  buildThing,
  setThing,
  createThing,
  createContainerAt,
} from "@inrupt/solid-client";

import { RDF } from "@inrupt/vocab-common-rdf";
import { getAuthFetch, getWebId } from "./auth.js";

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatAccess(access) {
  const modes = [];
  if (access.read) modes.push("read");
  if (access.write) modes.push("write");
  if (access.append) modes.push("append");
  if (access.controlRead || access.control) modes.push("control-read");
  if (access.controlWrite || access.control) modes.push("control-write");
  return modes.length > 0 ? modes.join(", ") : "(none)";
}

function parseModes(modesStr) {
  const parts = modesStr.split(",").map(s => s.trim().toLowerCase());
  return {
    read: parts.includes("read"),
    write: parts.includes("write"),
    append: parts.includes("append"),
    controlRead: parts.includes("control") || parts.includes("control-read"),
    controlWrite: parts.includes("control") || parts.includes("control-write"),
  };
}

// ─── Show Access ───────────────────────────────────────────────────────────────

export async function showAccess(resourceUrl, log = console.log) {
  const authFetch = await getAuthFetch();

  let accessMap;
  try {
    accessMap = await getAgentAccessAll(resourceUrl, { fetch: authFetch });
  } catch (e) {
    throw new Error(`Could not read access for ${resourceUrl}: ${e.message}`);
  }

  log(`\nAccess control for: ${resourceUrl}`);
  log(`${"─".repeat(60)}`);

  const webIds = Object.keys(accessMap);
  if (webIds.length === 0) {
    log("  No agent-specific access entries.");
    return;
  }

  for (const webId of webIds) {
    log(`  ${webId}`);
    log(`    modes: ${formatAccess(accessMap[webId])}`);
  }
}

// ─── Grant Access ──────────────────────────────────────────────────────────────

export async function grantAccess(resourceUrl, webId, modesStr, log = console.log) {
  const authFetch = await getAuthFetch();
  const modes = parseModes(modesStr);

  try {
    await setAgentAccess(resourceUrl, webId, modes, { fetch: authFetch });
    log(`Granted access on ${resourceUrl}`);
    log(`  Agent: ${webId}`);
    log(`  Modes: ${formatAccess(modes)}`);
  } catch (e) {
    throw new Error(`Could not grant access: ${e.message}`);
  }
}

// ─── Revoke Access ─────────────────────────────────────────────────────────────

export async function revokeAccess(resourceUrl, webId, log = console.log) {
  const authFetch = await getAuthFetch();

  const noAccess = {
    read: false,
    write: false,
    append: false,
    controlRead: false,
    controlWrite: false,
  };

  try {
    await setAgentAccess(resourceUrl, webId, noAccess, { fetch: authFetch });
    log(`Revoked all access for ${webId} on ${resourceUrl}`);
  } catch (e) {
    throw new Error(`Could not revoke access: ${e.message}`);
  }
}

// ─── Access Requests ───────────────────────────────────────────────────────────

// RDF namespace URI for Solid interoperability — https:// per W3C Solid spec
const ACCESS_REQUEST_TYPE = "https://www.w3.org/ns/solid/interop#AccessRequest";
const SOLIDPOD_DATA_NS = "https://solidpod-data.example/ns#";

export async function requestAccess(resourceUrl, reason, log = console.log) {
  const authFetch = await getAuthFetch();
  const requesterWebId = await getWebId();

  const podUrl = process.env.SOLID_POD_URL;
  if (!podUrl) throw new Error("SOLID_POD_URL required to place access requests.");

  const containerUrl = podUrl.replace(/\/$/, "") + "/access-requests/";
  const requestUrl = containerUrl + Date.now() + ".ttl";

  const requestThing = buildThing(createThing({ url: requestUrl }))
    .addUrl(RDF.type, ACCESS_REQUEST_TYPE)
    .addStringNoLocale(`${SOLIDPOD_DATA_NS}requestedResource`, resourceUrl)
    .addStringNoLocale(`${SOLIDPOD_DATA_NS}requester`, requesterWebId)
    .addStringNoLocale(`${SOLIDPOD_DATA_NS}reason`, reason || "(no reason given)")
    .addStringNoLocale(`${SOLIDPOD_DATA_NS}createdAt`, new Date().toISOString())
    .build();

  // Ensure the access-requests container exists using the authenticated SOLID client
  try {
    await createContainerAt(containerUrl, { fetch: authFetch });
  } catch (e) {
    // Container likely already exists — continue
    if (process.env.SOLIDPOD_DATA_DEBUG) console.error(`[debug] createContainerAt ${containerUrl}: ${e.message}`);
  }

  let dataset = createSolidDataset();
  dataset = setThing(dataset, requestThing);
  await saveSolidDatasetAt(requestUrl, dataset, { fetch: authFetch });

  log(`Access request created: ${requestUrl}`);
  log(`  Requesting access to: ${resourceUrl}`);
  log(`  As: ${requesterWebId}`);
  if (reason) log(`  Reason: ${reason}`);
  log("\n  Share this URL with the resource owner so they can grant access.");
}

// ─── Check My Access ───────────────────────────────────────────────────────────

export async function checkMyAccess(resourceUrl, log = console.log) {
  const authFetch = await getAuthFetch();
  const webId = await getWebId();

  let access;
  try {
    access = await getAgentAccess(resourceUrl, webId, { fetch: authFetch });
  } catch (e) {
    throw new Error(`Could not check access for ${resourceUrl}: ${e.message}`);
  }

  log(`\nYour access (${webId})`);
  log(`Resource: ${resourceUrl}`);
  log(`${"─".repeat(60)}`);
  log(`  Modes: ${formatAccess(access || {})}`);
}
