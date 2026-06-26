#!/usr/bin/env node
/**
 * WeryAI image toolkits CLI.
 *
 * Commands:
 *   tools
 *   submit --tool <id> --json '{...}'
 *   wait --tool <id> --json '{...}'
 *   status --task-id <id>
 *
 * Runtime secret:
 *   WERYAI_API_KEY
 */

const fs = require("node:fs/promises");
const path = require("node:path");
const { fileURLToPath } = require("node:url");

const BASE_URL = (process.env.WERYAI_BASE_URL || "https://api.weryai.com").replace(/\/$/, "");
const UPLOAD_API_PATH = "/v1/generation/upload-file";
const POLL_INTERVAL_MS = Number(process.env.WERYAI_POLL_INTERVAL_MS || 6000);
const POLL_TIMEOUT_MS = Number(process.env.WERYAI_POLL_TIMEOUT_MS || 300000);

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
  1001: {
    category: "rate_limit",
    title: "Too many requests",
    message: "Too many requests in a short time. Please wait a moment and try again.",
    retryable: true,
  },
  1003: {
    category: "not_found",
    title: "Resource not found",
    message: "The requested item could not be found. Please check the ID or input and try again.",
    retryable: false,
  },
  1010: {
    category: "not_found",
    title: "Resource not found",
    message: "The requested item could not be found. Please check the ID or input and try again.",
    retryable: false,
  },
  1011: {
    category: "credits",
    title: "Not enough credits",
    message: "You do not have enough credits to complete this request.",
    retryable: false,
  },
  1014: {
    category: "upload",
    title: "Upload limit reached",
    message: "You have reached an upload limit. Please wait and try again later.",
    retryable: true,
  },
  1015: {
    category: "upload",
    title: "Upload limit reached",
    message: "You have reached an upload limit. Please wait and try again later.",
    retryable: true,
  },
  1102: {
    category: "upload",
    title: "Upload failed",
    message: "We could not upload the file right now. Please try again.",
    retryable: true,
  },
  2001: {
    category: "content_safety",
    title: "Input image flagged",
    message: "The provided image was flagged by the safety system. Please use a different image and try again.",
    retryable: false,
  },
  2003: {
    category: "content_safety",
    title: "Content flagged",
    message: "The provided prompt or image was flagged by the safety system. Please revise it and try again.",
    retryable: false,
  },
  2004: {
    category: "validation",
    title: "Unsupported image format",
    message: "The image format is not supported. Please use JPG, JPEG, PNG, or WEBP.",
    retryable: false,
  },
  6001: {
    category: "server",
    title: "Temporary service issue",
    message: "Something went wrong on our side. Please try again in a moment.",
    retryable: true,
  },
  6002: {
    category: "rate_limit",
    title: "Too many requests",
    message: "Too many requests in a short time. Please wait a moment and try again.",
    retryable: true,
  },
  6003: {
    category: "server",
    title: "Temporary service issue",
    message: "Something went wrong on our side. Please try again in a moment.",
    retryable: true,
  },
  6004: {
    category: "server",
    title: "Generation failed",
    message: "The request could not be completed. Please try again with different input or try again later.",
    retryable: true,
  },
  6010: {
    category: "active_job_limit",
    title: "Too many active jobs",
    message: "You already have too many active jobs. Please wait for current jobs to finish before starting a new one.",
    retryable: true,
  },
  6101: {
    category: "daily_limit",
    title: "Daily limit reached",
    message: "You have reached the daily limit for this workflow. Please try again later.",
    retryable: true,
  },
};

