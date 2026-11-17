#!/usr/bin/env node

// webclaw3 — L0 层（Relay + CDP Proxy）启停与健康检查
//
// 子命令：start | stop | status | restart | doctor
//         cdp-start | cdp-stop | cdp-status | cdp-restart
// 内部封装同目录下 start-relay.mjs / start-cdp-proxy.mjs 的 spawn/端口探测
// 输出 stdout JSON：{port, listening, extensionConnected, pid}
// 退出码：0=端口监听中（status）、spawn 成功（start）、通道就绪（doctor）；1=异常

import { spawn, execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, unlinkSync, mkdirSync, openSync, readdirSync, symlinkSync, readlinkSync, lstatSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';
import http from 'node:http';
import https from 'node:https';

const __dirname = dirname(fileURLToPath(import.meta.url));
const RELAY_SCRIPT = join(__dirname, 'start-relay.mjs');
const CDP_SCRIPT = join(__dirname, 'start-cdp-proxy.mjs');

const DEFAULT_PORT = 3459;
const CDP_DEFAULT_PORT = 3456;
const PID_DIR = join(homedir(), '.webclaw3');
const PID_FILE = join(PID_DIR, 'relay.pid');
const CDP_PID_FILE = join(PID_DIR, 'cdp-proxy.pid');
const CONFIG_FILE = join(PID_DIR, 'config.json');
const LOG_FILE = '/tmp/relay.log';
const CDP_LOG_FILE = '/tmp/cdp-proxy.log';

// 宿主环境 → 期望的 Code CLI（生成器 spawn 的 LLM）。三种支持环境：
//   claude-code   —— Claude Code CLI
//   workbuddy-cn  —— WorkBuddy 国内桌面版
//   qoderwork-cn  —— QoderWork 国内桌面版
// 注意：国内/国际两套账户与 CLI 各自独立、不互通。国际版 QoderWork 的 CLI 叫 qodercli，
// 与国内 qoderclicn 不是同一个东西；这里只覆盖我们支持的国内版。
const ENV_CLI = {
  'claude-code':  { type: 'claude-code',   binary: 'claude',     label: 'Claude Code',    doc: 'npm i -g @anthropic-ai/claude-code' },
  'workbuddy-cn': { type: 'codebuddy-code', binary: 'codebuddy',  label: 'WorkBuddy 国内', doc: 'npm install -g @tencent-ai/codebuddy-code' },
  'qoderwork-cn': { type: 'qoder-code',     binary: 'qoderclicn', label: 'QoderWork 国内', doc: 'curl -fsSL https://qoder.cn/install | bash' },
};

// dist/ 里的随包文件（扩展 zip、生成器 tarball）在导入部分 skill 平台时会被剥离，
// 缺失时从 GitHub raw 兜底下载。
const DIST_RAW_BASE = 'https://raw.githubusercontent.com/fatmind/webclaw3/main/dist';

function log(msg) {
  process.stderr.write(`[webclaw3] ${msg}\n`);
}

function printUsage() {
  process.stdout.write(`webclaw3 — L0 层（Relay + CDP Proxy）启停与健康检查

Usage:
  webclaw3 doctor --env <claude-code|workbuddy-cn|qoderwork-cn> [--port 3459]
  webclaw3 start [--port 3459] [--wait 10]
  webclaw3 stop [--port 3459]
  webclaw3 status [--port 3459] [--timeout 5]
  webclaw3 restart [--port 3459] [--wait 10]
  webclaw3 cdp-start [--port 3456] [--wait 10]
  webclaw3 cdp-stop [--port 3456]
  webclaw3 cdp-status [--port 3456] [--timeout 5]
  webclaw3 cdp-restart [--port 3456] [--wait 10]
  webclaw3 pipeline-start [--wait 10]
  webclaw3 pipeline-stop
  webclaw3 pipeline-status [--timeout 5]
  webclaw3 pipeline-restart
  webclaw3 config ak <access-key> [--app-base <url>]
  webclaw3 -h | --help

Relay Commands:
  doctor   分两层诊断。先查【最必需】(能探索即可)：Node 版本 → relay(未启动则自动 start) → 扩展连接
           (未连接时区分 Chrome 没开 / 扩展未安装 / 已装未连，输出 advice；不碰 CDP)
           再查【提炼专用】(环节③才要)：按 --env 锁定对应 Code CLI(错配则拒绝并引导装对的)
           + 生成器自身(装了未跑则自动 start) + AK/剩余次数。dist/ 缺文件时自动下载兜底
           同时把本 skill 安装路径与 env 注册到 ~/.webclaw3/config.json(幂等)
  start    后台启动 relay（spawn start-relay.mjs），等端口 ready
  status   查询 3459 端口监听 + /api/status.extensionConnected
  stop     用 PID 文件杀进程
  restart  stop + start

CDP Proxy Commands:
  cdp-start    后台启动 CDP proxy（spawn start-cdp-proxy.mjs），等端口 ready
  cdp-status   查询 3456 端口监听 + /health
  cdp-stop     用 PID 文件杀进程
  cdp-restart  stop + start

Pipeline（生成器 :3460）Commands:
  pipeline-start    后台启动生成器（读 config.json pipeline.entry，spawn --serve）
  pipeline-status   查询 :3460 监听 + 运行中任务
  pipeline-stop     用 PID 文件杀进程
  pipeline-restart  stop + start

Config:
  config ak <access-key> [--app-base <url>]  写 config.json ak/appBase（生成/拉经验/回传需 AK）

Output:
  stdout 输出 JSON: {"port":N,"listening":bool,"connected":bool,"pid":N|null}
  退出码：start/status 0=正常，1=异常

Config:
  Relay PID 文件: ~/.webclaw3/relay.pid
  CDP PID 文件: ~/.webclaw3/cdp-proxy.pid
  Relay 日志: /tmp/relay.log
  CDP 日志: /tmp/cdp-proxy.log
`);
}

function parseOpts(args) {
  const opts = { port: DEFAULT_PORT, wait: 10, timeout: 5 };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--port' && args[i + 1]) opts.port = parseInt(args[++i], 10);
    else if (args[i] === '--wait' && args[i + 1]) opts.wait = parseInt(args[++i], 10);
    else if (args[i] === '--timeout' && args[i + 1]) opts.timeout = parseInt(args[++i], 10);
    else if (args[i] === '--env' && args[i + 1]) opts.env = args[++i];
    else if (args[i] === '-h' || args[i] === '--help') { printUsage(); process.exit(0); }
  }
  return opts;
}

