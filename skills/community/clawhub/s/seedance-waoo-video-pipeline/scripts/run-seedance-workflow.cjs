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

function runNodeScript(scriptPath, scriptArgs, cwd) {
  return spawnSync(process.execPath, [scriptPath, ...scriptArgs], {
    stdio: 'pipe',
    encoding: 'utf8',
    cwd,
  });
}

function buildPromptPack(options) {
  const {
    configPath,
    topic,
    outDir,
    hasReferenceImage,
    modeHint,
    durationHint,
    styleHint,
    cameraHint,
    scenarioHint,
    workdir,
  } = options;

  const promptPackPath = path.resolve(outDir, 'prompt-pack.result.json');
  const args = [
    '--topic', topic,
    '--duration', String(durationHint || '10'),
    '--mode', String(modeHint || '').trim() || (hasReferenceImage ? 'first-last-frame' : 'text-only'),
    '--has-reference-image', hasReferenceImage ? 'true' : 'false',
    '--result-json', promptPackPath,
  ];

  if (styleHint) args.push('--style', String(styleHint));
  if (cameraHint) args.push('--camera', String(cameraHint));
  if (scenarioHint) args.push('--scenario', String(scenarioHint));

  const child = runNodeScript(
    path.resolve(__dirname, 'build-seedance-prompt-pack.cjs'),
    args,
    workdir,
  );

  if (child.status !== 0) {
    return {
      ok: false,
      promptPackPath,
      error: (child.stderr || child.stdout || 'build prompt pack failed').trim(),
    };
  }

  if (!fs.existsSync(promptPackPath)) {
    return {
      ok: false,
      promptPackPath,
      error: 'prompt pack file not generated',
    };
  }

  return {
    ok: true,
    promptPackPath,
    promptPack: readJson(promptPackPath),
  };
}

function isPlaceholder(value) {
  const text = String(value || '').trim().toLowerCase();
  if (!text) return true;
  return text.includes('your-') || text.includes('placeholder') || text === 'demo';
}

function evaluatePromptPack(promptPackResult) {
  if (!promptPackResult?.ok || !promptPackResult?.promptPack) {
    return {
      score: 0,
      level: 'blocked',
      suggestions: ['Prompt Pack 生成失败，先检查 prompt 脚本与输入参数。'],
    };
  }

  const pack = promptPackResult.promptPack;
  let score = 20;
  if (pack.mode) score += 15;
  if (Array.isArray(pack.beats) && pack.beats.length >= 3) score += 20;
  if (typeof pack.prompt === 'string' && pack.prompt.includes('[目标]') && pack.prompt.includes('[时间节拍（Timecoded Beats）]')) score += 15;
  if (pack.assets?.referenceImage) score += 5;
  if (Array.isArray(pack.negatives) && pack.negatives.length >= 2) score += 10;
  score += pack.scenario && pack.scenario !== 'general' ? 20 : -5;
  score = Math.max(0, Math.min(100, score));

  const suggestions = [];
  if (!pack.mode) suggestions.push('补充 --prompt-mode 明确生成模式。');
  if (!Array.isArray(pack.beats) || pack.beats.length < 3) suggestions.push('增加时间节拍，保证镜头节奏可控。');
  if (!pack.scenario || pack.scenario === 'general') suggestions.push('可通过 --prompt-scenario 切换到 narrative/ecommerce/mv 等场景模板。');
  if (!Array.isArray(pack.negatives) || pack.negatives.length < 2) suggestions.push('补充负面约束，减少崩画与镜头漂移。');

  const level = score >= 90 ? 'excellent' : score >= 80 ? 'good' : score >= 65 ? 'fair' : 'weak';
  return { score, level, suggestions };
}

function inferScenarioFromTopic(topic) {
  const text = String(topic || '').toLowerCase();
  if (!text) return 'narrative';
  if (/(电商|带货|产品|上新|开箱|卖点|sku|优惠|直播)/.test(text)) return 'ecommerce';
  if (/(mv|音乐|歌曲|节拍|舞蹈|唱|rap|伴奏)/.test(text)) return 'mv';
  if (/(教程|教学|讲解|步骤|演示|怎么做|如何)/.test(text)) return 'tutorial';
  return 'narrative';
}

function uniqueList(items) {
  const out = [];
  for (const item of items) {
    const value = String(item || '').trim().toLowerCase();
    if (!value) continue;
    if (!out.includes(value)) out.push(value);
  }
  return out;
}

function buildFallbackScenarioList(currentScenario, topic) {
  const inferred = inferScenarioFromTopic(topic);
  const current = String(currentScenario || 'general').trim().toLowerCase();
  const candidates = uniqueList([
    inferred,
    current === 'general' ? 'narrative' : 'general',
    'ecommerce',
    'mv',
    'tutorial',
  ]);
  return candidates.filter((s) => s !== current);
}

