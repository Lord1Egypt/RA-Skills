#!/usr/bin/env node
'use strict';
/**
 * cli.js — 小红书转链 CLI (v2.0.0, 与 xhs-dpt 采集 skill 同框架, 自包含)。
 *
 * 输出规约 (对齐采集 skill): stdout 只输出 JSON, 提示走 stderr。
 * 退出码: 0 成功 / 1 参数错误 / 2 认证失败 / 3 点数不足 / 4 网络错误 / 5 其它。
 *
 * 命令: version / register --link / login --link / submit / query / quota / logout / config
 * (v2.0.0 起移除终端注册与密码登录: 服务端强制图形验证码, 统一走 --link 扫码/链接)
 */
const crypto = require('crypto');
const fs = require('fs');
const { ApiClient, BizError, NetworkError, allowInsecureTls } = require('./src/client');
const { loadConfig, saveConfig, resolveConfig, maskToken, configPaths, DEFAULT_BASE_URL } = require('./src/config');
const {
  UsageError, printOk, printFail, exitWithError, pollTask, parsePositiveNumber,
} = require('./src/output');

const SKILL_NAME = 'xhs-convert-url-pro';
const VERSION = '2.0.1';
const MIN_BATCH = 1;
const MAX_BATCH = 50;

// ---------------------------------------------------------------- 参数解析

const VALUE_FLAGS = new Set(['file', 'interval', 'timeout', 'token', 'base-url', 'access-token']);
const MULTI_FLAGS = new Set(['url']);
const BOOL_FLAGS = new Set(['wait', 'help', 'link', 'check', 'version']);

function camel(s) {
  return s.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

function parseArgs(argv) {
  const opts = {};
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    let arg = argv[i];
    if (!arg.startsWith('-')) {
      positional.push(arg);
      continue;
    }
    if (!arg.startsWith('--')) throw new UsageError(`未知参数: ${arg}`);
    let inline;
    const eq = arg.indexOf('=');
    if (eq > 2) {
      inline = arg.slice(eq + 1);
      arg = arg.slice(0, eq);
    }
    const name = arg.slice(2);
    if (VALUE_FLAGS.has(name)) {
      const value = inline !== undefined ? inline : argv[++i];
      if (value === undefined) throw new UsageError(`缺少参数值: ${arg}`);
      opts[camel(name)] = value;
    } else if (MULTI_FLAGS.has(name)) {
      const value = inline !== undefined ? inline : argv[++i];
      if (value === undefined) throw new UsageError(`缺少参数值: ${arg}`);
      (opts[camel(name)] = opts[camel(name)] || []).push(value);
    } else if (BOOL_FLAGS.has(name)) {
      if (inline !== undefined) throw new UsageError(`参数 ${arg} 不接受值`);
      opts[camel(name)] = true;
    } else {
      throw new UsageError(`未知参数: ${arg}`);
    }
  }
  const cmd = positional.shift() || '';
  return { cmd, args: positional, opts };
}

const USAGE = `小红书转链 CLI (v${VERSION})

用法: node cli.js <命令> [参数]

命令:
  version                           查看版本与安装信息
  register --link                   生成注册二维码/链接（注册即送 10 点数）
  register --check --access-token <串>  用户完成注册后确认并保存 token
  login --link                      生成登录二维码/链接（推荐）
  login --check --access-token <串> 用户完成授权后确认并保存 token
  submit --url <url> [--url ...] [--file <路径>] [--wait] [--interval 秒] [--timeout 秒]
                                    提交转链任务（1~50 条，--file 按行读取，忽略空行与 # 注释）
  query <task_id> [--wait] [--interval 秒] [--timeout 秒]
                                    查询任务状态与结果
  quota                             查询点数与个人信息
  logout                            登出当前账号
  config set base-url <url>         设置后端服务地址
  config set insecure true|false    忽略 HTTPS 证书校验（自签证书时开）
  config show                       查看当前配置（token 脱敏）

全局参数: --token <token>（临时覆盖）  --base-url <url>（默认 ${DEFAULT_BASE_URL}）

说明: 凭证与「小红书互动数采集」skill (xhs-dpt) 共用 ~/.xhs-platform/config.json，
     没有 token 或 token 失效时执行 login --link 重新登录即可。`;

