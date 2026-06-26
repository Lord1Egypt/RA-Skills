#!/usr/bin/env node
/**
 * Seedance 2.0 video generation CLI for WeryAI.
 *
 * Commands:
 *   wait | submit-text | submit-image | submit-multi-image | status | models
 *
 * Examples:
 *   node video_gen.js models
 *   node video_gen.js wait --json '{"prompt":"A neon koi swims through ink clouds","duration":5}'
 *   node video_gen.js wait --json '{"prompt":"Bridge the first frame to the last frame","first_frame":"https://...","last_frame":"https://...","duration":5}'
 *   node video_gen.js wait --json '...' --dry-run
 *
 * Required environment variable for paid calls:
 *   WERYAI_API_KEY
 */

const DEFAULT_MODEL = 'SEEDANCE_2_0';
const BASE_URL = (process.env.WERYAI_BASE_URL || 'https://api.weryai.com').replace(/\/$/, '');
const MODELS_BASE_URL = (process.env.WERYAI_MODELS_BASE_URL || 'https://api-growth-agent.weryai.com').replace(
  /\/$/,
  '',
);
const MODELS_API_PATH = '/growthai/v1/video/models';
const POLL_INTERVAL_MS = Number(process.env.WERYAI_POLL_INTERVAL_MS || 6000);
const POLL_TIMEOUT_MS = Number(process.env.WERYAI_POLL_TIMEOUT_MS || 600000);

const STATUS_MAP = {
  waiting: 'waiting',
  WAITING: 'waiting',
  pending: 'waiting',
  PENDING: 'waiting',
  processing: 'processing',
  PROCESSING: 'processing',
  succeed: 'completed',
  SUCCEED: 'completed',
  success: 'completed',
  SUCCESS: 'completed',
  failed: 'failed',
  FAILED: 'failed',
};

const ERROR_MESSAGES = {
  400: 'Bad request. Check your request parameters.',
  403: 'Invalid API key or IP access denied. Verify WERYAI_API_KEY.',
  500: 'WeryAI server error. Please try again later.',
  1001: 'Request rate limit exceeded. Slow down and retry.',
  1002: 'Parameter error. Check prompt, image URLs, aspect_ratio, model, resolution, and duration.',
  1003: 'Resource not found. The task_id may not exist or may have expired.',
  1006: 'Model not supported. Check the model key or try a different model.',
  1007: 'Queue full. The service is busy; retry later.',
  1011: 'Insufficient credits. Recharge at weryai.com.',
  2003: 'Content flagged by safety system. Revise your prompt or reference images.',
  2004: 'Image format not supported. Use jpg, png, or webp over HTTPS.',
  6004: 'Generation failed. Please try again later.',
  6010: 'Concurrent task limit reached. Wait for existing tasks to finish.',
};

