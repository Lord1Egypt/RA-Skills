#!/usr/bin/env node
/**
 * 离线测试：用 mock_server 覆盖 402 / 生成中 / 成功 / 失败 / 同订单重试。
 *
 * 不访问真实服务，不发起任何真实付款。
 * 运行：node tests/run_offline_tests.mjs
 */

import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SCRIPT = path.join(HERE, '..', 'scripts', 'travel_aipay.mjs');
const MOCK = path.join(HERE, 'mock_server.mjs');
const PORT = 8799;
const BASE = `http://127.0.0.1:${PORT}`;
const URL_RESOURCE = `${BASE}/aipay/travel_consultant`;

const passed = [];
const failed = [];

function check(name, condition, detail = '') {
  if (condition) {
    passed.push(name);
    console.log(`  PASS  ${name}`);
  } else {
    failed.push(`${name} ${detail}`);
    console.log(`  FAIL  ${name}  ${detail}`);
  }
}

function run(args, stateDir, expectCode) {
  const result = spawnSync(process.execPath, [SCRIPT, ...args, '--resource-url', URL_RESOURCE, '--state-dir', stateDir], {
    encoding: 'utf8',
  });
  if (result.status !== expectCode) {
    console.log(`    exit=${result.status} expect=${expectCode}\n    stdout=${String(result.stdout).slice(0, 1200)}\n    stderr=${String(result.stderr).slice(0, 1200)}`);
  }
  return result;
}

async function mockState() {
  const response = await fetch(`${BASE}/_state`);
  return response.json();
}

const BASE_ARGS = ['--query', '杭州三日亲子游', '--email', 'buyer@example.com', '--country-code', 'CN', '--topic-type', '7'];

