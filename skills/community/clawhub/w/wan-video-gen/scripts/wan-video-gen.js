#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(__dirname, '..', 'config.json');
const DEFAULT_BASE_URL = 'https://dashscope.aliyuncs.com';
const DEFAULT_MODEL = 'wan2.6-t2v';
const DEFAULT_OUTPUT_DIR = path.join(__dirname, '..', 'outputs');
const DEFAULT_POLL_INTERVAL = 15;
const DEFAULT_TIMEOUT = 1800;
const VIDEO_SIZE_PRESETS = {
  '480p': {
    '16:9': '832*480',
    '9:16': '480*832',
    '1:1': '624*624'
  },
  '720p': {
    '16:9': '1280*720',
    '9:16': '720*1280',
    '1:1': '960*960',
    '4:3': '1088*832',
    '3:4': '832*1088'
  },
  '1080p': {
    '16:9': '1920*1080',
    '9:16': '1080*1920',
    '1:1': '1440*1440',
    '4:3': '1632*1248',
    '3:4': '1248*1632'
  }
};
const MODEL_SIZE_RULES = {
  'wan2.6-t2v': { defaultQuality: '1080p', qualities: ['720p', '1080p'] },
  'wan2.6-t2v-us': { defaultQuality: '1080p', qualities: ['720p', '1080p'] },
  'wan2.5-t2v-preview': { defaultQuality: '1080p', qualities: ['480p', '720p', '1080p'] },
  'wan2.2-t2v-plus': { defaultQuality: '1080p', qualities: ['480p', '1080p'] },
  'wanx2.1-t2v-turbo': { defaultQuality: '720p', qualities: ['480p', '720p'] },
  'wanx2.1-t2v-plus': { defaultQuality: '720p', qualities: ['720p'] }
};
const MODEL_DURATION_RULES = {
  'wan2.6-t2v': { type: 'range', min: 2, max: 15, defaultValue: 5 },
  'wan2.6-t2v-us': { type: 'enum', values: [5, 10], defaultValue: 5 },
  'wan2.5-t2v-preview': { type: 'enum', values: [5, 10], defaultValue: 5 },
  'wan2.2-t2v-plus': { type: 'fixed', value: 5, defaultValue: 5 },
  'wanx2.1-t2v-plus': { type: 'fixed', value: 5, defaultValue: 5 },
  'wanx2.1-t2v-turbo': { type: 'fixed', value: 5, defaultValue: 5 }
};
const VIDEO_PRICING_CNY_PER_SEC = {
  'wan2.6-t2v': { '720p': 0.6, '1080p': 1.0 },
  'wan2.5-t2v-preview': { '480p': 0.3, '720p': 0.6, '1080p': 1.0 },
  'wan2.2-t2v-plus': { '480p': 0.14, '1080p': 0.7 },
  'wanx2.1-t2v-turbo': { '480p': 0.24, '720p': 0.24 },
  'wanx2.1-t2v-plus': { '720p': 0.7 }
};
const VIDEO_TIER_PROFILES = {
  draft: { model: 'wan2.2-t2v-plus', quality: '480p', ratio: '16:9', duration: 5 },
  standard: { model: 'wan2.5-t2v-preview', quality: '720p', ratio: '16:9', duration: 5 },
  final: { model: 'wan2.6-t2v', quality: '1080p', ratio: '16:9', duration: 5 }
};
const VIDEO_GOAL_PROFILES = {
  cheap: { tier: 'draft' },
  balanced: { tier: 'standard' },
  quality: { tier: 'final' }
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
  node scripts/wan-video-gen.js --prompt="..." [options]
  node scripts/wan-video-gen.js --task-id TASK_ID [options]

Options:
  --prompt              Prompt for a new video task.
  --negative-prompt     Negative prompt.
  --audio-url           Optional audio URL for wan2.6/wan2.5.
  --goal                cheap|balanced|quality
  --tier                draft|standard|final
  --model               Default: wan2.6-t2v
  --quality             480p|720p|1080p
  --ratio               16:9|9:16|1:1|4:3|3:4
  --size                Example: 1280*720
  --duration            Duration seconds. Default: 5
  --prompt-extend       true|false. Default: true
  --shot-type           single|multi
  --seed                Optional random seed.
  --task-id             Poll an existing task instead of creating one.
  --no-wait             Submit only, do not poll.
  --dry-run             Print resolved request and exit.
  --poll-interval       Seconds between polls. Default: 15
  --timeout             Max wait seconds. Default: 1800
  --output-dir          Download directory. Default: outputs/

Examples:
  node scripts/wan-video-gen.js --prompt="一只小猫在月光下奔跑" --tier=standard
  node scripts/wan-video-gen.js --prompt="复古地铁站街头音乐家" --no-wait
  node scripts/wan-video-gen.js --task-id="966cebcd-xxxx"
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
  return String(input).replace(/[^a-zA-Z0-9._-]+/g, '-');
}