function log(msg) {
  process.stderr.write(`[seedance] ${msg}\n`);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function coerceBool(value, defaultValue = false) {
  if (value == null) return defaultValue;
  if (typeof value === 'boolean') return value;
  return String(value).toLowerCase() === 'true';
}

function normalizeParams(input) {
  const params = { ...input };
  const firstFrame =
    params.first_frame ??
    params.firstFrame ??
    params.start_frame ??
    params.startFrame ??
    params.first_image ??
    params.firstImage;
  const lastFrame =
    params.last_frame ??
    params.lastFrame ??
    params.end_frame ??
    params.endFrame ??
    params.last_image ??
    params.lastImage;
  const singleImage =
    params.image ??
    params.source_image ??
    params.sourceImage ??
    firstFrame;

  if (singleImage && !params.image) {
    params.image = singleImage;
  }
  if ((!Array.isArray(params.images) || params.images.length === 0) && lastFrame && (firstFrame || params.image)) {
    params.images = [firstFrame || params.image, lastFrame];
  }

  return params;
}

function detectMode(params) {
  if (Array.isArray(params.images) && params.images.length > 0) return 'multi_image';
  if (typeof params.image === 'string' && params.image) return 'image';
  return 'text';
}

function validateHttpsUrl(value, fieldName, errors) {
  if (typeof value !== 'string' || value.trim().length === 0) {
    errors.push(`${fieldName} must be a non-empty URL string.`);
    return;
  }
  if (!value.startsWith('https://')) {
    errors.push(`${fieldName} must be a public https:// URL.`);
  }
}

function validateParams(params) {
  const errors = [];
  const firstFrame =
    params.first_frame ??
    params.firstFrame ??
    params.start_frame ??
    params.startFrame ??
    params.first_image ??
    params.firstImage ??
    params.image;
  const lastFrame =
    params.last_frame ??
    params.lastFrame ??
    params.end_frame ??
    params.endFrame ??
    params.last_image ??
    params.lastImage;

  if (!params.prompt || typeof params.prompt !== 'string' || params.prompt.trim().length === 0) {
    errors.push('prompt is required and must be a non-empty string.');
  }

  const duration = params.duration ?? params.dur;
  if (duration == null) {
    errors.push('duration is required (integer seconds).');
  } else {
    const numericDuration = Number(duration);
    if (!Number.isInteger(numericDuration) || numericDuration < 1) {
      errors.push('duration must be a positive integer (seconds).');
    }
  }

  if (!firstFrame && lastFrame) {
    errors.push('last_frame/last_image requires a start image (`image` or `first_frame`).');
  }

  const mode = detectMode(params);
  if (mode === 'image') {
    validateHttpsUrl(params.image, 'image', errors);
  }
  if (mode === 'multi_image') {
    if (!Array.isArray(params.images) || params.images.length === 0) {
      errors.push('images must be a non-empty array of public https URLs.');
    } else {
      params.images.forEach((url, index) => validateHttpsUrl(url, `images[${index}]`, errors));
    }
  }

  return errors;
}

function buildRequestBody(params, mode = detectMode(params)) {
  const body = {
    prompt: params.prompt,
    model: params.model || DEFAULT_MODEL,
    duration: Number(params.duration ?? params.dur) || 5,
  };

  if (params.aspect_ratio) body.aspect_ratio = params.aspect_ratio;
  if (params.resolution) body.resolution = params.resolution;
  if (params.generate_audio != null || params.generateAudio != null) {
    body.generate_audio = coerceBool(params.generate_audio ?? params.generateAudio, false);
  }
  if (params.negative_prompt || params.negativePrompt) {
    body.negative_prompt = params.negative_prompt || params.negativePrompt;
  }
  if (mode === 'image' && params.image) {
    body.image = params.image;
  }
  if (mode === 'multi_image' && Array.isArray(params.images) && params.images.length > 0) {
    body.images = params.images.slice(0, 3);
  }

  return body;
}

async function httpJson(method, fullUrl, body, apiKey) {
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  };
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 30000);

  try {
    const res = await fetch(fullUrl, {
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
      data = { status: res.status, msg: `Non-JSON response (HTTP ${res.status})` };
    }

    return { httpStatus: res.status, ...data };
  } catch (err) {
    clearTimeout(timer);
    if (err.name === 'AbortError') {
      throw new Error(`Request timeout: ${method} ${fullUrl}`);
    }
    throw err;
  }
}

async function apiRequest(method, path, body, apiKey) {
  return httpJson(method, BASE_URL + path, body, apiKey);
}

async function fetchModelsRegistry(apiKey) {
  return httpJson('GET', MODELS_BASE_URL + MODELS_API_PATH, null, apiKey);
}

function isApiSuccess(res) {
  const httpOk = res.httpStatus >= 200 && res.httpStatus < 300;
  const bodyOk = res.status === 0 || res.status === 200;
  return httpOk && bodyOk;
}

