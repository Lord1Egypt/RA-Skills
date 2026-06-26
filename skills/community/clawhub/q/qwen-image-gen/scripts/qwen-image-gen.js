#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(__dirname, '..', 'config.json');
const DEFAULT_BASE_URL = 'https://dashscope.aliyuncs.com';
const DEFAULT_MODEL = 'qwen-image-2.0-pro';
const DEFAULT_OUTPUT_DIR = path.join(__dirname, '..', 'outputs');
const DEFAULT_POLL_INTERVAL = 10;
const DEFAULT_TIMEOUT = 600;
const DEFAULT_TIER_PROFILES = {
  draft: { model: 'qwen-image-2.0', mode: 'sync', size: '2048*2048' },
  standard: { model: 'qwen-image-max', mode: 'sync', size: '1664*928' },
  final: { model: 'qwen-image-2.0-pro', mode: 'sync', size: '2048*2048' }
};
const DEFAULT_GOAL_PROFILES = {
  cheap: { tier: 'draft', size: '2048*2048' },
  balanced: { tier: 'standard', size: '1664*928' },
  quality: { tier: 'final', size: '2048*2048' }
};
const RATIO_MAPS = {
  'qwen-image-2.0': {
    '1:1': '2048*2048',
    '3:4': '1728*2368',
    '4:3': '2368*1728',
    '9:16': '1536*2688',
    '16:9': '2688*1536'
  },
  fixed: {
    '1:1': '1328*1328',
    '3:4': '1104*1472',
    '4:3': '1472*1104',
    '9:16': '928*1664',
    '16:9': '1664*928'
  }
};
const IMAGE_PRICING_CNY = {
  mainland: {
    'qwen-image-2.0-pro': 0.5,
    'qwen-image-2.0': 0.2,
    'qwen-image-max': 0.5,
    'qwen-image-plus': 0.2,
    'qwen-image': 0.25
  },
  intl: {
    'qwen-image-2.0-pro': 0.550443,
    'qwen-image-2.0': 0.256873,
    'qwen-image-max': 0.550443,
    'qwen-image-plus': 0.220177,
    'qwen-image': 0.256873
  }
};

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;

    const body = token.slice(2);
    const eqIndex = body.indexOf('=');
    let key;
    let value;

    if (eqIndex >= 0) {
      key = body.slice(0, eqIndex);
      value = body.slice(eqIndex + 1);
    } else {
      key = body;
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        value = next;
        i += 1;
      } else {
        value = 'true';
      }
    }

    if (args[key] === undefined) {
      args[key] = value;
    } else if (Array.isArray(args[key])) {
      args[key].push(value);
    } else {
      args[key] = [args[key], value];
    }
  }
  return args;
}

function printUsage() {
  console.log(`
Usage:
  node scripts/qwen-image-gen.js --prompt="..." [options]
  node scripts/qwen-image-gen.js --task-id TASK_ID [options]

Options:
  --prompt              Prompt for a new image task.
  --negative-prompt     Negative prompt.
  --goal                cheap|balanced|quality
  --tier                draft|standard|final
  --model               Default: qwen-image-2.0-pro
  --mode                auto|sync|async
  --ratio               1:1|3:4|4:3|9:16|16:9
  --size                Example: 2048*2048
  --n                   Number of images.
  --seed                Optional random seed.
  --prompt-extend       true|false. Default: true
  --watermark           true|false. Default: false
  --task-id             Poll an existing async task instead of creating one.
  --no-wait             Submit only, do not poll async tasks.
  --poll-interval       Seconds between polls. Default: 10
  --timeout             Max wait seconds. Default: 600
  --output-dir          Download directory. Default: outputs/
  --name                Optional output filename prefix.
  --dry-run             Print resolved request and exit.

Examples:
  node scripts/qwen-image-gen.js --prompt="一间花店" --goal=quality
  node scripts/qwen-image-gen.js --prompt="赛博朋克夜景" --model=qwen-image-plus --mode=async
  node scripts/qwen-image-gen.js --task-id="0385dc79-xxxx"
`);
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function toBoolean(value, defaultValue = false) {
  if (value === undefined) return defaultValue;
  return ['1', 'true', 'yes', 'on'].includes(String(value).toLowerCase());
}

function toNumber(value, defaultValue) {
  if (value === undefined) return defaultValue;
  const num = Number(value);
  return Number.isFinite(num) ? num : defaultValue;
}

function firstNonEmpty(...values) {
  for (const value of values) {
    if (value === undefined || value === null) continue;
    if (typeof value === 'string' && value.trim() === '') continue;
    return value;
  }
  return undefined;
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) return {};
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const parsed = JSON.parse(raw);
  return parsed && typeof parsed === 'object' ? parsed : {};
}