// ---------------------------------------------------------------- 各命令

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
    `请把下面这段${action}引导原样发给用户：\n` +
    '----\n' +
    (isRegister
      ? '需要先注册账号（注册即送 10 免费点数；不注册不登录没有点数，无法使用转链）。请用手机扫码或打开链接注册：\n\n'
      : '需要先登录。请用手机扫码或打开链接登录账号：\n\n') +
    `${action}方式（二选一）\n` +
    `二维码图片：${qrUrl}\n` +
    `${action}链接：${pageUrl}\n` +
    `access_token（${action}后校验用）：${data.access_token}\n` +
    `扫码/${action}完成后告诉我一声，我会执行校验并保存凭证，然后继续之前的操作：\n\n` +
    `node cli.js ${scene} --check --access-token "${data.access_token}"\n` +
    '（注册/使用中如遇问题，请拨打客服电话 18722121663）\n' +
    '----\n');
  printOk({
    qr_url: qrUrl,
    [isRegister ? 'register_url' : 'login_url']: pageUrl,
    access_token: data.access_token,
    expires_in: data.expires_in,
  });
}

async function cmdSessionCheck(cfg, opts, scene) {
  const action = scene === 'register' ? '注册' : '登录';
  const accessToken = opts.accessToken;
  if (!accessToken || !/^[0-9a-f]{16,64}$/.test(accessToken)) {
    throw new UsageError(`${scene} --check 需要 --access-token（${scene} --link 下发的十六进制串）`);
  }
  const client = new ApiClient({ baseUrl: cfg.baseUrl });
  const data = await client.checkCliSession(accessToken);
  if (data.status === 'pending') {
    printFail('LOGIN_PENDING', `用户尚未完成${action}，请提醒用户完成扫码/链接${action}后再执行本命令`);
    process.exit(2);
  }
  if (data.status !== 'ready' || !data.token) {
    printFail('LOGIN_EXPIRED', `${action}会话已过期或已使用，请重新执行 ${scene} --link 发起${action}`);
    process.exit(2);
  }
  saveConfig({ base_url: cfg.baseUrl, token: data.token });
  process.stderr.write(`${action}成功，token 已保存到配置文件（与采集 skill 通用）\n`);
  printOk({ phone: data.phone, quota_balance: data.quota_balance });
}

function collectUrls(opts) {
  const urls = [...(opts.url || [])];
  if (opts.file) {
    let content;
    try {
      content = fs.readFileSync(opts.file, 'utf8');
    } catch {
      throw new UsageError(`无法读取文件: ${opts.file}`);
    }
    for (const line of content.split(/\r?\n/)) {
      const s = line.trim();
      if (!s || s.startsWith('#')) continue;
      urls.push(s);
    }
  }
  if (urls.length < MIN_BATCH) throw new UsageError('请通过 --url 或 --file 提供至少 1 条 URL');
  if (urls.length > MAX_BATCH) throw new UsageError(`超出单次批量上限（${MAX_BATCH} 条），当前 ${urls.length} 条`);
  return urls;
}

async function cmdSubmit(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const urls = collectUrls(opts);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  const items = urls.map((url, i) => ({ id: i + 1, url }));
  // 幂等键按 URL 内容派生 (sha256 截断): 同一批 URL 重试/重复提交复用同键,
  // 服务端幂等返回原任务, 不重复扣费; 内容变化自动得到新键
  const idempotencyKey = crypto.createHash('sha256').update(urls.join('\n')).digest('hex').slice(0, 32);
  process.stderr.write(`提交 ${items.length} 条 URL（幂等键 ${idempotencyKey}）...\n`);
  const data = await client.submitTask(items, idempotencyKey);
  if (!opts.wait) {
    printOk(data);
    return;
  }
  process.stderr.write(`任务已创建 task_id=${data.task_id}，等待结果...\n`);
  const task = await pollTask(client, data.task_id, {
    intervalSec: parsePositiveNumber(opts.interval, 'interval', 2),
    timeoutSec: parsePositiveNumber(opts.timeout, 'timeout', 120),
  });
  printOk(task);
}

