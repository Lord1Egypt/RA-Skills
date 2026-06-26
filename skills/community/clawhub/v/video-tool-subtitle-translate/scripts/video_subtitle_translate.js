#!/usr/bin/env node
/** WeryAI video-subtitle-translate — this skill only. */

const TOOL = {
  id: "subtitle-translate",
  endpoint: "/v1/generation/video-subtitle-translate",
  summary: "Translate subtitles in a video to a target language code.",
  required: ["video_url", "target_language"],
  defaults: {},
  enums: {},
  urlFields: ["video_url"],
};

/**
 * WeryAI video tool CLI (self-contained).
 * Commands: help | spec | submit | wait | status
 */

const BASE_URL = "https://api.weryai.com";
const POLL_INTERVAL_MS = 6000;
const POLL_TIMEOUT_MS = 600000;

const STATUS_MAP = {
  waiting: "waiting",
  WAITING: "waiting",
  pending: "waiting",
  PENDING: "waiting",
  processing: "processing",
  PROCESSING: "processing",
  succeed: "completed",
  SUCCEED: "completed",
  success: "completed",
  SUCCESS: "completed",
  failed: "failed",
  FAILED: "failed",
};

const ERROR_MESSAGES = {
  400: "Some of the request details are invalid. Please review your input and try again.",
  403: "Authentication failed. Please check your API key and try again.",
  429: "Too many requests in a short time. Please wait a moment and try again.",
  500: "Something went wrong on our side. Please try again in a moment.",
};

const STATIC_ERROR_MAP = {
  1001: { category: "rate_limit", title: "Too many requests", message: "Too many requests in a short time. Please wait a moment and try again.", retryable: true },
  1003: { category: "not_found", title: "Resource not found", message: "The requested item could not be found. Please check the ID or input and try again.", retryable: false },
  1010: { category: "not_found", title: "Resource not found", message: "The requested item could not be found. Please check the ID or input and try again.", retryable: false },
  1011: { category: "credits", title: "Not enough credits", message: "You do not have enough credits to complete this request.", retryable: false },
  2003: { category: "content_safety", title: "Content flagged", message: "The provided video or request content was flagged by the safety system. Please revise it and try again.", retryable: false },
  6001: { category: "server", title: "Temporary service issue", message: "Something went wrong on our side. Please try again in a moment.", retryable: true },
  6002: { category: "rate_limit", title: "Too many requests", message: "Too many requests in a short time. Please wait a moment and try again.", retryable: true },
  6003: { category: "server", title: "Temporary service issue", message: "Something went wrong on our side. Please try again in a moment.", retryable: true },
  6004: { category: "server", title: "Generation failed", message: "The request could not be completed. Please try again with different input or try again later.", retryable: true },
  6010: { category: "active_job_limit", title: "Too many active jobs", message: "You already have too many active jobs. Please wait for current jobs to finish before starting a new one.", retryable: true },
  6101: { category: "daily_limit", title: "Daily limit reached", message: "You have reached the daily limit for this workflow. Please try again later.", retryable: true },
};

const RECT_FIELDS = ["lt_x", "lt_y", "rb_x", "rb_y"];

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeRectList(value) {
  if (value == null) return null;
  if (!Array.isArray(value)) return value;
  return value.map((rect) => {
    const next = {};
    for (const field of RECT_FIELDS) {
      if (rect?.[field] != null) next[field] = Number(rect[field]);
    }
    return next;
  });
}

function buildPayload(spec, input) {
  const payload = { ...spec.defaults, ...(input || {}) };
  if (typeof spec.preparePayload === "function") spec.preparePayload(payload);
  if (payload.rect_vo_list != null) payload.rect_vo_list = normalizeRectList(payload.rect_vo_list);
  return payload;
}

function validateHttpsUrl(value, fieldName, errors) {
  if (typeof value !== "string" || value.trim().length === 0) {
    errors.push(`${fieldName} must be a non-empty URL string.`);
    return;
  }
  if (!value.startsWith("https://")) {
    errors.push(`${fieldName} must be a public https:// URL.`);
  }
}