function sanitizeFilename(input) {
  return String(input)
    .replace(/[^a-zA-Z0-9._-]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function createTimestamp() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

function promptSlug(prompt) {
  const slug = sanitizeFilename(String(prompt).slice(0, 40));
  return slug || 'image';
}

function formatCny(value) {
  return `${value.toFixed(2)} 元`;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function requestJson(url, options) {
  const response = await fetch(url, options);
  const text = await response.text();
  let parsed = {};

  try {
    parsed = text ? JSON.parse(text) : {};
  } catch (_) {
    parsed = { raw: text };
  }

  if (!response.ok) {
    throw new Error(`请求失败: ${response.status} ${response.statusText}\n${text}`);
  }

  return parsed;
}

function isSyncModel(model) {
  return model.startsWith('qwen-image-2.0-pro') || model.startsWith('qwen-image-2.0') || model.startsWith('qwen-image-max');
}

function isAsyncModel(model) {
  return model.startsWith('qwen-image-plus') || model === 'qwen-image';
}

function modelFamily(model) {
  if (model.startsWith('qwen-image-2.0-pro')) return 'qwen-image-2.0';
  if (model.startsWith('qwen-image-2.0')) return 'qwen-image-2.0';
  if (model.startsWith('qwen-image-max')) return 'qwen-image-max';
  if (model.startsWith('qwen-image-plus') || model === 'qwen-image') return 'qwen-image-plus';
  return 'custom';
}

function pricingKey(model) {
  if (model.startsWith('qwen-image-2.0-pro')) return 'qwen-image-2.0-pro';
  if (model.startsWith('qwen-image-2.0')) return 'qwen-image-2.0';
  if (model.startsWith('qwen-image-max')) return 'qwen-image-max';
  if (model.startsWith('qwen-image-plus')) return 'qwen-image-plus';
  if (model === 'qwen-image') return 'qwen-image';
  return null;
}

function resolveConfiguredTiers(config) {
  if (!config.tiers || typeof config.tiers !== 'object') {
    return DEFAULT_TIER_PROFILES;
  }

  const tiers = {};
  for (const [name, profile] of Object.entries(config.tiers)) {
    if (!profile || typeof profile !== 'object' || typeof profile.model !== 'string' || !profile.model.trim()) {
      throw new Error(`config.tiers.${name} 必须包含非空 model`);
    }
    tiers[name] = {
      model: profile.model,
      mode: profile.mode,
      size: profile.size,
      ratio: profile.ratio
    };
  }

  return Object.keys(tiers).length ? tiers : DEFAULT_TIER_PROFILES;
}

function resolveConfiguredGoals(config, tiers) {
  if (!config.goals || typeof config.goals !== 'object') {
    return DEFAULT_GOAL_PROFILES;
  }

  const goals = {};
  for (const [name, profile] of Object.entries(config.goals)) {
    if (!profile || typeof profile !== 'object') {
      throw new Error(`config.goals.${name} 必须是对象`);
    }
    if (!profile.model && !profile.tier) {
      throw new Error(`config.goals.${name} 必须至少包含 model 或 tier`);
    }
    if (profile.tier && !tiers[profile.tier]) {
      throw new Error(`config.goals.${name}.tier 不支持: ${profile.tier}`);
    }
    goals[name] = {
      tier: profile.tier,
      model: profile.model || (profile.tier ? tiers[profile.tier].model : undefined),
      mode: profile.mode || (profile.tier ? tiers[profile.tier].mode : undefined),
      size: profile.size || (profile.tier ? tiers[profile.tier].size : undefined),
      ratio: profile.ratio || (profile.tier ? tiers[profile.tier].ratio : undefined)
    };
  }

  return Object.keys(goals).length ? goals : DEFAULT_GOAL_PROFILES;
}

function resolveProfileModel(profile, tiers) {
  if (!profile) return undefined;
  if (profile.model) return profile.model;
  if (profile.tier && tiers[profile.tier]) return tiers[profile.tier].model;
  return undefined;
}

function resolveSelection(args, config) {
  const tiers = resolveConfiguredTiers(config);
  const goals = resolveConfiguredGoals(config, tiers);
  const configuredDefaultGoal = firstNonEmpty(config.defaultGoal, config.goal);
  const configuredDefaultTier = firstNonEmpty(config.defaultTier, config.tier);

  if (args.model) {
    return { model: args.model, tier: null, goal: null, defaults: null, source: 'cli-model', tiers, goals };
  }

  if (args.tier) {
    const profile = tiers[args.tier];
    if (!profile) {
      throw new Error(`不支持的 --tier: ${args.tier}，可选值为 ${Object.keys(tiers).join('|')}`);
    }
    return { model: profile.model, tier: args.tier, goal: null, defaults: profile, source: 'cli-tier', tiers, goals };
  }

  if (args.goal) {
    const profile = goals[args.goal];
    if (!profile) {
      throw new Error(`不支持的 --goal: ${args.goal}，可选值为 ${Object.keys(goals).join('|')}`);
    }
    return {
      model: resolveProfileModel(profile, tiers),
      tier: profile.tier || null,
      goal: args.goal,
      defaults: profile,
      source: 'cli-goal',
      tiers,
      goals
    };
  }

  if (process.env.QWEN_IMAGE_MODEL) {
    return { model: process.env.QWEN_IMAGE_MODEL, tier: null, goal: null, defaults: null, source: 'env-model', tiers, goals };
  }

  if (configuredDefaultGoal) {
    const profile = goals[configuredDefaultGoal];
    if (!profile) {
      throw new Error(`config.defaultGoal 不支持: ${configuredDefaultGoal}，可选值为 ${Object.keys(goals).join('|')}`);
    }
    return {
      model: resolveProfileModel(profile, tiers),
      tier: profile.tier || null,
      goal: configuredDefaultGoal,
      defaults: profile,
      source: 'config-goal',
      tiers,
      goals
    };
  }

  if (configuredDefaultTier) {
    const profile = tiers[configuredDefaultTier];
    if (!profile) {
      throw new Error(`config.defaultTier 不支持: ${configuredDefaultTier}，可选值为 ${Object.keys(tiers).join('|')}`);
    }
    return {
      model: profile.model,
      tier: configuredDefaultTier,
      goal: null,
      defaults: profile,
      source: 'config-tier',
      tiers,
      goals
    };
  }

  if (config.model) {
    return { model: config.model, tier: null, goal: null, defaults: null, source: 'config-model', tiers, goals };
  }

  return {
    model: DEFAULT_MODEL,
    tier: 'final',
    goal: null,
    defaults: DEFAULT_TIER_PROFILES.final,
    source: 'default',
    tiers,
    goals
  };
}

function resolveMode(model, args, config, defaults) {
  const modeHint = firstNonEmpty(args.mode, defaults && defaults.mode, config.defaultMode, 'auto');
  if (modeHint === 'auto') {
    return isAsyncModel(model) ? 'async' : 'sync';
  }
  if (!['sync', 'async'].includes(modeHint)) {
    throw new Error(`不支持的 --mode: ${modeHint}，可选值为 auto|sync|async`);
  }
  if (modeHint === 'async' && !isAsyncModel(model)) {
    throw new Error(`模型 ${model} 不支持异步接口`);
  }
  if (modeHint === 'sync' && !isSyncModel(model) && !isAsyncModel(model)) {
    return 'sync';
  }
  if (modeHint === 'sync' && isAsyncModel(model)) {
    throw new Error(`模型 ${model} 仅支持异步接口`);
  }
  return modeHint;
}

function defaultSizeForModel(model) {
  return modelFamily(model) === 'qwen-image-2.0' ? '2048*2048' : '1664*928';
}

function resolveSize(args, config, defaults, model) {
  if (args.size) return args.size;

  const ratio = firstNonEmpty(args.ratio, defaults && defaults.ratio, config.ratio);
  if (ratio) {
    const family = modelFamily(model);
    const map = family === 'qwen-image-2.0' ? RATIO_MAPS['qwen-image-2.0'] : RATIO_MAPS.fixed;
    const resolved = map[ratio];
    if (!resolved) {
      throw new Error(`不支持的 --ratio: ${ratio}，可选值为 ${Object.keys(map).join('|')}`);
    }
    return resolved;
  }

  const size = firstNonEmpty(defaults && defaults.size, config.size);
  if (size) return size;

  return defaultSizeForModel(model);
}

function parseSize(size) {
  const match = /^(\d+)\*(\d+)$/.exec(String(size));
  if (!match) return null;
  const width = Number(match[1]);
  const height = Number(match[2]);
  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) return null;
  return { width, height, pixels: width * height };
}

function validateInputs({ prompt, size, n, outputDir, taskId, model, mode }) {
  const family = modelFamily(model);

  if (!taskId) {
    if (!prompt || !String(prompt).trim()) {
      throw new Error('提交新任务时，--prompt 不能为空');
    }
    const trimmedPrompt = String(prompt).trim();
    if (trimmedPrompt.length < 4) {
      throw new Error('--prompt 过短，至少应包含更明确的主体、风格或场景描述');
    }
    if (trimmedPrompt.length > 800) {
      throw new Error('--prompt 超过 800 字符限制');
    }
  }

  if (!taskId) {
    const parsedSize = parseSize(size);
    if (!parsedSize) {
      throw new Error(`非法尺寸格式: ${size}，应为 宽*高，例如 2048*2048`);
    }

    if (family === 'qwen-image-2.0') {
      const minPixels = 512 * 512;
      const maxPixels = 2048 * 2048;
      if (parsedSize.pixels < minPixels || parsedSize.pixels > maxPixels) {
        throw new Error(`尺寸 ${size} 不符合 qwen-image-2.0 系列要求：总像素需在 ${minPixels} 到 ${maxPixels} 之间`);
      }
    } else if (family === 'qwen-image-max' || family === 'qwen-image-plus') {
      const allowed = new Set(Object.values(RATIO_MAPS.fixed));
      if (!allowed.has(size)) {
        throw new Error(`尺寸 ${size} 不符合 ${family} 要求，可选值为 ${Array.from(allowed).join('|')}`);
      }
    }

    if (!Number.isInteger(n) || n < 1) {
      throw new Error(`非法 n: ${n}`);
    }

    if (family === 'qwen-image-2.0' && n > 6) {
      throw new Error(`模型 ${model} 最多支持 6 张`);
    }
    if ((family === 'qwen-image-max' || family === 'qwen-image-plus') && n !== 1) {
      throw new Error(`模型 ${model} 的 n 固定为 1`);
    }

    if (mode === 'async' && !isAsyncModel(model)) {
      throw new Error(`模型 ${model} 不支持异步模式`);
    }
  }

  ensureDir(outputDir);
}

function estimateImageCost(model, n, region) {
  const key = pricingKey(model);
  if (!key) return null;
  const table = IMAGE_PRICING_CNY[region] || IMAGE_PRICING_CNY.mainland;
  const unitPrice = table[key];
  if (unitPrice === undefined) return null;
  return { unitPrice, totalPrice: unitPrice * n };
}

function printPreflight({ model, tier, goal, mode, selectionSource, selectionNote, size, n, prompt, outputDir, noWait, taskId, baseUrl, region }) {
  const action = taskId ? 'poll-existing-task' : mode === 'sync' ? 'sync-generate' : 'create-task';
  console.error(`preflight mode=${action}`);
  console.error(`preflight model=${model}`);
  console.error(`preflight selection_source=${selectionSource}${goal ? ` goal=${goal}` : ''}${tier ? ` tier=${tier}` : ''}`);
  console.error(`preflight interface_mode=${mode}`);
  if (selectionNote) console.error(`preflight note=${selectionNote}`);
  if (!taskId) {
    console.error(`preflight size=${size} n=${n} no_wait=${noWait}`);
    console.error(`preflight prompt=${prompt}`);
  } else {
    console.error(`preflight task_id=${taskId}`);
  }
  console.error(`preflight output_dir=${outputDir}`);
  console.error(`preflight base_url=${baseUrl}`);

  if (!taskId) {
    const estimated = estimateImageCost(model, n, region);
    if (estimated) {
      console.error(
        `cost_estimate region=${region} unit=${formatCny(estimated.unitPrice)}/张 total=${formatCny(estimated.totalPrice)}`
      );
    } else {
      console.error(`cost_estimate region=${region} unavailable=未内置该模型价格`);
    }
  }
}

async function createTask(baseUrl, apiKey, request) {
  const result = await requestJson(`${baseUrl}${request.endpoint}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'X-DashScope-Async': 'enable'
    },
    body: JSON.stringify(request.body)
  });

  const taskId = result && result.output && result.output.task_id;
  if (!taskId) {
    throw new Error(`创建任务失败，响应中缺少 task_id: ${JSON.stringify(result)}`);
  }
  return result;
}

async function fetchTask(baseUrl, apiKey, taskId) {
  return requestJson(`${baseUrl}/api/v1/tasks/${encodeURIComponent(taskId)}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${apiKey}`
    }
  });
}

async function callSyncGeneration(baseUrl, apiKey, request) {
  return requestJson(`${baseUrl}${request.endpoint}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(request.body)
  });
}

function extractImageUrls(payload) {
  const urls = [];
  const output = payload && payload.output ? payload.output : {};

  if (Array.isArray(output.results)) {
    for (const item of output.results) {
      if (item && item.url) urls.push(item.url);
    }
  }

  if (Array.isArray(output.choices)) {
    for (const choice of output.choices) {
      const content = choice && choice.message && Array.isArray(choice.message.content) ? choice.message.content : [];
      for (const item of content) {
        if (item && item.image) urls.push(item.image);
      }
    }
  }

  return [...new Set(urls)];
}

async function waitForTask(baseUrl, apiKey, taskId, pollIntervalSec, timeoutSec) {
  const startedAt = Date.now();

  while (true) {
    const status = await fetchTask(baseUrl, apiKey, taskId);
    const output = status && status.output ? status.output : {};
    const taskStatus = output.task_status || 'UNKNOWN';
    console.error(`task=${taskId} status=${taskStatus}`);

    if (['SUCCEEDED', 'FAILED', 'CANCELED', 'UNKNOWN'].includes(taskStatus)) {
      return status;
    }

    if (Date.now() - startedAt > timeoutSec * 1000) {
      throw new Error(`等待任务超时: ${taskId}`);
    }

    await sleep(pollIntervalSec * 1000);
  }
}

async function downloadFile(url, filePath) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`下载失败: ${response.status} ${response.statusText}`);
  }
  const arrayBuffer = await response.arrayBuffer();
  fs.writeFileSync(filePath, Buffer.from(arrayBuffer));
}

