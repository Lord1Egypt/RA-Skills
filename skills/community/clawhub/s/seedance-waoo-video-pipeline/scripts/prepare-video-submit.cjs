const fs = require('node:fs');
const path = require('node:path');

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      result[key] = true;
      continue;
    }
    result[key] = next;
    i += 1;
  }
  return result;
}

function ensureDirForFile(filePath) {
  fs.mkdirSync(path.dirname(path.resolve(filePath)), { recursive: true });
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
}

function writeJson(outputPath, data) {
  const text = JSON.stringify(data, null, 2);
  if (outputPath) {
    ensureDirForFile(outputPath);
    fs.writeFileSync(path.resolve(outputPath), text + '\n', 'utf8');
  }
  console.log(text);
}

function canonicalVendor(name) {
  const value = String(name || '').trim().toLowerCase();
  if (!value) return '';
  if (value.includes('minimax') || value.includes('mini max') || value.includes('hailuo')) return 'minimax';
  if (value.includes('vidu')) return 'vidu';
  if (value.includes('seedance') || value.includes('doubao')) return 'seedance';
  return value;
}

function looksPlaceholder(value) {
  const text = String(value || '').trim().toLowerCase();
  return !text || text === 'demo' || text.includes('placeholder') || text === 'your_api_key';
}

function buildGuard(panel, requireImageApproval) {
  const errors = [];
  const warnings = [];
  if (!panel.panelId) errors.push('目标 panel 缺少稳定 panelId');
  if (!Number.isFinite(Number(panel.panelIndex)) || Number(panel.panelIndex) < 0) errors.push('目标 panel 缺少有效 panelIndex');
  if (!panel.imageUrl) warnings.push('目标 panel 缺少 imageUrl');
  if (!panel.videoPrompt) warnings.push('目标 panel 缺少 videoPrompt');
  if (!panel.subtitleText) warnings.push('目标 panel 缺少 subtitleText');

  return {
    ok: errors.length === 0,
    identityLocked: Boolean(panel.panelId) && Number(panel.panelIndex) >= 0,
    orderingValid: true,
    duplicates: [],
    skippedIndexes: [],
    needsUserConfirmation: Boolean(requireImageApproval) || warnings.length > 0,
    target: {
      panelId: panel.panelId,
      panelIndex: Number(panel.panelIndex),
      imageUrl: String(panel.imageUrl || ''),
      videoPrompt: String(panel.videoPrompt || ''),
      subtitleText: String(panel.subtitleText || ''),
      isMainClip: Boolean(panel.isMainClip),
    },
    orderedPanels: [panel],
    errors,
    warnings,
  };
}

function buildCheckpoint(guard, videoStage) {
  const reasons = [...guard.errors, ...guard.warnings];
  if (!videoStage?.厂商 || !videoStage?.接口地址 || !videoStage?.模型名 || looksPlaceholder(videoStage?.APIKey)) {
    reasons.push('视频配置不完整或仍是 demo / placeholder');
  }
  return {
    stage: 'panel-guard',
    status: guard.ok && reasons.length === 0 ? 'pass' : (guard.ok ? 'confirm' : 'stop'),
    summary: guard.ok ? '视频提交前置校验已完成。' : '视频提交前置校验失败。',
    reasons,
    nextStep: guard.ok
      ? '如用户确认进入付费视频生成，则可继续调用正式视频提交入口。'
      : '先修正 panel context / 图片 / 配置后，再继续视频提交。',
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const panelPath = args.panel;
  const configPath = args.config;
  const outputPath = args.out;
  const duration = args.duration || '6';
  const resolution = args.resolution || '768P';
  const requireImageApproval = args['require-image-approval'] === true;
  if (!panelPath) {
    throw new Error('用法: node prepare-video-submit.cjs --panel <panel-context.json> [--config <json>] [--duration 6] [--resolution 768P] [--require-image-approval] [--out <json>]');
  }

  const panel = readJson(panelPath);
  const config = configPath ? readJson(configPath) : {};
  const videoStage = config?.downstream?.waoo?.video;
  const guard = buildGuard(panel, requireImageApproval);
  const checkpoint = buildCheckpoint(guard, videoStage);
  const vendor = canonicalVendor(videoStage?.厂商);
  const supportedVideoVendors = new Set(['minimax', 'vidu', 'seedance']);
  const videoConfigReady = Boolean(supportedVideoVendors.has(vendor) && videoStage?.接口地址 && videoStage?.模型名 && !looksPlaceholder(videoStage?.APIKey));
  const ready = guard.ok && !guard.needsUserConfirmation && videoConfigReady;

  const nextCommand = [
    'node scripts/submit-official-video.cjs',
    configPath ? `--config ${configPath}` : '',
    `--panel ${panelPath}`,
    `--duration ${duration}`,
    `--resolution ${resolution}`,
  ].filter(Boolean).join(' ');

  const result = {
    ok: guard.ok,
    ready,
    panel,
    guard,
    checkpoint,
    nextCommand,
  };

  writeJson(outputPath, result);
  if (!result.ok) process.exit(2);
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
