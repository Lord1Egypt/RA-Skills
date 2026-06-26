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

function deriveProjectId(entry) {
  const outputDir = entry?.packResult?.outputDir || '';
  if (outputDir) {
    const parent = path.basename(path.dirname(path.resolve(outputDir)));
    if (parent) return parent;
  }
  return 'seedance-project';
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const entryResultPath = args['entry-result'];
  const firstImageResultPath = args['first-image-result'];
  const approvedImageFile = args['approved-image-file'] || '';
  const approvedImageUrl = args['approved-image-url'] || '';
  const outputPath = args.out;

  if (!entryResultPath || !firstImageResultPath) {
    throw new Error('用法: node prepare-approved-panel-context.cjs --entry-result <json> --first-image-result <json> [--approved-image-file <file>|--approved-image-url <url>] [--out <json>]');
  }

  const entry = readJson(entryResultPath);
  const firstImageState = readJson(firstImageResultPath);
  const bundle = entry?.confirmationBundle;
  const firstImage = firstImageState?.firstImageBundle || firstImageState;
  if (!bundle || !firstImage) {
    throw new Error('缺少四件套确认结果或首图确认结果');
  }

  const panelIndex = Number(firstImage.panelIndex || 1);
  const episodeId = String(bundle.episode || entry?.packResult?.episode || 'E01');
  const panelId = `${episodeId}-P${String(panelIndex).padStart(2, '0')}`;
  const resolvedImage = approvedImageUrl
    ? String(approvedImageUrl)
    : approvedImageFile
      ? path.resolve(approvedImageFile)
      : '';

  const result = {
    projectId: deriveProjectId(entry),
    episodeId,
    panelId,
    panelIndex,
    panelTitle: String(firstImage.panelTitle || ''),
    imageUrl: resolvedImage,
    videoPrompt: String(firstImage.promptText || ''),
    subtitleText: String(firstImage.subtitleCandidate || ''),
    existingVideoUrl: '',
    isMainClip: panelIndex === 1,
    stateLabel: resolvedImage ? 'image-approved' : 'first-image-direction-approved',
    sources: {
      entryResult: path.resolve(entryResultPath),
      firstImageResult: path.resolve(firstImageResultPath),
      approvedImageFile: approvedImageFile ? path.resolve(approvedImageFile) : '',
      approvedImageUrl: approvedImageUrl || '',
    },
  };

  writeJson(outputPath, result);
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