async function waitForServer() {
  for (let i = 0; i < 60; i += 1) {
    try {
      await mockState();
      return;
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }
  throw new Error('mock server 未启动');
}

async function main() {
  const workDir = fs.mkdtempSync(path.join(os.tmpdir(), 'aipay-skill-test-'));
  const server = spawn(process.execPath, [MOCK, '--port', String(PORT)], { stdio: ['ignore', 'pipe', 'pipe'] });

  try {
    await waitForServer();

    console.log('\n[1] 402：无凭证取账单');
    const probe = run(['probe', ...BASE_ARGS], workDir, 0);
    check('probe 生成账单文件', fs.existsSync(path.join(workDir, 'payment-needed.txt')));
    check('probe 保存请求体', fs.existsSync(path.join(workDir, 'body.json')));
    check('probe 保存状态文件', fs.existsSync(path.join(workDir, 'state.json')));
    check('对客展示含订单号', probe.stdout.includes('订单号'), probe.stdout.slice(0, 200));
    check('提示确认后付款', probe.stdout.includes('--confirm'));
    let state = await mockState();
    check('未产生交付调用', state.deliverCount === 0, JSON.stringify(state));
    const mode = (fs.statSync(path.join(workDir, 'payment-needed.txt')).mode & 0o777).toString(8);
    check('账单文件仅本人可读写', mode === '600', mode);

    console.log('\n[2] 参数校验：缺 email 应拒绝且不发请求');
    const before = (await mockState()).quoteCount;
    const missing = run(['probe', '--query', '杭州三日游'], workDir, 2);
    check('缺 email 提示必填', String(missing.stderr).includes('email 必填'));
    check('未发送请求', (await mockState()).quoteCount === before);

    console.log('\n[3] 付款前拦截：pay 无 --confirm 不得付款');
    const payBlocked = run(['pay'], workDir, 2);
    check('未确认时拒绝付款', String(payBlocked.stderr).includes('未确认付款'));
    check('未调用官方 CLI', String(payBlocked.stderr).includes('未确认付款') && !String(payBlocked.stderr).includes('402-buyer-pay 已执行'));

    console.log('\n[4] 成功：带凭证交付');
    const ok = run(['complete', '--proof', 'ok'], workDir, 0);
    check('成功输出含正文', ok.stdout.includes('杭州三日亲子游'), ok.stdout.slice(0, 300));
    check('成功输出含 PDF 链接', ok.stdout.includes('example.invalid'));
    check('成功输出含幂等标记', ok.stdout.includes('幂等重放'));
    fs.copyFileSync(path.join(workDir, 'delivery.json'), path.join(workDir, 'success.json'));

    console.log('\n[5] 同订单重试：同凭证再交付');
    const retry = run(['complete', '--proof', 'ok'], workDir, 0);
    check('重试仍成功', retry.stdout.includes('交付成功'));
    check('重试标记已履约', retry.stdout.includes('幂等重放：是'), retry.stdout.slice(0, 300));
    state = await mockState();
    check('重试未新建账单', state.quoteCount === before, `${state.quoteCount} vs ${before}`);
    check('请求体内容保持一致', state.seenBodies.every((body) => body.query === '杭州三日亲子游'));

    console.log('\n[6] 支付处理中：409');
    const pending = run(['complete', '--proof', 'pending'], workDir, 3);
    check('409 提示生成中', String(pending.stderr).includes('生成中'));
    check('409 提示不要重新付款', String(pending.stderr).includes('不要重新付款'));
    check('409 带 Retry-After', String(pending.stderr).includes('30 秒'));
    check('409 说明预计 2–3 分钟', String(pending.stderr).includes('2–3 分钟'));
    check('409 给出同一订单查询命令', String(pending.stderr).includes('--out-shake-no'));
    check('409 提示结果会发邮箱', String(pending.stderr).includes('邮箱'));

    console.log('\n[7] 凭证无效：402');
    const invalid = run(['complete', '--proof', 'invalid'], workDir, 5);
    check('402 提示凭证失效', String(invalid.stderr).includes('凭证无效'));

    console.log('\n[8] 服务端错误：500');
    const errorCase = run(['complete', '--proof', 'error'], workDir, 6);
    check('500 归类服务端错误', String(errorCase.stderr).includes('服务端错误'));

    console.log('\n[9] 业务失败：200 但 resp_code=400');
    const bizfail = run(['complete', '--proof', 'bizfail'], workDir, 4);
    check('业务失败提示', String(bizfail.stderr).includes('业务失败'));
    check('业务失败原因透出', String(bizfail.stderr).includes('召回结果为空'));

    console.log('\n[10] dry-run 不发送请求');
    const beforeDry = (await mockState()).quoteCount;
    const dry = run(['probe', '--dry-run', ...BASE_ARGS], workDir, 0);
    check('dry-run 标记存在', dry.stdout.includes('[dry-run]'));
    check('dry-run 未发送', (await mockState()).quoteCount === beforeDry);

    console.log('\n[11] render 独立渲染');
    const rendered = spawnSync(process.execPath, [SCRIPT, 'render', '--response', path.join(workDir, 'success.json')], { encoding: 'utf8' });
    check('render 输出目的地', rendered.stdout.includes('杭州'), rendered.stdout.slice(0, 300));
    check('render 退出码 0', rendered.status === 0, String(rendered.status));

    console.log('\n[12] 参数越界拒绝');
    const outOfRange = run(['probe', '--query', 'x', '--email', 'a@b.co', '--topic-type', '99'], workDir, 2);
    check('topic_type 越界被拒', String(outOfRange.stderr).includes('取值范围非法'));

    console.log('\n[13] complete 缺少查询单号应拒绝');
    const noOrder = run(['complete'], workDir, 2);
    check('缺单号提示', String(noOrder.stderr).includes('缺少查询单号'));

    console.log('\n[14] 官方查询：409 → 瞬时失败 → 成功（--wait 自动轮询）');
    // 用假 alipay-bot 喂固定载荷：覆盖 409 / resourceResponse:null / 成功三种形状
    const businessResult = {
      resp_code: 200,
      resp_message: 'SUCCESS',
      data: {
        content: '杭州三日亲子游（自动轮询命中）',
        pdf_oss_file_url: 'https://example.invalid/travel.pdf',
        travel_destination: '杭州',
        ref_travel_infos: [],
      },
    };
    const fakeBot = path.join(workDir, 'fake-alipay-bot.mjs');
    fs.writeFileSync(
      fakeBot,
      `#!/usr/bin/env node\nimport fs from 'node:fs';\nconst queueFile = process.env.FAKE_BOT_QUEUE;\nconst queue = JSON.parse(fs.readFileSync(queueFile, 'utf8'));\nconst next = queue.shift() || { payload: {}, exitCode: 1 };\nfs.writeFileSync(queueFile, JSON.stringify(queue));\nprocess.stdout.write(JSON.stringify(next.payload, null, 2) + "\\n");\nprocess.exit(next.exitCode);\n`,
      { mode: 0o755 },
    );
    fs.chmodSync(fakeBot, 0o755);
    const queueFile = path.join(workDir, 'fake-bot-queue.json');
    const generatingPayload = {
      active: true,
      bizNo: 'X123',
      code: 207,
      errorCode: 'RESOURCE_DELIVERY_FAILED',
      errorMessage: 'paid resource request returned HTTP 409',
      paymentCompleted: true,
      resourceDelivered: false,
      resourceResponse: { status: 409 },
      success: false,
    };
    const transientPayload = {
      active: true,
      bizNo: 'X123',
      code: 207,
      errorCode: 'RESOURCE_REQUEST_FAILED',
      errorMessage: 'paid resource request failed before delivery',
      paymentCompleted: true,
      resourceDelivered: false,
      resourceResponse: null,
      success: false,
    };
    const successPayload = {
      active: true,
      bizNo: 'X123',
      success: true,
      tradeNo: 'T123',
      resourceResponse: {
        status: 200,
        body: {
          content: JSON.stringify(businessResult),
          already_fulfilled: true,
          fulfillment_confirmed: true,
          out_trade_no: 'AIPAY_X123',
          trade_no: 'T123',
          resource_id: '/aipay/travel_consultant',
        },
      },
    };
    fs.writeFileSync(queueFile, JSON.stringify([{ payload: generatingPayload, exitCode: 1 }, { payload: transientPayload, exitCode: 1 }, { payload: successPayload, exitCode: 0 }]));
    process.env.ALIPAY_BOT_BIN = fakeBot;
    process.env.FAKE_BOT_QUEUE = queueFile;

    const polled = run(['complete', '--out-shake-no', 'X123', '--wait', '--poll-interval-ms', '20'], workDir, 0);
    check('轮询最终交付成功', polled.stdout.includes('交付成功'), polled.stdout.slice(0, 400));
    check('成功判定不依赖 resourceDelivered', polled.stdout.includes('自动轮询命中'), polled.stdout.slice(0, 400));
    check('轮询次数已标注', polled.stdout.includes('轮询次数：3'), polled.stdout.slice(0, 600));
    check('瞬时失败不当作失败退出', !String(polled.stderr).includes('不要重新付款') || polled.status === 0);
    check('delivery.json 已落盘', fs.existsSync(path.join(workDir, 'delivery.json')));

    console.log('\n[15] 官方查询：未加 --wait 时 409 返回 3 并提示不要重新付款');
    fs.writeFileSync(queueFile, JSON.stringify([{ payload: generatingPayload, exitCode: 1 }]));
    const pendingQuery = run(['complete', '--out-shake-no', 'X123'], workDir, 3);
    check('409 提示生成中', String(pendingQuery.stderr).includes('方案生成中'));
    check('409 提示勿重新付款', String(pendingQuery.stderr).includes('请勿重新付款'));
    check('409 给出 --wait 建议', String(pendingQuery.stderr).includes('--wait'));

    console.log('\n[16] 官方查询：瞬时失败（resourceResponse=null）单独出现时归为服务端错误');
    fs.writeFileSync(queueFile, JSON.stringify([{ payload: transientPayload, exitCode: 1 }]));
    const transientOnly = run(['complete', '--out-shake-no', 'X123'], workDir, 6);
    check('瞬时失败提示可原样重跑', String(transientOnly.stderr).includes('原样重跑'), String(transientOnly.stderr).slice(0, 400));
    check('瞬时失败明确不重新付款', String(transientOnly.stderr).includes('不要重新付款'));

    delete process.env.ALIPAY_BOT_BIN;
    delete process.env.FAKE_BOT_QUEUE;
  } finally {
    server.kill('SIGTERM');
    fs.rmSync(workDir, { recursive: true, force: true });
  }

  console.log(`\n===== 结果：${passed.length} 通过，${failed.length} 失败 =====`);
  for (const item of failed) console.log(`  - ${item}`);
  return failed.length ? 1 : 0;
}

main().then(
  (code) => process.exit(code),
  (error) => {
    console.error(error);
    process.exit(1);
  },
);