const VALIDATION_PATTERNS = [
  {
    pattern: /\bprompt and bg_color cannot both be empty\b/i,
    field: "prompt|bg_color",
    title: "Missing background settings",
    message: "Please provide either a background prompt or a background color.",
  },
  {
    pattern: /\bimage url cannot be empty\b/i,
    field: "img_url",
    title: "Missing image URL",
    message: "Please provide a valid image URL.",
  },
  {
    pattern: /\bimage url error\b/i,
    field: "img_url",
    title: "Invalid image URL",
    message: "The provided image URL is not valid. Please check it and try again.",
  },
  {
    pattern: /\bimage cannot be empty\b/i,
    field: "img_url",
    title: "Missing image",
    message: "Please provide an image for this request.",
  },
  {
    pattern: /\bimages cannot be empty\b/i,
    field: "images",
    title: "Missing images",
    message: "Please provide at least one image for this request.",
  },
  {
    pattern: /\bface.*cannot be empty\b|\bface_img_url cannot be empty\b/i,
    field: "face_img_url",
    title: "Missing face image",
    message: "Please provide a valid face reference image URL.",
  },
  {
    pattern: /\bonly support jpg|jpeg|png|webp image type\b/i,
    field: "img_url",
    title: "Unsupported image format",
    message: "The image format is not supported. Please use JPG, JPEG, PNG, or WEBP.",
  },
  {
    pattern: /\baspect ratio cannot be empty\b/i,
    field: "aspect_ratio",
    title: "Missing aspect ratio",
    message: "Please provide an aspect ratio for this request.",
  },
  {
    pattern: /\baspect ratio .* is not supported\b/i,
    field: "aspect_ratio",
    title: "Unsupported aspect ratio",
    message: "The selected aspect ratio is not supported for this request.",
  },
  {
    pattern: /\btarget language cannot be empty\b|\blanguage cannot be empty\b/i,
    field: "target_lang",
    title: "Missing target language",
    message: "Please provide a target language for this request.",
  },
  {
    pattern: /\btype .* is not supported\b/i,
    field: "type",
    title: "Unsupported type",
    message: "The selected type is not supported for this request.",
  },
  {
    pattern: /\btask id cannot be empty\b/i,
    field: "task_id",
    title: "Missing task ID",
    message: "Please provide a task ID.",
  },
  {
    pattern: /\btask id error\b/i,
    field: "task_id",
    title: "Invalid task ID",
    message: "The task ID is invalid. Please check it and try again.",
  },
  {
    pattern: /\btask not exist\b/i,
    field: "task_id",
    title: "Task not found",
    message: "The requested task could not be found. Please check the task ID and try again.",
  },
  {
    pattern: /\bbatch not exist\b|\bno tasks found\b/i,
    field: "batch_id",
    title: "Batch not found",
    message: "The requested batch could not be found. Please check the batch ID and try again.",
  },
  {
    pattern: /敏感内容|sensitive content|content flagged|safety/i,
    field: "content",
    title: "Content flagged",
    message: "The provided image or request content was flagged by the safety system. Please revise it and try again.",
  },
];

const ASPECT_RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "9:21"];
const TRANSLATE_TYPES = ["text", "image"];

const TOOLS = {
  "image-to-prompt": {
    endpoint: "/v1/generation/image-to-prompt",
    summary: "Analyze an image and return a descriptive prompt synchronously.",
    required: ["img_url", "image_size"],
    defaults: {},
    enums: {},
    urlFields: ["img_url"],
    sync: true,
  },
  "background-change": {
    endpoint: "/v1/generation/image-bg-change",
    summary: "Replace or modify the background using a prompt or a color.",
    required: ["img_url"],
    defaults: {},
    enums: {},
    urlFields: ["img_url"],
  },
  "background-remove": {
    endpoint: "/v1/generation/image-bg-remove",
    summary: "Automatically remove the background from an image.",
    required: ["img_url"],
    defaults: {},
    enums: {},
    urlFields: ["img_url"],
  },
  expand: {
    endpoint: "/v1/generation/image-expand",
    summary: "Expand canvas size and place the original image onto the new canvas.",
    required: ["img_url", "original_image_size", "canvas_size", "original_image_location"],
    defaults: {},
    enums: {},
    urlFields: ["img_url"],
  },
  "face-swap": {
    endpoint: "/v1/generation/image-face-swap",
    summary: "Swap the face in the source image using a face reference image.",
    required: ["img_url", "face_img_url"],
    defaults: {},
    enums: {},
    urlFields: ["img_url", "face_img_url"],
  },
  reframe: {
    endpoint: "/v1/generation/image-reframe",
    summary: "Change an image aspect ratio to a supported target ratio.",
    required: ["img_url", "aspect_ratio"],
    defaults: {},
    enums: { aspect_ratio: ASPECT_RATIOS },
    urlFields: ["img_url"],
  },
  repair: {
    endpoint: "/v1/generation/image-repair",
    summary: "Restore and enhance an old or damaged photo.",
    required: ["img_url"],
    defaults: {},
    enums: {},
    urlFields: ["img_url"],
  },
  "text-erase": {
    endpoint: "/v1/generation/image-text-erase",
    summary: "Erase text or watermarks from an image.",
    required: ["img_url"],
    defaults: {},
    enums: {},
    urlFields: ["img_url"],
  },
  translate: {
    endpoint: "/v1/generation/image-translate",
    summary: "Translate text inside an image to another language.",
    required: ["img_url", "target_lang"],
    defaults: { type: "image" },
    enums: { type: TRANSLATE_TYPES },
    urlFields: ["img_url"],
  },
  upscale: {
    endpoint: "/v1/generation/image-upscale",
    summary: "Enhance an image with 2x upscale.",
    required: ["img_url"],
    defaults: {},
    enums: {},
    urlFields: ["img_url"],
  },
};

