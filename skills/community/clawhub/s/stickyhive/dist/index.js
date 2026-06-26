#!/usr/bin/env node
"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// src/index.ts
var import_yargs = __toESM(require("yargs"));
var import_helpers = require("yargs/helpers");

// src/config.ts
function getApiKey() {
  const key = process.env.STICKYHIVE_API_KEY;
  if (!key) {
    console.error(JSON.stringify({ error: "STICKYHIVE_API_KEY environment variable is not set." }));
    process.exit(1);
  }
  return key;
}
function getBaseUrl() {
  return (process.env.STICKYHIVE_API_URL || "https://app.stickyhive.com").replace(/\/+$/, "");
}

// src/api.ts
async function apiRequest(method, path, body, query) {
  const baseUrl = getBaseUrl();
  const apiKey = getApiKey();
  let url = `${baseUrl}/api/v1${path}`;
  if (query) {
    const params = new URLSearchParams(
      Object.entries(query).filter(([, v]) => v !== void 0 && v !== "")
    );
    const qs = params.toString();
    if (qs) url += `?${qs}`;
  }
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json"
  };
  const opts = { method, headers };
  if (body && ["POST", "PUT", "PATCH"].includes(method)) {
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(url, opts);
  if (res.status === 204) {
    return { success: true };
  }
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    if (!res.ok) {
      return { error: `HTTP ${res.status}: ${text}` };
    }
    return { result: text };
  }
}
function output(data) {
  console.log(JSON.stringify(data, null, 2));
}

// src/commands/communities.ts
async function listCommunities() {
  output(await apiRequest("GET", "/communities/"));
}
async function getCommunity(argv) {
  output(await apiRequest("GET", `/communities/${argv.id}/`));
}

// src/commands/spaces.ts
async function listSpaces() {
  output(await apiRequest("GET", "/spaces/"));
}
async function getSpace(argv) {
  output(await apiRequest("GET", `/spaces/${argv.id}/`));
}

// src/commands/posts.ts
async function createPost(argv) {
  const body = {
    title: argv.title,
    content: argv.content,
    space_id: argv.spaceId
  };
  if (argv.date) body.scheduled_time = argv.date;
  if (argv.pin) body.pin_on_publish = true;
  if (argv.comment) body.first_comment_text = argv.comment;
  if (argv.poll) {
    try {
      body.poll_options = JSON.parse(argv.poll);
    } catch {
      body.poll_options = argv.poll.split(",");
    }
  }
  output(await apiRequest("POST", "/scheduled-posts/", body));
}
async function listPosts(argv) {
  const query = {};
  if (argv.status) query.status = argv.status;
  if (argv.draft !== void 0) query.is_draft = String(argv.draft);
  if (argv.spaceId) query.space_id = String(argv.spaceId);
  if (argv.dateFrom) query.date_from = argv.dateFrom;
  if (argv.dateTo) query.date_to = argv.dateTo;
  output(await apiRequest("GET", "/scheduled-posts/", void 0, query));
}
async function getPost(argv) {
  output(await apiRequest("GET", `/scheduled-posts/${argv.id}/`));
}
async function updatePost(argv) {
  const body = JSON.parse(argv.data);
  output(await apiRequest("PATCH", `/scheduled-posts/${argv.id}/`, body));
}
async function deletePost(argv) {
  output(await apiRequest("DELETE", `/scheduled-posts/${argv.id}/`));
}
async function reschedulePost(argv) {
  output(await apiRequest("POST", `/scheduled-posts/${argv.id}/reschedule/`, { scheduled_time: argv.date }));
}
async function publishNow(argv) {
  output(await apiRequest("POST", `/scheduled-posts/${argv.id}/publish-now/`));
}
async function bulkSchedule(argv) {
  const postIds = argv.ids.split(",").map(Number);
  output(await apiRequest("POST", "/scheduled-posts/bulk-schedule/", {
    post_ids: postIds,
    start_time: argv.startTime,
    interval_hours: argv.interval ?? 1
  }));
}

