#!/usr/bin/env node

/**
 * UCloud Skill - Manage UCloud cloud resources
 */

import { parseArgs } from "node:util";
import { exec } from "node:child_process";
import { promisify } from "node:util";
import { writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const execAsync = promisify(exec);

// Get current directory (where the script is executed from)
const __dirname = process.cwd();

// Ensure logs directory exists
const logsDir = join(__dirname, "logs");
if (!existsSync(logsDir)) {
  mkdirSync(logsDir, { recursive: true });
}

// Log function for resource operations
function logResourceOperation(action, resource, params, result) {
  // Only log create and delete operations
  if (!["create", "delete"].includes(action)) {
    return;
  }

  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    action,
    resource,
    params,
    success: result.success,
    ...(result.success ? { data: result.data || result.raw_output } : { error: result.error })
  };

  const logFile = join(logsDir, `ucloud-operations-${new Date().toISOString().split('T')[0]}.jsonl`);
  const logLine = JSON.stringify(logEntry) + "\n";

  try {
    writeFileSync(logFile, logLine, { flag: "a" });
  } catch (error) {
    console.error("Failed to write log:", error.message);
  }
}

// Parse command line arguments
const SKILL_VERSION = "1.0.0";

// Check for --version before parseArgs
if (process.argv.includes('--version') || process.argv.includes('-v')) {
  console.log(JSON.stringify({
    skill: "ucloud-infra",
    version: SKILL_VERSION,
    node: process.version,
    description: "UCloud Cloud Management - Complete Version"
  }, null, 2));
  process.exit(0);
}

const { values } = parseArgs({
  options: {
    action: { type: "string" },
    resource: { type: "string" },
    id: { type: "string" },
    "uhost-id": { type: "string" },
    "udb-id": { type: "string" },
    "cache-id": { type: "string" },
    "udisk-id": { type: "string" },
    "ulb-id": { type: "string" },
    "vpc-id": { type: "string" },
    "subnet-id": { type: "string" },
    "eip-id": { type: "string" },
    "firewall-id": { type: "string" },
    "image-id": { type: "string" },
    "snapshot-id": { type: "string" },
    "backup-id": { type: "string" },
    "conf-id": { type: "string" },
    "rule-id": { type: "string" },
    "vserver-id": { type: "string" },
    "backend-id": { type: "string" },
    "policy-id": { type: "string" },
    "cert-id": { type: "string" },
    "share-bandwidth-id": { type: "string" },
    "bw-pkg-id": { type: "string" },
    "location": { type: "string" },
    "uga-id": { type: "string" },
    cpu: { type: "string" },
    "memory-gb": { type: "string" },
    password: { type: "string" },
    name: { type: "string" },
    count: { type: "string", default: "1" },
    "memory-size-gb": { type: "string", default: "1" },
    "disk-size-gb": { type: "string", default: "20" },
    port: { type: "string", default: "3306" },
    mode: { type: "string", default: "Normal" },
    version: { type: "string" },
    "size-gb": { type: "string" },
    line: { type: "string" },
    "bandwidth-mb": { type: "string" },
    "traffic-mode": { type: "string" },
    segment: { type: "string" },
    "target-uhost-id": { type: "string" },
    "clone-udisk-id": { type: "string" },
    "snapshot-size-gb": { type: "string" },
    "resource-id": { type: "string" },
    "bind-eip": { type: "string" },
    "create-eip-bandwidth-mb": { type: "string" },
    "create-eip-line": { type: "string" },
    remark: { type: "string" },
    limit: { type: "string" },
    offset: { type: "string" },
    region: { type: "string" },
    zone: { type: "string" },
  },
});

const publicKey = process.env.UCLOUD_PUBLIC_KEY;
const privateKey = process.env.UCLOUD_PRIVATE_KEY;
const projectId = process.env.UCLOUD_PROJECT_ID;
const region = values.region || process.env.UCLOUD_REGION || "cn-wlcb";
const zone = values.zone || process.env.UCLOUD_ZONE || "cn-wlcb-01";

if (!publicKey || !privateKey) {
  console.error(JSON.stringify({
    error: "missing_credentials",
    message: "Please set UCLOUD_PUBLIC_KEY and UCLOUD_PRIVATE_KEY environment variables."
  }, null, 2));
  process.exit(1);
}

if (!projectId) {
  console.error(JSON.stringify({
    error: "missing_project_id",
    message: "Please set UCLOUD_PROJECT_ID environment variable."
  }, null, 2));
  process.exit(1);
}

