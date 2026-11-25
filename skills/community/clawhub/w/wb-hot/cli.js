#!/usr/bin/env node
'use strict';
/** 微博热榜采集 CLI：服务端直接 HTTP 采集，无需微博登录态；每次 1 点数。 */
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { ApiClient, BizError, allowInsecureTls } = require('./src/client');
const { loadConfig, saveConfig, resolveConfig, maskToken, configPaths, DEFAULT_BASE_URL } = require('./src/config');
const { UsageError, printOk, printFail, exitWithError, pollTask, parsePositiveNumber } = require('./src/output');

const CAPABILITY = 'wb_hot';
const VERSION = '1.0.0';
const DEFAULT_PRICE = 1;
const DOWNLOAD_TIMEOUT_MS = 60000;
const VALUE_FLAGS = new Set(['interval', 'timeout', 'token', 'base-url', 'access-token', 'out']);
const BOOL_FLAGS = new Set(['wait', 'help', 'link', 'check', 'force', 'version']);

function camel(s) { return s.replace(/-([a-z])/g, (_, c) => c.toUpperCase()); }

function parseArgs(argv) {
  const opts = {}, positional = [];
  for (let i = 0; i < argv.length; i++) {
    let arg = argv[i];
    if (!arg.startsWith('-')) { positional.push(arg); continue; }
    if (!arg.startsWith('--')) throw new UsageError(`未知参数: ${arg}`);
    let inline;
    const eq = arg.indexOf('=');
    if (eq > 2) { inline = arg.slice(eq + 1); arg = arg.slice(0, eq); }
    const name = arg.slice(2);
    if (VALUE_FLAGS.has(name)) {
      const value = inline !== undefined ? inline : argv[++i];
      if (value === undefined) throw new UsageError(`缺少参数值: ${arg}`);
      opts[camel(name)] = value;
    } else if (BOOL_FLAGS.has(name)) {
      if (inline !== undefined) throw new UsageError(`参数 ${arg} 不接受值`);
      opts[camel(name)] = true;
    } else throw new UsageError(`未知参数: ${arg}`);
  }
  return { cmd: positional.shift() || '', args: positional, opts };
}

const USAGE = `微博热榜采集 CLI（服务端直接 HTTP 采集，无需微博登录态）

用法: node cli.js <命令> [参数]

命令:
  register --link                     生成注册二维码/链接（注册即送 10 点数）
  register --check --access-token <串> 完成注册后确认并保存 token
  login --link                        生成登录二维码/链接
  login --check --access-token <串>   完成授权后确认并保存 token
  submit [--wait] [--force]           提交一次热榜采集（每次 1 点数）
                                      --force 跳过 24h 去重，重新采集最新热榜
  query <task_id> [--wait]            查询任务状态与完整热榜
  export <task_id> [--wait] [--out <文件路径>]
                                      导出 CSV
  quota                               查询点数与个人信息
  logout                              登出当前账号
  config set base-url <url>           设置后端服务地址
  config set insecure true|false      忽略 HTTPS 证书校验（自签证书时开）
  config show                         查看当前配置（token 脱敏）
  version                             显示版本

全局参数: --token <token>  --base-url <url>（默认 ${DEFAULT_BASE_URL}）
          --interval <秒> --timeout <秒>（等待任务时可用，默认 2 / 120）`;

function requireToken(cfg) {
  if (!cfg.token) throw new BizError(1002, '未登录：缺少 token');
}