function validateRectList(value, fieldName, errors) {
  if (value == null) return;
  if (!Array.isArray(value)) {
    errors.push(`${fieldName} must be an array of normalized rectangles.`);
    return;
  }
  value.forEach((rect, index) => {
    for (const field of RECT_FIELDS) {
      const n = rect?.[field];
      if (typeof n !== "number" || Number.isNaN(n) || n < 0 || n > 1) {
        errors.push(`${fieldName}[${index}].${field} must be a number between 0 and 1.`);
      }
    }
    if (typeof rect?.lt_x === "number" && typeof rect?.rb_x === "number" && rect.lt_x >= rect.rb_x) {
      errors.push(`${fieldName}[${index}] must satisfy lt_x < rb_x.`);
    }
    if (typeof rect?.lt_y === "number" && typeof rect?.rb_y === "number" && rect.lt_y >= rect.rb_y) {
      errors.push(`${fieldName}[${index}] must satisfy lt_y < rb_y.`);
    }
  });
}

function validatePayload(spec, payload) {
  const errors = [];

  for (const field of spec.required) {
    if (payload[field] == null || payload[field] === "") {
      errors.push(`${field} is required for tool ${spec.id}.`);
    }
  }

  for (const field of spec.urlFields) {
    if (payload[field] != null) validateHttpsUrl(payload[field], field, errors);
  }

  if (spec.rectField) {
    validateRectList(payload[spec.rectField], spec.rectField, errors);
  }

  for (const [field, allowedValues] of Object.entries(spec.enums || {})) {
    if (payload[field] == null) continue;
    const value = typeof allowedValues[0] === "number" ? Number(payload[field]) : String(payload[field]);
    if (!allowedValues.includes(value)) {
      errors.push(`${field} must be one of: ${allowedValues.join(", ")}.`);
    } else {
      payload[field] = value;
    }
  }

  return errors;
}

function getApiKey() {
  const apiKey = (process.env.WERYAI_API_KEY || "").trim();
  if (!apiKey) return null;
  return apiKey;
}

