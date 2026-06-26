const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

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

function readConfig(configPath) {
  const full = path.resolve(configPath);
  if (!fs.existsSync(full)) throw new Error(`配置文件不存在: ${full}`);
  const raw = fs.readFileSync(full, 'utf8').trim();
  if (!raw) throw new Error(`配置文件为空: ${full}`);
  return { full, config: JSON.parse(raw) };
}

function looksPlaceholder(value) {
  const text = String(value || '').trim().toLowerCase();
  return !text || text === 'demo' || text.includes('placeholder') || text === 'your_api_key';
}

function resolveSourceImage(sourceImage) {
  const file = String(sourceImage?.file || '').trim();
  const url = String(sourceImage?.url || '').trim();
  if (file && fs.existsSync(path.resolve(file))) {
    return { ok: true, value: path.resolve(file), mode: 'file' };
  }
  if (/^https?:\/\//i.test(url)) {
    return { ok: true, value: url, mode: 'url' };
  }
  return { ok: false, value: '', mode: '' };
}

function normalizeFirstImageStrategy(value) {
  const text = String(value || '').trim().toLowerCase();
  if (!text) return '';
  if (['direct', 'first-frame', 'firstframe', '原图', '原图直绑', 'a'].includes(text)) return 'direct';
  if (['img2img', 'image2image', 'i2i', '图生图', 'b'].includes(text)) return 'img2img';
  return '';
}

