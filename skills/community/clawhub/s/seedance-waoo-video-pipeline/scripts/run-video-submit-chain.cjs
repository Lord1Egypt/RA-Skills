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

function toBool(value, defaultValue = false) {
  if (value === undefined) return defaultValue;
  if (value === true) return true;
  const text = String(value).trim().toLowerCase();
  if (!text) return defaultValue;
  return ['1', 'true', 'yes', 'y', 'on'].includes(text);
}

function toInt(value, defaultValue) {
  const num = Number(value);
  return Number.isFinite(num) ? Math.floor(num) : defaultValue;
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

function trimSlash(url) {
  return String(url || '').replace(/\/+$/, '');
}

function canonicalVendor(name) {
  const value = String(name || '').trim().toLowerCase();
  if (!value) return '';
  if (value.includes('minimax') || value.includes('mini max')) return 'minimax';
  if (value.includes('vidu')) return 'vidu';
  if (value.includes('seedance') || value.includes('doubao') || value.includes('ark') || value.includes('volc')) return 'seedance';
  return value;
}

function mapMinimaxStatus(value) {
  const status = String(value || '').toLowerCase();
  if (status === 'success') return 'success';
  if (status === 'fail' || status === 'failed') return 'fail';
  if (status === 'preparing' || status === 'queue' || status === 'queued') return 'queued';
  return 'processing';
}

function runNodeScript(scriptPath, scriptArgs, cwd) {
  return spawnSync(process.execPath, [scriptPath, ...scriptArgs], {
    stdio: 'pipe',
    encoding: 'utf8',
    cwd,
  });
}

function commandExists(command) {
  const checker = process.platform === 'win32' ? 'where' : 'which';
  const res = spawnSync(checker, [command], { stdio: 'ignore' });
  return res.status === 0;
}

function getPollScript() {
  const cjsPath = path.resolve(__dirname, 'poll-official-video.cjs');
  const tsPath = path.resolve(__dirname, 'poll-official-video.ts');
  if (fs.existsSync(cjsPath)) return { type: 'node', script: cjsPath };
  if (!commandExists('tsx')) {
    throw new Error('缺少 poll-official-video.cjs 且当前环境没有 tsx，无法执行轮询。');
  }
  return { type: 'tsx', script: tsPath };
}

function getDownloadScript() {
  const cjsPath = path.resolve(__dirname, 'download-official-video.cjs');
  const tsPath = path.resolve(__dirname, 'download-official-video.ts');
  if (fs.existsSync(cjsPath)) return { type: 'node', script: cjsPath };
  if (!commandExists('tsx')) {
    throw new Error('缺少 download-official-video.cjs 且当前环境没有 tsx，无法执行下载。');
  }
  return { type: 'tsx', script: tsPath };
}

function runScriptEntry(entry, args, cwd) {
  if (entry.type === 'node') {
    return runNodeScript(entry.script, args, cwd);
  }
  return spawnSync('tsx', [entry.script, ...args], {
    stdio: 'pipe',
    encoding: 'utf8',
    cwd,
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function pollUntilTerminal({ configPath, taskId, isProbe, outDir, wait, maxPolls, intervalMs, downloadOnSuccess, outputFile, cwd }) {
  const pollHistory = [];
  let latest = null;
  let currentStage = 'video-task-submitted';

  if (!wait) {
    return {
      ok: true,
      currentStage,
      pollHistory,
      latestPoll: null,
      downloadResult: null,
      nextStep: '需要时可再次调用 run-video-submit-chain.cjs 并传入 --state 继续轮询/下载。',
    };
  }

  const pollScript = getPollScript();
  const downloadScript = downloadOnSuccess ? getDownloadScript() : null;

  for (let i = 0; i < maxPolls; i += 1) {
    const pollResultPath = path.resolve(outDir, `video-poll.${taskId}.${i + 1}.json`);
    const args = ['--config', configPath, '--task-id', taskId, '--out', pollResultPath];
    if (isProbe) args.push('--probe');

    const child = runScriptEntry(pollScript, args, cwd);
    if (child.status !== 0) {
      throw new Error(child.stderr || child.stdout || '视频轮询失败');
    }

    latest = readJson(pollResultPath);
    pollHistory.push({
      attempt: i + 1,
      status: latest.status,
      fileId: latest.fileId || '',
      pollResultPath,
      at: new Date().toISOString(),
    });

    if (latest.status === 'success') {
      currentStage = 'video-task-success';
      break;
    }

    if (latest.status === 'fail') {
      currentStage = 'video-task-failed';
      return {
        ok: false,
        currentStage,
        pollHistory,
        latestPoll: latest,
        downloadResult: null,
        nextStep: '检查模型/提示词/配额后重试提交。',
      };
    }

    currentStage = 'video-task-processing';
    if (i < maxPolls - 1) {
      await sleep(intervalMs);
    }
  }

  if (currentStage !== 'video-task-success') {
    return {
      ok: true,
      currentStage: 'video-task-processing',
      pollHistory,
      latestPoll: latest,
      downloadResult: null,
      nextStep: '任务仍在处理中；后续可用 --state 继续轮询。',
    };
  }

  if (!downloadOnSuccess) {
    return {
      ok: true,
      currentStage: 'video-task-success',
      pollHistory,
      latestPoll: latest,
      downloadResult: null,
      nextStep: '已到 success；如需落地 mp4 可再次调用并开启 --download。',
    };
  }

  const fileId = String(latest?.fileId || '');
  if (!fileId) {
    throw new Error('轮询成功但缺少 fileId，无法下载。');
  }

  const resolvedOutputFile = path.resolve(outputFile || path.join(outDir, 'raw', 'main-clip.mp4'));
  const downloadResultJson = path.resolve(outDir, `video-download.${taskId}.json`);
  const downloadArgs = [
    '--config', configPath,
    '--task-id', taskId,
    '--file-id', fileId,
    '--out', resolvedOutputFile,
    '--result-json', downloadResultJson,
  ];
  if (isProbe) downloadArgs.push('--probe');

  const downloadChild = runScriptEntry(downloadScript, downloadArgs, cwd);
  if (downloadChild.status !== 0) {
    throw new Error(downloadChild.stderr || downloadChild.stdout || '视频下载失败');
  }

  const downloadResult = readJson(downloadResultJson);
  return {
    ok: true,
    currentStage: 'video-file-downloaded',
    pollHistory,
    latestPoll: latest,
    downloadResult,
    nextStep: '视频已下载，可继续进入字幕/TTS/环境音与最终合成。',
  };
}

function loadVideoStage(configPath) {
  const config = readJson(configPath);
  const stage = config?.downstream?.waoo?.video;
  if (!stage?.厂商 || !stage?.接口地址 || !stage?.模型名 || !stage?.APIKey) {
    throw new Error('视频配置不完整，请先补齐 downstream.waoo.video 的 厂商/接口地址/模型名/APIKey');
  }
  const vendor = canonicalVendor(stage.厂商);
  if (!['minimax', 'vidu', 'seedance'].includes(vendor)) {
    throw new Error(`当前 run-video-submit-chain 仅支持 MiniMax / Vidu / Seedance，收到: ${stage.厂商}`);
  }
  return stage;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = path.resolve(args.config || './config/pipeline.config.json');
  const statePath = args.state ? path.resolve(args.state) : '';
  const panelPath = args.panel ? path.resolve(args.panel) : '';
  const outDir = path.resolve(args['out-dir'] || (statePath ? path.dirname(statePath) : process.cwd()));
  const resultJson = args['result-json'] ? path.resolve(args['result-json']) : '';
  const wait = toBool(args.wait, false);
  const downloadOnSuccess = toBool(args.download, false);
  const isProbe = toBool(args.probe, false);
  const maxPolls = toInt(args['max-polls'], 40);
  const intervalMs = toInt(args['interval-ms'], 15000);
  const outputFile = args['output-file'] ? path.resolve(args['output-file']) : '';

  if (!fs.existsSync(configPath)) {
    throw new Error(`配置文件不存在: ${configPath}`);
  }
  loadVideoStage(configPath);

  let submitResult = null;
  let taskId = '';
  let bootstrap = { mode: '', source: '' };

  if (statePath) {
    if (!fs.existsSync(statePath)) {
      throw new Error(`state 文件不存在: ${statePath}`);
    }
    const state = readJson(statePath);
    submitResult = state?.submitResult || null;
    taskId = String(state?.submitResult?.taskId || state?.taskId || state?.latestPoll?.taskId || '').trim();
    if (!taskId) {
      throw new Error('从 state 恢复时缺少 taskId/submitResult.taskId，无法继续。');
    }
    bootstrap = { mode: 'resume', source: statePath };
  } else {
    if (!panelPath) {
      throw new Error('新提交模式需要 --panel；恢复模式可传 --state。');
    }
    if (!fs.existsSync(panelPath)) {
      throw new Error(`panel 文件不存在: ${panelPath}`);
    }

    const submitOut = path.resolve(outDir, 'video-submit.result.json');
    const submitArgs = ['--config', configPath, '--panel', panelPath, '--out', submitOut];
    if (args.duration) submitArgs.push('--duration', String(args.duration));
    if (args.resolution) submitArgs.push('--resolution', String(args.resolution));
    if (isProbe) submitArgs.push('--probe');

    const child = runNodeScript(path.resolve(__dirname, 'submit-official-video.cjs'), submitArgs, process.cwd());
    if (child.status !== 0) {
      throw new Error(child.stderr || child.stdout || '正式视频提交失败');
    }

    submitResult = readJson(submitOut);
    taskId = String(submitResult?.taskId || '').trim();
    if (!taskId) {
      throw new Error('视频提交结果缺少 taskId');
    }
    bootstrap = { mode: 'submit', source: submitOut };
  }

  const chainResult = await pollUntilTerminal({
    configPath,
    taskId,
    isProbe,
    outDir,
    wait,
    maxPolls,
    intervalMs,
    downloadOnSuccess,
    outputFile,
    cwd: process.cwd(),
  });

  const result = {
    ok: chainResult.ok,
    currentStage: chainResult.currentStage,
    submitResult,
    taskId,
    latestPoll: chainResult.latestPoll,
    pollHistory: chainResult.pollHistory,
    downloadResult: chainResult.downloadResult,
    bootstrap,
    configPath,
    outDir,
    wait,
    downloadOnSuccess,
    isProbe,
    nextStep: chainResult.nextStep,
  };

  writeJson(resultJson || path.resolve(outDir, 'video-submit-chain.result.json'), result);

  if (!result.ok) {
    process.exit(2);
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
