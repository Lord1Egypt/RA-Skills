#!/usr/bin/env node

// bin/pulse.ts
import { Command as Command7 } from "commander";

// src/lib/output.ts
import chalk from "chalk";
var jsonMode = false;
function setJsonMode(enabled) {
  jsonMode = enabled;
}
function isJsonMode() {
  return jsonMode;
}
function output(data) {
  if (jsonMode) {
    console.log(JSON.stringify(data, bigintReplacer, 2));
  } else if (Array.isArray(data)) {
    printTable(data);
  } else if (typeof data === "object" && data !== null) {
    printKeyValue(data);
  } else {
    console.log(data);
  }
}
function success(msg) {
  if (!jsonMode) {
    console.log(chalk.green("\u2713") + " " + msg);
  }
}
function error(msg) {
  if (jsonMode) {
    console.error(JSON.stringify({ error: msg }));
  } else {
    console.error(chalk.red("\u2717") + " " + msg);
  }
  process.exit(1);
}
function info(msg) {
  if (!jsonMode) {
    console.log(chalk.blue("\u2139") + " " + msg);
  }
}
function printKeyValue(obj) {
  const maxKey = Math.max(...Object.keys(obj).map((k) => k.length));
  for (const [key, val] of Object.entries(obj)) {
    const label = chalk.bold(key.padEnd(maxKey));
    console.log(`  ${label}  ${formatValue(val)}`);
  }
}
function printTable(rows) {
  if (rows.length === 0) {
    console.log("  (no data)");
    return;
  }
  const keys = Object.keys(rows[0]);
  const widths = keys.map(
    (k) => Math.max(k.length, ...rows.map((r) => String(r[k] ?? "").length))
  );
  const header = keys.map((k, i) => chalk.bold(k.padEnd(widths[i]))).join("  ");
  console.log("  " + header);
  console.log("  " + widths.map((w) => "\u2500".repeat(w)).join("  "));
  for (const row of rows) {
    const line = keys.map((k, i) => String(row[k] ?? "").padEnd(widths[i])).join("  ");
    console.log("  " + line);
  }
}
function formatValue(val) {
  if (typeof val === "bigint") return val.toString();
  if (val === void 0 || val === null) return chalk.dim("\u2014");
  return String(val);
}
function bigintReplacer(_key, value) {
  return typeof value === "bigint" ? value.toString() : value;
}

// src/commands/browse.ts
import { Command } from "commander";
import { DEFAULT_SCHEMAS, IndexerClient, ServiceType, formatUsdm } from "@pulseai/sdk";

// src/config.ts
import { createMainnetClient } from "@pulseai/sdk";
import { privateKeyToAccount } from "viem/accounts";
import fs from "fs";
import os from "os";
import path from "path";
var CONFIG_PATH = path.join(os.homedir(), ".pulse", "config.json");
var _client;
function loadConfig() {
  try {
    if (!fs.existsSync(CONFIG_PATH)) {
      return {};
    }
    const raw = fs.readFileSync(CONFIG_PATH, "utf8").trim();
    if (!raw) {
      return {};
    }
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") {
      return {};
    }
    const privateKey = parsed.privateKey;
    if (typeof privateKey !== "string" || !privateKey) {
      return {};
    }
    return { privateKey };
  } catch (e) {
    throw new Error(
      `Failed to load Pulse config from ${CONFIG_PATH}: ${e instanceof Error ? e.message : String(e)}`
    );
  }
}
function saveConfig(config) {
  try {
    fs.mkdirSync(path.dirname(CONFIG_PATH), { recursive: true });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + "\n", "utf8");
  } catch (e) {
    throw new Error(
      `Failed to save Pulse config to ${CONFIG_PATH}: ${e instanceof Error ? e.message : String(e)}`
    );
  }
}
function getPrivateKey() {
  if (process.env.PULSE_PRIVATE_KEY) {
    return process.env.PULSE_PRIVATE_KEY;
  }
  return loadConfig().privateKey;
}
function getClient() {
  if (_client) return _client;
  const key = getPrivateKey();
  if (!key) {
    throw new Error(
      "No wallet private key found. Set PULSE_PRIVATE_KEY or run `pulse wallet generate`.\nConfig fallback path: ~/.pulse/config.json"
    );
  }
  const account = privateKeyToAccount(key);
  _client = createMainnetClient({ account });
  return _client;
}
function getReadClient() {
  if (_client) return _client;
  const key = getPrivateKey();
  if (key) {
    return getClient();
  }
  _client = createMainnetClient();
  return _client;
}
function getAddress() {
  const key = getPrivateKey();
  if (!key) {
    throw new Error("No wallet private key found. Set PULSE_PRIVATE_KEY or run `pulse wallet generate`.");
  }
  return privateKeyToAccount(key).address;
}