// src/commands/workflows.ts
async function listWorkflows(argv) {
  output(await apiRequest("GET", "/workflows/", void 0, { community_id: String(argv.communityId) }));
}
async function getWorkflow(argv) {
  output(await apiRequest("GET", `/workflows/${argv.id}/`, void 0, { community_id: String(argv.communityId) }));
}
async function createWorkflow(argv) {
  output(await apiRequest("POST", "/workflows/", {
    community_id: argv.communityId,
    name: argv.name,
    config: JSON.parse(argv.config),
    daily_limit: argv.dailyLimit ?? 50
  }));
}
async function updateWorkflow(argv) {
  const body = JSON.parse(argv.data);
  body.community_id = argv.communityId;
  output(await apiRequest("PATCH", `/workflows/${argv.id}/`, body));
}
async function deleteWorkflow(argv) {
  output(await apiRequest("DELETE", `/workflows/${argv.id}/`, void 0, { community_id: String(argv.communityId) }));
}
async function toggleWorkflow(argv) {
  output(await apiRequest("POST", `/workflows/${argv.id}/toggle/`, { community_id: argv.communityId }));
}
async function runWorkflow(argv) {
  output(await apiRequest("POST", `/workflows/${argv.id}/run/`, { community_id: argv.communityId }));
}
async function listWorkflowRuns(argv) {
  output(await apiRequest("GET", `/workflows/${argv.id}/runs/`, void 0, {
    community_id: String(argv.communityId),
    ...argv.limit ? { limit: String(argv.limit) } : {}
  }));
}
async function testWorkflow(argv) {
  const body = { community_id: argv.communityId };
  if (argv.triggerData) body.trigger_data = JSON.parse(argv.triggerData);
  output(await apiRequest("POST", `/workflows/${argv.id}/test/`, body));
}
async function getWorkflowRegistry(argv) {
  output(await apiRequest("GET", "/workflows/registry/", void 0, { platform: argv.platform ?? "skool" }));
}

// src/commands/sequences.ts
async function listSequences(argv) {
  output(await apiRequest("GET", "/sequences/", void 0, { community_id: String(argv.communityId) }));
}
async function getSequence(argv) {
  output(await apiRequest("GET", `/sequences/${argv.id}/`, void 0, { community_id: String(argv.communityId) }));
}
async function createSequence(argv) {
  const body = {
    community_id: argv.communityId,
    name: argv.name
  };
  if (argv.description) body.description = argv.description;
  if (argv.steps) body.steps = JSON.parse(argv.steps);
  output(await apiRequest("POST", "/sequences/", body));
}
async function updateSequence(argv) {
  const body = JSON.parse(argv.data);
  body.community_id = argv.communityId;
  output(await apiRequest("PATCH", `/sequences/${argv.id}/`, body));
}
async function deleteSequence(argv) {
  output(await apiRequest("DELETE", `/sequences/${argv.id}/`, void 0, { community_id: String(argv.communityId) }));
}
async function toggleSequence(argv) {
  output(await apiRequest("POST", `/sequences/${argv.id}/toggle/`, { community_id: argv.communityId }));
}
async function enrollMember(argv) {
  output(await apiRequest("POST", `/sequences/${argv.id}/enroll/`, {
    community_id: argv.communityId,
    member_id: argv.memberId
  }));
}
async function listEnrollments(argv) {
  const query = { community_id: String(argv.communityId) };
  if (argv.status) query.status = argv.status;
  output(await apiRequest("GET", `/sequences/${argv.id}/enrollments/`, void 0, query));
}
async function manageEnrollment(argv) {
  output(await apiRequest("POST", `/sequences/${argv.sequenceId}/enrollments/${argv.enrollmentId}/manage/`, {
    community_id: argv.communityId,
    action: argv.action
  }));
}
async function getStepTypes() {
  output(await apiRequest("GET", "/sequences/step-types/"));
}

// src/commands/webhooks.ts
async function listWebhooks() {
  output(await apiRequest("GET", "/webhooks/"));
}
async function createWebhook(argv) {
  const events = argv.events.split(",").map((e) => e.trim());
  output(await apiRequest("POST", "/webhooks/", { url: argv.url, events }));
}
async function deleteWebhook(argv) {
  output(await apiRequest("DELETE", `/webhooks/${argv.id}/`));
}