function formatCny(value) {
  return `${value.toFixed(2)} 元`;
}

function qualityForSize(size) {
  for (const [quality, presets] of Object.entries(VIDEO_SIZE_PRESETS)) {
    if (Object.values(presets).includes(size)) {
      return quality;
    }
  }
  return null;
}

function estimateVideoCost(model, size, duration) {
  const quality = qualityForSize(size);
  if (!quality) {
    return null;
  }

  const pricingMap = VIDEO_PRICING_CNY_PER_SEC[model];
  if (!pricingMap || pricingMap[quality] === undefined) {
    return null;
  }

  const unitPrice = pricingMap[quality];
  return {
    quality,
    unitPrice,
    totalPrice: unitPrice * duration
  };
}

function resolveConfiguredVideoTiers(config) {
  if (!config.tiers || typeof config.tiers !== 'object') {
    return VIDEO_TIER_PROFILES;
  }

  const tiers = {};
  for (const [name, profile] of Object.entries(config.tiers)) {
    if (!profile || typeof profile !== 'object' || typeof profile.model !== 'string' || !profile.model.trim()) {
      throw new Error(`config.tiers.${name} 必须包含非空 model`);
    }
    tiers[name] = {
      model: profile.model,
      quality: profile.quality,
      ratio: profile.ratio,
      duration: profile.duration
    };
  }
  return Object.keys(tiers).length ? tiers : VIDEO_TIER_PROFILES;
}

function resolveConfiguredVideoGoals(config, tiers) {
  if (!config.goals || typeof config.goals !== 'object') {
    return VIDEO_GOAL_PROFILES;
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
    const tierProfile = profile.tier ? tiers[profile.tier] : null;
    goals[name] = {
      tier: profile.tier,
      model: profile.model || (tierProfile ? tierProfile.model : undefined),
      quality: profile.quality || (tierProfile ? tierProfile.quality : undefined),
      ratio: profile.ratio || (tierProfile ? tierProfile.ratio : undefined),
      duration: profile.duration !== undefined ? profile.duration : tierProfile ? tierProfile.duration : undefined
    };
  }
  return Object.keys(goals).length ? goals : VIDEO_GOAL_PROFILES;
}

function resolveVideoSelection(args, config) {
  const tiers = resolveConfiguredVideoTiers(config);
  const goals = resolveConfiguredVideoGoals(config, tiers);
  const configuredDefaultGoal = firstNonEmpty(config.defaultGoal, config.goal);
  const configuredDefaultTier = firstNonEmpty(config.defaultTier, config.tier);

  if (args.model) {
    return { model: args.model, tier: null, goal: null, profile: null, source: 'cli-model', tiers, goals };
  }

  if (args.tier) {
    const profile = tiers[args.tier];
    if (!profile) {
      throw new Error(`不支持的 --tier: ${args.tier}，可选值为 ${Object.keys(tiers).join('|')}`);
    }
    return { model: profile.model, tier: args.tier, goal: null, profile, source: 'cli-tier', tiers, goals };
  }

  if (args.goal) {
    const goalProfile = goals[args.goal];
    if (!goalProfile) {
      throw new Error(`不支持的 --goal: ${args.goal}，可选值为 ${Object.keys(goals).join('|')}`);
    }
    return { model: goalProfile.model, tier: goalProfile.tier || null, goal: args.goal, profile: goalProfile, source: 'cli-goal', tiers, goals };
  }

  if (process.env.WAN_VIDEO_MODEL) {
    return { model: process.env.WAN_VIDEO_MODEL, tier: null, goal: null, profile: null, source: 'env-model', tiers, goals };
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
      profile: goalProfile,
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
    return { model: profile.model, tier: configuredDefaultTier, goal: null, profile, source: 'config-tier', tiers, goals };
  }

  if (config.model) {
    return { model: config.model, tier: null, goal: null, profile: null, source: 'config-model', tiers, goals };
  }

  return {
    model: DEFAULT_MODEL,
    tier: DEFAULT_TIER,
    goal: null,
    profile: VIDEO_TIER_PROFILES.final,
    source: 'default',
    tiers,
    goals
  };
}