async function cmdSessionLink(cfg, scene) {
  const client = new ApiClient({ baseUrl: cfg.baseUrl });
  const data = await client.createCliSession();
  const isRegister = scene === 'register';
  const pageUrl = cfg.baseUrl + (isRegister ? data.register_path : data.login_path);
  const qrUrl = cfg.baseUrl + (isRegister ? data.register_qr_path : data.qr_path);
  const action = isRegister ? '注册' : '登录';
  process.stderr.write(
    `请把下面这段${action}引导原样发给用户：\n----\n` +
    (isRegister
      ? '需要先注册平台账号（注册即送 10 免费点数）。这不是微博登录，采集热榜不需要微博账号。请用手机扫码或打开链接注册：\n\n'
      : '需要登录平台账号。这不是微博登录，采集热榜不需要微博账号。请用手机扫码或打开链接：\n\n') +
    `${action}方式（二选一）\n二维码图片：${qrUrl}\n${action}链接：${pageUrl}\n` +
    `access_token（${action}后校验用）：${data.access_token}\n` +
    `扫码/${action}完成后告诉我一声，我会执行校验并保存凭证：\n\n` +
    `node cli.js ${scene} --check --access-token "${data.access_token}"\n----\n`);
  printOk({ qr_url: qrUrl, [isRegister ? 'register_url' : 'login_url']: pageUrl,
    access_token: data.access_token, expires_in: data.expires_in });
}

async function cmdSessionCheck(cfg, opts, scene) {
  const action = scene === 'register' ? '注册' : '登录';
  if (!opts.accessToken || !/^[0-9a-f]{16,64}$/.test(opts.accessToken)) {
    throw new UsageError(`${scene} --check 需要 --access-token（--link 下发的十六进制串）`);
  }
  const client = new ApiClient({ baseUrl: cfg.baseUrl });
  const data = await client.checkCliSession(opts.accessToken);
  if (data.status === 'pending') {
    printFail('LOGIN_PENDING', `用户尚未完成${action}，请提醒用户完成后再试`);
    process.exit(2);
  }
  if (data.status !== 'ready' || !data.token) {
    printFail('LOGIN_EXPIRED', `${action}会话已过期或已使用，请重新执行 ${scene} --link`);
    process.exit(2);
  }
  saveConfig({ base_url: cfg.baseUrl, token: data.token });
  process.stderr.write(`${action}成功，token 已保存到配置文件\n`);
  printOk({ phone: data.phone, quota_balance: data.quota_balance });
}

async function fetchPrice(baseUrl) {
  try {
    const data = await new ApiClient({ baseUrl }).request('GET', '/platform/capabilities');
    const cap = ((data && data.items) || []).find((c) => c.name === CAPABILITY);
    return cap && Number(cap.price) > 0 ? Number(cap.price) : DEFAULT_PRICE;
  } catch { return DEFAULT_PRICE; }
}

async function waitTask(client, taskId, opts) {
  return pollTask(client, taskId, {
    intervalSec: parsePositiveNumber(opts.interval, 'interval', 2),
    timeoutSec: parsePositiveNumber(opts.timeout, 'timeout', 120),
  });
}

async function cmdSubmit(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const price = await fetchPrice(cfg.baseUrl);
  const idempotencyKey = crypto.createHash('sha256')
    .update('weibo-hot' + (opts.force ? `|${Date.now()}` : '')).digest('hex').slice(0, 32);
  process.stderr.write(`提交微博热榜采集：${price} 点数/次，失败全额返还；服务端直接 HTTP 执行，无需微博登录态\n`);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  const data = await client.submitTask(CAPABILITY, [{ id: 1, payload: {} }], idempotencyKey, !!opts.force);
  if (!opts.wait) { printOk({ ...data, estimated_points: price }); return; }
  const task = await waitTask(client, data.task_id, opts);
  const result = task.items && task.items[0] && task.items[0].result;
  process.stderr.write(`任务完成: status=${task.status}，采集 ${(result && result.collected_count) || 0} 条热榜\n`);
  printOk(task);
}

async function cmdQuery(args, opts) {
  if (!args[0]) throw new UsageError('query 需要 task_id 参数');
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  printOk(opts.wait ? await waitTask(client, args[0], opts) : await client.getTask(args[0]));
}