function printHelp() {
  const lines = [
    "Usage:",
    "  node scripts/image_toolkits.js tools",
    "  node scripts/image_toolkits.js submit --tool <tool-id> --json '{...}' [--dry-run]",
    "  node scripts/image_toolkits.js wait --tool <tool-id> --json '{...}' [--dry-run]",
    "  node scripts/image_toolkits.js status --task-id <task-id>",
    "",
    "Tool IDs:",
    ...Object.entries(TOOLS).map(([id, tool]) => `  - ${id}: ${tool.summary}`),
    "",
    "Notes:",
    "  - Real submit/wait/status calls require WERYAI_API_KEY.",
    "  - Dry-run validates and prints the request body without calling WeryAI.",
    "  - img_url and face_img_url can be http/https URLs; local/non-http(s) sources are uploaded first.",
  ];
  process.stdout.write(lines.join("\n") + "\n");
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeToolId(value) {
  return String(value || "").trim().toLowerCase().replace(/[_\s]+/g, "-");
}

function parseJsonInput(raw) {
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Invalid JSON passed to --json: ${error.message}`);
  }
}

function normalizePayload(toolId, input) {
  const payload = { ...(input || {}) };
  if (toolId === "translate" && payload.target_language && payload.target_lang == null) {
    payload.target_lang = payload.target_language;
  }
  if (toolId === "background-change" && payload.background_color && payload.bg_color == null) {
    payload.bg_color = payload.background_color;
  }
  return payload;
}

function buildPayload(toolId, input) {
  const spec = TOOLS[toolId];
  return { ...spec.defaults, ...normalizePayload(toolId, input) };
}

function validateHttpsUrl(value, fieldName, errors) {
  if (typeof value !== "string" || value.trim().length === 0) {
    errors.push(`${fieldName} must be a non-empty source string.`);
  }
}

function validateSizeString(value, fieldName, errors) {
  if (typeof value !== "string" || !/^\d+x\d+$/i.test(value.trim())) {
    errors.push(`${fieldName} must use WIDTHxHEIGHT format, e.g. 1024x1024.`);
  }
}

function validateLocationString(value, fieldName, errors) {
  if (typeof value !== "string" || !/^\d+\s*,\s*\d+$/.test(value.trim())) {
    errors.push(`${fieldName} must use x,y pixel coordinates, e.g. 256,256.`);
  }
}

function validateHexColor(value, fieldName, errors) {
  if (value == null) return;
  if (typeof value !== "string" || !/^#[0-9a-fA-F]{6}$/.test(value.trim())) {
    errors.push(`${fieldName} must be a hex color like #FFFFFF.`);
  }
}

function validatePayload(toolId, payload) {
  const spec = TOOLS[toolId];
  const errors = [];

  for (const field of spec.required) {
    if (payload[field] == null || payload[field] === "") {
      errors.push(`${field} is required for tool ${toolId}.`);
    }
  }

  for (const field of spec.urlFields) {
    if (payload[field] != null) validateHttpsUrl(payload[field], field, errors);
  }

  for (const [field, allowedValues] of Object.entries(spec.enums)) {
    if (payload[field] == null) continue;
    const value = String(payload[field]);
    if (!allowedValues.includes(value)) {
      errors.push(`${field} must be one of: ${allowedValues.join(", ")}.`);
    } else {
      payload[field] = value;
    }
  }

  if (toolId === "image-to-prompt" && payload.image_size != null) {
    const n = Number(payload.image_size);
    if (!Number.isInteger(n) || n < 1) errors.push("image_size must be a positive integer in KB.");
    else payload.image_size = n;
  }

  if (toolId === "background-change") {
    if (!payload.prompt && !payload.bg_color) {
      errors.push("background-change requires either prompt or bg_color.");
    }
    validateHexColor(payload.bg_color, "bg_color", errors);
  }

  if (toolId === "expand") {
    validateSizeString(payload.original_image_size, "original_image_size", errors);
    validateSizeString(payload.canvas_size, "canvas_size", errors);
    validateLocationString(payload.original_image_location, "original_image_location", errors);
  }

  return errors;
}

