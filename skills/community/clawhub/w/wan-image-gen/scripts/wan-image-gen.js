#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(__dirname, '..', 'config.json');
const DEFAULT_BASE_URL = 'https://dashscope.aliyuncs.com';
const DEFAULT_MODEL = 'wan2.6-t2i';
const DEFAULT_OUTPUT_DIR = path.join(__dirname, '..', 'outputs');
const DEFAULT_POLL_INTERVAL = 10;
const DEFAULT_TIMEOUT = 600;
const SIZE_PRESETS = {
  draft: '1280*1280',
  final: '1440*1440',
  square: '1280*1280',
  portrait: '1104*1472',
  landscape: '1472*1104',
  story: '960*1696',
  widescreen: '1696*960'
};
const RATIO_PRESETS = {
  '1:1': '1280*1280',
  '3:4': '1104*1472',
  '4:3': '1472*1104',
  '9:16': '960*1696',
  '16:9': '1696*960'
};
const IMAGE_PRICING_CNY = {
  'wan2.6-t2i': 0.2,
  'wan2.5-t2i-preview': 0.2,
  'wan2.2-t2i-plus': 0.2,
  'wan2.2-t2i-flash': 0.14,
  'wanx2.1-t2i-plus': 0.2,
  'wanx2.1-t2i-turbo': 0.14,
  'wanx2.0-t2i-turbo': 0.04,
  'wanx-v1': 0.16
};
const IMAGE_TIER_PROFILES = {
  draft: { model: 'wanx2.0-t2i-turbo' },
  standard: { model: 'wan2.2-t2i-flash' },
  final: { model: 'wan2.6-t2i' }
};
const IMAGE_GOAL_PROFILES = {
  cheap: { tier: 'draft', preset: 'draft' },
  balanced: { tier: 'standard' },
  quality: { tier: 'final', preset: 'final' }
};
const DEFAULT_TIER = 'final';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      continue;
    }
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
  node scripts/wan-image-gen.js --prompt="..." [options]
  node scripts/wan-image-gen.js --task-id TASK_ID [options]

Options:
  --prompt              Prompt for a new image task.
  --negative-prompt     Negative prompt.
  --goal                cheap|balanced|quality
  --tier                draft|standard|final
  --model               Default: wan2.6-t2i
  --ratio               1:1|3:4|4:3|9:16|16:9
  --preset              draft|final|square|portrait|landscape|story|widescreen
  --size                Example: 1280*1280
  --n                   Number of images. Default: 1
  --seed                Optional random seed.
  --prompt-extend       true|false. Default: true
  --watermark           true|false. Default: false
  --task-id             Poll an existing task instead of creating one.
  --no-wait             Submit only, do not poll.
  --poll-interval       Seconds between polls. Default: 10
  --timeout             Max wait seconds. Default: 600
  --output-dir          Download directory. Default: outputs/
  --name                Optional output filename prefix.
  --dry-run             Print resolved request and exit.

Examples:
  node scripts/wan-image-gen.js --prompt="一间有着精致窗户的花店" --tier=standard --ratio=3:4
  node scripts/wan-image-gen.js --prompt="赛博朋克夜景" --no-wait
  node scripts/wan-image-gen.js --task-id="0385dc79-xxxx"
