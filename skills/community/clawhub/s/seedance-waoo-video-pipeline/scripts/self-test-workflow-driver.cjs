const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { spawnSync } = require('node:child_process');

/**
 * 解析命令行参数（--key value）
 */
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

/**
 * 写入 JSON 文件并确保目录存在
 */
function writeJson(filePath, data) {
  const full = path.resolve(filePath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

/**
 * 执行 Node 脚本并返回标准输出/错误
 */
function runNode(scriptPath, scriptArgs, cwd) {
  return spawnSync(process.execPath, [scriptPath, ...scriptArgs], {
    cwd,
    stdio: 'pipe',
    encoding: 'utf8',
  });
}

/**
 * 断言文本包含关键词
 */
function contains(text, keyword) {
  return String(text || '').includes(keyword);
}

/**
 * 构建一条用例执行结果
 */
function buildCaseResult(name, passed, details) {
  return {
    case: name,
    passed,
    details,
  };
}

/**
 * 运行单条阶段/审批映射用例
 */
function runCase({ name, driverPath, configPath, statePath, approval, expectedExitNonZero = true, expectedText }) {
  const args = [
    '--action', 'continue',
    '--config', configPath,
    '--state', statePath,
    '--approval', approval,
  ];
  const result = runNode(driverPath, args, process.cwd());
  const merged = `${result.stdout || ''}\n${result.stderr || ''}`;
  const exitOk = expectedExitNonZero ? result.status !== 0 : result.status === 0;
  const textOk = expectedText ? contains(merged, expectedText) : true;
  return buildCaseResult(name, exitOk && textOk, {
    exitCode: result.status,
    expectedExitNonZero,
    expectedText,
    outputPreview: merged.slice(0, 400),
  });
}

/**
 * 主执行入口
 */
function main() {
  const args = parseArgs(process.argv.slice(2));
  const driverPath = path.resolve(args.driver || path.resolve(__dirname, 'run-seedance-workflow.cjs'));
  const workRoot = path.resolve(args['work-dir'] || path.join(os.tmpdir(), `seedance-driver-selftest-${Date.now()}`));

  fs.mkdirSync(workRoot, { recursive: true });

  const configPath = path.resolve(args.config || path.join(workRoot, 'selftest.config.json'));
  if (!args.config) {
    writeJson(configPath, {
      runtime: {
        pipelineMode: 'seedance_simple',
      },
      downstream: {
        waoo: {
          video: {
            厂商: 'seedance',
            接口地址: 'https://ark.cn-beijing.volces.com',
            模型名: 'doubao-seedance-1-5-pro-250428',
            APIKey: 'selftest-key',
          },
        },
      },
    });
  }

  const stageFourPackPath = path.join(workRoot, 'state.four-pack.json');
  const stageFirstImagePath = path.join(workRoot, 'state.first-image-confirm.json');
  const stageBlockedPath = path.join(workRoot, 'state.first-image-blocked.json');
  const stageUnknownPath = path.join(workRoot, 'state.unknown.json');

  writeJson(stageFourPackPath, { currentStage: 'seedance-four-pack-confirm' });
  writeJson(stageFirstImagePath, { currentStage: 'first-image-asset-confirm', firstImageBundle: { panelIndex: 1 } });
  writeJson(stageBlockedPath, { currentStage: 'first-image-asset-blocked', firstImageBundle: { panelIndex: 2 } });
  writeJson(stageUnknownPath, { currentStage: 'unknown-stage' });

  const results = [];

  results.push(runCase({
    name: 'four-pack 阶段拒绝错误审批',
    driverPath,
    configPath,
    statePath: stageFourPackPath,
    approval: 'first-image-approved',
    expectedText: '当前阶段需要 --approval four-pack-approved',
  }));

  results.push(runCase({
    name: '首图确认阶段拒绝错误审批',
    driverPath,
    configPath,
    statePath: stageFirstImagePath,
    approval: 'four-pack-approved',
    expectedText: '当前阶段需要 --approval first-image-approved',
  }));

  results.push(runCase({
    name: '首图阻塞阶段拒绝错误审批',
    driverPath,
    configPath,
    statePath: stageBlockedPath,
    approval: 'first-image-approved',
    expectedText: '当前阶段需要 --approval retry-first-image',
  }));

  results.push(runCase({
    name: '首图阻塞阶段接受 retry 审批并进入重试分支',
    driverPath,
    configPath,
    statePath: stageBlockedPath,
    approval: 'retry-first-image',
    expectedText: '重试首图时缺少 workflow.result.json',
  }));

  results.push(runCase({
    name: '未知阶段拒绝继续',
    driverPath,
    configPath,
    statePath: stageUnknownPath,
    approval: 'first-image-approved',
    expectedText: '当前 workflow driver 暂不支持从阶段继续',
  }));

  const passed = results.every((item) => item.passed);
  const summary = {
    ok: passed,
    total: results.length,
    passed: results.filter((item) => item.passed).length,
    failed: results.filter((item) => !item.passed).length,
    driverPath,
    configPath,
    workRoot,
    results,
  };

  console.log(JSON.stringify(summary, null, 2));
  if (!passed) {
    process.exit(1);
  }
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