async function httpJson(method, url, body, apiKey) {
  const headers = { "Content-Type": "application/json" };
  if (apiKey) headers.Authorization = `Bearer ${apiKey}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 30000);

  try {
    const res = await fetch(url, {
      method,
      headers,
      body: body != null ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });
    clearTimeout(timer);

    let data;
    try {
      data = await res.json();
    } catch {
      data = { status: res.status, message: `Non-JSON response (HTTP ${res.status})` };
    }

    return { httpStatus: res.status, ...data };
  } catch (error) {
    clearTimeout(timer);
    if (error?.name === "AbortError") {
      throw new Error(`Request timeout: ${method} ${url}`);
    }
    throw error;
  }
}

function isApiSuccess(res) {
  const httpOk = res.httpStatus >= 200 && res.httpStatus < 300;
  const bodyOk = res.status === 0 || res.status === 200;
  return httpOk && bodyOk;
}

function createFailure(errorCode, title, message, extra = {}) {
  return {
    ok: false,
    phase: "failed",
    errorCode: errorCode != null ? String(errorCode) : null,
    errorTitle: title,
    errorMessage: message,
    ...extra,
  };
}

function pickRawMessage(res) {
  return String(res.msg || res.message || res.desc || "").trim();
}

function formatApiError(res) {
  const httpStatus = res.httpStatus || 0;
  const code = res.status;

  if (httpStatus === 403) {
    return createFailure("403", "Authentication failed", ERROR_MESSAGES[403], {
      errorCategory: "auth",
      retryable: false,
    });
  }
  if (httpStatus === 429) {
    return createFailure("429", "Too many requests", ERROR_MESSAGES[429], {
      errorCategory: "rate_limit",
      retryable: true,
    });
  }
  if (httpStatus >= 500) {
    return createFailure("500", "Temporary service issue", ERROR_MESSAGES[500], {
      errorCategory: "server",
      retryable: true,
    });
  }
  if (httpStatus === 400) {
    return createFailure("400", "Invalid request", ERROR_MESSAGES[400], {
      errorCategory: "validation",
      retryable: false,
    });
  }

  const mapped = STATIC_ERROR_MAP[code];
  if (mapped) {
    return createFailure(code, mapped.title, mapped.message, {
      errorCategory: mapped.category,
      retryable: mapped.retryable,
    });
  }

  return createFailure(code, "Request failed", pickRawMessage(res) || "We could not complete this request right now. Please try again later.", {
    errorCategory: "server",
    retryable: true,
  });
}

function extractVideos(taskData) {
  const raw = taskData?.videos || taskData?.task_result?.videos || [];
  return raw.map((item) => {
    if (typeof item === "string") return { url: item };
    return {
      url: item?.url || item?.video_url || "",
      cover_url: item?.cover_url || item?.cover_image_url || "",
    };
  });
}

async function submitTool(spec, payload, apiKey) {
  const res = await httpJson("POST", BASE_URL + spec.endpoint, payload, apiKey);
  if (!isApiSuccess(res)) return formatApiError(res);

  const data = res.data || {};
  const taskIds = data.task_ids ?? (data.task_id ? [data.task_id] : []);
  return {
    ok: true,
    phase: "submitted",
    tool: spec.id,
    endpoint: spec.endpoint,
    batchId: data.batch_id ?? null,
    taskIds,
    taskId: taskIds[0] ?? data.task_id ?? null,
    taskStatus: null,
    videos: null,
    errorTitle: null,
    errorCode: null,
    errorCategory: null,
    retryable: null,
    errorMessage: null,
  };
}

async function statusTask(taskId, apiKey) {
  const res = await httpJson("GET", `${BASE_URL}/v1/generation/${taskId}/status`, null, apiKey);
  if (!isApiSuccess(res)) return formatApiError(res);

  const taskData = res.data || {};
  const rawStatus = taskData.task_status || "";
  const normalized = STATUS_MAP[rawStatus] || "unknown";
  const result = taskData.task_result || {};

  return {
    ok: normalized !== "failed",
    phase: normalized === "completed" ? "completed" : normalized === "failed" ? "failed" : "running",
    taskId,
    taskStatus: rawStatus,
    videos: extractVideos(taskData),
    errorTitle: normalized === "failed" ? "Task failed" : null,
    errorCode: normalized === "failed" ? "TASK_FAILED" : null,
    errorCategory: normalized === "failed" ? "task" : null,
    retryable: normalized === "failed" ? false : null,
    errorMessage:
      normalized === "failed"
        ? result.message || taskData.msg || "The task could not be completed. Please review the request and try again."
        : null,
  };
}

async function waitForTask(taskId, apiKey) {
  const startedAt = Date.now();
  while (Date.now() - startedAt < POLL_TIMEOUT_MS) {
    await sleep(POLL_INTERVAL_MS);
    const status = await statusTask(taskId, apiKey);
    if (!status.ok && status.phase === "failed") return status;
    if (status.phase === "completed") return status;
  }
  return {
    ok: false,
    phase: "failed",
    taskId,
    taskStatus: "unknown",
    videos: null,
    errorTitle: "Request timed out",
    errorCode: "TIMEOUT",
    errorCategory: "timeout",
    retryable: true,
    errorMessage: `Poll timeout after ${Math.floor(POLL_TIMEOUT_MS / 1000)}s.`,
  };
}

function parseArgs(argv) {
  const command = argv[0] || "help";
  const args = {
    command,
    json: null,
    taskId: null,
    dryRun: false,
    pretty: false,
  };

  for (let i = 1; i < argv.length; i++) {
    const current = argv[i];
    if (current === "--json") args.json = argv[++i] ?? null;
    else if (current === "--task-id") args.taskId = argv[++i] ?? null;
    else if (current === "--dry-run") args.dryRun = true;
    else if (current === "--pretty") args.pretty = true;
    else if (current === "--help" || current === "-h") args.command = "help";
  }

  return args;
}

function parseJsonInput(raw) {
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Invalid JSON passed to --json: ${error.message}`);
  }
}

function print(result, pretty = false) {
  const spaces = pretty ? 2 : 0;
  process.stdout.write(JSON.stringify(result, null, spaces) + "\n");
}

function printHelp(spec, scriptName) {
  const lines = [
    "Usage:",
    `  node scripts/${scriptName} help`,
    `  node scripts/${scriptName} spec`,
    `  node scripts/${scriptName} submit --json '{...}' [--dry-run] [--pretty]`,
    `  node scripts/${scriptName} wait --json '{...}' [--dry-run] [--pretty]`,
    `  node scripts/${scriptName} status --task-id <task-id> [--pretty]`,
    "",
    `Tool: ${spec.id}`,
    spec.summary || "",
    "",
    "Required fields:",
    ...spec.required.map((f) => `  - ${f}`),
    "",
    "Notes:",
    "  - Real submit/wait/status calls require WERYAI_API_KEY.",
    "  - Dry-run validates and prints the request body without calling WeryAI.",
    "  - video_url, image_url, and audio_url (when used) must be public https:// URLs.",
  ];
  process.stdout.write(lines.filter(Boolean).join("\n") + "\n");
}