function inferFirstImageStrategy(revisionNote) {
  const note = String(revisionNote || '').toLowerCase();
  if (!note) return '';
  if (/(图生图|转绘|重绘|风格化|统一画风|img2img|image2image|i2i|换风格)/i.test(note)) return 'img2img';
  if (/(原图|保脸|一致|direct|first(?:[_ -]?frame)|首图直绑)/i.test(note)) return 'direct';
  return '';
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = args.config;
  const entryResultPath = args['entry-result'];
  const confirmed = String(args.confirmed || '').toLowerCase();
  const resultJson = args['result-json'];
  const panelIndex = Number(args['panel-index'] || '1');
  const revisionNote = String(args['revision-note'] || '').trim();
  const firstImageStrategyArg = normalizeFirstImageStrategy(args['first-image-strategy']);

  if (!configPath || !entryResultPath) {
    throw new Error('用法: node continue-seedance-flow.cjs --config <json> --entry-result <json> --confirmed true [--panel-index 1] [--result-json <json>]');
  }
  if (confirmed !== 'true' && confirmed !== 'yes' && confirmed !== '1') {
    throw new Error('继续后续流程前，必须显式传入 --confirmed true');
  }

  const entry = readJson(entryResultPath);
  if (!entry?.confirmationRequired || !entry?.confirmationBundle) {
    throw new Error('当前入口结果不在四件套确认阶段，无法继续');
  }

  const argSourceImageFile = args['reference-image-file'] ? path.resolve(String(args['reference-image-file'])) : '';
  const argSourceImageUrl = String(args['reference-image-url'] || '').trim();
  const bundleSourceImage = entry?.confirmationBundle?.sourceImage || {};
  const sourceImage = {
    file: argSourceImageFile || String(bundleSourceImage?.file || '').trim(),
    url: argSourceImageUrl || String(bundleSourceImage?.url || '').trim(),
  };

  const outDir = path.resolve(path.dirname(entryResultPath), 'next');
  const firstImageResultPath = path.resolve(outDir, `P${String(panelIndex).padStart(2, '0')}.first-image.result.json`);
  ensureDirForFile(firstImageResultPath);

  const child = spawnSync(
    process.execPath,
    [
      path.resolve(__dirname, 'generate-first-image-pack.cjs'),
      '--config', configPath,
      '--entry-result', entryResultPath,
      '--panel-index', String(panelIndex),
      '--out-dir', outDir,
      '--result-json', firstImageResultPath,
      ...(revisionNote ? ['--revision-note', revisionNote] : []),
    ],
    { stdio: 'pipe', encoding: 'utf8', cwd: process.cwd() },
  );

  if (child.status !== 0) {
    const failure = {
      ok: false,
      stage: 'first-image-pack',
      status: 'stop',
      summary: '四件套确认后，首图确认包生成失败。',
      reasons: [child.stderr || child.stdout || '未知错误'],
      nextStep: '先修正首图确认包生成错误，再继续后续流程。',
    };
    writeJson(resultJson, failure);
    process.exit(child.status || 1);
  }

  const firstImage = readJson(firstImageResultPath);
  const { config } = readConfig(configPath);
  const imageStage = config?.downstream?.waoo?.image;
  const videoStage = config?.downstream?.waoo?.video;
  const imageConfigReady = Boolean(imageStage?.厂商 && imageStage?.接口地址 && imageStage?.模型名 && !looksPlaceholder(imageStage?.APIKey));
  const videoConfigReady = Boolean(videoStage?.厂商 && videoStage?.接口地址 && videoStage?.模型名 && !looksPlaceholder(videoStage?.APIKey));
  const sourceImageResolved = resolveSourceImage(sourceImage);
  const bundleStrategy = normalizeFirstImageStrategy(entry?.confirmationBundle?.firstImageStrategy?.default);
  const noteStrategy = inferFirstImageStrategy(revisionNote);
  const resolvedFirstImageStrategy = firstImageStrategyArg || noteStrategy || bundleStrategy || 'direct';
  const directFirstFrameEnabled = sourceImageResolved.ok && videoConfigReady && resolvedFirstImageStrategy !== 'img2img';
  const firstImageAssetResultPath = path.resolve(outDir, `P${String(panelIndex).padStart(2, '0')}.first-image.asset.result.json`);

  if (directFirstFrameEnabled) {
    const directPanelContext = {
      projectId: String(firstImage.projectId || 'seedance-project'),
      episodeId: String(firstImage.episodeId || entry?.confirmationBundle?.episode || 'E01'),
      panelId: String(firstImage.panelId || `${entry?.confirmationBundle?.episode || 'E01'}-P${String(panelIndex).padStart(2, '0')}`),
      panelIndex: Number(firstImage.panelIndex || panelIndex),
      panelTitle: String(firstImage.panelTitle || ''),
      imageUrl: sourceImageResolved.value,
      videoPrompt: String(firstImage.promptText || ''),
      subtitleText: String(firstImage.subtitleCandidate || ''),
      existingVideoUrl: '',
      isMainClip: true,
      stateLabel: 'image-approved',
      sourceImageBound: true,
      sourceImageMode: sourceImageResolved.mode,
      sourceImageRef: sourceImageResolved.value,
      firstImageStrategy: resolvedFirstImageStrategy,
    };

    writeJson(firstImageAssetResultPath, {
      ok: true,
      panelIndex: directPanelContext.panelIndex,
      panelTitle: directPanelContext.panelTitle,
      imageFile: sourceImageResolved.mode === 'file' ? sourceImageResolved.value : '',
      imageUrl: sourceImageResolved.mode === 'url' ? sourceImageResolved.value : '',
      caption: `【Panel ${directPanelContext.panelIndex}${directPanelContext.panelTitle ? `｜${directPanelContext.panelTitle}` : ''}】已绑定用户原图作为 first_frame，跳过首图生成，直接进入视频提交。`,
      stateLabel: 'image-approved-candidate',
      promptText: String(firstImage.promptText || ''),
      negativePrompt: String(firstImage.negativePrompt || ''),
      subtitleCandidate: String(firstImage.subtitleCandidate || ''),
      rawResponsePreview: {
        mode: 'direct-first-frame',
        sourceImageMode: sourceImageResolved.mode,
      },
      sourceImageBound: true,
      sourceImageMode: sourceImageResolved.mode,
      sourceImageRef: sourceImageResolved.value,
      firstImageStrategy: resolvedFirstImageStrategy,
      directPanelContext,
    });

    const output = {
      ok: true,
      currentStage: 'first-image-asset-confirm',
      confirmationRequired: false,
      autoContinue: true,
      firstImageBundle: firstImage,
      firstImageAsset: readJson(firstImageAssetResultPath),
      directPanelContext,
      checkpoint: {
        stage: 'first-image-approved',
        status: 'pass',
        summary: '检测到用户提供图 + 文本，已自动绑定原图为 first_frame 并跳过首图生成。',
        reasons: ['source image 可用', 'video 配置可用', '按默认策略进入直提视频'],
        nextStep: '继续调用 continue-after-first-image.cjs 进入正式视频提交。',
      },
      firstImageStrategy: resolvedFirstImageStrategy,
      nextStep: '已进入原图直绑模式，继续正式视频提交。',
    };
    writeJson(resultJson, output);
    return;
  }

  if (!imageConfigReady) {
    const output = {
      ok: true,
      currentStage: 'first-image-asset-blocked',
      confirmationRequired: false,
      firstImageBundle: firstImage,
      checkpoint: {
        stage: 'first-image-approved',
        status: 'stop',
        summary: '首图内部规格已生成，但真实首图图片生成仍缺少可用的 downstream.waoo.image 配置。',
        reasons: ['缺少真实可用的 downstream.waoo.image 厂商 / 接口地址 / 模型名 / API Key'],
        nextStep: '补齐首图图片生成配置后，继续由 skill 内部生成真实首图图片，再把图片发给用户确认。',
      },
      firstImageStrategy: resolvedFirstImageStrategy,
      strategyPrompt: '可切换首图策略：A 原图直绑（默认）/ B 图生图（风格化重绘）。',
      nextStep: '先补齐 downstream.waoo.image 配置。',
    };
    writeJson(resultJson, output);
    return;
  }

  const assetChild = spawnSync(
    process.execPath,
    [
      path.resolve(__dirname, 'generate-first-image-asset.cjs'),
      '--config', configPath,
      '--first-image-result', firstImageResultPath,
      '--out-dir', outDir,
      '--result-json', firstImageAssetResultPath,
    ],
    { stdio: 'pipe', encoding: 'utf8', cwd: process.cwd() },
  );

  if (assetChild.status !== 0) {
    const output = {
      ok: false,
      currentStage: 'first-image-asset-blocked',
      confirmationRequired: false,
      firstImageBundle: firstImage,
      checkpoint: {
        stage: 'first-image-approved',
        status: 'stop',
        summary: '首图内部规格已生成，但真实首图图片生成失败。',
        reasons: [assetChild.stderr || assetChild.stdout || '未知错误'],
        nextStep: '先修正首图图片生成错误，再由 skill 内部继续。',
      },
    };
    writeJson(resultJson, output);
    process.exit(assetChild.status || 1);
  }

  const firstImageAsset = readJson(firstImageAssetResultPath);
  const output = {
    ok: true,
    currentStage: 'first-image-asset-confirm',
    confirmationRequired: true,
    firstImageBundle: firstImage,
    firstImageAsset,
    firstImageStrategy: resolvedFirstImageStrategy,
    strategyPrompt: '可切换首图策略：A 原图直绑（默认）/ B 图生图（风格化重绘）。',
    userMessage: `${firstImageAsset.caption}\n\n可切换首图策略：A 原图直绑（默认）/ B 图生图（风格化重绘）。如需切换，请直接回复“切到图生图”或“切到原图直绑”。`,
    nextStep: '把真实首图图片发给用户确认；用户确认前不要进入视频生成。',
  };
  writeJson(resultJson, output);
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
