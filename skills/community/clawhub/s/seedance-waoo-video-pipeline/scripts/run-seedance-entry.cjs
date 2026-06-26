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

function writeJson(outputPath, data) {
  const text = JSON.stringify(data, null, 2);
  if (outputPath) {
    ensureDirForFile(outputPath);
    fs.writeFileSync(path.resolve(outputPath), text + '\n', 'utf8');
  }
  console.log(text);
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
}

function readText(filePath) {
  return fs.readFileSync(path.resolve(filePath), 'utf8');
}

function summarizeMarkdown(filePath, maxLines = 12) {
  const full = path.resolve(filePath);
  if (!fs.existsSync(full)) return '';
  const lines = fs.readFileSync(full, 'utf8').split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  return lines.slice(0, maxLines).join('\n');
}

function buildConfirmationBundle(result, sourceImage = {}) {
  return {
    title: result.title,
    topic: result.topic,
    episode: result.episode,
    files: result.files,
    sourceImage,
    previews: {
      intentBrief: summarizeMarkdown(result.files.intentBrief, 10),
      script: summarizeMarkdown(result.files.script, 18),
      assets: summarizeMarkdown(result.files.assets, 16),
      storyboard: summarizeMarkdown(result.files.storyboard, 20),
    },
    fullText: {
      intentBrief: readText(result.files.intentBrief),
      script: readText(result.files.script),
      assets: readText(result.files.assets),
      storyboard: readText(result.files.storyboard),
    },
    firstImageStrategy: {
      default: 'direct',
      options: {
        direct: '原图直绑（默认，身份一致、速度快）',
        img2img: '图生图（风格化重绘，可统一画风）',
      },
      note: '四件套确认后可切换首图策略：direct（原图直绑）或 img2img（图生图）。',
    },
    userPrompt: '请确认这套正式 Seedance 四件套。并选择首图策略：A 原图直绑（默认）/ B 图生图。未确认前，流程不会继续进入首图/视频生成。',
  };
}

function buildUserMessage(bundle) {
  return [
    `【${bundle.title}】正式 Seedance 四件套已生成，请先确认：`,
    '',
    '一、前置思考',
    bundle.fullText.intentBrief,
    '',
    '二、剧本',
    bundle.fullText.script,
    '',
    '三、素材清单',
    bundle.fullText.assets,
    '',
    '四、分镜',
    bundle.fullText.storyboard,
    '',
    '五、首图策略（可切换）',
    `- A 原图直绑（默认）：${bundle.firstImageStrategy?.options?.direct || '身份一致、速度快'}`,
    `- B 图生图：${bundle.firstImageStrategy?.options?.img2img || '风格化重绘，可统一画风'}`,
    `- 默认策略：${bundle.firstImageStrategy?.default || 'direct'}`,
    '',
    bundle.userPrompt,
  ].join('\n');
}

function buildFourPackCheckpoint(result, confirmationBundle) {
  return {
    stage: 'seedance-four-pack',
    status: 'confirm',
    summary: '正式 Seedance 四件套已生成，需先由用户确认后，才能继续首图/视频下游生产。',
    reasons: [
      '已生成 E01_前置思考.md',
      '已生成 E01_剧本.md',
      '已生成 E01_素材清单.md',
      '已生成 E01_分镜.md',
    ],
    nextStep: '把 confirmationBundle.userMessage 发给用户确认；用户确认前不得进入首图生成、panel 执行或视频提交。',
    confirmationBundle,
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const topic = args.topic;
  const configPath = args.config || './config/pipeline.config.json';
  const episode = args.episode || 'E01';
  const outDir = args['out-dir'] || `./work/seedance/${episode}`;
  const resultJson = args['result-json'];
  const clipCount = args['clip-count'] || '8';
  const style = args.style || '古装短剧写实风';
  const aspectRatio = args['aspect-ratio'] || '9:16';
  const revisionNote = String(args['revision-note'] || '').trim();
  const sourceImage = {
    file: args['reference-image-file'] ? path.resolve(String(args['reference-image-file'])) : '',
    url: String(args['reference-image-url'] || '').trim(),
  };

  if (!topic) {
    throw new Error('用法: node run-seedance-entry.cjs --config <json> --topic <题材> [--episode E01] [--out-dir <目录>] [--result-json <json>]');
  }

  const packResultPath = path.resolve(outDir, 'seedance-pack.result.json');
  ensureDirForFile(packResultPath);

  const child = spawnSync(
    process.execPath,
    [
      path.resolve(__dirname, 'generate-seedance-pack.cjs'),
      '--config', configPath,
      '--topic', topic,
      '--episode', episode,
      '--out-dir', outDir,
      '--result-json', packResultPath,
      '--clip-count', clipCount,
      '--style', style,
      '--aspect-ratio', aspectRatio,
      ...(revisionNote ? ['--revision-note', revisionNote] : []),
    ],
    { stdio: 'pipe', encoding: 'utf8', cwd: process.cwd() },
  );

  if (child.status !== 0) {
    const failure = {
      ok: false,
      stage: 'seedance-four-pack',
      status: 'stop',
      summary: '正式 Seedance 四件套生成失败，已停止后续流程。',
      reasons: [child.stderr || child.stdout || '未知错误'],
      nextStep: '先修正上游配置或生成错误，再重新进入入口脚本。',
    };
    writeJson(resultJson, failure);
    process.exit(child.status || 1);
  }

  const packResult = readJson(packResultPath);
  const confirmationBundle = buildConfirmationBundle(packResult, sourceImage);
  confirmationBundle.userMessage = buildUserMessage(confirmationBundle);
  const checkpoint = buildFourPackCheckpoint(packResult, confirmationBundle);
  const output = {
    ok: true,
    entry: 'seedance-auto-entry',
    currentStage: 'seedance-four-pack-confirm',
    autoContinue: false,
    confirmationRequired: true,
    checkpoint,
    confirmationBundle,
    packResult,
  };
  writeJson(resultJson, output);
}

try {
  main();
} catch (error) {
  const message = error && error.stack ? error.stack : String(error);
  console.error(message);
  process.exit(1);
}