function formatApiError(res) {
  const httpStatus = res.httpStatus || 0;
  const code = res.status;
  const msg = res.msg || res.message || '';

  if (httpStatus === 403) {
    return { ok: false, phase: 'failed', errorCode: '403', errorMessage: `${ERROR_MESSAGES[403]}${msg ? ` (${msg})` : ''}` };
  }
  if (httpStatus === 429) {
    return { ok: false, phase: 'failed', errorCode: 'RATE_LIMIT', errorMessage: 'Rate limited by WeryAI API. Please wait and retry.' };
  }
  if (httpStatus >= 500) {
    return { ok: false, phase: 'failed', errorCode: '500', errorMessage: `${ERROR_MESSAGES[500]} (HTTP ${httpStatus})` };
  }
  if (httpStatus === 400) {
    return { ok: false, phase: 'failed', errorCode: '400', errorMessage: `${ERROR_MESSAGES[400]}${msg ? ` (${msg})` : ''}` };
  }

  const friendly = ERROR_MESSAGES[code] || '';
  const errorMessage = friendly && msg ? `${friendly} (${msg})` : friendly || msg || `API error (status ${code}, HTTP ${httpStatus})`;
  return {
    ok: false,
    phase: 'failed',
    errorCode: code != null ? String(code) : null,
    errorMessage,
  };
}

function extractVideos(taskData) {
  const result = taskData.task_result || {};
  const raw = result.videos || taskData.videos || [];
  return raw.map((item) => {
    if (typeof item === 'string') {
      return { url: item, cover_url: '' };
    }
    return {
      url: item?.url || item?.video_url || '',
      cover_url: item?.cover_image_url || item?.cover_url || '',
    };
  });
}

async function submitTask(params, apiKey, allowedModes = null) {
  const errors = validateParams(params);
  if (errors.length > 0) {
    return { ok: false, phase: 'failed', errorCode: 'VALIDATION', errorMessage: errors.join(' ') };
  }

  const mode = detectMode(params);
  if (Array.isArray(allowedModes) && allowedModes.length > 0 && !allowedModes.includes(mode)) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'VALIDATION',
      errorMessage: `This command expects mode ${allowedModes.join(' or ')}, but the normalized payload resolves to ${mode}.`,
    };
  }
  const pathMap = {
    text: '/v1/generation/text-to-video',
    image: '/v1/generation/image-to-video',
    multi_image: '/v1/generation/multi-image-to-video',
  };
  const body = buildRequestBody(params, mode);

  let res;
  try {
    res = await apiRequest('POST', pathMap[mode], body, apiKey);
  } catch (err) {
    return { ok: false, phase: 'failed', errorCode: 'NETWORK_ERROR', errorMessage: err.message || String(err) };
  }

  if (!isApiSuccess(res)) return formatApiError(res);

  const data = res.data || {};
  const taskIds = data.task_ids ?? (data.task_id ? [data.task_id] : []);
  return {
    ok: true,
    phase: 'submitted',
    batchId: data.batch_id ?? null,
    taskIds,
    taskId: taskIds[0] ?? null,
    taskStatus: null,
    videos: null,
    errorCode: null,
    errorMessage: null,
  };
}