async function runUcloudCommand(args, options = {}) {
  const { skipProjectParams = false, skipZone = false } = options;

  const baseArgs = [
    "--public-key", publicKey,
    "--private-key", privateKey,
    "--json"
  ];

  // Some commands (like 'region') don't accept project-id, region, zone
  if (!skipProjectParams) {
    baseArgs.push("--project-id", projectId);
    baseArgs.push("--region", region);
    // Some commands (like 'eip list') don't accept --zone
    if (!skipZone) {
      baseArgs.push("--zone", zone);
    }
  }

  const fullArgs = [...baseArgs, ...args];
  const command = "ucloud " + fullArgs.join(" ");
  try {
    const { stdout, stderr } = await execAsync(command);
    if (stderr) {
      return { success: false, error: stderr };
    }
    try {
      const data = JSON.parse(stdout);
      return { success: true, data: data };
    } catch {
      return { success: true, raw_output: stdout };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

async function handleUHost(action) {
  let result;
  switch (action) {
    case "list":
      return await runUcloudCommand(["uhost", "list"]);
    case "create":
      if (!values.cpu || !values["memory-gb"] || !values.password || !values["image-id"]) {
        return { success: false, error: "Missing required: --cpu, --memory-gb, --password, --image-id" };
      }
      const createArgs = ["uhost", "create", "--cpu", values.cpu, "--memory-gb", values["memory-gb"], "--password", values.password, "--image-id", values["image-id"]];
      if (values.name) createArgs.push("--name", values.name);
      if (values.count) createArgs.push("--count", values.count);
      result = await runUcloudCommand(createArgs);
      logResourceOperation("create", "uhost", {
        cpu: values.cpu,
        memoryGb: values["memory-gb"],
        imageId: values["image-id"],
        name: values.name,
        count: values.count
      }, result);
      return result;
    case "start":
    case "stop":
    case "restart":
      const uhostId = values.id || values["uhost-id"];
      if (!uhostId) return { success: false, error: "Missing: --id or --uhost-id" };
      return await runUcloudCommand(["uhost", action, "--uhost-id", uhostId]);
    case "delete":
      const deleteUhostId = values.id || values["uhost-id"];
      if (!deleteUhostId) return { success: false, error: "Missing: --id or --uhost-id" };
      result = await runUcloudCommand(["uhost", "delete", "--uhost-id", deleteUhostId]);
      logResourceOperation("delete", "uhost", { uhostId: deleteUhostId }, result);
      return result;
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleMySQL(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["mysql", "db", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleRedis(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["redis", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleMemcache(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["memcache", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleEIP(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["eip", "list"], { skipZone: true });
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleUDisk(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["udisk", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleULB(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["ulb", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleVPC(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["vpc", "list"], { skipZone: true });
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleSubnet(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["subnet", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleFirewall(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["firewall", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleImage(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["image", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleProject(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["project", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleGSSH(action) {
  switch (action) {
    case "list":
      return await runUcloudCommand(["gssh", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handlePathX(action) {
  switch (action) {
    case "uga":
      return await runUcloudCommand(["pathx", "uga", "list"]);
    default:
      return { success: false, error: "Unknown action: " + action };
  }
}

async function handleRegion() {
  return await runUcloudCommand(["region"], { skipProjectParams: true });
}

async function handleConfig(action) {
  if (action === "list") {
    return await runUcloudCommand(["config", "list"]);
  }
  return { success: false, error: "Unknown action: " + action };
}

(async () => {
  if (!values.action || !values.resource) {
    console.error(JSON.stringify({
      error: "missing_parameters",
      message: "Please provide --action and --resource parameters"
    }, null, 2));
    process.exit(1);
  }

  let result;
  switch (values.resource) {
    case "uhost":
      result = await handleUHost(values.action);
      break;
    case "mysql":
      result = await handleMySQL(values.action);
      break;
    case "redis":
      result = await handleRedis(values.action);
      break;
    case "memcache":
      result = await handleMemcache(values.action);
      break;
    case "eip":
      result = await handleEIP(values.action);
      break;
    case "udisk":
      result = await handleUDisk(values.action);
      break;
    case "ulb":
      result = await handleULB(values.action);
      break;
    case "vpc":
      result = await handleVPC(values.action);
      break;
    case "subnet":
      result = await handleSubnet(values.action);
      break;
    case "firewall":
      result = await handleFirewall(values.action);
      break;
    case "image":
      result = await handleImage(values.action);
      break;
    case "project":
      result = await handleProject(values.action);
      break;
    case "gssh":
      result = await handleGSSH(values.action);
      break;
    case "pathx":
      result = await handlePathX(values.action);
      break;
    case "region":
      result = await handleRegion();
      break;
    case "config":
      result = await handleConfig(values.action);
      break;
    default:
      result = {
        success: false,
        error: "Unknown resource: " + values.resource
      };
  }

  console.log(JSON.stringify(result, null, 2));

  if (!result.success) {
    process.exit(1);
  }
})();