async function cmdQuery(args, opts) {
  const taskId = args[0];
  if (!taskId) throw new UsageError('query 需要 task_id 参数');
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  if (!opts.wait) {
    printOk(await client.getTask(taskId));
    return;
  }
  const task = await pollTask(client, taskId, {
    intervalSec: parsePositiveNumber(opts.interval, 'interval', 2),
    timeoutSec: parsePositiveNumber(opts.timeout, 'timeout', 120),
  });
  printOk(task);
}

async function cmdQuota(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  printOk(await client.profile());
}

async function cmdLogout(opts) {
  const cfg = resolveConfig(opts);
  if (!cfg.token) throw new BizError(1002, '未登录：本地没有已保存的 token');
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  try {
    await client.logout(); // 服务端吊销 token; 失败不阻塞本地清理
  } catch (err) {
    process.stderr.write(`服务端登出异常（已忽略，继续清除本地 token）: ${err.message}\n`);
  }
  saveConfig({ token: '' });
  process.stderr.write('已登出，本地 token 已清除（采集 skill 同步失效）；可执行 login --link 登录其他账号\n');
  printOk({ logged_out: true });
}

async function cmdConfig(args, opts) {
  const sub = args[0];
  if (sub === 'set' && args[1] === 'base-url') {
    const url = args[2];
    if (!url || !/^https?:\/\//.test(url)) throw new UsageError('config set base-url 需要 http(s):// 开头的地址');
    saveConfig({ base_url: url.replace(/\/+$/, '') });
    process.stderr.write(`base_url 已保存到 ${configPaths.configPath}\n`);
    printOk({ base_url: loadConfig().base_url });
    return;
  }
  if (sub === 'set' && args[1] === 'insecure') {
    const v = args[2];
    if (v !== 'true' && v !== 'false') throw new UsageError('config set insecure 需要 true 或 false');
    saveConfig({ insecure: v === 'true' });
    process.stderr.write(`insecure 已保存到 ${configPaths.configPath}\n`);
    printOk({ insecure: loadConfig().insecure === true });
    return;
  }
  if (sub === 'show') {
    const cfg = resolveConfig(opts);
    printOk({
      base_url: cfg.baseUrl,
      insecure: cfg.insecure,
      token: maskToken(cfg.token),
      config_path: configPaths.configPath,
    });
    return;
  }
  throw new UsageError('config 仅支持: config set base-url <url> / config set insecure true|false / config show');
}

// ---------------------------------------------------------------- 入口

async function main() {
  const { cmd, args, opts } = parseArgs(process.argv.slice(2));
  if (opts.version) {
    printOk({ name: SKILL_NAME, version: VERSION, node_version: process.version, config_path: configPaths.configPath });
    return;
  }
  if (opts.help || !cmd) throw new UsageError('缺少命令');
  if (resolveConfig(opts).insecure) allowInsecureTls();
  switch (cmd) {
    case 'version':
      return printOk({ name: SKILL_NAME, version: VERSION, node_version: process.version, config_path: configPaths.configPath });
    case 'register':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'register');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'register');
      throw new UsageError('register 仅支持 --link / --check (终端注册会被 2003 拒绝)');
    case 'login':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'login');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'login');
      throw new UsageError('login 仅支持 --link / --check (密码登录会被 2003 拒绝)');
    case 'submit': return cmdSubmit(opts);
    case 'query': return cmdQuery(args, opts);
    case 'quota': return cmdQuota(opts);
    case 'logout': return cmdLogout(opts);
    case 'config': return cmdConfig(args, opts);
    default: throw new UsageError(`未知命令: ${cmd}`);
  }
}

main().catch(exitWithError);
