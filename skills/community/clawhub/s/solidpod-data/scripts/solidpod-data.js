#!/usr/bin/env node
/**
 * SolidPod-Data — Main CLI Dispatcher
 * Routes commands to pod.js or access.js handlers.
 *
 * Usage: node solidpod-data.js <command> [args...]
 */

import {
  readDataset,
  readThing,
  listContainer,
  readPodResource,
  podInfo,
  createContainer,
  writeDataset,
  deleteResource,
  listAreas,
  createArea,
  createPod,
  setPodUrl,
} from "./pod.js";

import {
  showAccess,
  grantAccess,
  revokeAccess,
  requestAccess,
  checkMyAccess,
} from "./access.js";

// ─── Argument Parsing ─────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = argv.slice(2);
  const flags = {};
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      const val = args[i + 1] && !args[i + 1].startsWith("--") ? args[++i] : true;
      flags[key] = val;
    } else {
      positional.push(args[i]);
    }
  }

  return { positional, flags };
}

function usage() {
  console.log(`
SolidPod-Data — SOLID Pod CLI

Usage: solidpod-data <command> [options]

Read commands:
  read <url>                         Read all Things from an RDF dataset
  thing <dataset-url> <thing-url>    Read a specific Thing
  list <container-url>               List contents of a container
  resource <url>                     Read a non-RDF pod resource
  pod info [url]                     Show pod info

Write commands:
  mkdir <url>                        Create a container
  write <url> <predicate> <object>   Write a triple to a dataset
  delete <url>                       Delete a resource

Access commands:
  acl show <url>                     Show access control entries
  acl grant <url> <webid> <modes>    Grant access (modes: read,write,append,control)
  acl revoke <url> <webid>           Revoke all access for a WebID
  acl request <url>                  Request access  [--reason "text"]
  acl check <url>                    Check your own access

Area commands:
  area list [pod-url]                List SolidPod-Data areas
  area create <name>                 Create an area  [--description "text"] [--pod-url <url>]
  area request <url>                 Request access to an area  [--reason "text"]

Pod provisioning:
  pod create <username>              Print CSS registration instructions  --server <url>

Options:
  --description <t>  Description for area create
  --pod-url <url>    Override SOLID_POD_URL
  --server <url>     CSS base URL for pod create
  --reason <text>    Reason for access request
`);
}

// ─── Command Router ───────────────────────────────────────────────────────────

async function main() {
  const { positional, flags } = parseArgs(process.argv);

  if (flags["pod-url"]) setPodUrl(flags["pod-url"]);

  const [cmd, sub, ...rest] = positional;

  if (!cmd || cmd === "help" || cmd === "--help" || cmd === "-h") {
    usage();
    process.exit(0);
  }

  try {
    switch (cmd) {

      // ── Read ──
      case "read":
        if (!sub) throw new Error("Usage: solidpod-data read <url>");
        await readDataset(sub);
        break;

      case "thing": {
        const [datasetUrl, thingUrl] = [sub, rest[0]];
        if (!datasetUrl || !thingUrl) throw new Error("Usage: solidpod-data thing <dataset-url> <thing-url>");
        await readThing(datasetUrl, thingUrl);
        break;
      }

      case "list":
        if (!sub) throw new Error("Usage: solidpod-data list <container-url>");
        await listContainer(sub);
        break;

      case "resource":
        if (!sub) throw new Error("Usage: solidpod-data resource <url>");
        await readPodResource(sub);
        break;

      // ── Write ──
      case "mkdir":
        if (!sub) throw new Error("Usage: solidpod-data mkdir <url>");
        await createContainer(sub);
        break;

      case "write": {
        const [url, predicate, object] = [sub, rest[0], rest[1]];
        if (!url || !predicate || !object)
          throw new Error("Usage: solidpod-data write <url> <predicate> <object>");
        await writeDataset(url, predicate, object);
        break;
      }

      case "delete":
        if (!sub) throw new Error("Usage: solidpod-data delete <url>");
        await deleteResource(sub);
        break;

      // ── Pod ──
      case "pod":
        if (sub === "info") {
          await podInfo(rest[0] || null);
        } else if (sub === "create") {
          const username = rest[0];
          if (!username || !flags.server)
            throw new Error("Usage: solidpod-data pod create <username> --server <css-base-url>");
          await createPod(username, flags.server);
        } else {
          throw new Error(`Unknown pod subcommand: ${sub}. Use: info, create`);
        }
        break;

      // ── ACL ──
      case "acl":
        if (sub === "show") {
          if (!rest[0]) throw new Error("Usage: solidpod-data acl show <url>");
          await showAccess(rest[0]);
        } else if (sub === "grant") {
          const [url, webId, modes] = rest;
          if (!url || !webId || !modes)
            throw new Error("Usage: solidpod-data acl grant <url> <webid> <modes>");
          await grantAccess(url, webId, modes);
        } else if (sub === "revoke") {
          const [url, webId] = rest;
          if (!url || !webId)
            throw new Error("Usage: solidpod-data acl revoke <url> <webid>");
          await revokeAccess(url, webId);
        } else if (sub === "request") {
          const url = rest[0];
          if (!url) throw new Error("Usage: solidpod-data acl request <url> [--reason <text>]");
          await requestAccess(url, flags.reason || "");
        } else if (sub === "check") {
          const url = rest[0];
          if (!url) throw new Error("Usage: solidpod-data acl check <url>");
          await checkMyAccess(url);
        } else {
          throw new Error(`Unknown acl subcommand: ${sub}. Use: show, grant, revoke, request, check`);
        }
        break;

      // ── Area ──
      case "area":
        if (sub === "list") {
          await listAreas(rest[0] || null);
        } else if (sub === "create") {
          const name = rest[0];
          if (!name) throw new Error("Usage: solidpod-data area create <name> [--description <text>]");
          await createArea(name, flags.description || "", flags["pod-url"] || null);
        } else if (sub === "request") {
          const url = rest[0];
          if (!url) throw new Error("Usage: solidpod-data area request <url> [--reason <text>]");
          await requestAccess(url, flags.reason || "");
        } else {
          throw new Error(`Unknown area subcommand: ${sub}. Use: list, create, request`);
        }
        break;

      default:
        console.error(`Unknown command: ${cmd}`);
        usage();
        process.exit(1);
    }
  } catch (err) {
    console.error(`\nError: ${err.message}`);
    if (process.env.SOLIDPOD_DATA_DEBUG) console.error(err.stack);
    process.exit(1);
  }
}

main();