// src/index.ts
(0, import_yargs.default)((0, import_helpers.hideBin)(process.argv)).scriptName("stickyhive").usage("$0 <command> [options]").command("communities:list", "List all communities in your organization", {}, listCommunities).command(
  "communities:get <id>",
  "Get a community by ID",
  (y) => y.positional("id", { type: "number", demandOption: true }),
  getCommunity
).command("spaces:list", "List all spaces (posting destinations)", {}, listSpaces).command(
  "spaces:get <id>",
  "Get a space by ID",
  (y) => y.positional("id", { type: "number", demandOption: true }),
  getSpace
).command(
  "posts:create",
  "Create a scheduled post or draft",
  (y) => y.option("title", { alias: "t", type: "string", demandOption: true, describe: "Post title" }).option("content", { alias: "c", type: "string", demandOption: true, describe: "Post body content" }).option("spaceId", { alias: "i", type: "number", demandOption: true, describe: "Space ID to post to" }).option("date", { alias: "s", type: "string", describe: "Scheduled time (ISO 8601). Omit for draft." }).option("pin", { type: "boolean", default: false, describe: "Pin on publish (Skool only)" }).option("comment", { type: "string", describe: "First comment text" }).option("poll", { type: "string", describe: "Poll options as JSON array or comma-separated" }).example('$0 posts:create -t "Hello" -c "World" -i 42 -s "2026-06-01T09:00:00Z"', "Schedule a post").example('$0 posts:create -t "Draft" -c "Content" -i 42', "Save as draft"),
  createPost
).command(
  "posts:list",
  "List scheduled posts with optional filters",
  (y) => y.option("status", { type: "string", choices: ["pending", "publishing", "published", "failed", "expired"] }).option("draft", { type: "boolean", describe: "Filter drafts" }).option("spaceId", { type: "number", describe: "Filter by space" }).option("dateFrom", { type: "string", describe: "Start date (ISO 8601)" }).option("dateTo", { type: "string", describe: "End date (ISO 8601)" }),
  listPosts
).command(
  "posts:get <id>",
  "Get a scheduled post by ID",
  (y) => y.positional("id", { type: "number", demandOption: true }),
  getPost
).command(
  "posts:update <id>",
  "Update a scheduled post",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("data", { alias: "d", type: "string", demandOption: true, describe: "JSON object with fields to update" }).example(`$0 posts:update 123 -d '{"title":"New title"}'`, "Update title"),
  updatePost
).command(
  "posts:delete <id>",
  "Delete a scheduled post",
  (y) => y.positional("id", { type: "number", demandOption: true }),
  deletePost
).command(
  "posts:reschedule <id>",
  "Change the scheduled time of a post",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("date", { alias: "s", type: "string", demandOption: true, describe: "New scheduled time (ISO 8601)" }),
  reschedulePost
).command(
  "posts:publish <id>",
  "Queue a post for immediate publishing",
  (y) => y.positional("id", { type: "number", demandOption: true }),
  publishNow
).command(
  "posts:bulk-schedule",
  "Schedule multiple draft posts with even spacing",
  (y) => y.option("ids", { type: "string", demandOption: true, describe: "Comma-separated post IDs" }).option("startTime", { type: "string", demandOption: true, describe: "Start time (ISO 8601)" }).option("interval", { type: "number", default: 1, describe: "Hours between posts" }),
  bulkSchedule
).command(
  "workflows:list",
  "List workflows for a community",
  (y) => y.option("communityId", { alias: "C", type: "number", demandOption: true }),
  listWorkflows
).command(
  "workflows:get <id>",
  "Get workflow details with run stats",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }),
  getWorkflow
).command(
  "workflows:create",
  "Create a new custom workflow",
  (y) => y.option("communityId", { alias: "C", type: "number", demandOption: true }).option("name", { alias: "n", type: "string", demandOption: true }).option("config", { type: "string", demandOption: true, describe: "Workflow config as JSON string" }).option("dailyLimit", { type: "number", default: 50 }),
  createWorkflow
).command(
  "workflows:update <id>",
  "Update a workflow",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }).option("data", { alias: "d", type: "string", demandOption: true, describe: "JSON with fields to update" }),
  updateWorkflow
).command(
  "workflows:delete <id>",
  "Soft-delete a workflow",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }),
  deleteWorkflow
).command(
  "workflows:toggle <id>",
  "Enable or disable a workflow",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }),
  toggleWorkflow
).command(
  "workflows:run <id>",
  "Manually trigger a workflow",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }),
  runWorkflow
).command(
  "workflows:runs <id>",
  "Get run history for a workflow",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }).option("limit", { type: "number", default: 20 }),
  listWorkflowRuns
).command(
  "workflows:test <id>",
  "Dry-run a workflow and preview actions",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }).option("triggerData", { type: "string", describe: "Sample trigger data as JSON" }),
  testWorkflow
).command(
  "workflows:registry",
  "Get available triggers, actions, conditions, and operators",
  (y) => y.option("platform", { type: "string", default: "skool", choices: ["skool", "circle", "mighty", "discord", "slack"] }),
  getWorkflowRegistry
).command(
  "sequences:list",
  "List DM sequences for a community",
  (y) => y.option("communityId", { alias: "C", type: "number", demandOption: true }),
  listSequences
).command(
  "sequences:get <id>",
  "Get sequence details with steps and enrollment stats",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }),
  getSequence
).command(
  "sequences:create",
  "Create a new DM sequence",
  (y) => y.option("communityId", { alias: "C", type: "number", demandOption: true }).option("name", { alias: "n", type: "string", demandOption: true }).option("description", { type: "string" }).option("steps", { type: "string", describe: "Step tree as JSON" }),
  createSequence
).command(
  "sequences:update <id>",
  "Update a sequence",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }).option("data", { alias: "d", type: "string", demandOption: true, describe: "JSON with fields to update" }),
  updateSequence
).command(
  "sequences:delete <id>",
  "Soft-delete a sequence",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }),
  deleteSequence
).command(
  "sequences:toggle <id>",
  "Enable or disable a sequence",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }),
  toggleSequence
).command(
  "sequences:enroll <id>",
  "Enroll a member in a sequence",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }).option("memberId", { alias: "m", type: "string", demandOption: true, describe: "Platform ID or numeric ID" }),
  enrollMember
).command(
  "sequences:enrollments <id>",
  "List enrollments for a sequence",
  (y) => y.positional("id", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }).option("status", { type: "string", choices: ["active", "paused", "completed", "exited", "cancelled"] }),
  listEnrollments
).command(
  "sequences:manage-enrollment",
  "Pause, resume, or cancel an enrollment",
  (y) => y.option("sequenceId", { type: "number", demandOption: true }).option("enrollmentId", { type: "number", demandOption: true }).option("communityId", { alias: "C", type: "number", demandOption: true }).option("action", { alias: "a", type: "string", demandOption: true, choices: ["pause", "resume", "cancel"] }),
  manageEnrollment
).command("sequences:step-types", "Get available step types for building sequences", {}, getStepTypes).command("webhooks:list", "List registered webhook endpoints", {}, listWebhooks).command(
  "webhooks:create",
  "Register a webhook endpoint",
  (y) => y.option("url", { alias: "u", type: "string", demandOption: true }).option("events", { alias: "e", type: "string", demandOption: true, describe: "Comma-separated events or * for all" }),
  createWebhook
).command(
  "webhooks:delete <id>",
  "Delete a webhook endpoint",
  (y) => y.positional("id", { type: "number", demandOption: true }),
  deleteWebhook
).demandCommand(1, "You need at least one command").help().alias("h", "help").version().alias("v", "version").epilogue(
  "For more information, visit: https://stickyhive.com\n\nAuthentication:\n  export STICKYHIVE_API_KEY=hm_live_...\n\nAll commands output structured JSON for AI agent consumption."
).parse();
//# sourceMappingURL=index.js.map