/**
 * @param {string[]} argv - process.argv.slice(2)
 * @param {object} spec - { id, endpoint, summary, required, defaults, enums, urlFields, rectField?, preparePayload? }
 * @param {string} scriptName - basename for help text, e.g. "video_anime_replace.js"
 */
async function runMain(argv, spec, scriptName) {
  const name = scriptName || "video-tool.js";
  const args = parseArgs(argv);
  if (args.command === "help" || args.command === "--help" || args.command === "-h") {
    printHelp(spec, name);
    return;
  }

  if (args.command === "spec") {
    print(
      {
        ok: true,
        tool: {
          id: spec.id,
          endpoint: spec.endpoint,
          summary: spec.summary,
          required: spec.required,
          defaults: spec.defaults,
          enums: spec.enums || {},
          urlFields: spec.urlFields,
          rectField: spec.rectField || null,
        },
      },
      true
    );
    return;
  }

  if (args.command === "status") {
    if (!args.taskId) throw new Error("--task-id is required for status");
    const apiKey = getApiKey();
    if (!apiKey) {
      print({
        ok: false,
        phase: "failed",
        errorTitle: "Missing API key",
        errorCode: "NO_API_KEY",
        errorCategory: "auth",
        retryable: false,
        errorMessage:
          "Missing WERYAI_API_KEY environment variable. Get one from https://www.weryai.com/api/keys and configure it only in the runtime environment before using this skill.",
      }, true);
      process.exitCode = 1;
      return;
    }
    const result = await statusTask(args.taskId, apiKey);
    print(result, true);
    if (!result.ok) process.exitCode = 1;
    return;
  }

  if (args.command !== "submit" && args.command !== "wait") {
    throw new Error(`Unsupported command: ${args.command}`);
  }

  const payload = buildPayload(spec, parseJsonInput(args.json));
  const validationErrors = validatePayload(spec, payload);
  if (validationErrors.length > 0) {
    print({
      ok: false,
      phase: "failed",
      tool: spec.id,
      errorTitle: "Invalid request",
      errorCode: "VALIDATION",
      errorCategory: "validation",
      retryable: false,
      errorMessage: validationErrors.join(" "),
      required: spec.required,
      defaults: spec.defaults,
    }, true);
    process.exitCode = 1;
    return;
  }

  if (args.dryRun) {
    print({
      ok: true,
      phase: args.command === "wait" ? "wait-dry-run" : "submit-dry-run",
      tool: spec.id,
      endpoint: spec.endpoint,
      requestPreview: {
        method: "POST",
        url: `${BASE_URL}${spec.endpoint}`,
        body: payload,
      },
    }, true);
    return;
  }

  const apiKey = getApiKey();
  if (!apiKey) {
    print({
      ok: false,
      phase: "failed",
      errorTitle: "Missing API key",
      errorCode: "NO_API_KEY",
      errorCategory: "auth",
      retryable: false,
      errorMessage:
        "Missing WERYAI_API_KEY environment variable. Get one from https://www.weryai.com/api/keys and configure it only in the runtime environment before using this skill.",
    }, true);
    process.exitCode = 1;
    return;
  }

  const submitResult = await submitTool(spec, payload, apiKey);
  if (!submitResult.ok) {
    print(submitResult, true);
    process.exitCode = 1;
    return;
  }

  if (args.command === "submit") {
    print(submitResult, true);
    return;
  }

  const waitResult = await waitForTask(submitResult.taskId, apiKey);
  print(
    {
      ...waitResult,
      tool: spec.id,
      batchId: submitResult.batchId,
      taskIds: submitResult.taskIds,
    },
    true
  );
  if (!waitResult.ok) process.exitCode = 1;
}

function mainSync(argv, spec, scriptName) {
  runMain(argv, spec, scriptName).catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exit(1);
  });
}


mainSync(process.argv.slice(2), TOOL, "video_subtitle_translate.js");