function printPreflight({ model, tier, goal, selectionSource, selectionNote, size, duration, outputDir, taskId }) {
  const mode = taskId ? 'poll-existing-task' : 'create-task';
  console.error(`preflight mode=${mode}`);
  console.error(`preflight model=${model}`);
  console.error(`preflight selection_source=${selectionSource}${goal ? ` goal=${goal}` : ''}${tier ? ` tier=${tier}` : ''}`);
  if (selectionNote) {
    console.error(`preflight note=${selectionNote}`);
  }
  if (!taskId) {
    console.error(`preflight size=${size} duration=${duration}`);
  } else {
    console.error(`preflight task_id=${taskId}`);
  }
  console.error(`preflight output_dir=${outputDir}`);

  if (!taskId) {
    const estimated = estimateVideoCost(model, size, duration);
    if (estimated) {
      console.error(
        `cost_estimate region=中国内地 quality=${estimated.quality} unit=${formatCny(estimated.unitPrice)}/秒 total=${formatCny(estimated.totalPrice)}`
      );
    } else {
      console.error('cost_estimate region=中国内地 unavailable=未内置该模型或地域价格');
    }
  }
}

function getModelRule(model) {
  return MODEL_SIZE_RULES[model] || MODEL_SIZE_RULES[DEFAULT_MODEL];
}

function getDurationRule(model) {
  return MODEL_DURATION_RULES[model] || MODEL_DURATION_RULES[DEFAULT_MODEL];
}

