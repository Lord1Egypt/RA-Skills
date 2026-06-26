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

function asPosixRelative(targetPath, cwd) {
  const rel = path.relative(cwd, targetPath);
  if (!rel || rel.startsWith('..')) return targetPath;
  return `.${path.sep}${rel}`;
}

function quoteIfNeeded(value) {
  const text = String(value || '');
  return /\s/.test(text) ? `"${text}"` : text;
}

function makeContinueCommand({ configPath, statePath, approval, resultJsonPath, panelIndex, revisionNote }) {
  const parts = [
    'node',
    'scripts/run-seedance-workflow.cjs',
    '--action', 'continue',
    '--config', configPath,
    '--state', statePath,
    '--approval', approval,
  ];
  if (panelIndex !== undefined && panelIndex !== null) {
    parts.push('--panel-index', String(panelIndex));
  }
  if (resultJsonPath) {
    parts.push('--result-json', resultJsonPath);
  }
  if (revisionNote) {
    parts.push('--revision-note', revisionNote);
  }
  return parts.map(quoteIfNeeded).join(' ');
}

function makeVideoChainCommand({ configPath, panelPath, statePath, outDir, wait, download }) {
  const parts = [
    'node',
    'scripts/run-video-submit-chain.cjs',
    '--config', configPath,
  ];
  if (panelPath) {
    parts.push('--panel', panelPath);
  }
  if (statePath) {
    parts.push('--state', statePath);
  }
  if (outDir) {
    parts.push('--out-dir', outDir);
  }
  parts.push('--wait', wait ? 'true' : 'false');
  parts.push('--download', download ? 'true' : 'false');
  return parts.map(quoteIfNeeded).join(' ');
}