function readPidFile() {
  try {
    const v = parseInt(readFileSync(PID_FILE, 'utf-8').trim(), 10);
    return Number.isFinite(v) ? v : null;
  } catch { return null; }
}

function checkPort(port, timeoutMs = 1000) {
  return new Promise((resolve) => {
    const req = http.get({ host: '127.0.0.1', port, path: '/api/status', timeout: timeoutMs }, (res) => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => {
        try {
          const data = JSON.parse(body);
          resolve({ listening: true, extensionConnected: !!data.extensionConnected, raw: data });
        } catch {
          resolve({ listening: true, extensionConnected: false, raw: body });
        }
      });
    });
    req.on('error', () => resolve({ listening: false, extensionConnected: false }));
    req.on('timeout', () => { req.destroy(); resolve({ listening: false, extensionConnected: false }); });
  });
}

async function startRelayCore(opts) {
  const existing = await checkPort(opts.port);
  if (existing.listening) {
    log(`port ${opts.port} already listening`);
    return { port: opts.port, ...existing, pid: readPidFile() };
  }

  if (!existsSync(RELAY_SCRIPT)) {
    log(`relay script not found: ${RELAY_SCRIPT}`);
    return { port: opts.port, listening: false, extensionConnected: false, error: 'relay-script-not-found' };
  }

  mkdirSync(PID_DIR, { recursive: true });

  const out = openSync(LOG_FILE, 'a');
  const child = spawnDaemonViaLoginShell('node', [RELAY_SCRIPT, String(opts.port)], out);
  writeFileSync(PID_FILE, String(child.pid));
  log(`spawned relay pid=${child.pid} port=${opts.port}, waiting up to ${opts.wait}s`);

  const deadline = Date.now() + opts.wait * 1000;
  let last = { listening: false, extensionConnected: false };
  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, 500));
    last = await checkPort(opts.port);
    if (last.listening) break;
  }

  if (!last.listening) {
    log(`port ${opts.port} not listening after ${opts.wait}s; check ${LOG_FILE}`);
  }
  return { port: opts.port, ...last, pid: child.pid };
}

async function cmdStart(opts) {
  const result = await startRelayCore(opts);
  process.stdout.write(JSON.stringify(result) + '\n');
  return result.listening ? 0 : 1;
}

async function cmdStop(opts) {
  const pid = readPidFile();
  if (!pid) {
    log('no pid file, nothing to stop');
    process.stdout.write(JSON.stringify({ port: opts.port, listening: false, extensionConnected: false, stopped: false }) + '\n');
    return 0;
  }
  try {
    process.kill(pid, 'SIGTERM');
    log(`sent SIGTERM to pid=${pid}`);
  } catch (e) {
    log(`kill pid=${pid} failed: ${e.message}`);
  }
  const deadline = Date.now() + 5000;
  while (Date.now() < deadline) {
    if (!(await checkPort(opts.port)).listening) break;
    await new Promise(r => setTimeout(r, 200));
  }
  try { unlinkSync(PID_FILE); } catch {}
  process.stdout.write(JSON.stringify({ port: opts.port, listening: false, extensionConnected: false, stopped: true }) + '\n');
  return 0;
}

async function cmdStatus(opts) {
  const r = await checkPort(opts.port, opts.timeout * 1000);
  const out = { port: opts.port, ...r, pid: readPidFile() };
  process.stdout.write(JSON.stringify(out) + '\n');
  return r.listening ? 0 : 1;
}

async function cmdRestart(opts) {
  await cmdStop(opts);
  return cmdStart(opts);
}

// --- 生成器（wc3-pipeline :3460）生命周期 ---
// 定位唯一定位 = config.json 的 pipeline.entry（install.sh / npm 安装时写入）
// 状态探测直接打 /api/status，与 server.mjs 一致

const PIPELINE_PORT = 3460;
const PIPELINE_PID_FILE = join(PID_DIR, 'pipeline.pid');
const PIPELINE_LOG_FILE = '/tmp/wc3-pipeline.log';

function findPipelineBinary() {
  try {
    return execFileSync('which', ['wc3-pipeline'], { encoding: 'utf-8' }).trim();
  } catch { return null; }
}