function resolveVideoSize(model, args, config, profile) {
  if (args.size) {
    return args.size;
  }

  const rule = getModelRule(model);
  const quality = String(firstNonEmpty(args.quality, config.quality, profile && profile.quality, rule.defaultQuality)).toLowerCase();
  const ratio = String(firstNonEmpty(args.ratio, config.ratio, profile && profile.ratio, '16:9'));

  if (!rule.qualities.includes(quality)) {
    throw new Error(`${model} 不支持质量档位 ${quality}，可选值为 ${rule.qualities.join('|')}`);
  }

  const presetGroup = VIDEO_SIZE_PRESETS[quality];
  const size = presetGroup && presetGroup[ratio];
  if (!size) {
    throw new Error(`${quality} 不支持比例 ${ratio}，可选值为 ${Object.keys(presetGroup || {}).join('|')}`);
  }

  return size;
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

function buildCreateBody(model, args, profile) {
  const size = resolveVideoSize(model, args, {}, profile);
  const durationRule = getDurationRule(model);
  const duration =
    args.duration !== undefined
      ? Math.trunc(toNumber(args.duration, durationRule.defaultValue))
      : profile && profile.duration !== undefined
        ? profile.duration
        : durationRule.defaultValue;
  const body = {
    model,
    input: {
      prompt: args.prompt
    },
    parameters: {
      size,
      prompt_extend: toBoolean(args['prompt-extend'], true)
    }
  };

  if (args['negative-prompt']) {
    body.input.negative_prompt = args['negative-prompt'];
  }
  if (args['audio-url']) {
    body.input.audio_url = args['audio-url'];
  }
  if (args.duration !== undefined || (profile && profile.duration !== undefined)) {
    body.parameters.duration = duration;
  }
  if (args['shot-type']) {
    body.parameters.shot_type = args['shot-type'];
  }
  if (args.seed !== undefined) {
    body.parameters.seed = Math.trunc(toNumber(args.seed, 0));
  }

  return body;
}

function validateDuration(model, args, profile) {
  const rule = getDurationRule(model);
  const requested = args.duration !== undefined
    ? Math.trunc(toNumber(args.duration, rule.defaultValue))
    : profile && profile.duration !== undefined
      ? profile.duration
      : rule.defaultValue;

  if (rule.type === 'fixed') {
    if (args.duration !== undefined && requested !== rule.value) {
      throw new Error(`${model} 时长固定为 ${rule.value} 秒，不支持修改 --duration`);
    }
    return rule.value;
  }

  if (rule.type === 'enum') {
    if (!rule.values.includes(requested)) {
      throw new Error(`${model} 仅支持时长 ${rule.values.join('、')} 秒`);
    }
    return requested;
  }

  if (rule.type === 'range') {
    if (requested < rule.min || requested > rule.max) {
      throw new Error(`${model} 支持时长范围为 ${rule.min} 到 ${rule.max} 秒`);
    }
    return requested;
  }

  return requested;
}

function validateArgs(model, args, size) {
  const isLegacySilent = model.startsWith('wan2.2') || model.startsWith('wanx2.1');
  if (isLegacySilent && args['audio-url']) {
    throw new Error(`${model} 不支持 --audio-url，音频输入仅适用于 wan2.6/wan2.5 系列`);
  }
  if (args['shot-type'] && !model.startsWith('wan2.6')) {
    throw new Error('--shot-type 目前仅在 wan2.6 系列中启用');
  }
  if (!/^\d+\*\d+$/.test(String(size))) {
    throw new Error(`非法尺寸格式: ${size}，应为 宽*高，例如 1280*720`);
  }

  const allowedSizes = new Set();
  getModelRule(model).qualities.forEach((quality) => {
    Object.values(VIDEO_SIZE_PRESETS[quality]).forEach((value) => allowedSizes.add(value));
  });
  if (!allowedSizes.has(size)) {
    throw new Error(`${model} 不支持尺寸 ${size}。请使用 --size 指定官方允许值，或改用 --quality + --ratio`);
  }
}

async function createTask(baseUrl, apiKey, body) {
  const result = await requestJson(`${baseUrl}/api/v1/services/aigc/video-generation/video-synthesis`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'X-DashScope-Async': 'enable'
    },
    body: JSON.stringify(body)
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
  const selection = resolveVideoSelection(args, config);
  const model = selection.model;
  const selectionNote =
    config.model && firstNonEmpty(config.defaultGoal, config.goal, config.defaultTier, config.tier)
      ? 'config 同时包含 model 与 goal/tier 默认项，当前优先使用 goal/tier'
      : '';
  const outputDirInput = firstNonEmpty(args['output-dir'], config.outputDir, DEFAULT_OUTPUT_DIR);
  const outputDir = path.isAbsolute(outputDirInput)
    ? outputDirInput
    : path.resolve(path.join(__dirname, '..'), outputDirInput);
  const size = resolveVideoSize(model, args, config, selection.profile);

  const pollIntervalSec = Math.max(1, Math.trunc(toNumber(args['poll-interval'], DEFAULT_POLL_INTERVAL)));
  const timeoutSec = Math.max(30, Math.trunc(toNumber(args.timeout, DEFAULT_TIMEOUT)));
  const taskId = args['task-id'];
  const duration = validateDuration(model, args, selection.profile);

  if (!taskId && !args.prompt) {
    printUsage();
    throw new Error('提交新任务需要 --prompt，或使用 --task-id 查询已有任务');
  }

  if (!apiKey && !dryRun) {
    throw new Error(`缺少 DASHSCOPE_API_KEY。请设置环境变量，或在 ${CONFIG_PATH} 中配置 apiKey`);
  }

  printPreflight({
    model,
    tier: selection.tier,
    goal: selection.goal,
    selectionSource: selection.source,
    selectionNote,
    size,
    duration,
    outputDir,
    taskId
  });

  let createdTaskId = taskId;
  if (!createdTaskId) {
    validateArgs(model, args, size);
    const body = buildCreateBody(model, { ...args, size, duration }, selection.profile);
    if (dryRun) {
      console.log(JSON.stringify({
        baseUrl,
        endpoint: '/api/v1/services/aigc/video-generation/video-synthesis',
        body
      }, null, 2));
      return;
    }
    const created = await createTask(baseUrl, apiKey, body);
    createdTaskId = created.output.task_id;
    console.log(`task_id=${createdTaskId}`);
    console.error(`submitted model=${model}`);

    if (toBoolean(args['no-wait'], false)) {
      return;
    }
  }

  const status = await waitForTask(baseUrl, apiKey, createdTaskId, pollIntervalSec, timeoutSec);
  const output = status && status.output ? status.output : {};

  if (output.task_status !== 'SUCCEEDED') {
    throw new Error(`任务未成功结束: ${JSON.stringify(output)}`);
  }

  if (!output.video_url) {
    throw new Error(`任务成功但未找到 video_url: ${JSON.stringify(status)}`);
  }

  ensureDir(outputDir);
  const savePath = path.join(outputDir, `${sanitizeFilename(createdTaskId)}.mp4`);
  await downloadFile(output.video_url, savePath);
  console.log(savePath);
}

main().catch((error) => {
  console.error(`错误: ${error.message}`);
  process.exit(1);
});