function getApiKey() {
  const apiKey = (process.env.WERYAI_API_KEY || "").trim();
  return apiKey || null;
}

function isRemoteUrl(value) {
  if (typeof value !== "string" || value.trim().length === 0) return false;
  try {
    const url = new URL(value);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

function normalizeLocalFilePath(value) {
  if (typeof value !== "string" || value.trim().length === 0) return null;
  if (value.startsWith("file://")) return fileURLToPath(new URL(value));
  return path.resolve(value);
}

function inferMimeTypeByExtension(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
  if (ext === ".png") return "image/png";
  if (ext === ".webp") return "image/webp";
  if (ext === ".gif") return "image/gif";
  if (ext === ".bmp") return "image/bmp";
  if (ext === ".tiff" || ext === ".tif") return "image/tiff";
  if (ext === ".mp4") return "video/mp4";
  if (ext === ".mov") return "video/quicktime";
  if (ext === ".m4v") return "video/x-m4v";
  if (ext === ".webm") return "video/webm";
  if (ext === ".avi") return "video/x-msvideo";
  if (ext === ".mkv") return "video/x-matroska";
  if (ext === ".mp3") return "audio/mpeg";
  if (ext === ".wav") return "audio/wav";
  if (ext === ".m4a") return "audio/mp4";
  if (ext === ".aac") return "audio/aac";
  if (ext === ".flac") return "audio/flac";
  if (ext === ".ogg") return "audio/ogg";
  return "application/octet-stream";
}

function extractUploadUrl(res) {
  const list = res?.data?.object_url_list;
  if (Array.isArray(list) && typeof list[0] === "string" && list[0].trim()) {
    return list[0].trim();
  }
  return null;
}

function collectUploadPreview(toolId, payload) {
  const spec = TOOLS[toolId];
  const out = [];
  for (const field of spec.urlFields) {
    const value = payload[field];
    if (typeof value === "string" && value.trim() && !isRemoteUrl(value)) {
      out.push({ field, source: value });
    }
  }
  return out;
}

async function uploadLocalFile(apiKey, source) {
  const localPath = normalizeLocalFilePath(source);
  if (!localPath) throw new Error(`Invalid local path: ${source}`);

  const stat = await fs.stat(localPath);
  if (!stat.isFile()) throw new Error(`Local path is not a file: ${source}`);

  const fileBuffer = await fs.readFile(localPath);
  const fileName = path.basename(localPath);
  const mimeType = inferMimeTypeByExtension(localPath);
  const form = new FormData();
  form.append("file", new Blob([fileBuffer], { type: mimeType }), fileName);
  form.append("batch_no", `image-toolkits-upload-${Date.now()}`);
  form.append("fixed", "false");

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 60000);

  let res;
  try {
    res = await fetch(`${BASE_URL}${UPLOAD_API_PATH}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}` },
      body: form,
      signal: controller.signal,
    });
  } catch (error) {
    clearTimeout(timer);
    if (error?.name === "AbortError") throw new Error(`Upload timeout: ${source}`);
    throw error;
  }
  clearTimeout(timer);

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error(`Upload failed with non-JSON response (HTTP ${res.status}).`);
  }

  const wrapped = { httpStatus: res.status, ...data };
  if (!isApiSuccess(wrapped)) {
    const apiErr = formatApiError(wrapped);
    throw new Error(apiErr.errorMessage || `Upload failed (HTTP ${res.status}).`);
  }

  const uploaded = extractUploadUrl(wrapped);
  if (!uploaded) throw new Error("Upload succeeded but object_url_list[0] is missing.");
  return uploaded;
}

async function resolvePayloadMediaSources(toolId, payload, apiKey) {
  const spec = TOOLS[toolId];
  const out = { ...payload };
  for (const field of spec.urlFields) {
    const value = out[field];
    if (typeof value !== "string" || value.trim().length === 0) continue;
    if (!isRemoteUrl(value)) {
      out[field] = await uploadLocalFile(apiKey, value);
    }
  }
  return out;
}