// webclaw3 拉起的常驻后台进程（pipeline daemon / relay / cdp-proxy）的统一启动入口——从干净环境起。
// 背景：这些进程常被宿主 Agent（如 WorkBuddy/QoderWork）里跑的 webclaw3.mjs 拉起，宿主注入的变量
// （托管 node 优先的 PATH、CODEBUDDY_*/QODER_*/MCP 配置等）会一路继承进子进程。对 pipeline daemon
// 危害最大：它再 spawn 的 code CLI（codebuddy/qoderclicn）会切进 SDK 模式、连错沙箱端口、登录态错位。
// relay/cdp 虽不 spawn code CLI、危害小，但统一走干净环境可保证「凡 webclaw3 拉起的常驻进程都等价
// 终端手敲」，node 也统一由登录 shell 的 PATH 解析，避免以后埋坑。
// 收口方案：不在下游各 spawn 点逐个黑名单过滤（散且难查），而在此唯一咽喉点用
// 「env -i 语义（只留 HOME）+ 登录 shell（-l）」重建环境——登录 shell 读 ~/.zprofile/~/.zshrc
// 把 PATH、登录态重新搭起来。与探测用的 execViaLoginShell 同源同语义。
// command 走 PATH 解析（如 'node'）或用绝对路径均可；command/args 用单引号转义防注入。
function spawnDaemonViaLoginShell(command, args, out) {
  const shell = process.env.SHELL || '/bin/zsh';
  const shq = (s) => `'${String(s).replace(/'/g, `'\\''`)}'`;
  const line = `exec ${[command, ...args].map(shq).join(' ')}`;
  const child = spawn(shell, ['-lc', line], {
    detached: true,
    stdio: ['ignore', out, out],
    env: { HOME: process.env.HOME },
  });
  child.unref();
  return child;
}

// 确保 dist/ 里存在匹配文件；本地有就返回其路径，没有则从 GitHub raw 下载兜底。
// pattern: 匹配已存在文件的正则；filename: 兜底下载时的确切文件名。失败返回 null。
function ensureDistFile(skillDir, pattern, filename) {
  try {
    const distDir = join(skillDir, 'dist');
    mkdirSync(distDir, { recursive: true });
    let hit = null;
    try { hit = readdirSync(distDir).filter(f => pattern.test(f)).sort().pop() || null; } catch { /* dir 读失败 */ }
    if (hit) return join(distDir, hit);
    // 本地缺失 → 下载兜底
    const dest = join(distDir, filename);
    const url = `${DIST_RAW_BASE}/${filename}`;
    log(`dist/${filename} 缺失，正在从 GitHub 下载兜底…`);
    execFileSync('curl', ['-fsSL', '--max-time', '60', '-o', dest, url], { stdio: ['ignore', 'ignore', 'inherit'] });
    if (existsSync(dest)) { log(`已下载 dist/${filename}`); return dest; }
    return null;
  } catch (e) {
    log(`dist/${filename} 下载失败：${e.message}`);
    return null;
  }
}

// 把扩展 zip 解压到用户 Downloads 下一个好找的文件夹
// （~/Downloads/wc3-chrome-extension-<版本号>，文件夹名带当前版本，装的是哪版一眼能分清），
// 免得小白用户去隐藏目录里找。返回解压后的文件夹绝对路径；失败返回 null。
function extractExtensionToDownloads(zipPath) {
  try {
    const ver = /wc3-chrome-extension-(\d+\.\d+\.\d+)\.zip$/.exec(zipPath)?.[1];
    const destDir = join(homedir(), 'Downloads', ver ? `wc3-chrome-extension-${ver}` : 'wc3-chrome-extension');
    mkdirSync(destDir, { recursive: true });
    // -o 覆盖已存在文件，-q 安静模式；zip 内 manifest.json 在根目录，直接解到 destDir
    execFileSync('unzip', ['-o', '-q', zipPath, '-d', destDir], { stdio: ['ignore', 'ignore', 'inherit'] });
    return destDir;
  } catch (e) {
    log(`扩展解压到 Downloads 失败：${e.message}`);
    return null;
  }
}

// 从 skill 目录的 dist/ 里就地安装生成器 tarball（随包分发、无依赖、离线可装）。
// 成功返回 wc3-pipeline 二进制路径，失败返回 null。doctor 用它做"未装则自动装"，
// 免去让用户手敲 npm i -g。
function installPipelineFromDist(skillDir) {
  try {
    const tgzPath = ensureDistFile(skillDir, /^wc3-pipeline-.*\.tgz$/, 'wc3-pipeline-2.0.0.tgz');
    if (!tgzPath) return null;
    log('检测到生成器尚未安装，正在自动安装，请稍候…');
    // 底层执行 npm i -g <skillDir>/dist/wc3-pipeline-*.tgz（离线安装，无外部依赖）
    execFileSync('npm', ['i', '-g', tgzPath], { stdio: ['ignore', 'ignore', 'inherit'] });
    log('生成器安装完成。');
    return findPipelineBinary();
  } catch (e) {
    log(`生成器自动安装失败：${e.message}`);
    return null;
  }
}

function readPipelinePidFile() {
  try {
    const v = parseInt(readFileSync(PIPELINE_PID_FILE, 'utf-8').trim(), 10);
    return Number.isFinite(v) ? v : null;
  } catch { return null; }
}

function checkPipelinePort(timeoutMs = 1000) {
  return new Promise((resolve) => {
    const req = http.get({ host: '127.0.0.1', port: PIPELINE_PORT, path: '/api/status', timeout: timeoutMs }, (res) => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => {
        try { resolve({ listening: true, data: JSON.parse(body) }); }
        catch { resolve({ listening: true, data: null }); }
      });
    });
    req.on('error', () => resolve({ listening: false }));
    req.on('timeout', () => { req.destroy(); resolve({ listening: false }); });
  });
}

async function cmdPipelineStart(opts) {
  let binary = findPipelineBinary();
  if (!binary) {
    const activeEnv = readConfigValue('activeEnv');
    const skillDir = activeEnv ? readEnvValue(activeEnv, 'skillDir') : null;
    if (skillDir) binary = installPipelineFromDist(skillDir);
  }
  if (!binary) {
    log('生成器组件安装失败，暂时无法启动。请重新运行一次诊断（doctor）重试；若仍失败，可联系支持。');
    // 手动兜底（供排障，不打给普通用户）：npm i -g <skillDir>/dist/wc3-pipeline-*.tgz
    process.stdout.write(JSON.stringify({ installed: false, listening: false, error: 'pipeline-not-installed' }) + '\n');
    return 1;
  }
  const existing = await checkPipelinePort();
  if (existing.listening) {
    log(`pipeline 已在 :${PIPELINE_PORT} 监听`);
    process.stdout.write(JSON.stringify({ installed: true, listening: true, port: PIPELINE_PORT, pid: readPipelinePidFile() }) + '\n');
    return 0;
  }

  mkdirSync(PID_DIR, { recursive: true });
  const out = openSync(PIPELINE_LOG_FILE, 'a');
  const child = spawnDaemonViaLoginShell(binary, ['--serve'], out);
  writeFileSync(PIPELINE_PID_FILE, String(child.pid));
  log(`spawned pipeline pid=${child.pid} :${PIPELINE_PORT}, waiting up to ${opts.wait}s`);

  const deadline = Date.now() + opts.wait * 1000;
  let last = { listening: false };
  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, 500));
    last = await checkPipelinePort();
    if (last.listening) break;
  }
  if (!last.listening) log(`pipeline :${PIPELINE_PORT} 未就绪，看日志 ${PIPELINE_LOG_FILE}`);
  process.stdout.write(JSON.stringify({ installed: true, listening: last.listening, port: PIPELINE_PORT, pid: child.pid }) + '\n');
  return last.listening ? 0 : 1;
}

async function cmdPipelineStop() {
  const pid = readPipelinePidFile();
  if (pid) {
    try { process.kill(pid, 'SIGTERM'); log(`sent SIGTERM to pipeline pid=${pid}`); }
    catch (e) { log(`kill pipeline pid=${pid} failed: ${e.message}`); }
    const deadline = Date.now() + 5000;
    while (Date.now() < deadline) {
      if (!(await checkPipelinePort()).listening) break;
      await new Promise(r => setTimeout(r, 200));
    }
    try { unlinkSync(PIPELINE_PID_FILE); } catch {}
  } else {
    log('no pipeline pid file, nothing to stop');
  }
  process.stdout.write(JSON.stringify({ listening: await checkPipelinePort().then(r => r.listening), stopped: true }) + '\n');
  return 0;
}

async function cmdPipelineStatus(opts) {
  const r = await checkPipelinePort(opts.timeout * 1000);
  const binary = findPipelineBinary();
  const out = { installed: !!binary, listening: r.listening, port: PIPELINE_PORT, pid: readPipelinePidFile(), running: r.data?.running ?? [] };
  process.stdout.write(JSON.stringify(out) + '\n');
  return r.listening ? 0 : 1;
}

async function cmdPipelineRestart(opts) {
  await cmdPipelineStop();
  return cmdPipelineStart(opts);
}

// --- 配置写入（ak / appBase）---

function writeConfig(patch) {
  let cfg = {};
  try { cfg = JSON.parse(readFileSync(CONFIG_FILE, 'utf-8')); } catch {}
  Object.assign(cfg, patch);
  mkdirSync(PID_DIR, { recursive: true });
  writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2));
  return cfg;
}

async function cmdConfig(args) {
  const key = args[0];
  const value = args[1];
  if (!key || !value) {
    log('用法: webclaw3 config ak <access-key> [--app-base <url>]');
    log('AK 在 wc3-app 网页登录后获取（生成/拉经验/回传需要）');
    return 1;
  }
  if (key !== 'ak') {
    log(`暂只支持 config ak；收到: ${key}`);
    return 1;
  }
  let appBase = null;
  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--app-base' && args[i + 1]) appBase = args[++i];
  }
  const patch = { ak: value };
  if (appBase) patch.appBase = appBase;
  writeConfig(patch);
  log(`config.json 已写: ak=${value.slice(0, 6)}…${appBase ? ` appBase=${appBase}` : ''}`);
  process.stdout.write(JSON.stringify({ ok: true, ak: true, appBase: appBase ?? null }) + '\n');
  return 0;
}

// --- Doctor ---

function isChromeRunning() {
  try {
    execFileSync('pgrep', ['-f', 'Google Chrome|google-chrome|chromium'], { stdio: 'ignore' });
    return true;
  } catch { return false; }
}

// 读 Chrome Preferences 判断 wc3 扩展是否安装过（未打包扩展记录在 extensions.settings，
// macOS 上多在 Secure Preferences）。返回 true/false/null（null=无法判断）
// 注：新版 macOS 对 Chrome 配置目录有 TCC 保护，读取会 EPERM，此时返回 null，
// doctor 给合并建议（实测 2026-07：darwin 上即使完整权限也读不到）
function detectExtensionInstalled() {
  const roots = process.platform === 'darwin'
    ? [join(homedir(), 'Library/Application Support/Google/Chrome')]
    : [join(homedir(), '.config/google-chrome'), join(homedir(), '.config/chromium')];
  let sawSettings = false;
  for (const root of roots) {
    if (!existsSync(root)) continue;
    let profiles = [];
    try { profiles = readdirSync(root).filter(d => d === 'Default' || d.startsWith('Profile ')); } catch { continue; }
    for (const profile of profiles) {
      for (const file of ['Secure Preferences', 'Preferences']) {
        const fp = join(root, profile, file);
        if (!existsSync(fp)) continue;
        try {
          const settings = JSON.parse(readFileSync(fp, 'utf-8'))?.extensions?.settings;
          if (!settings) continue;
          sawSettings = true;
          for (const ext of Object.values(settings)) {
            const name = ext?.manifest?.name || '';
            const path = ext?.path || '';
            if (name === 'wc3' || /wc3-chrome[\/\\]extension/.test(path)) return true;
          }
        } catch { /* 单个文件解析失败不影响其它 profile */ }
      }
    }
  }
  return sawSettings ? false : null;
}

function readConfig() {
  try { return JSON.parse(readFileSync(CONFIG_FILE, 'utf-8')); } catch { return {}; }
}

// 读顶层扁平键（activeEnv / ak / appBase）
function readConfigValue(key) {
  return readConfig()?.[key] ?? null;
}

// 读某环境下的字段：envs[env][key]（如 cli / skillDir）
function readEnvValue(env, key) {
  return readConfig()?.envs?.[env]?.[key] ?? null;
}

// 深合并写入 envs[env]（保留该环境已有字段与其它环境）
function writeEnvValue(env, patch) {
  const cfg = readConfig();
  cfg.envs = cfg.envs || {};
  cfg.envs[env] = { ...(cfg.envs[env] || {}), ...patch };
  mkdirSync(PID_DIR, { recursive: true });
  writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2));
  return cfg;
}

// 解析宿主环境：--env（合法则幂等写入 config.activeEnv 并确保 envs[env] 存在）> config.activeEnv > null。
// 返回：合法 env key 字符串 / { invalid: <传入值> } / null（完全无信息）。
function resolveEnv(opts) {
  if (opts.env) {
    if (ENV_CLI[opts.env]) {
      writeConfig({ activeEnv: opts.env });
      writeEnvValue(opts.env, {}); // 确保 envs[env] 存在（初始化成功过的环境都进 envs）
      return opts.env;
    }
    return { invalid: opts.env };
  }
  const saved = readConfigValue('activeEnv');
  if (saved && ENV_CLI[saved]) return saved;
  return null;
}

// doctor 探测 CLI（登录态/版本）时，必须与 daemon 执行 CLI 用同一套环境，否则
// 「探测时用宿主污染 PATH 命中 CLI-A、daemon 用干净 PATH 命中 CLI-B」会让 doctor 说 OK
// 却实跑失败。故探测统一走登录 shell 重建环境——与 spawnDaemonViaLoginShell 同源、同「终端手敲」语义：
// env 只留 HOME，PATH/登录态由 ~/.zprofile/~/.zshrc 重建，顺带天然剥离宿主注入的
// QODER_*/CODEBUDDY_*/MCP 等。command 走 PATH 解析（探测到的即执行时会命中的那个）。
// command/args 用单引号转义防 shell 注入。
function execViaLoginShell(command, args, opts = {}) {
  const shell = process.env.SHELL || '/bin/zsh';
  const shq = (s) => `'${String(s).replace(/'/g, `'\\''`)}'`;
  const line = `exec ${[command, ...args].map(shq).join(' ')}`;
  return execFileSync(shell, ['-lc', line], {
    encoding: 'utf-8',
    env: { HOME: process.env.HOME },
    ...opts,
  });
}