async function downloadImages(urls, outputDir, prefix) {
  ensureDir(outputDir);
  const saved = [];

  for (let i = 0; i < urls.length; i += 1) {
    const filename = `${prefix}-${String(i + 1).padStart(2, '0')}.png`;
    const filePath = path.join(outputDir, filename);
    await downloadFile(urls[i], filePath);
    saved.push(filePath);
  }

  return saved;
}

function buildSyncRequest(model, prompt, negativePrompt, size, n, seed, promptExtend, watermark) {
  const parameters = {
    prompt_extend: promptExtend,
    watermark,
    size,
    negative_prompt: negativePrompt || ''
  };
  if (n !== undefined) parameters.n = n;
  if (seed !== undefined) parameters.seed = seed;

  return {
    endpoint: '/api/v1/services/aigc/multimodal-generation/generation',
    body: {
      model,
      input: {
        messages: [
          {
            role: 'user',
            content: [{ text: prompt }]
          }
        ]
      },
      parameters
    }
  };
}

function buildAsyncRequest(model, prompt, negativePrompt, size, n, seed, promptExtend, watermark) {
  const parameters = {
    prompt_extend: promptExtend,
    watermark,
    size,
    negative_prompt: negativePrompt || ''
  };
  if (n !== undefined) parameters.n = n;
  if (seed !== undefined) parameters.seed = seed;

  return {
    endpoint: '/api/v1/services/aigc/text2image/image-synthesis',
    body: {
      model,
      input: {
        prompt
      },
      parameters
    }
  };
}