function runPromptFallback(options) {
  const {
    enabled,
    minScore,
    topic,
    basePromptPackResult,
    basePromptQuality,
    outDir,
    hasReferenceImage,
    modeHint,
    durationHint,
    styleHint,
    cameraHint,
    workdir,
  } = options;

  const report = {
    enabled: Boolean(enabled),
    minScore,
    triggered: false,
    applied: false,
    fromScenario: basePromptPackResult?.promptPack?.scenario || 'general',
    toScenario: '',
    fromScore: basePromptQuality?.score || 0,
    toScore: basePromptQuality?.score || 0,
    attempts: [],
    reason: '',
  };

  if (!enabled) {
    report.reason = 'disabled';
    return {
      promptPackResult: basePromptPackResult,
      promptQuality: basePromptQuality,
      report,
    };
  }

  if ((basePromptQuality?.score || 0) >= minScore) {
    report.reason = 'score-above-threshold';
    return {
      promptPackResult: basePromptPackResult,
      promptQuality: basePromptQuality,
      report,
    };
  }

  report.triggered = true;
  report.reason = 'score-below-threshold';

  const scenarios = buildFallbackScenarioList(report.fromScenario, topic);
  let bestResult = basePromptPackResult;
  let bestQuality = basePromptQuality;
  let bestScenario = report.fromScenario;

  for (const scenario of scenarios) {
    const candidate = buildPromptPack({
      topic,
      outDir,
      hasReferenceImage,
      modeHint,
      durationHint,
      styleHint,
      cameraHint,
      scenarioHint: scenario,
      workdir,
    });
    const quality = evaluatePromptPack(candidate);
    report.attempts.push({ scenario, score: quality.score, level: quality.level, ok: Boolean(candidate.ok) });

    if (quality.score > (bestQuality?.score || 0)) {
      bestResult = candidate;
      bestQuality = quality;
      bestScenario = scenario;
    }
    if (quality.score >= minScore) break;
  }

  if ((bestQuality?.score || 0) > (basePromptQuality?.score || 0)) {
    report.applied = true;
    report.toScenario = bestScenario;
    report.toScore = bestQuality.score;
  } else {
    report.toScenario = report.fromScenario;
    report.toScore = basePromptQuality?.score || 0;
  }

  return {
    promptPackResult: bestResult,
    promptQuality: bestQuality,
    report,
  };
}

function getPipelineMode(config) {
  const mode = String(config?.runtime?.pipelineMode || 'minimax_full').trim().toLowerCase();
  return mode || 'minimax_full';
}

function canonicalVendor(name) {
  const value = String(name || '').trim().toLowerCase();
  if (!value) return '';
  if (value.includes('minimax') || value.includes('mini max') || value.includes('hailuo')) return 'minimax';
  if (value.includes('vidu')) return 'vidu';
  if (value.includes('seedance') || value.includes('doubao') || value.includes('ark') || value.includes('volc')) return 'seedance';
  return value;
}

function isObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function trimSlash(url) {
  return String(url || '').replace(/\/+$/, '');
}

function endpointMatchesVendor(vendor, endpoint) {
  const url = trimSlash(endpoint).toLowerCase();
  if (!vendor || !url) return true;

  const hints = {
    seedance: /ark|volc|doubao|byte|bytedance/,
    vidu: /vidu|toapis/,
    minimax: /minimax|hailuo/,
  };
  const competitorHints = {
    seedance: [/vidu|toapis/],
    vidu: [/ark|volc|doubao|byte|bytedance/],
    minimax: [/ark|volc|doubao|byte|bytedance/, /vidu|toapis/],
  };

  const directHint = hints[vendor];
  if (directHint && directHint.test(url)) return true;

  const conflicts = competitorHints[vendor] || [];
  for (const pattern of conflicts) {
    if (pattern.test(url)) return false;
  }

  // custom gateway/proxy domains are allowed when no conflicting hint exists
  return true;
}

function readStageCandidates(config, stageKind) {
  const waoo = config?.downstream?.waoo || {};
  const legacy = waoo[stageKind];
  const map = waoo[`${stageKind}s`];
  const items = [];

  if (isObject(map)) {
    for (const [name, block] of Object.entries(map)) {
      if (!isObject(block)) continue;
      const vendor = canonicalVendor(block?.厂商 || name);
      items.push({
        vendor,
        stage: block,
        source: `downstream.waoo.${stageKind}s.${name}`,
        legacy: false,
      });
    }
  }

  if (isObject(legacy)) {
    const vendor = canonicalVendor(legacy?.厂商);
    items.push({
      vendor,
      stage: legacy,
      source: `downstream.waoo.${stageKind}`,
      legacy: true,
    });
  }

  return items;
}

function isStageReady(stage) {
  if (!isObject(stage)) return false;
  if (!stage.厂商 || !stage.接口地址 || !stage.模型名) return false;
  if (isPlaceholder(stage.APIKey)) return false;
  return true;
}

function normalizePriorityList(value, fallback) {
  if (Array.isArray(value)) {
    const normalized = value.map((v) => canonicalVendor(v)).filter(Boolean);
    return normalized.length ? normalized : fallback;
  }
  const text = String(value || '').trim();
  if (!text) return fallback;
  const normalized = text
    .split(/[>,|,\s]+/)
    .map((v) => canonicalVendor(v))
    .filter(Boolean);
  return normalized.length ? normalized : fallback;
}