async function pollUntilDone(taskId, batchId, taskIds, apiKey) {
  const start = Date.now();

  while (true) {
    if (Date.now() - start >= POLL_TIMEOUT_MS) {
      return {
        ok: false,
        phase: 'failed',
        errorCode: 'TIMEOUT',
        errorMessage: `Poll timeout after ${Math.floor((Date.now() - start) / 1000)}s.`,
        batchId,
        taskIds,
        taskId,
        taskStatus: 'unknown',
        videos: null,
      };
    }

    await sleep(POLL_INTERVAL_MS);

    let res;
    try {
      res = await apiRequest('GET', `/v1/generation/${taskId}/status`, null, apiKey);
    } catch (err) {
      log(`Warning: poll failed (${err.message}). Retrying.`);
      continue;
    }

    if (!isApiSuccess(res)) {
      log('Warning: poll returned non-success status. Retrying.');
      continue;
    }

    const taskData = res.data || {};
    const rawStatus = taskData.task_status || '';
    const normalized = STATUS_MAP[rawStatus] || 'unknown';
    log(`Polling ${taskId}: ${rawStatus || 'unknown'}`);

    if (normalized === 'completed') {
      const videos = extractVideos(taskData);
      return {
        ok: true,
        phase: 'completed',
        batchId,
        taskIds,
        taskId,
        taskStatus: rawStatus,
        videos: videos.length > 0 ? videos : null,
        errorCode: null,
        errorMessage: null,
      };
    }

    if (normalized === 'failed') {
      const result = taskData.task_result || {};
      return {
        ok: false,
        phase: 'failed',
        batchId,
        taskIds,
        taskId,
        taskStatus: rawStatus,
        videos: null,
        errorCode: 'TASK_FAILED',
        errorMessage: result.message || taskData.msg || 'Task failed.',
      };
    }
  }
}

async function cmdWait(params, apiKey) {
  const submitResult = await submitTask(params, apiKey);
  if (!submitResult.ok) return submitResult;

  return pollUntilDone(
    submitResult.taskId,
    submitResult.batchId,
    submitResult.taskIds || [submitResult.taskId],
    apiKey,
  );
}

async function cmdStatus(taskId, apiKey) {
  let res;
  try {
    res = await apiRequest('GET', `/v1/generation/${taskId}/status`, null, apiKey);
  } catch (err) {
    return { ok: false, phase: 'failed', errorCode: 'NETWORK_ERROR', errorMessage: err.message || String(err) };
  }

  if (!isApiSuccess(res)) return formatApiError(res);

  const taskData = res.data || {};
  const rawStatus = taskData.task_status || '';
  const normalized = STATUS_MAP[rawStatus] || 'unknown';
  const videos = extractVideos(taskData);
  const phase = normalized === 'completed' ? 'completed' : normalized === 'failed' ? 'failed' : 'running';
  const result = taskData.task_result || {};

  return {
    ok: phase !== 'failed',
    phase,
    batchId: null,
    taskIds: [taskId],
    taskId,
    taskStatus: rawStatus,
    videos: videos.length > 0 ? videos : null,
    errorCode: phase === 'failed' ? 'TASK_FAILED' : null,
    errorMessage: phase === 'failed' ? result.message || taskData.msg || null : null,
  };
}

const VALID_MODEL_MODES = ['text_to_video', 'image_to_video', 'multi_image_to_video'];

async function cmdModels(modeFilter, apiKey) {
  let res;
  try {
    res = await fetchModelsRegistry(apiKey);
  } catch (err) {
    return { ok: false, phase: 'failed', errorCode: 'NETWORK_ERROR', errorMessage: err.message || String(err) };
  }

  if (!isApiSuccess(res)) return formatApiError(res);

  const data = res.data || {};
  const out = { ok: true, phase: 'completed' };

  if (modeFilter) {
    if (!VALID_MODEL_MODES.includes(modeFilter)) {
      return {
        ok: false,
        phase: 'failed',
        errorCode: 'VALIDATION',
        errorMessage: `Invalid --mode. Use one of: ${VALID_MODEL_MODES.join(', ')}`,
      };
    }
    out[modeFilter] = data[modeFilter] || [];
    return out;
  }

  out.text_to_video = data.text_to_video || [];
  out.image_to_video = data.image_to_video || [];
  out.multi_image_to_video = data.multi_image_to_video || [];
  return out;
}

function parseArgs(argv) {
  const command = argv[0];
  let jsonStr = null;
  let taskId = null;
  let dryRun = false;
  let modelsMode = null;

  for (let i = 1; i < argv.length; i += 1) {
    if (argv[i] === '--json') jsonStr = argv[++i];
    else if (argv[i] === '--task-id') taskId = argv[++i];
    else if (argv[i] === '--dry-run') dryRun = true;
    else if (argv[i] === '--mode') modelsMode = argv[++i];
  }

  return { command, jsonStr, taskId, dryRun, modelsMode };
}