// 廉价探测 qodercli 登录态：`qodercli status` 不发起 LLM 调用、不计费。
// 返回 true=已登录 / false=未登录 / null=无法判定。
function checkQoderCliLogin(command) {
  try {
    const out = execViaLoginShell(command, ['status'], {
      stdio: ['ignore', 'pipe', 'ignore'],
    });
    if (/Not logged in/i.test(out)) return false;
    if (/Username:/i.test(out)) return true;
    return null;
  } catch { return null; }
}

// 探测 Code CLI：生成器 spawn 的 LLM。**按宿主环境锁定期望 type**（env 来自 --env / config.env）：
//   claude-code → claude ；workbuddy-cn → codebuddy ；qoderwork-cn → qoderclicn
// 只接受与期望 type 匹配的 CLI；探测到的与环境对不上（如 qoderwork-cn 却只有 codebuddy）→ 拒绝、
// 不注册，found:false 并引导装对的那个。国内/国际账户不互通，绝不混用。
// 优先级（均限定在期望 type 内）：registered(匹配且可用) > PATH 期望 binary
//   两个 env 都不做任何内置兜底：新方案要求各 env 独立安装 CLI 并自己登录（登录态不复用宿主 App），
//   所以 codebuddy-code 只认独立安装的 codebuddy，qoder-code 只认国内 qoderclicn。
function detectCodeCli(env) {
  const expected = ENV_CLI[env];
  if (!expected) {
    // 理论上 doctor 会在 env 缺失时提前短路；这里兜底返回未就绪。
    return { type: null, command: null, found: false, version: null };
  }

  // 只在期望 type 内构造候选
  const candidates = [{ type: expected.type, command: expected.binary }];
  // 不做任何内置兜底：codebuddy-code 只认独立安装的 codebuddy，qoder-code 只认国内 qoderclicn。
  // 绝不回退到宿主 App 内置的 CLI（WorkBuddy 内置 codebuddy / QoderWork 内置国际版 qodercli）——
  // 内置 CLI 复用宿主登录态，与新方案「各 env 独立安装、自己登录」冲突；国内/国际账户更是不互通。
  // 没装期望 binary 时直接 found:false，引导用户装对的那个。

  const registered = readEnvValue(env, 'cli');
  const probe = (command) => {
    try { return execViaLoginShell(command, ['--version'], { stdio: ['ignore', 'pipe', 'ignore'] }).trim(); }
    catch { return null; }
  };

  // envs[env].cli 复用有两道闸：type 与当前环境一致，且 binary 名也得对得上（防脏数据）。
  // 新 schema 下 cli 存在各自 env 键下，跨环境串味结构上已不可能；这里只兜同环境内的损坏/错记。
  const regBaseOk = registered?.command && basename(registered.command).replace(/\.exe$/i, '') === expected.binary;
  if (registered?.command && registered.type === expected.type && regBaseOk) {
    const version = probe(registered.command);
    if (version) return { type: registered.type, command: registered.command, found: true, version };
    log(`envs.${env}.cli 不可用（${registered.command}），重新探测...`);
  } else if (registered?.command && (registered.type !== expected.type || !regBaseOk)) {
    log(`envs.${env}.cli（${registered.type} / ${registered.command}）与期望不符，重新探测...`);
  }

  for (const c of candidates) {
    const version = probe(c.command);
    if (!version) continue;
    if (!registered || registered.command !== c.command || registered.type !== c.type) {
      writeEnvValue(env, { cli: { type: c.type, command: c.command } });
      log(`envs.${env}.cli registered: ${c.type} → ${c.command}`);
    }
    return { type: c.type, command: c.command, found: true, version };
  }
  // 环境期望的 CLI 一个都没找到 → 未就绪。每个环境有各自独立的 cli 槽（envs[env].cli），
  // 这里把它设成当前环境期望的 binary（哪怕没装），让 pipeline 绑到「对的但没装」的 CLI 上干净失败，
  // 而不会误用别的环境的 CLI/账户。
  if (!registered || registered.command !== expected.binary || registered.type !== expected.type) {
    writeEnvValue(env, { cli: { type: expected.type, command: expected.binary } });
    log(`envs.${env}.cli 同步为期望值（未安装）：${expected.type} → ${expected.binary}`);
  }
  return { type: expected.type, command: expected.binary, found: false, version: null };
}