function resolveRoutePreferences(config, hasReferenceImage) {
  const routing = config?.runtime?.routing || {};
  const videoPriority = hasReferenceImage
    ? normalizePriorityList(routing?.videoPriorityImageText, ['seedance', 'vidu', 'minimax'])
    : normalizePriorityList(routing?.videoPriorityTextOnly, ['seedance', 'vidu', 'minimax']);
  const imagePriority = normalizePriorityList(routing?.imagePriorityTextOnly, ['seedance', 'minimax']);
  const defaultVideoVendor = canonicalVendor(routing?.defaultVideoVendor || config?.runtime?.defaultVideoVendor || config?.runtime?.defaultVendor);
  const defaultImageVendor = canonicalVendor(routing?.defaultImageVendor || config?.runtime?.defaultImageVendor);
  return {
    videoPriority,
    imagePriority,
    defaultVideoVendor,
    defaultImageVendor,
  };
}

function selectStage(candidates, options = {}) {
  const {
    forcedVendor = '',
    defaultVendor = '',
    priority = [],
    label = 'stage',
  } = options;

  if (!candidates.length) {
    return {
      ok: false,
      reason: `${label} 配置缺失`,
      candidateSummary: [],
    };
  }

  const candidateSummary = candidates.map((item) => ({
    vendor: item.vendor || '(unknown)',
    source: item.source,
    ready: isStageReady(item.stage),
  }));

  const order = [];
  const pushVendor = (name) => {
    const vendor = canonicalVendor(name);
    if (vendor && !order.includes(vendor)) order.push(vendor);
  };
  pushVendor(forcedVendor);
  pushVendor(defaultVendor);
  priority.forEach(pushVendor);
  candidates.forEach((item) => pushVendor(item.vendor));

  const preferred = [];
  for (const vendor of order) {
    const group = candidates.filter((item) => item.vendor === vendor);
    group.sort((a, b) => Number(a.legacy) - Number(b.legacy));
    preferred.push(...group);
  }
  const leftovers = candidates.filter((item) => !preferred.includes(item));
  preferred.push(...leftovers);

  const selected = preferred.find((item) => isStageReady(item.stage));
  if (!selected) {
    return {
      ok: false,
      reason: `${label} 候选存在但都未就绪（缺字段或 APIKey 仍是占位符）`,
      candidateSummary,
    };
  }

  if (forcedVendor && selected.vendor !== canonicalVendor(forcedVendor)) {
    return {
      ok: false,
      reason: `${label} 已强制选择 ${forcedVendor}，但未找到该厂商可用配置`,
      candidateSummary,
    };
  }

  if (!endpointMatchesVendor(selected.vendor, selected.stage?.接口地址)) {
    return {
      ok: false,
      reason: `${label} 厂商与接口地址疑似不匹配（${selected.vendor} vs ${selected.stage?.接口地址}）`,
      candidateSummary,
    };
  }

  return {
    ok: true,
    selected,
    candidateSummary,
  };
}

function buildEffectiveConfig(configPath, config, selectedStages, outDir) {
  const desiredVideo = selectedStages?.video?.selected;
  const desiredImage = selectedStages?.image?.selected;
  const waoo = config?.downstream?.waoo || {};
  const legacyVideo = waoo.video;
  const legacyImage = waoo.image;

  const needVideoPatch = desiredVideo && desiredVideo.source !== 'downstream.waoo.video';
  const needImagePatch = desiredImage && desiredImage.source !== 'downstream.waoo.image';

  if (!needVideoPatch && !needImagePatch) {
    return {
      effectiveConfigPath: path.resolve(configPath),
      patched: false,
    };
  }

  const next = JSON.parse(JSON.stringify(config));
  next.downstream = next.downstream || {};
  next.downstream.waoo = next.downstream.waoo || {};
  if (needVideoPatch) {
    next.downstream.waoo.video = desiredVideo.stage;
  } else if (!next.downstream.waoo.video && legacyVideo) {
    next.downstream.waoo.video = legacyVideo;
  }

  if (needImagePatch) {
    next.downstream.waoo.image = desiredImage.stage;
  } else if (!next.downstream.waoo.image && legacyImage) {
    next.downstream.waoo.image = legacyImage;
  }

  const targetDir = path.resolve(outDir || path.dirname(configPath));
  fs.mkdirSync(targetDir, { recursive: true });
  const effectiveConfigPath = path.resolve(targetDir, 'pipeline.effective.auto-route.json');
  fs.writeFileSync(effectiveConfigPath, `${JSON.stringify(next, null, 2)}\n`, 'utf8');

  return {
    effectiveConfigPath,
    patched: true,
  };
}