// src/commands/browse.ts
var SERVICE_TYPE_NAMES = {
  0: "TextGeneration",
  1: "ImageGeneration",
  2: "DataAnalysis",
  3: "CodeGeneration",
  4: "Translation",
  5: "Custom"
};
var browseCommand = new Command("browse").description("Browse available offerings on the Pulse marketplace").argument("[query]", "Search query (filters by description)").option("--type <serviceType>", "Filter by service type (0-5 or name)").option("--max-price <usdm>", 'Maximum price in USDm (e.g. "10.0")').option("--agent-id <id>", "Filter by provider agent ID").option("--json", "Output as JSON").action(async (query, opts) => {
  try {
    const client = getReadClient();
    const indexer = new IndexerClient({ baseUrl: client.indexerUrl });
    const filter = {
      active: true
    };
    if (opts.type !== void 0) {
      filter.serviceType = parseServiceType(opts.type);
    }
    if (opts.agentId !== void 0) {
      filter.agentId = Number(opts.agentId);
    }
    info("Searching Pulse marketplace...");
    let offerings = await indexer.getOfferings(filter);
    if (opts.maxPrice) {
      const maxPrice = parseFloat(opts.maxPrice);
      offerings = offerings.filter((o) => {
        const price = parseFloat(formatUsdm(BigInt(o.priceUsdm)));
        return price <= maxPrice;
      });
    }
    if (query) {
      const q = query.toLowerCase();
      offerings = offerings.filter(
        (o) => o.description?.toLowerCase().includes(q)
      );
    }
    if (offerings.length === 0) {
      if (isJsonMode()) {
        output({ offerings: [], count: 0 });
      } else {
        info("No offerings found matching your criteria.");
      }
      return;
    }
    if (isJsonMode()) {
      output({
        offerings: offerings.map((o) => ({
          offeringId: o.offeringId,
          agentId: o.agentId,
          serviceType: SERVICE_TYPE_NAMES[o.serviceType] ?? String(o.serviceType),
          priceUsdm: formatUsdm(BigInt(o.priceUsdm)),
          slaMinutes: o.slaMinutes,
          description: o.description,
          requirementsSchemaUri: o.requirementsSchemaUri ?? null,
          fallbackSchema: o.requirementsSchemaUri ? null : DEFAULT_SCHEMAS[o.serviceType] ?? null
        })),
        count: offerings.length
      });
    } else {
      output(
        offerings.map((o) => ({
          id: o.offeringId,
          agent: o.agentId,
          type: SERVICE_TYPE_NAMES[o.serviceType] ?? String(o.serviceType),
          price: formatUsdm(BigInt(o.priceUsdm)) + " USDm",
          sla: o.slaMinutes ? `${o.slaMinutes}m` : "\u2014",
          description: truncate(o.description ?? "", 50)
        }))
      );
    }
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
function truncate(s, max) {
  return s.length > max ? s.slice(0, max - 1) + "\u2026" : s;
}
function parseServiceType(val) {
  const num = Number(val);
  if (!isNaN(num) && num >= 0 && num <= 5) return num;
  const key = val;
  if (key in ServiceType) return ServiceType[key];
  throw new Error(
    `Invalid service type: ${val}. Use 0-5 or name (TextGeneration, ImageGeneration, DataAnalysis, CodeGeneration, Translation, Custom)`
  );
}

// src/commands/agent.ts
import { Command as Command2 } from "commander";
import { registerAgent, initAgent, getAgent, setOperator, IndexerClient as IndexerClient2 } from "@pulseai/sdk";
var agentCommand = new Command2("agent").description("Agent registration and info");
agentCommand.command("register").description("Register a new agent and initialize it in Pulse").option("--name <name>", "Agent name (used as URI)", "pulse-agent").option("--json", "Output as JSON").action(async (opts) => {
  try {
    const client = getClient();
    const address = getAddress();
    info("Registering agent in ERC-8004 Identity Registry...");
    const result = await registerAgent(client, opts.name);
    info(`Agent ID: ${result.agentId}. Initializing in Pulse...`);
    const initHash = await initAgent(client, result.agentId, address);
    output({
      agentId: result.agentId,
      owner: address,
      operator: address,
      registerTx: result.txHash,
      initTx: initHash
    });
    success(`Agent registered and initialized with ID: ${result.agentId}`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
agentCommand.command("info").description("Get agent information").argument("<agentId>", "Agent ID").option("--json", "Output as JSON").action(async (agentIdStr) => {
  try {
    const client = getReadClient();
    try {
      const data = await getAgent(client, BigInt(agentIdStr));
      output({
        agentId: agentIdStr,
        owner: data.owner,
        operator: data.pulseData.operator,
        warrenContract: data.pulseData.warrenMasterContract,
        registeredAt: data.pulseData.registeredAt,
        active: data.active
      });
    } catch {
      const indexer = new IndexerClient2({ baseUrl: client.indexerUrl });
      const agent = await indexer.getAgent(Number(agentIdStr));
      output({
        agentId: agent.agentId,
        owner: agent.owner,
        operator: agent.operator,
        warrenContract: agent.warrenContract,
        registeredAt: agent.registeredAt,
        active: agent.active
      });
    }
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
agentCommand.command("set-operator").description("Set operator for an agent (owner only)").requiredOption("--agent-id <id>", "Agent ID").requiredOption("--operator <address>", "Operator address").option("--json", "Output as JSON").action(async (opts) => {
  try {
    const client = getClient();
    info("Setting operator...");
    const txHash = await setOperator(client, BigInt(opts.agentId), opts.operator);
    output({ agentId: opts.agentId, operator: opts.operator, txHash });
    success("Operator updated");
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});

// src/commands/job.ts
import { Command as Command3 } from "commander";
import {
  createJob,
  acceptJob,
  submitDeliverable,
  evaluate,
  settle,
  cancelJob,
  getJob,
  getAgent as getAgent2,
  getOffering,
  createJobTerms,
  deployRequirements,
  deployDeliverable,
  readRequirements,
  readDeliverable,
  IndexerClient as IndexerClient3,
  formatUsdm as formatUsdm2,
  DEFAULT_SCHEMAS as DEFAULT_SCHEMAS2,
  validateAgainstSchema
} from "@pulseai/sdk";
var STATUS_NAMES = {
  0: "Created",
  1: "Accepted",
  2: "InProgress",
  3: "Delivered",
  4: "Evaluated",
  5: "Completed",
  6: "Disputed",
  7: "Cancelled"
};
var jobCommand = new Command3("job").description("Job lifecycle commands");
jobCommand.command("create").description("Create a new job (auto-approves USDm, deploys WARREN terms)").requiredOption("--offering <id>", "Offering ID").requiredOption("--agent-id <id>", "Your (buyer) agent ID").option("--requirements <json>", "JSON requirements to attach").option("--json", "Output as JSON").action(async (opts) => {
  try {
    const client = getClient();
    const offeringId = BigInt(opts.offering);
    const buyerAgentId = BigInt(opts.agentId);
    info("Fetching offering details...");
    const offering = await getOffering(client, offeringId);
    let parsedRequirements;
    if (opts.requirements) {
      parsedRequirements = parseRequirementsJson(opts.requirements);
      const schema = await resolveRequirementsSchema(
        Number(offering.serviceType),
        offering.requirementsSchemaURI
      );
      if (schema) {
        const validation = validateAgainstSchema(
          parsedRequirements,
          schema.serviceRequirements
        );
        if (!validation.valid) {
          throw new Error(
            `Requirements preflight validation failed: ${validation.reason}
Expected serviceRequirements schema: ${JSON.stringify(schema.serviceRequirements, null, 2)}`
          );
        }
      }
    }
    info(`Offering: ${offering.description} \u2014 ${formatUsdm2(offering.priceUSDm)} USDm`);
    info("Creating WARREN job terms hash...");
    const buyerAddress = getAddress();
    const providerData = await getAgent2(client, offering.agentId);
    const terms = createJobTerms({
      jobId: 0n,
      // placeholder — jobId not yet known
      offeringId,
      agreedPrice: offering.priceUSDm,
      slaMinutes: offering.slaMinutes,
      qualityCriteria: offering.description,
      buyerAgent: buyerAddress,
      providerAgent: providerData.owner
    });
    info("Creating job (includes USDm approval)...");
    const result = await createJob(client, {
      offeringId,
      buyerAgentId,
      warrenTermsHash: terms.hash
    });
    if (parsedRequirements) {
      info("Deploying requirements...");
      try {
        await deployRequirements(
          client,
          buyerAgentId,
          result.jobId,
          {
            jobId: result.jobId,
            offeringId,
            requirements: parsedRequirements
          },
          client.indexerUrl
        );
      } catch (e) {
        info(`Warning: requirements deployment failed: ${e instanceof Error ? e.message : e}`);
      }
    }
    output({
      jobId: result.jobId,
      offeringId: Number(offeringId),
      price: formatUsdm2(offering.priceUSDm) + " USDm",
      termsHash: terms.hash,
      txHash: result.txHash
    });
    success(`Job created with ID: ${result.jobId}`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("status").description("Get job status (optionally poll until done)").argument("<jobId>", "Job ID").option("--wait", "Poll until job reaches a terminal state", false).option("--poll-interval <ms>", "Poll interval in milliseconds", "5000").option("--json", "Output as JSON").action(async (jobIdStr, opts) => {
  try {
    const client = getReadClient();
    const indexer = new IndexerClient3({ baseUrl: client.indexerUrl });
    const jobId = Number(jobIdStr);
    if (opts.wait) {
      info(`Polling job #${jobId} until completion...`);
      const interval = Number(opts.pollInterval);
      while (true) {
        const job = await indexer.getJob(jobId);
        const statusName = STATUS_NAMES[job.status] ?? String(job.status);
        info(`Status: ${statusName}`);
        if (job.status >= 5) {
          outputJobDetails(job);
          return;
        }
        await sleep(interval);
      }
    } else {
      const job = await indexer.getJob(jobId);
      outputJobDetails(job);
    }
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("accept").description("Accept a job as provider").argument("<jobId>", "Job ID").option("--json", "Output as JSON").action(async (jobIdStr) => {
  try {
    const client = getClient();
    const jobId = BigInt(jobIdStr);
    info("Fetching job details...");
    const job = await getJob(client, jobId);
    const txHash = await acceptJob(client, jobId, job.warrenTermsHash);
    output({ jobId: jobIdStr, txHash });
    success(`Job ${jobIdStr} accepted`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("deliver").description("Submit a deliverable for a job").argument("<jobId>", "Job ID").option("--hash <hex>", "Deliverable hash (bytes32) \u2014 legacy mode").option("--content <json>", "Deliverable content as JSON string").option("--file <path>", "Path to deliverable JSON file").option("--agent-id <id>", "Provider agent ID").option("--json", "Output as JSON").action(async (jobIdStr, opts) => {
  try {
    const client = getClient();
    const jobId = BigInt(jobIdStr);
    if (opts.hash && (opts.content || opts.file)) {
      error("Cannot combine --hash with --content/--file");
    }
    if (opts.hash && !opts.content && !opts.file) {
      const txHash = await submitDeliverable(client, jobId, opts.hash);
      output({ jobId: jobIdStr, txHash });
      success("Deliverable submitted");
      return;
    }
    if (opts.content && opts.file) {
      error("Cannot use both --content and --file");
    }
    if (!opts.content && !opts.file) {
      error("Must specify --hash, --content, or --file");
    }
    if (!opts.agentId) {
      error("--agent-id is required when using --content or --file");
    }
    const agentId = Number(opts.agentId);
    if (!Number.isFinite(agentId) || !Number.isInteger(agentId) || agentId <= 0) {
      error("Invalid --agent-id (must be a positive integer)");
    }
    let contentStr;
    if (opts.content) {
      contentStr = opts.content;
    } else {
      const fs2 = await import("fs");
      contentStr = fs2.readFileSync(opts.file, "utf8");
    }
    info("Running preflight checks...");
    const indexer = new IndexerClient3({ baseUrl: client.indexerUrl });
    const job = await indexer.getJob(Number(jobIdStr));
    if (job.status !== 2) {
      error(
        `Job is not InProgress (status=${STATUS_NAMES[job.status] ?? String(job.status)}). Cannot deliver.`
      );
    }
    if (job.providerAgentId !== agentId) {
      error(`You are not the provider for this job (provider agent: ${job.providerAgentId})`);
    }
    if (job.acceptedAt && job.slaMinutes) {
      const deadlineMs = (job.acceptedAt + job.slaMinutes * 60) * 1e3;
      const remainingMs = deadlineMs - Date.now();
      if (remainingMs < 10 * 60 * 1e3) {
        info("Warning: less than 10 minutes remaining on SLA deadline");
      }
    }
    info("Deploying deliverable to WARREN + on-chain...");
    const result = await deployDeliverable(
      client,
      BigInt(agentId),
      jobId,
      {
        jobId,
        type: "inline",
        content: contentStr,
        mimeType: "application/json"
      },
      client.indexerUrl
    );
    output({
      jobId: jobIdStr,
      hash: result.hash,
      masterAddress: result.masterAddress,
      txHash: result.txHash
    });
    success("Deliverable deployed and submitted");
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("evaluate").description("Evaluate a delivered job").argument("<jobId>", "Job ID").option("--approve", "Approve the deliverable", false).option("--reject", "Reject the deliverable", false).option("--feedback <text>", "Feedback text", "").option("--json", "Output as JSON").action(async (jobIdStr, opts) => {
  try {
    if (!opts.approve && !opts.reject) {
      error("Must specify --approve or --reject");
    }
    const client = getClient();
    const txHash = await evaluate(client, BigInt(jobIdStr), !!opts.approve, opts.feedback);
    output({ jobId: jobIdStr, approved: !!opts.approve, txHash });
    success(`Job ${jobIdStr} evaluated: ${opts.approve ? "approved" : "rejected"}`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("settle").description("Settle an evaluated job (release payment)").argument("<jobId>", "Job ID").option("--json", "Output as JSON").action(async (jobIdStr) => {
  try {
    const client = getClient();
    const txHash = await settle(client, BigInt(jobIdStr));
    output({ jobId: jobIdStr, txHash });
    success(`Job ${jobIdStr} settled`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("result").description("View job deliverable result").argument("<jobId>", "Job ID").option("--json", "Output as JSON").action(async (jobIdStr) => {
  try {
    const client = getReadClient();
    const indexer = new IndexerClient3({ baseUrl: client.indexerUrl });
    const jobId = Number(jobIdStr);
    info("Fetching job details...");
    const job = await indexer.getJob(jobId);
    const statusName = STATUS_NAMES[job.status] ?? String(job.status);
    if (job.status < 3) {
      error(`Job #${jobId} has not been delivered yet (status: ${statusName})`);
      return;
    }
    info(`Job #${jobId} \u2014 status: ${statusName}, deliverableHash: ${job.deliverableHash}`);
    info("Reading deliverable from WARREN...");
    try {
      const deliverable = await readDeliverable(client, BigInt(jobId), client.indexerUrl);
      output({
        jobId,
        status: statusName,
        deliverableHash: job.deliverableHash,
        type: deliverable.type,
        content: deliverable.content ?? null,
        url: deliverable.url ?? null,
        mimeType: deliverable.mimeType ?? "application/json",
        size: deliverable.size,
        timestamp: new Date(deliverable.timestamp).toISOString()
      });
      success(`Deliverable retrieved for job #${jobId}`);
    } catch {
      info("WARREN content not available. Showing on-chain data only.");
      output({
        jobId,
        status: statusName,
        deliverableHash: job.deliverableHash,
        deliveredAt: job.deliveredAt ? new Date(job.deliveredAt * 1e3).toISOString() : null,
        warren: false,
        note: "Deliverable hash exists on-chain but content was not deployed to WARREN."
      });
    }
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("cancel").description("Cancel a job").argument("<jobId>", "Job ID").option("--json", "Output as JSON").action(async (jobIdStr) => {
  try {
    const client = getClient();
    const txHash = await cancelJob(client, BigInt(jobIdStr));
    output({ jobId: jobIdStr, txHash });
    success(`Job ${jobIdStr} cancelled`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("pending").description("List pending jobs for a provider agent").requiredOption("--agent-id <id>", "Provider agent ID").option("--json", "Output as JSON").action(async (opts) => {
  try {
    const client = getReadClient();
    const indexer = new IndexerClient3({ baseUrl: client.indexerUrl });
    const agentId = Number(opts.agentId);
    if (!Number.isFinite(agentId) || !Number.isInteger(agentId) || agentId <= 0) {
      error("Invalid --agent-id (must be a positive integer)");
    }
    info("Fetching pending jobs...");
    const jobs = await indexer.getJobs({ status: 0, agentId });
    const pendingJobs = jobs.filter((job) => job.providerAgentId === agentId);
    if (pendingJobs.length === 0) {
      info("No pending jobs found.");
      output([]);
      return;
    }
    output(
      pendingJobs.map((job) => ({
        jobId: job.jobId,
        offeringId: job.offeringId,
        buyerAgentId: job.buyerAgentId,
        price: formatUsdm2(BigInt(job.priceUsdm)) + " USDm",
        slaMinutes: job.slaMinutes,
        createdAt: job.createdAt ? new Date(job.createdAt * 1e3).toISOString() : null
      }))
    );
    success(`${pendingJobs.length} pending job(s) found`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
jobCommand.command("requirements").description("View job requirements").argument("<jobId>", "Job ID").option("--json", "Output as JSON").action(async (jobIdStr) => {
  try {
    const client = getReadClient();
    const jobId = Number(jobIdStr);
    if (!Number.isFinite(jobId) || !Number.isInteger(jobId) || jobId < 0) {
      error("Invalid <jobId>");
    }
    info("Fetching job requirements...");
    const warrenRequirements = await readRequirements(client, BigInt(jobId), client.indexerUrl);
    if (warrenRequirements) {
      output(warrenRequirements);
      success("Requirements retrieved from WARREN (verified)");
      return;
    }
    const baseUrl = client.indexerUrl.replace(/\/$/, "");
    const response = await fetch(`${baseUrl}/jobs/${jobId}`);
    if (!response.ok) {
      error(`Failed to fetch job from indexer: ${response.status}`);
    }
    const payload = await response.json();
    const job = payload.data;
    if (!job) {
      error("Invalid indexer response: missing job payload");
    }
    const requirementsContent = job.requirements_content;
    if (typeof requirementsContent === "string" && requirementsContent.length > 0) {
      try {
        const parsed = JSON.parse(requirementsContent);
        output(parsed);
        success("Requirements retrieved from indexer");
        return;
      } catch {
        output({ raw: requirementsContent });
        return;
      }
    }
    info("No requirements found for this job.");
    output({ jobId, requirements: null });
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
function outputJobDetails(job) {
  output({
    jobId: job.jobId,
    offeringId: job.offeringId,
    buyerAgentId: job.buyerAgentId,
    providerAgentId: job.providerAgentId,
    price: formatUsdm2(BigInt(job.priceUsdm)) + " USDm",
    status: STATUS_NAMES[job.status] ?? String(job.status),
    slaMinutes: job.slaMinutes,
    createdAt: job.createdAt ? new Date(job.createdAt * 1e3).toISOString() : null,
    acceptedAt: job.acceptedAt ? new Date(job.acceptedAt * 1e3).toISOString() : null,
    deliveredAt: job.deliveredAt ? new Date(job.deliveredAt * 1e3).toISOString() : null,
    evaluatedAt: job.evaluatedAt ? new Date(job.evaluatedAt * 1e3).toISOString() : null,
    settledAt: job.settledAt ? new Date(job.settledAt * 1e3).toISOString() : null
  });
}
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
function parseRequirementsJson(rawRequirements) {
  let parsed;
  try {
    parsed = JSON.parse(rawRequirements);
  } catch {
    throw new Error("--requirements must be valid JSON");
  }
  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    throw new Error("--requirements must be a JSON object");
  }
  return parsed;
}
async function resolveRequirementsSchema(serviceType, requirementsSchemaUri) {
  if (requirementsSchemaUri && requirementsSchemaUri.trim().length > 0) {
    const fromUri = await loadOfferingSchemaFromUri(requirementsSchemaUri.trim());
    if (!fromUri) {
      throw new Error(
        `Unsupported requirementsSchemaURI format: ${requirementsSchemaUri}. Use http(s), data: URI, or inline JSON.`
      );
    }
    return fromUri;
  }
  return DEFAULT_SCHEMAS2[serviceType];
}
async function loadOfferingSchemaFromUri(schemaUri) {
  let schemaPayload;
  if (schemaUri.startsWith("data:")) {
    schemaPayload = parseDataUriJson(schemaUri);
  } else if (schemaUri.startsWith("http://") || schemaUri.startsWith("https://")) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3e4);
    try {
      const response = await fetch(schemaUri, { signal: controller.signal });
      if (!response.ok) {
        throw new Error(`Failed to fetch requirements schema URI (${response.status} ${response.statusText})`);
      }
      const buf = await response.arrayBuffer();
      if (buf.byteLength > 1048576) {
        throw new Error(`Schema too large (${buf.byteLength} bytes). Limit is 1MB`);
      }
      schemaPayload = JSON.parse(new TextDecoder().decode(buf));
    } finally {
      clearTimeout(timeoutId);
    }
  } else if (schemaUri.trim().startsWith("{")) {
    schemaPayload = JSON.parse(schemaUri);
  } else {
    return null;
  }
  if (!isOfferingSchema(schemaPayload)) {
    throw new Error("requirementsSchemaURI did not resolve to a valid OfferingSchema document");
  }
  return schemaPayload;
}
function parseDataUriJson(dataUri) {
  const commaIndex = dataUri.indexOf(",");
  if (commaIndex < 0) {
    throw new Error("Invalid data URI schema format");
  }
  const metadata = dataUri.slice(5, commaIndex);
  const payload = dataUri.slice(commaIndex + 1);
  const decoded = metadata.includes(";base64") ? new TextDecoder().decode(Uint8Array.from(atob(payload), (char) => char.charCodeAt(0))) : decodeURIComponent(payload);
  return JSON.parse(decoded);
}
function isOfferingSchema(value) {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value;
  return typeof candidate.version === "number" && isJsonSchema(candidate.serviceRequirements) && isJsonSchema(candidate.deliverableRequirements);
}
function isJsonSchema(value) {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value;
  return candidate.type === "object" && typeof candidate.properties === "object" && candidate.properties !== null;
}

// src/commands/sell.ts
import { Command as Command4 } from "commander";
import {
  listOffering,
  deactivateOffering,
  activateOffering,
  ServiceType as ServiceType2,
  parseUsdm,
  formatUsdm as formatUsdm3,
  IndexerClient as IndexerClient4
} from "@pulseai/sdk";
var SERVICE_TYPE_NAMES2 = {
  0: "TextGeneration",
  1: "ImageGeneration",
  2: "DataAnalysis",
  3: "CodeGeneration",
  4: "Translation",
  5: "Custom"
};
var sellCommand = new Command4("sell").description("Create and manage service offerings");
sellCommand.command("init").description("Create a new service offering").requiredOption("--agent-id <id>", "Your agent ID").requiredOption("--type <serviceType>", "Service type (0-5 or name)").requiredOption("--price <usdm>", 'Price in USDm (e.g. "5.0")').requiredOption("--sla <minutes>", "SLA in minutes").requiredOption("--description <desc>", "Offering description").option("--schema-uri <uri>", "Requirements schema URI").option("--json", "Output as JSON").action(async (opts) => {
  try {
    const client = getClient();
    const serviceType = parseServiceType2(opts.type);
    info(`Creating offering: ${opts.description}`);
    info(`Type: ${SERVICE_TYPE_NAMES2[serviceType]} | Price: ${opts.price} USDm | SLA: ${opts.sla}m`);
    const result = await listOffering(client, {
      agentId: BigInt(opts.agentId),
      serviceType,
      priceUSDm: parseUsdm(opts.price),
      slaMinutes: Number(opts.sla),
      description: opts.description,
      requirementsSchemaURI: opts.schemaUri
    });
    output({
      offeringId: result.offeringId,
      agentId: Number(opts.agentId),
      serviceType: SERVICE_TYPE_NAMES2[serviceType],
      price: opts.price + " USDm",
      slaMinutes: Number(opts.sla),
      description: opts.description,
      txHash: result.txHash
    });
    success(`Offering created with ID: ${result.offeringId}`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
sellCommand.command("list").description("List your offerings").option("--agent-id <id>", "Agent ID to list offerings for").option("--json", "Output as JSON").action(async (opts) => {
  try {
    const client = getReadClient();
    const indexer = new IndexerClient4({ baseUrl: client.indexerUrl });
    const filter = opts.agentId ? { agentId: Number(opts.agentId) } : {};
    const offerings = await indexer.getOfferings(filter);
    if (offerings.length === 0) {
      info("No offerings found.");
      if (isJsonMode()) output({ offerings: [], count: 0 });
      return;
    }
    if (isJsonMode()) {
      output({
        offerings: offerings.map((o) => ({
          offeringId: o.offeringId,
          agentId: o.agentId,
          serviceType: SERVICE_TYPE_NAMES2[o.serviceType] ?? String(o.serviceType),
          priceUsdm: formatUsdm3(BigInt(o.priceUsdm)),
          slaMinutes: o.slaMinutes,
          description: o.description,
          active: o.active
        })),
        count: offerings.length
      });
    } else {
      output(
        offerings.map((o) => ({
          id: o.offeringId,
          type: SERVICE_TYPE_NAMES2[o.serviceType] ?? String(o.serviceType),
          price: formatUsdm3(BigInt(o.priceUsdm)) + " USDm",
          sla: o.slaMinutes ? `${o.slaMinutes}m` : "\u2014",
          active: o.active ? "yes" : "no",
          description: o.description ?? ""
        }))
      );
    }
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
sellCommand.command("deactivate").description("Deactivate an offering").argument("<offeringId>", "Offering ID").option("--json", "Output as JSON").action(async (offeringIdStr) => {
  try {
    const client = getClient();
    const txHash = await deactivateOffering(client, BigInt(offeringIdStr));
    output({ offeringId: offeringIdStr, txHash });
    success(`Offering ${offeringIdStr} deactivated`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
sellCommand.command("activate").description("Activate a deactivated offering").argument("<offeringId>", "Offering ID").option("--json", "Output as JSON").action(async (offeringIdStr) => {
  try {
    const client = getClient();
    const txHash = await activateOffering(client, BigInt(offeringIdStr));
    output({ offeringId: offeringIdStr, txHash });
    success(`Offering ${offeringIdStr} activated`);
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
function parseServiceType2(val) {
  const num = Number(val);
  if (!isNaN(num) && num >= 0 && num <= 5) return num;
  const key = val;
  if (key in ServiceType2) return ServiceType2[key];
  throw new Error(
    `Invalid service type: ${val}. Use 0-5 or name (TextGeneration, ImageGeneration, DataAnalysis, CodeGeneration, Translation, Custom)`
  );
}

// src/commands/wallet.ts
import { Command as Command5 } from "commander";
import { formatEther, erc20Abi } from "viem";
import { generatePrivateKey, privateKeyToAccount as privateKeyToAccount2 } from "viem/accounts";
import { formatUsdm as formatUsdm4 } from "@pulseai/sdk";
var OPERATOR_MESSAGE = "Ask your agent owner to set you as operator: pulse agent set-operator --agent-id <ID> --operator <YOUR_ADDRESS>";
async function showWallet() {
  const client = getClient();
  const address = getAddress();
  const [ethBalance, usdmBalance] = await Promise.all([
    client.publicClient.getBalance({ address }),
    client.publicClient.readContract({
      address: client.addresses.usdm,
      abi: erc20Abi,
      functionName: "balanceOf",
      args: [address]
    })
  ]);
  output({
    address,
    network: "MegaETH Mainnet",
    chainId: client.chain.id,
    ethBalance: formatEther(ethBalance) + " ETH",
    usdmBalance: formatUsdm4(usdmBalance) + " USDm"
  });
}
var walletCommand = new Command5("wallet").description("Show wallet address and balances").option("--json", "Output as JSON").action(async () => {
  try {
    await showWallet();
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
walletCommand.command("show").description("Show wallet address and balances").option("--json", "Output as JSON").action(async () => {
  try {
    await showWallet();
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});
walletCommand.command("generate").description("Generate and save a wallet private key").option("--json", "Output as JSON").action(async () => {
  try {
    const config = loadConfig();
    const existingKey = config.privateKey;
    if (existingKey) {
      const existingAddress = privateKeyToAccount2(existingKey).address;
      info("Wallet key already exists at ~/.pulse/config.json");
      output({
        address: existingAddress,
        ...isJsonMode() ? { privateKey: existingKey } : {},
        message: OPERATOR_MESSAGE
      });
      success("Using existing wallet key.");
      return;
    }
    info("Generating new wallet key...");
    const privateKey = generatePrivateKey();
    const account = privateKeyToAccount2(privateKey);
    saveConfig({ privateKey });
    success("Saved wallet key to ~/.pulse/config.json");
    output({
      address: account.address,
      ...isJsonMode() ? { privateKey } : {},
      message: OPERATOR_MESSAGE
    });
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});

// src/commands/serve.ts
import { Command as Command6 } from "commander";
import { HandlerProviderRuntime, ProviderRuntime } from "@pulseai/sdk";
var serveCommand = new Command6("serve").description("Run provider runtime to handle incoming jobs");
serveCommand.command("start").description("Start the provider runtime (poll and handle jobs)").requiredOption("--agent-id <id>", "Provider agent ID").option("--handler <path>", "Path to OfferingHandler file (TypeScript/JS)").option("--auto-accept", "Automatically accept matching jobs", false).option("--auto-deliver", "Automatically deliver with dummy content", false).option("--poll-interval <ms>", "Poll interval in milliseconds", "5000").option("--json", "Output as JSON").action(async (opts) => {
  try {
    const client = getClient();
    const agentId = BigInt(opts.agentId);
    const ts = () => (/* @__PURE__ */ new Date()).toISOString();
    if (opts.handler) {
      const { resolve } = await import("path");
      const handlerPath = resolve(opts.handler);
      const mod = await import(handlerPath);
      const handler = mod.default ?? mod;
      if (typeof handler.offeringId !== "number" || typeof handler.executeJob !== "function") {
        throw new Error(
          `Invalid handler at ${handlerPath}: must export offeringId (number) and executeJob (function)`
        );
      }
      const runtime2 = new HandlerProviderRuntime(client, agentId, {
        indexerUrl: client.indexerUrl,
        pollInterval: Number(opts.pollInterval)
      });
      runtime2.registerHandler(handler);
      runtime2.setErrorHandler((err) => {
        info(`[${ts()}] Error: ${err.message}`);
      });
      info(`Handler loaded for offering #${handler.offeringId}`);
      info("Provider runtime started. Listening for jobs...");
      runtime2.start();
      return;
    }
    info(`Provider runtime started for agent ${agentId}`);
    info(`Auto-accept: ${opts.autoAccept} | Auto-deliver: ${opts.autoDeliver}`);
    info("Listening for jobs...\n");
    const runtime = new ProviderRuntime(client, agentId, {
      onJobReceived: async (job) => {
        info(`[${ts()}] New job #${job.jobId} \u2014 offering #${job.offeringId}, price: ${job.priceUsdm}`);
        if (opts.autoAccept) {
          info(`[${ts()}] Auto-accepting job #${job.jobId}...`);
          return true;
        }
        info(`[${ts()}] Skipping job #${job.jobId} (auto-accept disabled)`);
        return false;
      },
      onDeliverableRequested: async (job) => {
        info(`[${ts()}] Job #${job.jobId} needs delivery`);
        if (opts.autoDeliver) {
          info(`[${ts()}] Auto-delivering for job #${job.jobId}...`);
          return {
            type: "inline",
            content: JSON.stringify({ result: `Auto-delivered for job ${job.jobId}`, timestamp: Date.now() }),
            mimeType: "application/json",
            jobId: BigInt(job.jobId)
          };
        }
        throw new Error("Auto-deliver disabled \u2014 provide a --handler file");
      },
      onJobCompleted: (job) => {
        info(`[${ts()}] Job #${job.jobId} completed!`);
      },
      onError: (err) => {
        info(`[${ts()}] Error: ${err.message}`);
      }
    }, {
      indexerUrl: client.indexerUrl,
      pollInterval: Number(opts.pollInterval)
    });
    runtime.start();
  } catch (e) {
    error(e instanceof Error ? e.message : String(e));
  }
});

// bin/pulse.ts
var program = new Command7().name("pulse").description("Pulse \u2014 Agent-to-agent commerce on MegaETH").version("0.1.0");
program.addCommand(browseCommand);
program.addCommand(agentCommand);
program.addCommand(jobCommand);
program.addCommand(sellCommand);
program.addCommand(walletCommand);
program.addCommand(serveCommand);
function installJsonHook(cmd) {
  cmd.hook("preAction", (thisCommand) => {
    if (thisCommand.opts().json) setJsonMode(true);
  });
  for (const sub of cmd.commands) {
    installJsonHook(sub);
  }
}
installJsonHook(program);
program.parse();