async function cmdDoctor(opts) {
  const advice = [];

  // 0a. 先弄清楚你在哪个环境跑（doctor 必须知道，才能对上正确的 CLI）。
  //     顺序：--env（会记到 config）> 上次记的 config.env > 都没有就问你一句。
  const envResult = resolveEnv(opts);
  if (envResult === null || (envResult && envResult.invalid)) {
    const bad = envResult && envResult.invalid;
    const msg = bad
      ? `没认出环境「${bad}」。请在这三个里挑一个重跑：claude-code（你在用 Claude Code）、workbuddy-cn（你在用 WorkBuddy 国内版）、qoderwork-cn（你在用 QoderWork 国内版）。像这样：doctor --env qoderwork-cn`
      : `先告诉我你在哪个环境跑，我才能装对应的 CLI。三选一，用 --env 带上：claude-code（Claude Code）、workbuddy-cn（WorkBuddy 国内版）、qoderwork-cn（QoderWork 国内版）。像这样：doctor --env qoderwork-cn`;
    advice.push(msg);
    log(`advice: ${msg}`);
    process.stdout.write(JSON.stringify({ ok: false, needEnv: true, env: null, advice }) + '\n');
    return 1;
  }
  const env = envResult;
  log(`host env: ${env}（${ENV_CLI[env].label}）`);

  // 0b. 把「当前这份 skill 拷贝」的安装路径登记到共享 ~/.webclaw3/config.json 的 envs[env].skillDir（幂等）：
  //    各宿主装的是各自隔离的物理拷贝，各自记在自己 env 名下；activeEnv 指向谁，pipeline 就用谁的 skillDir。
  //    与「切宿主后要重跑 doctor --env」的规矩自洽：那次重跑会把 activeEnv 切过来、并刷新该 env 的 skillDir。
  const skillDir = registerSkillDir(env);

  // 1. Node 版本（relay 依赖原生 WebSocket）
  const nodeMajor = parseInt(process.versions.node.split('.')[0], 10);
  const nodeOk = nodeMajor >= 22;
  if (!nodeOk) advice.push(`Node ${process.version} 过低，需要 >= 22`);

  // 2. relay：未监听则自动启动
  let relay = await checkPort(opts.port);
  let justStarted = false;
  if (!relay.listening) {
    log('relay not listening, auto-starting...');
    const started = await startRelayCore(opts);
    relay = { listening: started.listening, extensionConnected: started.extensionConnected };
    justStarted = true;
  }
  if (!relay.listening) advice.push(`relay 启动失败，查看日志 ${LOG_FILE}`);

  // 3. 扩展连接：扩展 keepalive 每 20s 重连，刚启动 relay 时多等一会
  let extConnected = relay.extensionConnected;
  if (relay.listening && !extConnected) {
    const deadline = Date.now() + (justStarted ? 25000 : 5000);
    log(`extension not connected, waiting up to ${justStarted ? 25 : 5}s...`);
    while (Date.now() < deadline) {
      await new Promise(r => setTimeout(r, 2000));
      if ((await checkPort(opts.port)).extensionConnected) { extConnected = true; break; }
    }
  }

  // 4. 未连接 → 区分三种情况。全程不碰 cdp-start（CDP 懒启动，探索中 CSP 兜底时才用）
  let chromeRunning = null;
  let extInstalled = null;
  if (relay.listening && !extConnected) {
    chromeRunning = isChromeRunning();
    if (!chromeRunning) {
      advice.push('Chrome 未运行：请打开 Chrome，扩展会在 20 秒内自动连上，然后重跑 doctor');
    } else {
      extInstalled = detectExtensionInstalled();
      // 扩展 zip 优先用本地 dist/ 里的（缺了自动下载兜底）；拿到后自动解压到 Downloads，好让用户找得到
      const zipPath = ensureDistFile(skillDir, /^wc3-chrome-extension-.*\.zip$/, 'wc3-chrome-extension-2.0.0.zip');
      const extractedDir = zipPath ? extractExtensionToDownloads(zipPath) : null;
      const folderHint = extractedDir
        ? `扩展文件夹已给你放到「${extractedDir}」`
        : '先下载 https://github.com/fatmind/webclaw3/blob/main/dist/wc3-chrome-extension-2.0.0.zip 并解压到一个好找的文件夹';
      const installSteps = '打开 chrome://extensions/ → 右上角打开「开发者模式」→ 点「加载已解压的扩展程序」→ 选中那个文件夹';
      if (extInstalled === false) {
        advice.push(`还没装浏览器扩展。${folderHint}，然后：${installSteps}。装完等 20 秒重跑 doctor。`);
      } else if (extInstalled === true) {
        advice.push('扩展装了但没连上：打开 chrome://extensions，确认 wc3 没被关掉，点一下「重新加载」，等 20 秒再重跑 doctor。');
      } else {
        advice.push(`没法确认扩展装没装，请打开 chrome://extensions 看一眼：没装的话，${folderHint}，然后 ${installSteps}；装了的话，确认 wc3 没被关掉、点「重新加载」，等 20 秒重跑 doctor。`);
      }
    }
  }

  // ── 生成四件套（本地生成需要；环境就绪≠可生成，ok 不含这层的 OK）──
  // "Chrome 登录态可用"：登录态是用户自己的、按站点，无法通用检查——
  // 以扩展连通为浏览器通道就绪的近似（生成时 explore 走真实站点登录态，按站点引导）

  // 5. Code CLI：生成器 spawn 的 LLM（烧用户 token）。按当前环境锁定，错配会被拒绝。
  const codeCli = detectCodeCli(env);
  if (!codeCli.found) {
    const exp = ENV_CLI[env];
    advice.push(`还差一个工具「${exp.binary}」没装（生成功能要用它）。请在终端直接运行这行命令装好：${exp.doc}。装完后按提示登录一次就行（一定要用它自己登录，App 里登过的不算）。注意认准${exp.label}，国内版和国际版不通用，别装错。`);
  }

  // 5a. codebuddy-code 双落 skills：WorkBuddy 把 skill 装在 ~/.workbuddy/skills/，
  //     但 spawn 出的 codebuddy CLI 读 ~/.codebuddy/skills/，需 symlink
  if (codeCli.type === 'codebuddy-code') {
    const codebuddySkills = join(homedir(), '.codebuddy', 'skills');
    const codebuddySkillLink = join(codebuddySkills, 'webclaw3');
    try {
      let cur = null;
      try { cur = existsSync(codebuddySkillLink) && lstatSync(codebuddySkillLink).isSymbolicLink() ? readlinkSync(codebuddySkillLink) : null; }
      catch { /* 路径不存在或无权限 */ }
      if (cur !== skillDir) {
        mkdirSync(codebuddySkills, { recursive: true });
        try { unlinkSync(codebuddySkillLink); } catch {}
        symlinkSync(skillDir, codebuddySkillLink);
        log(`codebuddy skills symlink: ${codebuddySkillLink} → ${skillDir}`);
      }
    } catch (e) {
      advice.push(`无法创建 ~/.codebuddy/skills/webclaw3 软链（${e.message}），explore 子会话可能加载不到 webclaw3 skill`);
    }
  }

  // 5b. qoder-code 登录引导：qodercli 无法复用 QoderWork 宿主登录态（宿主只把
  //     一次性凭证喂给自己的直系子进程），需用户手动 login 一次。skills 目录
  //     ~/.qoderwork/skills 与 CLI 读取目录一致，不需软链。
  if (codeCli.type === 'qoder-code' && codeCli.found) {
    const isCn = /qoderclicn/i.test(codeCli.command);
    const loginHint = isCn
      ? `在终端运行一次「${codeCli.command}」，进 TUI 后敲「/login」（浏览器授权，记得选国内站）`
      : `在终端运行一次「${codeCli.command} login」（浏览器授权）`;
    const loggedIn = checkQoderCliLogin(codeCli.command);
    if (loggedIn === false) {
      advice.push(`${codeCli.command} 还没登录：生成功能得先登录才能用。请${loginHint}，登录一次后就不用再管。注意：新装的 CLI 必须自己登录，App 里登过不算，登录态不能直接搬过来。`);
    } else if (loggedIn === null) {
      advice.push(`没法确认 ${codeCli.command} 登录没：要是生成时报未登录，就${loginHint} 登录一次。新装的 CLI 一定要自己登录，不能复用 App 的登录态。`);
    }
  }

  // 6. 生成器自身（wc3-pipeline :3460）：未装则从 dist/ 就地自动安装；装了没跑则自动启动
  let pipelineBinary = findPipelineBinary();
  if (!pipelineBinary) {
    pipelineBinary = installPipelineFromDist(skillDir);
  }
  const pipelineInstalled = !!pipelineBinary;
  let pipeline = await checkPipelinePort();
  if (pipelineInstalled && !pipeline.listening) {
    log('pipeline 已装未运行，自动启动...');
    pipeline = await startPipelineCore(opts);
  }
  if (!pipelineInstalled) {
    advice.push('生成器组件自动安装失败：请重新运行一次诊断（doctor）重试；若仍失败，可联系支持。');
  } else if (!pipeline.listening) {
    advice.push(`生成器启动失败，看日志 ${PIPELINE_LOG_FILE}`);
  }

  // 7. AK 与剩余次数：生成/拉经验/回传要 AK（过期/耗尽是软性信号，不拦 doctor 的 ok）
  const ak = readConfigValue('ak');
  let quota = null;
  if (!ak) {
    advice.push('未配置 AK：wc3-app 网页登录后获取，然后跑 webclaw3 config ak <key>（生成会扣次数）');
  } else {
    quota = await checkQuota(readConfigValue('appBase'), ak);
    if (quota?.error) advice.push(`AK 校验失败（${quota.error}）：重新获取或确认 wc3-app 地址`);
    else if (quota && quota.remaining_quota === 0) advice.push('剩余次数为 0：到 wc3-app 购买额度');
  }

  // 两层就绪判定：
  //   必需层（能探索）：Node + relay + 扩展连通
  //   提炼层（能提炼，环节③）：对应环境的 Code CLI 就绪 + 生成器安装并运行
  const l0Ok = nodeOk && relay.listening && extConnected;
  const genOk = codeCli.found && pipelineInstalled && pipeline.listening;
  const ok = l0Ok && genOk;
  const result = {
    ok,
    env,
    ready: { explore: l0Ok, generate: genOk },
    node: { version: process.version, ok: nodeOk },
    relay: { port: opts.port, listening: relay.listening, pid: readPidFile() },
    extension: { connected: extConnected, chromeRunning, installed: extInstalled },
    skill: { dir: skillDir },
    codeCli,
    pipeline: { installed: pipelineInstalled, listening: pipeline.listening, port: PIPELINE_PORT, binary: pipelineBinary },
    ak: { configured: !!ak, remainingQuota: quota?.remaining_quota ?? null },
    advice,
  };
  for (const a of advice) log(`advice: ${a}`);
  if (ok) log('all checks passed, ready to go');
  process.stdout.write(JSON.stringify(result) + '\n');
  return ok ? 0 : 1;
}