function resolveStageSelection(config, options = {}) {
  const hasReferenceImage = Boolean(options.hasReferenceImage);
  const forcedVideoVendor = canonicalVendor(options.forceVideoVendor || '');
  const forcedImageVendor = canonicalVendor(options.forceImageVendor || '');
  const prefs = resolveRoutePreferences(config, hasReferenceImage);

  const videoCandidates = readStageCandidates(config, 'video');
  const imageCandidates = readStageCandidates(config, 'image');

  const selectedVideo = selectStage(videoCandidates, {
    forcedVendor: forcedVideoVendor,
    defaultVendor: prefs.defaultVideoVendor,
    priority: prefs.videoPriority,
    label: '视频',
  });

  const selectedImage = hasReferenceImage
    ? { ok: true, skipped: true, reason: '输入已含参考图，跳过首图模型路由。', candidateSummary: imageCandidates.map((item) => ({ vendor: item.vendor || '(unknown)', source: item.source, ready: isStageReady(item.stage) })) }
    : selectStage(imageCandidates, {
      forcedVendor: forcedImageVendor,
      defaultVendor: prefs.defaultImageVendor,
      priority: prefs.imagePriority,
      label: '首图',
    });

  return {
    video: selectedVideo,
    image: selectedImage,
    preferences: prefs,
    hasReferenceImage,
  };
}

function summarizeRouting(selection) {
  return {
    hasReferenceImage: selection.hasReferenceImage,
    preferences: selection.preferences,
    video: {
      ok: selection.video.ok,
      reason: selection.video.reason || '',
      selectedVendor: selection.video.selected?.vendor || '',
      selectedSource: selection.video.selected?.source || '',
      candidates: selection.video.candidateSummary || [],
    },
    image: {
      ok: selection.image.ok,
      skipped: Boolean(selection.image.skipped),
      reason: selection.image.reason || '',
      selectedVendor: selection.image.selected?.vendor || '',
      selectedSource: selection.image.selected?.source || '',
      candidates: selection.image.candidateSummary || [],
    },
  };
}

function isSimpleMode(mode) {
  return ['vidu_simple', 'seedance_simple'].includes(mode);
}

function parseBool(value, fallback = false) {
  if (value === undefined) return fallback;
  if (value === true) return true;
  const text = String(value || '').trim().toLowerCase();
  if (!text) return fallback;
  return ['1', 'true', 'yes', 'y', 'on'].includes(text);
}

function toResultRelative(baseDir, targetFile) {
  return path.relative(path.resolve(baseDir), path.resolve(targetFile)).replace(/\\/g, '/');
}