function buildRequest(mode, model, prompt, negativePrompt, size, n, seed, promptExtend, watermark) {
  return mode === 'async'
    ? buildAsyncRequest(model, prompt, negativePrompt, size, n, seed, promptExtend, watermark)
    : buildSyncRequest(model, prompt, negativePrompt, size, n, seed, promptExtend, watermark);
}

function regionFromBaseUrl(baseUrl) {
  return baseUrl.includes('dashscope-intl') ? 'intl' : 'mainland';
}

function makeOutputPrefix({ name, taskId, model, prompt }) {
  const parts = [createTimestamp(), sanitizeFilename(model)];
  if (taskId) parts.push(sanitizeFilename(taskId));
  parts.push(name ? sanitizeFilename(name) : promptSlug(prompt));
  return parts.filter(Boolean).join('-');
}

async function main() {
  if (typeof fetch !== 'function') {
    throw new Error('当前 Node.js 不支持全局 fetch，请升级到 Node.js 18 或更高版本');
  }

  const args = parseArgs(process.argv.slice(2));
  if (args.help || args.h) {
    printUsage();
    return;
  }

  const config = loadConfig();
  const dryRun = toBoolean(args['dry-run'], false);
  const apiKey = firstNonEmpty(process.env.DASHSCOPE_API_KEY, config.apiKey);
  const baseUrl = String(firstNonEmpty(process.env.DASHSCOPE_BASE_URL, config.baseUrl, DEFAULT_BASE_URL)).replace(/\/$/, '');
  const selection = resolveSelection(args, config);
  const resolvedMode = resolveMode(selection.model, args, config, selection.defaults);
  const outputDirInput = firstNonEmpty(args['output-dir'], config.outputDir, DEFAULT_OUTPUT_DIR);
  const outputDir = path.isAbsolute(outputDirInput)
    ? outputDirInput
    : path.resolve(path.join(__dirname, '..'), outputDirInput);
  const pollIntervalSec = Math.max(1, Math.trunc(toNumber(args['poll-interval'], DEFAULT_POLL_INTERVAL)));
  const timeoutSec = Math.max(5, Math.trunc(toNumber(args.timeout, DEFAULT_TIMEOUT)));
  const taskId = args['task-id'];
  const mode = taskId ? 'async' : resolvedMode;
  const size = resolveSize(args, config, selection.defaults, selection.model);
  const n = Math.max(1, Math.trunc(toNumber(args.n, 1)));
  const noWait = toBoolean(args['no-wait'], false);
  const promptExtend = toBoolean(args['prompt-extend'], true);
  const watermark = toBoolean(args.watermark, false);
  const seed = args.seed !== undefined ? Number(args.seed) : undefined;
  if (seed !== undefined && !Number.isFinite(seed)) {
    throw new Error(`非法 seed: ${args.seed}`);
  }

  if (taskId && args.mode === 'sync') {
    throw new Error('--task-id 只能用于异步任务模式');
  }
  if (!taskId && !args.prompt) {
    printUsage();
    throw new Error('提交新任务需要 --prompt，或使用 --task-id 查询已有任务');
  }
  if (!apiKey && !dryRun) {
    throw new Error(`缺少 DASHSCOPE_API_KEY。请设置环境变量，或在 ${CONFIG_PATH} 中配置 apiKey`);
  }

  validateInputs({
    prompt: args.prompt,
    size,
    n,
    outputDir,
    taskId,
    model: selection.model,
    mode
  });

  const selectionNote =
    config.model && firstNonEmpty(config.defaultGoal, config.goal, config.defaultTier, config.tier)
      ? 'config 同时包含 model 与 goal/tier 默认项，当前优先使用 goal/tier'
      : '';

  printPreflight({
    model: selection.model,
    tier: selection.tier,
    goal: selection.goal,
    mode,
    selectionSource: selection.source,
    selectionNote,
    size,
    n,
    prompt: args.prompt || '',
    outputDir,
    noWait,
    taskId,
    baseUrl,
    region: regionFromBaseUrl(baseUrl)
  });

  if (dryRun) {
    return;
  }

  const region = regionFromBaseUrl(baseUrl);
  if (!taskId) {
    const request = buildRequest(
      mode,
      selection.model,
      args.prompt,
      args['negative-prompt'],
      size,
      n,
      seed,
      promptExtend,
      watermark
    );

    if (mode === 'sync') {
      const result = await callSyncGeneration(baseUrl, apiKey, request);
      const urls = extractImageUrls(result);
      if (!urls.length) {
        throw new Error(`同步调用成功但未找到图像链接: ${JSON.stringify(result)}`);
      }
      const prefix = makeOutputPrefix({
        name: args.name,
        model: selection.model,
        prompt: args.prompt
      });
      const saved = await downloadImages(urls, outputDir, prefix);
      console.log(saved.join('\n'));
      return;
    }

    const created = await createTask(baseUrl, apiKey, request);
    const createdTaskId = created.output.task_id;
    console.error(`task_id=${createdTaskId}`);
    if (noWait) {
      console.log(createdTaskId);
      return;
    }

    const status = await waitForTask(baseUrl, apiKey, createdTaskId, pollIntervalSec, timeoutSec);
    const finalStatus = status && status.output ? status.output.task_status : 'UNKNOWN';
    if (finalStatus !== 'SUCCEEDED') {
      throw new Error(`任务未成功结束: ${createdTaskId} status=${finalStatus}`);
    }
    const urls = extractImageUrls(status);
    if (!urls.length) {
      throw new Error(`任务成功但未找到图像链接: ${JSON.stringify(status)}`);
    }
    const prefix = makeOutputPrefix({
      name: args.name,
      taskId: createdTaskId,
      model: selection.model,
      prompt: args.prompt
    });
    const saved = await downloadImages(urls, outputDir, prefix);
    console.log(saved.join('\n'));
    return;
  }

  const status = await waitForTask(baseUrl, apiKey, taskId, pollIntervalSec, timeoutSec);
  const finalStatus = status && status.output ? status.output.task_status : 'UNKNOWN';
  if (finalStatus !== 'SUCCEEDED') {
    throw new Error(`任务未成功结束: ${taskId} status=${finalStatus}`);
  }
  const urls = extractImageUrls(status);
  if (!urls.length) {
    throw new Error(`任务成功但未找到图像链接: ${JSON.stringify(status)}`);
  }
  const prefix = makeOutputPrefix({
    name: args.name,
    taskId,
    model: selection.model,
    prompt: args.name || taskId
  });
  const saved = await downloadImages(urls, outputDir, prefix);
  console.log(saved.join('\n'));
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exitCode = 1;
});