// 供 doctor 复用的 pipeline 启动（与 cmdPipelineStart 同逻辑，但返回结果而非写 stdout）
async function startPipelineCore(opts) {
  const binary = findPipelineBinary();
  if (!binary) return { listening: false };
  mkdirSync(PID_DIR, { recursive: true });
  const out = openSync(PIPELINE_LOG_FILE, 'a');
  const child = spawnDaemonViaLoginShell(binary, ['--serve'], out);
  writeFileSync(PIPELINE_PID_FILE, String(child.pid));
  const deadline = Date.now() + opts.wait * 1000;
  let last = { listening: false };
  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, 500));
    last = await checkPipelinePort();
    if (last.listening) break;
  }
  return last;
}

function checkQuota(appBase, ak) {
  return new Promise((resolve) => {
    const url = new URL('/api/user', appBase || 'https://webclaw3.com');
    const mod = url.protocol === 'https:' ? https : http;
    const req = mod.get({ host: url.hostname, port: url.port, path: url.pathname, timeout: 3000, headers: { Authorization: `Bearer ${ak}` } }, (res) => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => {
        if (res.statusCode !== 200) return resolve({ error: `HTTP ${res.statusCode}` });
        try {
          const d = JSON.parse(body);
          resolve({ remaining_quota: d.remaining_quota ?? null });
        } catch { resolve({ error: '响应非 JSON' }); }
      });
    });
    req.on('error', (e) => resolve({ error: e.message }));
    req.on('timeout', () => { req.destroy(); resolve({ error: '超时' }); });
  });
}