function checkConfigReadiness(configPath, options = {}) {
  if (!fs.existsSync(configPath)) {
    return {
      ready: false,
      mode: 'minimax_full',
      missing: [{ item: 'config', reason: `配置文件不存在: ${configPath}` }],
      guidance: ['先创建配置文件，再继续流程。'],
      route: null,
      effectiveConfigPath: path.resolve(configPath),
    };
  }

  const config = readJson(configPath);
  const mode = getPipelineMode(config);
  const missing = [];
  const referenceImageProvided = Boolean(String(options.referenceImageFile || '').trim() || String(options.referenceImageUrl || '').trim());

  const routeSelection = resolveStageSelection(config, {
    hasReferenceImage: referenceImageProvided,
    forceVideoVendor: options.forceVideoVendor,
    forceImageVendor: options.forceImageVendor,
  });

  function checkBlock(label, block, requiredKeys = ['厂商', '接口地址', '模型名', 'APIKey']) {
    if (!block) {
      missing.push({ item: label, reason: '配置块缺失' });
      return;
    }
    for (const key of requiredKeys) {
      const value = block[key];
      if (!value || (key === 'APIKey' && isPlaceholder(value))) {
        missing.push({ item: `${label}.${key}`, reason: key === 'APIKey' ? '未填写或仍是占位符' : '缺失' });
      }
    }
  }

  if (!isSimpleMode(mode)) {
    checkBlock('upstream.seedance', config?.upstream?.seedance);
  }

  if (!routeSelection.video.ok) {
    missing.push({ item: 'downstream.waoo.video', reason: routeSelection.video.reason || '视频路由不可用' });
  }

  if (!isSimpleMode(mode) && !referenceImageProvided && !routeSelection.image.ok) {
    missing.push({ item: 'downstream.waoo.image', reason: routeSelection.image.reason || '首图路由不可用' });
  }

  const routeSummary = summarizeRouting(routeSelection);
  const guidance = isSimpleMode(mode)
    ? [
      `当前是 ${mode} 模式：按能力路由自动选择可用视频模型（优先级 ${routeSummary.preferences.videoPriority.join(' > ')}）。`,
      referenceImageProvided
        ? '检测到图+文字输入：将直接进入视频提交流程，不要求 image 模型。'
        : '纯文字输入：直接走 text->video，后续可按需补 image/tts。',
      '可通过 --video-vendor 强制指定视频厂商。',
    ]
    : [
      referenceImageProvided
        ? '当前是 minimax_full：四件套确认后默认图+文字直绑 first_frame，跳过首图模型。'
        : '当前是 minimax_full：四件套确认后需要首图路由可用，再进入视频阶段。',
      `视频路由优先级：${routeSummary.preferences.videoPriority.join(' > ')}`,
      '可通过 --video-vendor / --image-vendor 指定厂商。',
    ];

  const effectiveOutDir = options.outDir || path.dirname(path.resolve(configPath));
  const effectiveConfig = buildEffectiveConfig(configPath, config, routeSelection, effectiveOutDir);

  return {
    ready: missing.length === 0,
    mode,
    missing,
    guidance,
    route: routeSummary,
    effectiveConfigPath: effectiveConfig.effectiveConfigPath,
    effectiveConfigPatched: Boolean(effectiveConfig.patched),
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const action = args.action || 'start';
  const configPath = args.config || './config/pipeline.config.json';
  const workdir = process.cwd();
  const resultJson = args['result-json'];

  if (action === 'start') {
    const topic = args.topic;
    const episode = args.episode || 'E01';
    const outDir = args['out-dir'] || `./work/seedance/${episode}`;
    const revisionNote = String(args['revision-note'] || '').trim();
    const sourceImageFile = args['reference-image-file'] ? path.resolve(String(args['reference-image-file'])) : '';
    const sourceImageUrl = String(args['reference-image-url'] || '').trim();
    const forceVideoVendor = String(args['video-vendor'] || '').trim();
    const forceImageVendor = String(args['image-vendor'] || '').trim();
    const probeMode = parseBool(args.probe, false);

    const readiness = checkConfigReadiness(configPath, {
      referenceImageFile: sourceImageFile,
      referenceImageUrl: sourceImageUrl,
      forceVideoVendor,
      forceImageVendor,
      outDir,
    });
    if (!readiness.ready) {
      writeJson(resultJson || path.resolve(outDir, 'workflow.config-guidance.json'), {
        ok: false,
        currentStage: 'configuration-guidance',
        workflow: { action: 'start', driver: 'run-seedance-workflow.cjs', blocked: true },
        pipelineMode: readiness.mode,
        missing: readiness.missing,
        guidance: readiness.guidance,
        routing: readiness.route,
      });
      return;
    }

    const activeConfigPath = readiness.effectiveConfigPath || path.resolve(configPath);

    if (!topic) throw new Error('start 模式需要 --topic');

    const resolvedOutDir = path.resolve(outDir);
    fs.mkdirSync(resolvedOutDir, { recursive: true });
    let promptPackResult = buildPromptPack({
      configPath: activeConfigPath,
      topic,
      outDir: resolvedOutDir,
      hasReferenceImage: Boolean(sourceImageFile || sourceImageUrl),
      modeHint: args['prompt-mode'] || '',
      durationHint: args.duration || '',
      styleHint: args['prompt-style'] || '',
      cameraHint: args['prompt-camera'] || '',
      scenarioHint: args['prompt-scenario'] || '',
      workdir,
    });
    let promptQuality = evaluatePromptPack(promptPackResult);

    const fallbackEnabled = parseBool(args['prompt-auto-fallback'], true);
    const fallbackMinScore = Number(args['prompt-min-score'] || '80');
    const fallbackResult = runPromptFallback({
      enabled: fallbackEnabled,
      minScore: Number.isFinite(fallbackMinScore) ? fallbackMinScore : 80,
      topic,
      basePromptPackResult: promptPackResult,
      basePromptQuality: promptQuality,
      outDir: resolvedOutDir,
      hasReferenceImage: Boolean(sourceImageFile || sourceImageUrl),
      modeHint: args['prompt-mode'] || '',
      durationHint: args.duration || '',
      styleHint: args['prompt-style'] || '',
      cameraHint: args['prompt-camera'] || '',
      workdir,
    });
    promptPackResult = fallbackResult.promptPackResult;
    promptQuality = fallbackResult.promptQuality;

    if (isSimpleMode(readiness.mode)) {
      const panelContextPath = path.resolve(resolvedOutDir, 'panel-context.approved.json');
      const config = readJson(activeConfigPath);

      const startImageRef = sourceImageFile
        ? (fs.existsSync(sourceImageFile) ? sourceImageFile : '')
        : (sourceImageUrl || '');
      const panelContext = {
        panelId: `${episode}-p1`,
        panelIndex: 1,
        title: `Episode ${episode} - Direct Video Run`,
        imageUrl: startImageRef,
        videoPrompt: String(topic),
        subtitleText: String(topic),
        isMainClip: true,
      };
      writeJson(panelContextPath, panelContext);

      const duration = String(args.duration || config?.runtime?.时长秒数 || '6');
      const resolution = String(args.resolution || config?.runtime?.分辨率 || '720P');
      const wait = String(args.wait || 'false').toLowerCase() === 'true';
      const download = String(args.download || 'false').toLowerCase() === 'true';
      const chainResultPath = path.resolve(resolvedOutDir, wait ? 'video-submit-chain.poll.result.json' : 'video-submit-chain.result.json');

      const chainArgs = [
        '--config', activeConfigPath,
        '--panel', panelContextPath,
        '--out-dir', resolvedOutDir,
        '--duration', duration,
        '--resolution', resolution,
        '--wait', wait ? 'true' : 'false',
        '--download', download ? 'true' : 'false',
        '--result-json', chainResultPath,
      ];
      if (String(args.probe || '').toLowerCase() === 'true') {
        chainArgs.push('--probe');
      }

      const chainChild = runNodeScript(
        path.resolve(__dirname, 'run-video-submit-chain.cjs'),
        chainArgs,
        workdir,
      );

      if (chainChild.status !== 0) {
        console.error(chainChild.stderr || chainChild.stdout || 'simple video start failed');
        process.exit(chainChild.status || 1);
      }

      const chain = readJson(chainResultPath);
      const outputPath = resultJson || path.resolve(outDir, 'workflow.result.json');
      const result = {
        ok: true,
        currentStage: chain.currentStage || 'video-task-submitted',
        pipelineMode: readiness.mode,
        topic,
        episode,
        routing: readiness.route,
        configPath: activeConfigPath,
        configPatched: Boolean(readiness.effectiveConfigPatched),
        promptPack: promptPackResult.ok ? promptPackResult.promptPack : null,
        promptPackStatus: promptPackResult.ok ? 'ready' : 'failed',
        promptPackError: promptPackResult.ok ? '' : promptPackResult.error,
        promptQuality,
        promptFallback: fallbackResult.report,
        panelContext,
        submitResult: chain.submitResult || null,
        taskId: chain.taskId || '',
        latestPoll: chain.latestPoll || null,
        downloadResult: chain.downloadResult || null,
        artifacts: {
          panelContextPath,
          chainResultPath,
          promptPackPath: promptPackResult.promptPackPath,
          outDir: resolvedOutDir,
        },
        workflow: {
          action: 'start',
          driver: 'run-seedance-workflow.cjs',
          mode: readiness.mode,
        },
        nextStep: chain.nextStep || '可继续轮询并下载视频。',
      };
      writeJson(outputPath, result);
      return;
    }

    const child = runNodeScript(
      path.resolve(__dirname, 'run-seedance-entry.cjs'),
      [
        '--config', activeConfigPath,
        '--topic', topic,
        '--episode', episode,
        '--out-dir', outDir,
        '--result-json', resultJson || path.resolve(outDir, 'workflow.result.json'),
        ...(revisionNote ? ['--revision-note', revisionNote] : []),
        ...(sourceImageFile ? ['--reference-image-file', sourceImageFile] : []),
        ...(sourceImageUrl ? ['--reference-image-url', sourceImageUrl] : []),
      ],
      workdir,
    );

    if (child.status !== 0) {
      console.error(child.stderr || child.stdout || 'workflow start failed');
      process.exit(child.status || 1);
    }

    const outputPath = resultJson || path.resolve(outDir, 'workflow.result.json');
    const data = readJson(outputPath);
    data.routing = readiness.route;
    data.configPath = activeConfigPath;
    data.configPatched = Boolean(readiness.effectiveConfigPatched);
    data.promptPack = promptPackResult.ok ? promptPackResult.promptPack : null;
    data.promptPackStatus = promptPackResult.ok ? 'ready' : 'failed';
    data.promptPackError = promptPackResult.ok ? '' : promptPackResult.error;
    data.promptQuality = promptQuality;
    data.promptFallback = fallbackResult.report;
    data.artifacts = data.artifacts || {};
    data.artifacts.promptPackPath = promptPackResult.promptPackPath;
    data.workflow = { action: 'start', driver: 'run-seedance-workflow.cjs' };
    writeJson(resultJson || outputPath, data);
    return;
  }

  if (action === 'continue') {
    const statePath = args.state || args['entry-result'];
    const approval = args.approval || '';
    const panelIndex = args['panel-index'] || '1';
    const revisionNote = String(args['revision-note'] || '').trim();
    const firstImageStrategy = String(args['first-image-strategy'] || '').trim();
    const sourceImageFile = args['reference-image-file'] ? path.resolve(String(args['reference-image-file'])) : '';
    const sourceImageUrl = String(args['reference-image-url'] || '').trim();
    const forceVideoVendor = String(args['video-vendor'] || '').trim();
    const forceImageVendor = String(args['image-vendor'] || '').trim();
    const probeMode = parseBool(args.probe, false);
    if (!statePath) throw new Error('continue 模式需要 --state 或 --entry-result');
    const state = readJson(statePath);
    const stateSourceImageFile = String(state?.confirmationBundle?.sourceImage?.file || '').trim();
    const stateSourceImageUrl = String(state?.confirmationBundle?.sourceImage?.url || '').trim();
    const readiness = checkConfigReadiness(configPath, {
      referenceImageFile: sourceImageFile || stateSourceImageFile,
      referenceImageUrl: sourceImageUrl || stateSourceImageUrl,
      forceVideoVendor,
      forceImageVendor,
      outDir: path.dirname(path.resolve(statePath)),
    });
    if (!readiness.ready) {
      writeJson(resultJson || path.resolve(path.dirname(statePath), 'workflow.config-guidance.json'), {
        ok: false,
        currentStage: 'configuration-guidance',
        workflow: { action: 'continue', driver: 'run-seedance-workflow.cjs', blocked: true },
        pipelineMode: readiness.mode,
        missing: readiness.missing,
        guidance: readiness.guidance,
        routing: readiness.route,
      });
      return;
    }
    const activeConfigPath = readiness.effectiveConfigPath || path.resolve(configPath);

    if (state.currentStage === 'seedance-four-pack-confirm') {
      if (approval === 'revise-four-pack') {
        if (!revisionNote) {
          throw new Error('revise-four-pack 需要同时提供 --revision-note');
        }
        const topic = String(state?.confirmationBundle?.topic || state?.packResult?.topic || '').trim();
        const episode = String(state?.confirmationBundle?.episode || state?.packResult?.episode || 'E01').trim();
        const outDir = path.dirname(path.resolve(statePath));
        if (!topic) {
          throw new Error('无法从当前 state 提取 topic，不能执行 revise-four-pack');
        }

        const child = runNodeScript(
          path.resolve(__dirname, 'run-seedance-entry.cjs'),
          [
            '--config', activeConfigPath,
            '--topic', topic,
            '--episode', episode || 'E01',
            '--out-dir', outDir,
            '--result-json', resultJson || statePath,
            '--revision-note', revisionNote,
          ],
          workdir,
        );
        if (child.status !== 0) {
          console.error(child.stderr || child.stdout || 'workflow revise failed');
          process.exit(child.status || 1);
        }
        const outputPath = resultJson || statePath;
        const data = readJson(outputPath);
        data.routing = readiness.route;
        data.configPath = activeConfigPath;
        data.configPatched = Boolean(readiness.effectiveConfigPatched);
        data.workflow = { action: 'continue', driver: 'run-seedance-workflow.cjs', approval: 'revise-four-pack', revisionApplied: true };
        writeJson(resultJson || outputPath, data);
        return;
      }

      if (approval !== 'four-pack-approved') {
        throw new Error('当前阶段需要 --approval four-pack-approved 或 --approval revise-four-pack');
      }
      const child = runNodeScript(
        path.resolve(__dirname, 'continue-seedance-flow.cjs'),
        [
          '--config', activeConfigPath,
          '--entry-result', statePath,
          '--confirmed', 'true',
          '--panel-index', String(panelIndex),
          '--result-json', resultJson || path.resolve(path.dirname(statePath), 'workflow.continue.result.json'),
          ...(firstImageStrategy ? ['--first-image-strategy', firstImageStrategy] : []),
          ...(revisionNote ? ['--revision-note', revisionNote] : []),
          ...(sourceImageFile ? ['--reference-image-file', sourceImageFile] : []),
          ...(sourceImageUrl ? ['--reference-image-url', sourceImageUrl] : []),
        ],
        workdir,
      );
      if (child.status !== 0) {
        console.error(child.stderr || child.stdout || 'workflow continue failed');
        process.exit(child.status || 1);
      }
      const outputPath = resultJson || path.resolve(path.dirname(statePath), 'workflow.continue.result.json');
      const data = readJson(outputPath);

      if (data?.autoContinue && data?.currentStage === 'first-image-asset-confirm') {
        const afterPath = resultJson || path.resolve(path.dirname(statePath), 'workflow.after-first-image.auto.result.json');
        const autoChild = runNodeScript(
          path.resolve(__dirname, 'continue-after-first-image.cjs'),
          ['--config', activeConfigPath, '--state', outputPath, '--confirmed', 'true', '--result-json', afterPath],
          workdir,
        );
        if (autoChild.status !== 0) {
          console.error(autoChild.stderr || autoChild.stdout || 'workflow auto-continue failed');
          process.exit(autoChild.status || 1);
        }
        const afterData = readJson(afterPath);

        if (afterData?.currentStage === 'video-submit-ready' && afterData?.artifacts?.panelContextPath) {
          const submitOutDir = path.resolve(path.dirname(afterPath), 'video-submit-auto');
          const submitResultPath = path.resolve(submitOutDir, 'video-submit-chain.result.json');
          const submitArgs = [
            '--config', activeConfigPath,
            '--panel', afterData.artifacts.panelContextPath,
            '--out-dir', submitOutDir,
            '--wait', 'true',
            '--download', 'true',
            '--result-json', submitResultPath,
          ];
          if (probeMode) {
            submitArgs.push('--probe');
          }
          const submitChild = runNodeScript(
            path.resolve(__dirname, 'run-video-submit-chain.cjs'),
            submitArgs,
            workdir,
          );
          if (submitChild.status !== 0) {
            console.error(submitChild.stderr || submitChild.stdout || 'workflow auto video submit failed');
            process.exit(submitChild.status || 1);
          }
          const submitData = readJson(submitResultPath);
          submitData.routing = readiness.route;
          submitData.configPath = activeConfigPath;
          submitData.configPatched = Boolean(readiness.effectiveConfigPatched);
          submitData.workflow = { action: 'continue', driver: 'run-seedance-workflow.cjs', approval: 'four-pack-approved', autoContinued: true, autoSubmitted: true };
          writeJson(resultJson || submitResultPath, submitData);
          return;
        }

        afterData.routing = readiness.route;
        afterData.configPath = activeConfigPath;
        afterData.configPatched = Boolean(readiness.effectiveConfigPatched);
        afterData.workflow = { action: 'continue', driver: 'run-seedance-workflow.cjs', approval: 'four-pack-approved', autoContinued: true };
        writeJson(resultJson || afterPath, afterData);
        return;
      }

      data.routing = readiness.route;
      data.configPath = activeConfigPath;
      data.configPatched = Boolean(readiness.effectiveConfigPatched);
      data.workflow = { action: 'continue', driver: 'run-seedance-workflow.cjs', approval: 'four-pack-approved' };
      writeJson(resultJson || outputPath, data);
      return;
    }

    if (
      state.currentStage === 'first-image-confirm'
      || state.currentStage === 'first-image-internal-generated'
      || state.currentStage === 'first-image-asset-confirm'
    ) {
      if (approval === 'revise-first-image') {
        if (!revisionNote) {
          throw new Error('revise-first-image 需要同时提供 --revision-note');
        }
        const baseDir = path.dirname(path.resolve(statePath));
        const entryResultPath = path.resolve(baseDir, 'workflow.result.json');
        if (!fs.existsSync(entryResultPath)) {
          throw new Error(`重生首图时缺少 workflow.result.json: ${entryResultPath}`);
        }
        const revisedPanelIndex = String(state?.firstImageBundle?.panelIndex || panelIndex || '1');

        const child = runNodeScript(
          path.resolve(__dirname, 'continue-seedance-flow.cjs'),
          [
            '--config', activeConfigPath,
            '--entry-result', entryResultPath,
            '--confirmed', 'true',
            '--panel-index', revisedPanelIndex,
            '--result-json', resultJson || statePath,
            ...(firstImageStrategy ? ['--first-image-strategy', firstImageStrategy] : []),
            '--revision-note', revisionNote,
            ...(sourceImageFile ? ['--reference-image-file', sourceImageFile] : []),
            ...(sourceImageUrl ? ['--reference-image-url', sourceImageUrl] : []),
          ],
          workdir,
        );
        if (child.status !== 0) {
          console.error(child.stderr || child.stdout || 'workflow revise first-image failed');
          process.exit(child.status || 1);
        }
        const outputPath = resultJson || statePath;
        const data = readJson(outputPath);
        data.routing = readiness.route;
        data.configPath = activeConfigPath;
        data.configPatched = Boolean(readiness.effectiveConfigPatched);
        data.workflow = { action: 'continue', driver: 'run-seedance-workflow.cjs', approval: 'revise-first-image', revisionApplied: true };
        writeJson(resultJson || outputPath, data);
        return;
      }

      if (approval !== 'first-image-approved') {
        throw new Error('当前阶段需要 --approval first-image-approved 或 --approval revise-first-image');
      }
      const child = runNodeScript(
        path.resolve(__dirname, 'continue-after-first-image.cjs'),
        ['--config', activeConfigPath, '--state', statePath, '--confirmed', 'true', '--result-json', resultJson || path.resolve(path.dirname(statePath), 'workflow.after-first-image.result.json')],
        workdir,
      );
      if (child.status !== 0) {
        console.error(child.stderr || child.stdout || 'workflow continue failed');
        process.exit(child.status || 1);
      }
      const outputPath = resultJson || path.resolve(path.dirname(statePath), 'workflow.after-first-image.result.json');
      const data = readJson(outputPath);
      data.routing = readiness.route;
      data.configPath = activeConfigPath;
      data.configPatched = Boolean(readiness.effectiveConfigPatched);
      data.workflow = { action: 'continue', driver: 'run-seedance-workflow.cjs', approval: 'first-image-approved' };
      writeJson(resultJson || outputPath, data);
      return;
    }

    if (state.currentStage === 'first-image-asset-blocked') {
      if (approval !== 'retry-first-image') {
        throw new Error('当前阶段需要 --approval retry-first-image');
      }
      const panelIndex = String(state?.firstImageBundle?.panelIndex || args['panel-index'] || '1');
      const baseDir = path.dirname(path.resolve(statePath));
      const entryResultPath = path.resolve(baseDir, 'workflow.result.json');
      if (!fs.existsSync(entryResultPath)) {
        throw new Error(`重试首图时缺少 workflow.result.json: ${entryResultPath}`);
      }

      const child = runNodeScript(
        path.resolve(__dirname, 'continue-seedance-flow.cjs'),
        [
          '--config', activeConfigPath,
          '--entry-result', entryResultPath,
          '--confirmed', 'true',
          '--panel-index', panelIndex,
          '--result-json', resultJson || path.resolve(baseDir, 'workflow.continue.retry-first-image.result.json'),
          ...(firstImageStrategy ? ['--first-image-strategy', firstImageStrategy] : []),
          ...(revisionNote ? ['--revision-note', revisionNote] : []),
          ...(sourceImageFile ? ['--reference-image-file', sourceImageFile] : []),
          ...(sourceImageUrl ? ['--reference-image-url', sourceImageUrl] : []),
        ],
        workdir,
      );
      if (child.status !== 0) {
        console.error(child.stderr || child.stdout || 'workflow continue failed');
        process.exit(child.status || 1);
      }
      const outputPath = resultJson || path.resolve(baseDir, 'workflow.continue.retry-first-image.result.json');
      const data = readJson(outputPath);
      data.routing = readiness.route;
      data.configPath = activeConfigPath;
      data.configPatched = Boolean(readiness.effectiveConfigPatched);
      data.workflow = { action: 'continue', driver: 'run-seedance-workflow.cjs', approval: 'retry-first-image' };
      writeJson(resultJson || outputPath, data);
      return;
    }

    throw new Error(`当前 workflow driver 暂不支持从阶段继续: ${state.currentStage || 'unknown'}`);
  }

  throw new Error(`未知 action: ${action}`);
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}