async function cmdExport(args, opts) {
  const taskId = args[0];
  if (!taskId) throw new UsageError('export 需要 task_id 参数');
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  if (opts.wait) await waitTask(client, taskId, opts);
  const created = await client.createExport(taskId);
  if (!opts.wait) { printOk(created); return; }
  const deadline = Date.now() + 120000;
  let info;
  for (;;) {
    info = await client.getExport(created.export_id);
    if (info.status !== 'pending' && info.status !== 'running') break;
    if (Date.now() + 1000 > deadline) {
      printFail('TIMEOUT', '等待导出超时，可稍后重试');
      process.exit(5);
    }
    await new Promise((r) => setTimeout(r, 1000));
  }
  if (info.status !== 'done') {
    printFail('EXPORT_FAILED', `导出未完成 (status=${info.status})`);
    process.exit(5);
  }
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), DOWNLOAD_TIMEOUT_MS);
  let buf;
  try {
    const res = await fetch(`${cfg.baseUrl}/api/v1/platform/exports/${encodeURIComponent(info.export_id)}/file`,
      { headers: { Authorization: `Bearer ${cfg.token}` }, signal: ctrl.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    buf = Buffer.from(await res.arrayBuffer());
  } catch (err) {
    printFail('EXPORT_FAILED', `下载失败: ${err.message || err}`);
    process.exit(5);
  } finally { clearTimeout(timer); }
  const out = opts.out || `${taskId}_wb_hot.csv`;
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  if (fs.existsSync(out)) process.stderr.write(`[warn] 目标文件已存在，将覆盖: ${out}\n`);
  fs.writeFileSync(out, buf);
  printOk({ export_id: info.export_id, file: out, size: buf.length });
}

async function cmdQuota(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  printOk(await new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token }).profile());
}

async function cmdLogout(opts) {
  const cfg = resolveConfig(opts);
  if (!cfg.token) throw new BizError(1002, '未登录：本地没有已保存的 token');
  try { await new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token }).logout(); }
  catch (err) { process.stderr.write(`服务端登出异常（已忽略）: ${err.message}\n`); }
  saveConfig({ token: '' });
  printOk({ logged_out: true });
}

async function cmdConfig(args, opts) {
  if (args[0] === 'set' && args[1] === 'base-url') {
    const url = args[2];
    if (!url || !/^https?:\/\//.test(url)) throw new UsageError('base-url 需要 http(s):// 开头的地址');
    saveConfig({ base_url: url.replace(/\/+$/, '') });
    printOk({ base_url: loadConfig().base_url });
    return;
  }
  if (args[0] === 'set' && args[1] === 'insecure') {
    if (!['true', 'false'].includes(args[2])) throw new UsageError('insecure 需要 true 或 false');
    saveConfig({ insecure: args[2] === 'true' });
    printOk({ insecure: loadConfig().insecure === true });
    return;
  }
  if (args[0] === 'show') {
    const cfg = resolveConfig(opts);
    printOk({ base_url: cfg.baseUrl, insecure: cfg.insecure, token: maskToken(cfg.token),
      config_path: configPaths.configPath });
    return;
  }
  throw new UsageError('config 仅支持 set base-url / set insecure / show');
}

async function main() {
  const { cmd, args, opts } = parseArgs(process.argv.slice(2));
  if (opts.version || cmd === 'version') {
    printOk({ name: 'wb-hot', version: VERSION, capability: CAPABILITY });
    return;
  }
  if (opts.help || !cmd) throw new UsageError('缺少命令');
  if (resolveConfig(opts).insecure) allowInsecureTls();
  switch (cmd) {
    case 'register':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'register');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'register');
      throw new UsageError('register 仅支持 --link / --check');
    case 'login':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'login');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'login');
      throw new UsageError('login 仅支持 --link / --check');
    case 'submit': return cmdSubmit(opts);
    case 'query': return cmdQuery(args, opts);
    case 'export': return cmdExport(args, opts);
    case 'quota': return cmdQuota(opts);
    case 'logout': return cmdLogout(opts);
    case 'config': return cmdConfig(args, opts);
    default: throw new UsageError(`未知命令: ${cmd}`);
  }
}

main().catch((e) => exitWithError(e, { usage: USAGE }));