/** 把本 skill 安装目录（scripts/ 的上级）登记到 config.json 的 envs[env].skillDir，幂等回写 */
function registerSkillDir(env) {
  const skillDir = dirname(__dirname);
  try {
    if (readEnvValue(env, 'skillDir') !== skillDir) {
      writeEnvValue(env, { skillDir });
      log(`envs.${env}.skillDir registered: ${skillDir}`);
    }
  } catch (e) {
    log(`skillDir register failed: ${e.message}`);
  }
  return skillDir;
}

// --- CDP Proxy commands ---

function readCdpPidFile() {
  try {
    const v = parseInt(readFileSync(CDP_PID_FILE, 'utf-8').trim(), 10);
    return Number.isFinite(v) ? v : null;
  } catch { return null; }
}

function checkCdpPort(port, timeoutMs = 1000) {
  return new Promise((resolve) => {
    const req = http.get({ host: '127.0.0.1', port, path: '/health', timeout: timeoutMs }, (res) => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => {
        try {
          const data = JSON.parse(body);
          resolve({ listening: true, connected: !!data.connected, raw: data });
        } catch {
          resolve({ listening: true, connected: false, raw: body });
        }
      });
    });
    req.on('error', () => resolve({ listening: false, connected: false }));
    req.on('timeout', () => { req.destroy(); resolve({ listening: false, connected: false }); });
  });
}