function getAllowedModesForCommand(command) {
  if (command === 'submit-text') return ['text'];
  if (command === 'submit-image') return ['image', 'multi_image'];
  if (command === 'submit-multi-image') return ['multi_image'];
  return null;
}

function printJson(obj) {
  process.stdout.write(`${JSON.stringify(obj, null, 2)}\n`);
}

async function main() {
  const validCommands = new Set(['wait', 'submit-text', 'submit-image', 'submit-multi-image', 'status', 'models']);
  const { command, jsonStr, taskId: cliTaskId, dryRun, modelsMode } = parseArgs(process.argv.slice(2));

  if (!command || !validCommands.has(command)) {
    printJson({
      ok: false,
      phase: 'failed',
      errorCode: 'USAGE',
      errorMessage:
        'Usage: node video_gen.js <wait|submit-text|submit-image|submit-multi-image|status|models> [--json \'...\'] [--task-id id] [--dry-run] [--mode text_to_video|image_to_video|multi_image_to_video]',
    });
    process.exit(1);
  }

  let params = {};
  if (jsonStr) {
    try {
      params = normalizeParams(JSON.parse(jsonStr));
    } catch (err) {
      printJson({ ok: false, phase: 'failed', errorCode: 'INVALID_JSON', errorMessage: `Invalid JSON: ${err.message}` });
      process.exit(1);
    }
  }

  if (command === 'models') {
    const apiKey = (process.env.WERYAI_API_KEY || '').trim();
    if (!apiKey) {
      printJson({ ok: false, phase: 'failed', errorCode: 'NO_API_KEY', errorMessage: 'Missing WERYAI_API_KEY environment variable.' });
      process.exit(1);
    }
    const result = await cmdModels(modelsMode, apiKey);
    printJson(result);
    process.exit(result.ok ? 0 : 1);
  }

  if (dryRun) {
    const validationErrors = command === 'status' ? [] : validateParams(params);
    if (validationErrors.length > 0) {
      printJson({ ok: false, phase: 'failed', errorCode: 'VALIDATION', errorMessage: validationErrors.join(' ') });
      process.exit(1);
    }

    const mode = detectMode(params);
    const pathMap = {
      text: '/v1/generation/text-to-video',
      image: '/v1/generation/image-to-video',
      multi_image: '/v1/generation/multi-image-to-video',
    };
    printJson({
      ok: true,
      phase: 'dry-run',
      dryRun: true,
      requestMode: mode,
      requestBody: command === 'status' ? {} : buildRequestBody(params, mode),
      requestUrl: BASE_URL + (pathMap[mode] || pathMap.text),
    });
    process.exit(0);
  }

  const apiKey = (process.env.WERYAI_API_KEY || '').trim();
  if (!apiKey) {
    printJson({ ok: false, phase: 'failed', errorCode: 'NO_API_KEY', errorMessage: 'Missing WERYAI_API_KEY environment variable.' });
    process.exit(1);
  }

  let result;
  if (command === 'status') {
    const taskId = cliTaskId || params.task_id || params.taskId;
    if (!taskId) {
      printJson({ ok: false, phase: 'failed', errorCode: 'MISSING_PARAM', errorMessage: 'status requires --task-id <id>.' });
      process.exit(1);
    }
    result = await cmdStatus(taskId, apiKey);
  } else {
    result =
      command === 'wait'
        ? await cmdWait(params, apiKey)
        : await submitTask(params, apiKey, getAllowedModesForCommand(command));
  }

  printJson(result);
  process.exit(result.ok ? 0 : 1);
}

main().catch((err) => {
  printJson({ ok: false, phase: 'failed', errorCode: 'FATAL', errorMessage: err.message || String(err) });
  process.exit(1);
});