async function httpJson(method, url, body, apiKey) {
  const headers = {
    "Content-Type": "application/json; charset=utf-8",
    Accept: "application/json; charset=utf-8",
  };
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
    if (error?.name === "AbortError") throw new Error(`Request timeout: ${method} ${url}`);
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

function parseValidationError(res) {
  const rawText = pickRawMessage(res);

  for (const rule of VALIDATION_PATTERNS) {
    if (rule.pattern.test(rawText)) {
      return createFailure("1002", rule.title, rule.message, {
        errorCategory: "validation",
        retryable: false,
        field: rule.field,
      });
    }
  }

  if (/missing|cannot be empty|required/i.test(rawText)) {
    return createFailure("1002", "Missing required input", "Some required information is missing. Please review your input and try again.", {
      errorCategory: "validation",
      retryable: false,
    });
  }

  if (/invalid|unsupported|error/i.test(rawText)) {
    return createFailure("1002", "Invalid request parameters", "One or more request settings are invalid or not supported. Please review your input and try again.", {
      errorCategory: "validation",
      retryable: false,
    });
  }

  return createFailure("1002", "Invalid request", "Some of the request details are missing or not supported. Please review your input and try again.", {
    errorCategory: "validation",
    retryable: false,
  });
}

function formatApiError(res) {
  const httpStatus = res.httpStatus || 0;
  const code = res.status;
  const msg = pickRawMessage(res);

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

  if (String(code) === "1002") {
    return parseValidationError(res);
  }

  const mapped = STATIC_ERROR_MAP[code];
  if (mapped) {
    return createFailure(code, mapped.title, mapped.message, {
      errorCategory: mapped.category,
      retryable: mapped.retryable,
    });
  }

  return createFailure(code, "Request failed", msg || "We could not complete your request right now. Please try again later.", {
    errorCategory: "server",
    retryable: true,
  });
}

function extractImages(taskData) {
  const raw = taskData?.images || taskData?.task_result?.images || [];
  return raw.map((item) => {
    if (typeof item === "string") return { url: item };
    return { url: item?.url || item?.image_url || "" };
  });
}

async function submitTool(toolId, payload, apiKey) {
  const spec = TOOLS[toolId];
  const res = await httpJson("POST", BASE_URL + spec.endpoint, payload, apiKey);
  if (!isApiSuccess(res)) return formatApiError(res);

  if (spec.sync) {
    return {
      ok: true,
      phase: "completed",
      tool: toolId,
      endpoint: spec.endpoint,
      taskId: null,
      taskStatus: "succeed",
      prompt: res.data?.prompt ?? null,
      cost_mill: res.data?.cost_mill ?? null,
      images: null,
      requestSummary: buildRequestSummary(payload),
      errorCode: null,
      errorMessage: null,
    };
  }

  const data = res.data || {};
  const taskIds = data.task_ids ?? (data.task_id ? [data.task_id] : []);
  return {
    ok: true,
    phase: "submitted",
    tool: toolId,
    endpoint: spec.endpoint,
    batchId: data.batch_id ?? null,
    taskIds,
    taskId: taskIds[0] ?? data.task_id ?? null,
    taskStatus: data.task_status ?? null,
    images: null,
    requestSummary: buildRequestSummary(payload),
    errorCode: null,
    errorMessage: null,
  };
}

function buildRequestSummary(payload) {
  return {
    model: payload?.model ?? null,
    aspectRatio: payload?.aspect_ratio ?? null,
    imageNumber: payload?.image_number ?? null,
    resolution: payload?.resolution ?? null,
    tool: null,
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
    images: extractImages(taskData),
      errorTitle: normalized === "failed" ? "Task failed" : null,
    errorCode: normalized === "failed" ? "TASK_FAILED" : null,
      errorCategory: normalized === "failed" ? "task" : null,
      retryable: normalized === "failed" ? false : null,
      errorMessage: normalized === "failed" ? pickRawMessage(result) || pickRawMessage(taskData) || "The task could not be completed. Please review the request and try again." : null,
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
    images: null,
    errorTitle: "Request timed out",
    errorCode: "TIMEOUT",
    errorCategory: "timeout",
    retryable: true,
    errorMessage: `Poll timeout after ${Math.floor(POLL_TIMEOUT_MS / 1000)}s.`,
    timeoutSeconds: Math.floor(POLL_TIMEOUT_MS / 1000),
  };
}

function parseArgs(argv) {
  const command = argv[0] || "help";
  const args = {
    command,
    tool: null,
    json: null,
    taskId: null,
    dryRun: false,
  };
  for (let i = 1; i < argv.length; i++) {
    const current = argv[i];
    if (current === "--tool") args.tool = argv[++i] ?? null;
    else if (current === "--json") args.json = argv[++i] ?? null;
    else if (current === "--task-id") args.taskId = argv[++i] ?? null;
    else if (current === "--dry-run") args.dryRun = true;
    else if (current === "--help" || current === "-h") args.command = "help";
  }
  return args;
}

function print(result) {
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.command === "help" || args.command === "--help" || args.command === "-h") {
    printHelp();
    return;
  }

  if (args.command === "tools") {
    print({
      ok: true,
      tools: Object.entries(TOOLS).map(([id, tool]) => ({
        id,
        endpoint: tool.endpoint,
        summary: tool.summary,
        required: tool.required,
        defaults: tool.defaults,
        enums: tool.enums,
        sync: Boolean(tool.sync),
      })),
    });
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
        errorMessage: "Missing WERYAI_API_KEY environment variable. Get one from https://www.weryai.com/api/keys and configure it only in the runtime environment before using this skill.",
      });
      process.exitCode = 1;
      return;
    }
    const result = await statusTask(args.taskId, apiKey);
    print(result);
    if (!result.ok) process.exitCode = 1;
    return;
  }

  if (args.command !== "submit" && args.command !== "wait") {
    throw new Error(`Unsupported command: ${args.command}`);
  }

  const toolId = normalizeToolId(args.tool);
  if (!TOOLS[toolId]) {
    throw new Error(`Unknown --tool: ${args.tool}. Use "tools" to list supported tool IDs.`);
  }

  const payload = buildPayload(toolId, parseJsonInput(args.json));
  const validationErrors = validatePayload(toolId, payload);
  if (validationErrors.length > 0) {
    print({
      ok: false,
      phase: "failed",
      tool: toolId,
      errorTitle: "Invalid request",
      errorCode: "VALIDATION",
      errorCategory: "validation",
      retryable: false,
      errorMessage: validationErrors.join(" "),
      required: TOOLS[toolId].required,
      defaults: TOOLS[toolId].defaults,
    });
    process.exitCode = 1;
    return;
  }

  if (args.dryRun) {
    const uploadPreview = collectUploadPreview(toolId, payload);
    print({
      ok: true,
      phase: args.command === "wait" ? "wait-dry-run" : "submit-dry-run",
      tool: toolId,
      endpoint: TOOLS[toolId].endpoint,
      uploadPreview,
      requestPreview: {
        method: "POST",
        url: `${BASE_URL}${TOOLS[toolId].endpoint}`,
        body: payload,
      },
      notes: uploadPreview.length > 0
        ? "dry-run does not upload local files. Local sources in uploadPreview will be uploaded in a real run via /v1/generation/upload-file."
        : null,
    });
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
      errorMessage: "Missing WERYAI_API_KEY environment variable. Get one from https://www.weryai.com/api/keys and configure it only in the runtime environment before using this skill.",
    });
    process.exitCode = 1;
    return;
  }

  let resolvedPayload;
  try {
    resolvedPayload = await resolvePayloadMediaSources(toolId, payload, apiKey);
  } catch (error) {
    print({
      ok: false,
      phase: "failed",
      tool: toolId,
      errorTitle: "Upload failed",
      errorCode: "UPLOAD_FAILED",
      errorCategory: "upload",
      retryable: true,
      errorMessage: error instanceof Error ? error.message : String(error),
    });
    process.exitCode = 1;
    return;
  }

  const submitResult = await submitTool(toolId, resolvedPayload, apiKey);
  if (!submitResult.ok) {
    print(submitResult);
    process.exitCode = 1;
    return;
  }

  if (args.command === "submit" || TOOLS[toolId].sync) {
    print({
      ...submitResult,
      requestSummary: {
        ...submitResult.requestSummary,
        tool: toolId,
      },
    });
    return;
  }

  const waitResult = await waitForTask(submitResult.taskId, apiKey);
  print({
    ...waitResult,
    tool: toolId,
    batchId: submitResult.batchId,
    taskIds: submitResult.taskIds,
    requestSummary: {
      ...submitResult.requestSummary,
      tool: toolId,
    },
    nextStatusCommand: waitResult.errorCode === "TIMEOUT"
      ? `node {baseDir}/scripts/image_toolkits.js status --task-id ${submitResult.taskId}`
      : null,
  });
  if (!waitResult.ok) process.exitCode = 1;
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
});