async function cmdCdpStart(opts) {
  const port = opts.port || CDP_DEFAULT_PORT;
  const existing = await checkCdpPort(port);
  if (existing.listening) {
    log(`CDP proxy port ${port} already listening`);
    const out = { port, ...existing, pid: readCdpPidFile() };
    process.stdout.write(JSON.stringify(out) + '\n');
    return 0;
  }

  if (!existsSync(CDP_SCRIPT)) {
    log(`CDP proxy script not found: ${CDP_SCRIPT}`);
    process.stdout.write(JSON.stringify({ port, listening: false, connected: false, error: 'cdp-script-not-found' }) + '\n');
    return 1;
  }

  mkdirSync(PID_DIR, { recursive: true });

  const out = openSync(CDP_LOG_FILE, 'a');
  const child = spawnDaemonViaLoginShell('node', [CDP_SCRIPT, String(port)], out);
  writeFileSync(CDP_PID_FILE, String(child.pid));
  log(`spawned CDP proxy pid=${child.pid} port=${port}, waiting up to ${opts.wait}s`);

  const deadline = Date.now() + opts.wait * 1000;
  let last = { listening: false, connected: false };
  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, 500));
    last = await checkCdpPort(port);
    if (last.listening) break;
  }

  const result = { port, ...last, pid: child.pid };
  process.stdout.write(JSON.stringify(result) + '\n');
  if (!last.listening) {
    log(`CDP proxy port ${port} not listening after ${opts.wait}s; check ${CDP_LOG_FILE}`);
    return 1;
  }
  return 0;
}

async function cmdCdpStop(opts) {
  const port = opts.port || CDP_DEFAULT_PORT;
  const pid = readCdpPidFile();
  if (!pid) {
    log('CDP proxy: no pid file, nothing to stop');
    process.stdout.write(JSON.stringify({ port, listening: false, connected: false, stopped: false }) + '\n');
    return 0;
  }
  try {
    process.kill(pid, 'SIGTERM');
    log(`sent SIGTERM to CDP proxy pid=${pid}`);
  } catch (e) {
    log(`kill CDP proxy pid=${pid} failed: ${e.message}`);
  }
  const deadline = Date.now() + 5000;
  while (Date.now() < deadline) {
    if (!(await checkCdpPort(port)).listening) break;
    await new Promise(r => setTimeout(r, 200));
  }
  try { unlinkSync(CDP_PID_FILE); } catch {}
  process.stdout.write(JSON.stringify({ port, listening: false, connected: false, stopped: true }) + '\n');
  return 0;
}

async function cmdCdpStatus(opts) {
  const port = opts.port || CDP_DEFAULT_PORT;
  const r = await checkCdpPort(port, opts.timeout * 1000);
  const out = { port, ...r, pid: readCdpPidFile() };
  process.stdout.write(JSON.stringify(out) + '\n');
  return r.listening ? 0 : 1;
}

async function cmdCdpRestart(opts) {
  await cmdCdpStop(opts);
  return cmdCdpStart(opts);
}

async function main() {
  const sub = process.argv[2];
  if (!sub || sub === '-h' || sub === '--help') {
    printUsage();
    process.exit(0);
  }
  const opts = parseOpts(process.argv.slice(3));
  const isCdp = sub.startsWith('cdp-');
  if (!process.argv.slice(3).includes('--port')) {
    opts.port = isCdp ? CDP_DEFAULT_PORT : DEFAULT_PORT;
  }

  let code = 1;
  try {
    switch (sub) {
      case 'doctor':      code = await cmdDoctor(opts);      break;
      case 'start':       code = await cmdStart(opts);       break;
      case 'stop':        code = await cmdStop(opts);        break;
      case 'status':      code = await cmdStatus(opts);      break;
      case 'restart':     code = await cmdRestart(opts);     break;
      case 'cdp-start':   code = await cmdCdpStart(opts);    break;
      case 'cdp-stop':    code = await cmdCdpStop(opts);     break;
      case 'cdp-status':  code = await cmdCdpStatus(opts);   break;
      case 'cdp-restart': code = await cmdCdpRestart(opts);  break;
      case 'pipeline-start':   code = await cmdPipelineStart(opts);   break;
      case 'pipeline-stop':    code = await cmdPipelineStop();        break;
      case 'pipeline-status':  code = await cmdPipelineStatus(opts);  break;
      case 'pipeline-restart': code = await cmdPipelineRestart(opts); break;
      case 'config':      code = await cmdConfig(process.argv.slice(3)); break;
      default:
        log(`unknown subcommand: ${sub}`);
        printUsage();
        code = 1;
    }
  } catch (e) {
    log(`error: ${e.message}`);
    process.stdout.write(JSON.stringify({ port: opts.port, error: e.message }) + '\n');
    code = 1;
  }
  process.exit(code);
}

main();
