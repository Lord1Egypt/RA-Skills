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

function commandExists(command) {
  const checker = process.platform === 'win32' ? 'where' : 'which';
  const res = spawnSync(checker, [command], { stdio: 'ignore' });
  return res.status === 0;
}

function runNodeScript(scriptPath, scriptArgs) {
  return spawnSync(process.execPath, [scriptPath, ...scriptArgs], {
    stdio: 'pipe',
    encoding: 'utf8',
    cwd: process.cwd(),
  });
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

function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = args.config;
  const statePath = args.state || args['entry-result'];
  const resultJson = args['result-json'];
  const confirmed = String(args.confirmed || '').toLowerCase();

  if (!configPath || !statePath) {
    throw new Error('用法: node continue-after-first-image.cjs --config <json> --state <json> --confirmed true [--result-json <json>]');
  }
  if (confirmed !== 'true' && confirmed !== 'yes' && confirmed !== '1') {
    throw new Error('继续首图确认后流程前，必须显式传入 --confirmed true');
  }

  const state = readJson(statePath);
  if (!['first-image-confirm', 'first-image-internal-generated', 'first-image-asset-confirm'].includes(String(state?.currentStage || '')) || !state?.firstImageBundle) {
    throw new Error('当前 state 不在首图确认阶段，无法继续');
  }

  const { full: fullConfigPath, config } = readConfig(configPath);
  const imageStage = config?.downstream?.waoo?.image;
  const videoStage = config?.downstream?.waoo?.video;
  const approvedImage = state?.firstImageAsset?.imageFile || state?.firstImageAsset?.imageUrl || state?.firstImageBundle?.approvedImage || state?.firstImageBundle?.imageUrl || '';
  const tsxAvailable = commandExists('tsx');
  const baseDir = path.dirname(path.resolve(statePath));
  const entryResultPath = path.resolve(baseDir, 'workflow.result.json');
  const panelContextPath = path.resolve(baseDir, 'panel-context.approved.json');
  const prepareResultPath = path.resolve(baseDir, 'prepare-submit.result.json');

  const panelContextArgs = ['--entry-result', entryResultPath, '--first-image-result', statePath];
  if (state?.firstImageAsset?.imageFile) {
    panelContextArgs.push('--approved-image-file', String(state.firstImageAsset.imageFile));
  }
  if (state?.firstImageAsset?.imageUrl) {
    panelContextArgs.push('--approved-image-url', String(state.firstImageAsset.imageUrl));
  }
  panelContextArgs.push('--out', panelContextPath);

  const panelContextChild = runNodeScript(
    path.resolve(__dirname, 'prepare-approved-panel-context.cjs'),
    panelContextArgs,
  );
  if (panelContextChild.status !== 0) {
    throw new Error(panelContextChild.stderr || panelContextChild.stdout || 'prepare-approved-panel-context failed');
  }

  const prepareSubmitChild = runNodeScript(
    path.resolve(__dirname, 'prepare-video-submit.cjs'),
    ['--config', configPath, '--panel', panelContextPath, '--out', prepareResultPath],
  );
  if (prepareSubmitChild.status !== 0 && prepareSubmitChild.status !== 2) {
    throw new Error(prepareSubmitChild.stderr || prepareSubmitChild.stdout || 'prepare-video-submit failed');
  }

  const panelContext = readJson(panelContextPath);
  const prepareResult = readJson(prepareResultPath);

  const readiness = {
    imageConfigReady: Boolean(imageStage?.厂商 && imageStage?.接口地址 && imageStage?.模型名 && !looksPlaceholder(imageStage?.APIKey)),
    approvedImageReady: Boolean(String(approvedImage || '').trim()),
    videoConfigReady: Boolean(videoStage?.厂商 && videoStage?.接口地址 && videoStage?.模型名 && !looksPlaceholder(videoStage?.APIKey)),
    tsxAvailable,
    panelContextReady: Boolean(panelContext?.panelId && Number.isFinite(Number(panelContext?.panelIndex))),
    prepareSubmitReady: Boolean(prepareResult?.ok),
    configPath: fullConfigPath,
  };

  const reasons = [...(prepareResult?.checkpoint?.reasons || [])];
  if (!readiness.imageConfigReady) {
    reasons.push('当前缺少可直跑的 downstream.waoo.image 配置，暂时还不能把已确认方向生成成正式首图产物。');
  }
  if (!readiness.approvedImageReady) {
    reasons.push('当前还没有正式锁定的 approved image 文件或 imageUrl，因此 panel context 仍处于方向已确认而非图片已确认状态。');
  }
  if (!readiness.videoConfigReady) {
    reasons.push('当前 downstream.waoo.video 仍未处于可直跑状态（例如 APIKey 仍是 demo / placeholder）。');
  }

  const uniqueReasons = [...new Set(reasons)];
  const blocked = !prepareResult?.ready;
  const output = {
    ok: true,
    blocked,
    currentStage: blocked ? 'video-submit-prepared-blocked' : 'video-submit-ready',
    autoContinue: false,
    readiness,
    panelContext,
    prepareSubmit: prepareResult,
    checkpoint: blocked
      ? {
          stage: 'first-image-approved',
          status: 'stop',
          summary: '首图方向已确认，skill 已完成内部 panel context 与视频提交前预备，但正式视频提交仍受未补齐条件阻塞。',
          reasons: uniqueReasons,
          nextStep: '补齐 approved image 与真实视频配置后，仍由 run-seedance-workflow.cjs 继续进入正式视频提交，不由 assistant 手工拼流程。',
        }
      : {
          stage: 'first-image-approved',
          status: 'pass',
          summary: '首图方向已确认，且已完成内部视频提交前预备，可继续进入正式视频提交。',
          reasons: uniqueReasons,
          nextStep: '继续调用统一 workflow driver 进入正式视频提交。',
        },
    statePath: path.resolve(statePath),
    artifacts: {
      panelContextPath,
      prepareResultPath,
    },
  };

  writeJson(resultJson, output);
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