`);
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function toBoolean(value, defaultValue = false) {
  if (value === undefined) {
    return defaultValue;
  }
  return ['1', 'true', 'yes', 'on'].includes(String(value).toLowerCase());
}

function toNumber(value, defaultValue) {
  if (value === undefined) {
    return defaultValue;
  }
  const num = Number(value);
  return Number.isFinite(num) ? num : defaultValue;
}

function firstNonEmpty(...values) {
  for (const value of values) {
    if (value === undefined || value === null) {
      continue;
    }
    if (typeof value === 'string' && value.trim() === '') {
      continue;
    }
    return value;
  }
  return undefined;
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    return {};
  }
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const parsed = JSON.parse(raw);
  return parsed && typeof parsed === 'object' ? parsed : {};
}

function sanitizeFilename(input) {
  return String(input).replace(/[^a-zA-Z0-9._-]+/g, '-').replace(/-+/g, '-').replace(/^-+|-+$/g, '');
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

function estimateImageCost(model, n) {
  const unitPrice = IMAGE_PRICING_CNY[model];
  if (unitPrice === undefined) {
    return null;
  }
  return {
    unitPrice,
    totalPrice: unitPrice * n
  };
}

function resolveConfiguredImageTiers(config) {
  if (!config.tiers || typeof config.tiers !== 'object') {
    return IMAGE_TIER_PROFILES;
  }

  const tiers = {};
  for (const [name, profile] of Object.entries(config.tiers)) {
    if (!profile || typeof profile !== 'object' || typeof profile.model !== 'string' || !profile.model.trim()) {
      throw new Error(`config.tiers.${name} 必须包含非空 model`);
    }
    tiers[name] = {
      model: profile.model
    };
  }
  return Object.keys(tiers).length ? tiers : IMAGE_TIER_PROFILES;
}

function resolveConfiguredImageGoals(config, tiers) {
  if (!config.goals || typeof config.goals !== 'object') {
    return IMAGE_GOAL_PROFILES;
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
      preset: profile.preset,
      ratio: profile.ratio
    };
  }
  return Object.keys(goals).length ? goals : IMAGE_GOAL_PROFILES;
}

function resolveImageSelection(args, config) {
  const tiers = resolveConfiguredImageTiers(config);
  const goals = resolveConfiguredImageGoals(config, tiers);
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
    const goalProfile = goals[args.goal];
    if (!goalProfile) {
      throw new Error(`不支持的 --goal: ${args.goal}，可选值为 ${Object.keys(goals).join('|')}`);
    }
    return {
      model: goalProfile.model,
      tier: goalProfile.tier || null,
      goal: args.goal,
      defaults: goalProfile,
      source: 'cli-goal',
      tiers,
      goals
    };
  }

  if (process.env.WAN_IMAGE_MODEL) {
    return { model: process.env.WAN_IMAGE_MODEL, tier: null, goal: null, defaults: null, source: 'env-model', tiers, goals };
  }

  if (configuredDefaultGoal) {
    const goalProfile = goals[configuredDefaultGoal];
    if (!goalProfile) {
      throw new Error(`config.defaultGoal 不支持: ${configuredDefaultGoal}，可选值为 ${Object.keys(goals).join('|')}`);
    }
    return {
      model: goalProfile.model,
      tier: goalProfile.tier || null,
      goal: configuredDefaultGoal,
      defaults: goalProfile,
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
    return { model: profile.model, tier: configuredDefaultTier, goal: null, defaults: profile, source: 'config-tier', tiers, goals };
  }

  if (config.model) {
    return { model: config.model, tier: null, goal: null, defaults: null, source: 'config-model', tiers, goals };
  }

  return {
    model: DEFAULT_MODEL,
    tier: DEFAULT_TIER,
    goal: null,
    defaults: IMAGE_TIER_PROFILES.final,
    source: 'default',
    tiers,
    goals
  };
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

function buildCreateRequest(model, prompt, negativePrompt, size, n, seed, promptExtend, watermark) {
  const isWan26 = model.startsWith('wan2.6');

  if (isWan26) {
    const parameters = {
      prompt_extend: promptExtend,
      watermark,
      n,
      negative_prompt: negativePrompt || '',
      size
    };
    if (seed !== undefined) {
      parameters.seed = seed;
    }

    return {
      endpoint: '/api/v1/services/aigc/image-generation/generation',
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

  const body = {
    model,
    input: {
      prompt
    },
    parameters: {
      size,
      n
    }
  };

  if (negativePrompt) {
    body.input.negative_prompt = negativePrompt;
  }
  if (seed !== undefined) {
    body.parameters.seed = seed;
  }

  return {
    endpoint: '/api/v1/services/aigc/text2image/image-synthesis',
    body
  };
}

function resolveSize(args, config, defaults) {
  if (args.size) {
    return args.size;
  }
  const ratio = firstNonEmpty(args.ratio, defaults && defaults.ratio, config.ratio);
  if (ratio) {
    const resolved = RATIO_PRESETS[ratio];
    if (!resolved) {
      throw new Error(`不支持的 --ratio: ${ratio}，可选值为 ${Object.keys(RATIO_PRESETS).join('|')}`);
    }
    return resolved;
  }
  const preset = firstNonEmpty(args.preset, defaults && defaults.preset, config.preset);
  if (preset) {
    const resolved = SIZE_PRESETS[preset];
    if (!resolved) {
      throw new Error(`不支持的 --preset: ${preset}，可选值为 ${Object.keys(SIZE_PRESETS).join('|')}`);
    }
    return resolved;
  }
  return '1280*1280';
}

function validateInputs({ prompt, size, n, outputDir, taskId }) {
  if (!taskId) {
    if (!prompt || !String(prompt).trim()) {
      throw new Error('提交新任务时，--prompt 不能为空');
    }
    if (String(prompt).trim().length < 4) {
      throw new Error('--prompt 过短，至少应包含更明确的主体、风格或场景描述');
    }
  }

  if (!/^\d+\*\d+$/.test(String(size))) {
    throw new Error(`非法尺寸格式: ${size}，应为 宽*高，例如 1280*1280`);
  }

  const [width, height] = String(size).split('*').map((value) => Number(value));
  const ratio = width / height;
  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
    throw new Error(`非法尺寸格式: ${size}`);
  }

  if (ratio < 0.25 || ratio > 4) {
    throw new Error(`尺寸 ${size} 不符合万相文生图要求：宽高比需在 [1:4, 4:1] 之间`);
  }

  if (!Number.isInteger(n) || n < 1) {
    throw new Error(`非法 n: ${n}`);
  }

  ensureDir(outputDir);
}

function printPreflight({ model, tier, goal, selectionSource, selectionNote, size, n, prompt, outputDir, noWait, taskId }) {
  const mode = taskId ? 'poll-existing-task' : 'create-task';
  console.error(`preflight mode=${mode}`);
  console.error(`preflight model=${model}`);
  console.error(`preflight selection_source=${selectionSource}${goal ? ` goal=${goal}` : ''}${tier ? ` tier=${tier}` : ''}`);
  if (selectionNote) {
    console.error(`preflight note=${selectionNote}`);
  }
  if (!taskId) {
    console.error(`preflight size=${size} n=${n} no_wait=${noWait}`);
    console.error(`preflight prompt=${prompt}`);
  } else {
    console.error(`preflight task_id=${taskId}`);
  }
  console.error(`preflight output_dir=${outputDir}`);

  if (!taskId) {
    const estimated = estimateImageCost(model, n);
    if (estimated) {
      console.error(
        `cost_estimate region=中国内地 unit=${formatCny(estimated.unitPrice)}/张 total=${formatCny(estimated.totalPrice)}`
      );
    } else {
      console.error('cost_estimate region=中国内地 unavailable=未内置该模型价格');
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

function extractImageUrls(status) {
  const urls = [];
  const output = status && status.output ? status.output : {};

  if (Array.isArray(output.results)) {
    output.results.forEach((item) => {
      if (item && item.url) {
        urls.push(item.url);
      }
    });
  }

  if (Array.isArray(output.choices)) {
    output.choices.forEach((choice) => {
      const content = choice && choice.message && Array.isArray(choice.message.content)
        ? choice.message.content
        : [];
      content.forEach((item) => {
        if (item && item.image) {
          urls.push(item.image);
        }
      });
    });
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
    const url = urls[i];
    const filename = `${prefix}-${String(i + 1).padStart(2, '0')}.png`;
    const filePath = path.join(outputDir, filename);
    await downloadFile(url, filePath);
    saved.push(filePath);
  }

  return saved;
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

  const baseUrl = String(
    firstNonEmpty(process.env.DASHSCOPE_BASE_URL, config.baseUrl, DEFAULT_BASE_URL)
  ).replace(/\/$/, '');
  const selection = resolveImageSelection(args, config);
  const model = selection.model;
  const selectionNote =
    config.model && firstNonEmpty(config.defaultGoal, config.goal, config.defaultTier, config.tier)
      ? 'config 同时包含 model 与 goal/tier 默认项，当前优先使用 goal/tier'
      : '';
  const outputDirInput = firstNonEmpty(args['output-dir'], config.outputDir, DEFAULT_OUTPUT_DIR);
  const outputDir = path.isAbsolute(outputDirInput)
    ? outputDirInput
    : path.resolve(path.join(__dirname, '..'), outputDirInput);

  const pollIntervalSec = Math.max(1, Math.trunc(toNumber(args['poll-interval'], DEFAULT_POLL_INTERVAL)));
  const timeoutSec = Math.max(5, Math.trunc(toNumber(args.timeout, DEFAULT_TIMEOUT)));
  const taskId = args['task-id'];
  const size = resolveSize(args, config, selection.defaults);
  const n = Math.max(1, Math.trunc(toNumber(args.n, 1)));
  const noWait = toBoolean(args['no-wait'], false);

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
    taskId
  });

  printPreflight({
    model,
    tier: selection.tier,
    goal: selection.goal,
    selectionSource: selection.source,
    selectionNote,
    size,
    n,
    prompt: args.prompt || '',
    outputDir,
    noWait,
    taskId
  });

  let createdTaskId = taskId;
  if (!createdTaskId) {
    const request = buildCreateRequest(
      model,
      args.prompt,
      args['negative-prompt'],
      size,
      n,
      args.seed !== undefined ? Math.trunc(toNumber(args.seed, 0)) : undefined,
      toBoolean(args['prompt-extend'], true),
      toBoolean(args.watermark, false)
    );

    if (dryRun) {
      console.log(JSON.stringify({
        baseUrl,
        endpoint: request.endpoint,
        body: request.body
      }, null, 2));
      return;
    }

    const created = await createTask(baseUrl, apiKey, request);
    createdTaskId = created.output.task_id;
    console.log(`task_id=${createdTaskId}`);
    console.error(`submitted model=${model}`);

    if (noWait) {
      return;
    }
  }

  const status = await waitForTask(baseUrl, apiKey, createdTaskId, pollIntervalSec, timeoutSec);
  const output = status && status.output ? status.output : {};

  if (output.task_status !== 'SUCCEEDED') {
    throw new Error(`任务未成功结束: ${JSON.stringify(output)}`);
  }

  const urls = extractImageUrls(status);
  if (!urls.length) {
    throw new Error(`任务成功但未找到图片 URL: ${JSON.stringify(status)}`);
  }

  const namePrefix = firstNonEmpty(args.name, config.name);
  const prefixParts = [
    createTimestamp(),
    sanitizeFilename(createdTaskId),
    sanitizeFilename(firstNonEmpty(namePrefix, promptSlug(args.prompt || 'image')))
  ].filter(Boolean);
  const saved = await downloadImages(urls, outputDir, prefixParts.join('-'));
  saved.forEach((filePath) => console.log(filePath));
}

main().catch((error) => {
  console.error(`错误: ${error.message}`);
  process.exit(1);
});
