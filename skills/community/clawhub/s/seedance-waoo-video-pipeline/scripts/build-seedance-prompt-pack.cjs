const fs = require('node:fs');
const path = require('node:path');

const SCENE_TEMPLATES = {
  general: {
    name: '通用叙事',
    style: '电影感写实，细节清晰，色彩统一',
    camera: '中近景推进 + 关键动作特写 + 收束全景',
    negatives: [
      '避免画面闪烁、人物面部崩坏、文字水印、镜头跳变',
      '避免与主题无关元素和突兀转场',
    ],
  },
  ecommerce: {
    name: '电商展示',
    style: '产品高质感写实，主体突出，背景干净',
    camera: '产品全景开场 + 细节微距 + 使用场景切换 + 品牌收束镜头',
    negatives: [
      '避免产品外观变形与品牌信息错位',
      '避免背景杂乱和主体遮挡',
    ],
  },
  narrative: {
    name: '剧情短片',
    style: '电影化叙事，人物情绪清晰，光影层次明显',
    camera: '建立镜头 + 冲突推进 + 情绪特写 + 转折收束',
    negatives: [
      '避免人物前后不一致',
      '避免镜头语义断裂和节奏失衡',
    ],
  },
  mv: {
    name: '音乐MV',
    style: '节奏驱动、风格化光效、动作连贯',
    camera: '节拍切镜 + 跟拍运动 + 情绪特写 + 高频转场',
    negatives: [
      '避免节拍错位与卡点失真',
      '避免口型与节奏明显不匹配',
    ],
  },
  tutorial: {
    name: '讲解演示',
    style: '清晰教学风，重点信息突出，镜头稳定',
    camera: '步骤全景 + 关键步骤特写 + 结果对比镜头',
    negatives: [
      '避免关键步骤被遮挡',
      '避免信息噪声与无关特效',
    ],
  },
};

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

function parseBool(value, fallback = false) {
  if (value === undefined) return fallback;
  if (value === true) return true;
  const text = String(value || '').trim().toLowerCase();
  if (!text) return fallback;
  return ['1', 'true', 'yes', 'y', 'on'].includes(text);
}

function clamp(n, min, max) {
  return Math.max(min, Math.min(max, n));
}

function toInt(value, fallback) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  return Math.floor(n);
}

function normalizeMode(mode, hasReferenceImage) {
  const value = String(mode || '').trim().toLowerCase();
  if (['text-only', 'first-last-frame', 'all-reference'].includes(value)) {
    return value;
  }
  return hasReferenceImage ? 'first-last-frame' : 'text-only';
}

function normalizeScenario(scenario) {
  const key = String(scenario || 'general').trim().toLowerCase();
  if (SCENE_TEMPLATES[key]) return key;
  return 'general';
}

function buildAssets(hasReferenceImage, mode) {
  return {
    referenceImage: {
      required: mode !== 'text-only',
      provided: Boolean(hasReferenceImage),
      notes: mode === 'text-only' ? '当前模式不依赖首图' : '用于锁定角色风格和构图连续性',
    },
    script: {
      required: true,
      notes: '使用四件套中的剧本摘要与分镜语义做生成约束',
    },
  };
}

function scenarioShotText(scenario, index) {
  const m = {
    general: ['建立镜头：交代场景与主体', '推进镜头：突出冲突与动作', '转折镜头：强化情绪与节奏', '高潮镜头：动作或对抗爆发', '收束镜头：落点与余韵'],
    ecommerce: ['产品主视觉开场', '核心卖点特写', '使用场景展示', '对比/细节强化', '品牌落版收束'],
    narrative: ['世界观建立', '人物冲突推进', '情绪爆点', '关键动作反转', '结尾悬念或落点'],
    mv: ['节拍开场镜头', '主旋律动作推进', '副歌情绪抬升', '高频切镜高潮', '尾段收束'],
    tutorial: ['步骤总览', '步骤一特写', '步骤二特写', '结果对比', '结论回收'],
  };
  const list = m[scenario] || m.general;
  return list[Math.min(index, list.length - 1)] || '关键镜头';
}

function buildBeats(duration, scenario) {
  const sec = clamp(toInt(duration, 10), 4, 20);
  const step = sec <= 8 ? 2 : 3;
  const beats = [];
  let t = 0;
  let idx = 1;
  while (t < sec) {
    const end = Math.min(sec, t + step);
    beats.push({
      id: `B${idx}`,
      start: t,
      end,
      shot: scenarioShotText(scenario, idx - 1),
    });
    idx += 1;
    t = end;
  }
  return beats;
}

function buildPrompt({ topic, mode, duration, style, camera, beats, negatives, scenarioName }) {
  const beatLines = beats
    .map((b) => `- ${String(b.start).padStart(2, '0')}-${String(b.end).padStart(2, '0')}s: ${b.shot}`)
    .join('\n');

  const negativeLines = negatives.map((n) => `- ${n}`).join('\n');

  return [
    '[目标]',
    `围绕主题“${topic}”生成 ${duration}s 的短视频，保持叙事清晰、镜头连贯。`,
    '',
    '[场景模板]',
    `${scenarioName}`,
    '',
    '[模式]',
    `使用模式：${mode}（text-only / first-last-frame / all-reference）。`,
    '',
    '[镜头与动作]',
    `主镜头语言：${camera}`,
    `视觉风格：${style}`,
    '',
    '[时间节拍（Timecoded Beats）]',
    beatLines,
    '',
    '[负面约束]',
    negativeLines,
    '',
    '[输出要求]',
    '- 画面主体清晰，动作可读，镜头过渡自然。',
    '- 成片可直接进入字幕/配音后处理。',
  ].join('\n');
}

function writeJson(outputPath, data) {
  const text = JSON.stringify(data, null, 2);
  if (outputPath) {
    const full = path.resolve(outputPath);
    fs.mkdirSync(path.dirname(full), { recursive: true });
    fs.writeFileSync(full, `${text}\n`, 'utf8');
  }
  console.log(text);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const topic = String(args.topic || '').trim();
  if (!topic) throw new Error('build-seedance-prompt-pack 需要 --topic');

  const duration = clamp(toInt(args.duration, 10), 4, 20);
  const hasReferenceImage = parseBool(args['has-reference-image'], false);
  const mode = normalizeMode(args.mode, hasReferenceImage);
  const scenario = normalizeScenario(args.scenario);
  const template = SCENE_TEMPLATES[scenario];

  const style = String(args.style || template.style).trim();
  const camera = String(args.camera || template.camera).trim();
  const beats = buildBeats(duration, scenario);
  const assets = buildAssets(hasReferenceImage, mode);
  const negatives = template.negatives;
  const prompt = buildPrompt({
    topic,
    mode,
    duration,
    style,
    camera,
    beats,
    negatives,
    scenarioName: template.name,
  });

  const data = {
    ok: true,
    version: 'prompt-pack.v2',
    topic,
    scenario,
    scenarioName: template.name,
    duration,
    mode,
    style,
    camera,
    assets,
    beats,
    negatives,
    prompt,
    notes: [
      '该输出用于 run-seedance-workflow 前置提示词工程层。',
      '可用 --scenario 在 general/ecommerce/narrative/mv/tutorial 间切换。',
    ],
  };

  writeJson(args['result-json'], data);
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