function buildPlan(stage, context) {
  const { state, statePath, configPath, cwd } = context;
  const stateDir = path.dirname(statePath);
  const normalizedConfig = asPosixRelative(configPath, cwd);
  const normalizedState = asPosixRelative(statePath, cwd);

  if (stage === 'seedance-four-pack-confirm') {
    const resultPath = asPosixRelative(path.resolve(stateDir, 'workflow.continue.result.json'), cwd);
    return {
      stage,
      summary: '等待用户确认四件套；确认后进入首图阶段。',
      checkpoint: '需要用户明确确认四件套通过。',
      dispatchActions: [
        {
          name: '用户确认后调度继续',
          when: '用户确认四件套通过',
          command: makeContinueCommand({
            configPath: normalizedConfig,
            statePath: normalizedState,
            approval: 'four-pack-approved',
            resultJsonPath: resultPath,
            panelIndex: 1,
          }),
        },
        {
          name: '用户给修改意见后重生四件套',
          when: '用户未通过四件套并给出修改提示',
          command: makeContinueCommand({
            configPath: normalizedConfig,
            statePath: normalizedState,
            approval: 'revise-four-pack',
            resultJsonPath: normalizedState,
            revisionNote: '<在这里写四件套修改意见>',
          }),
        },
      ],
    };
  }

  if (stage === 'first-image-asset-confirm' || stage === 'first-image-confirm' || stage === 'first-image-internal-generated') {
    const resultPath = asPosixRelative(path.resolve(stateDir, 'workflow.after-first-image.result.json'), cwd);
    return {
      stage,
      summary: '等待用户确认首图；确认后进入视频提交前预备。',
      checkpoint: '需要用户明确确认首图通过。',
      dispatchActions: [
        {
          name: '用户确认首图后调度继续',
          when: '用户确认首图通过',
          command: makeContinueCommand({
            configPath: normalizedConfig,
            statePath: normalizedState,
            approval: 'first-image-approved',
            resultJsonPath: resultPath,
          }),
        },
        {
          name: '用户给修改意见后重生首图',
          when: '用户未通过首图并给出修改提示',
          command: makeContinueCommand({
            configPath: normalizedConfig,
            statePath: normalizedState,
            approval: 'revise-first-image',
            resultJsonPath: normalizedState,
            revisionNote: '<在这里写首图修改意见>',
          }),
        },
      ],
    };
  }

  if (stage === 'first-image-asset-blocked') {
    const resultPath = asPosixRelative(path.resolve(stateDir, 'workflow.continue.retry-first-image.result.json'), cwd);
    return {
      stage,
      summary: '首图阶段被配置/输入阻塞；需先补配置，再触发重试。',
      checkpoint: '先确认阻塞原因已修复，再继续。',
      dispatchActions: [
        {
          name: '阻塞修复后调度重试首图',
          when: '确认 downstream 配置和首图输入均已补齐',
          command: makeContinueCommand({
            configPath: normalizedConfig,
            statePath: normalizedState,
            approval: 'retry-first-image',
            resultJsonPath: resultPath,
          }),
        },
      ],
    };
  }

  if (stage === 'video-submit-ready') {
    const panelPath = state?.artifacts?.panelContextPath ? asPosixRelative(path.resolve(state.artifacts.panelContextPath), cwd) : '';
    const outDir = asPosixRelative(stateDir, cwd);
    return {
      stage,
      summary: '已满足视频提交条件，可进入提交/轮询/下载链路。',
      checkpoint: '确认是否允许消耗正式视频额度。',
      dispatchActions: [
        {
          name: '仅提交（不等待）',
          when: '需要先占位任务，不等待完成',
          command: makeVideoChainCommand({
            configPath: normalizedConfig,
            panelPath,
            outDir,
            wait: false,
            download: false,
          }),
        },
        {
          name: '提交并等待到终态',
          when: '希望一轮拿到任务结果状态',
          command: `${makeVideoChainCommand({
            configPath: normalizedConfig,
            panelPath,
            outDir,
            wait: true,
            download: false,
          })} --max-polls 40 --interval-ms 15000`,
        },
      ],
    };
  }

  if (stage === 'video-task-submitted' || stage === 'video-task-processing' || stage === 'video-task-success') {
    const outDir = asPosixRelative(stateDir, cwd);
    return {
      stage,
      summary: '视频任务已提交，当前可从 state 继续轮询或下载。',
      checkpoint: '确认是否继续等待以及是否下载落地。',
      dispatchActions: [
        {
          name: '继续轮询',
          when: '任务未到 success/fail',
          command: `${makeVideoChainCommand({
            configPath: normalizedConfig,
            statePath: normalizedState,
            outDir,
            wait: true,
            download: false,
          })} --max-polls 40 --interval-ms 15000`,
        },
        {
          name: '成功后下载文件',
          when: '任务已 success 且需要落地 mp4',
          command: `${makeVideoChainCommand({
            configPath: normalizedConfig,
            statePath: normalizedState,
            outDir,
            wait: true,
            download: true,
          })} --output-file ${quoteIfNeeded(asPosixRelative(path.resolve(stateDir, 'raw', 'main-clip.mp4'), cwd))}`,
        },
      ],
    };
  }

  return {
    stage,
    summary: '当前阶段缺少预置调度模板。',
    checkpoint: '请先确认 stage 与输入 state 是否正确。',
    dispatchActions: [],
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const statePath = path.resolve(args.state || '');
  const outputPath = args.out ? path.resolve(args.out) : '';
  const cwd = process.cwd();

  if (!statePath) {
    throw new Error('用法: node build-dispatch-plan.cjs --state <state.json> [--config <pipeline.config.json>] [--out <plan.json>]');
  }
  if (!fs.existsSync(statePath)) {
    throw new Error(`state 文件不存在: ${statePath}`);
  }

  const state = readJson(statePath);
  const stage = String(state?.currentStage || '').trim();
  if (!stage) {
    throw new Error('state 缺少 currentStage');
  }

  const configPath = path.resolve(args.config || state?.configPath || './config/pipeline.config.json');
  const plan = buildPlan(stage, { state, stage, statePath, configPath, cwd });

  const result = {
    ok: true,
    mode: 'dispatch-only',
    principle: 'assistant-scheduling-only',
    statePath,
    configPath,
    generatedAt: new Date().toISOString(),
    ...plan,
  };

  writeJson(outputPath, result);
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
