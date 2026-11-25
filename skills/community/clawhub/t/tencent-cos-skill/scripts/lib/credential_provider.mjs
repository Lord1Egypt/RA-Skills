/**
 * 外部凭证提供方（credential process），做法参照 AWS CLI 的 credential_process。
 *
 * 没有任何已配置凭证时，执行一条命令取得临时密钥，登录与续期由该命令负责。典型提供方是 npm 包 tencentcloud-cos-oauth
 * 提供的 `tencentcloud-cos-oauth` 命令（浏览器授权登录，STS 临时密钥自动续期）。取得的临时密钥按「临时密钥」方式使用
 * （等同于设置了 TENCENT_COS_SECRET_ID / TENCENT_COS_SECRET_KEY / TENCENT_COS_TOKEN），只存在于当前进程内存。
 *
 * 只在以下条件都满足时启用（已有的凭证配置方式优先级都更高，行为不变）：
 *   - 未提供运行时凭证 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY / TENCENTCLOUD_TOKEN；
 *   - 未配置本地凭证 TENCENT_COS_SECRET_ID / TENCENT_COS_SECRET_KEY（含 .env / .env.enc）；
 *   - 非严格模式（KIKI 不为 1，由调用方判断）。
 *
 * 命令来源：
 *   - TENCENT_COS_CREDENTIAL_PROCESS：显式配置。JSON 字符串数组（如 ["node","/path/provider.mjs"]）或以空白分隔的命令行
 *     （路径含空格时用 JSON 数组）；设为 off / 0 / false / none 关闭。
 *   - 未配置：执行 `tencentcloud-cos-oauth credential --json`；命令不存在时视为没有提供方，静默回落到原有流程。
 *   命令存在但超时、异常退出或输出不是本协议时，同样回落，并在「缺少凭证」报错后附上原因。
 *
 * 执行方式：不经 shell。Windows 上自己按 PATH + PATHEXT 找到命令的完整路径（不搜当前目录），
 * 只有 .cmd / .bat（npm 全局命令就是 .cmd）必须经 cmd.exe 启动，此时每段参数加引号传入。
 *
 * 输出协议（stdout，JSON）：
 *   成功（退出码 0）：{ "success": true, "secretId", "secretKey", "sessionToken"?, "bucket"?, "region"? }
 *   失败（退出码非 0）：{ "success": false, "code", "error", "next"?, "hint"? }，如 NotLoggedIn
 *
 * 调用上下文：执行时设置 TENCENT_COS_CREDENTIAL_CONTEXT={"entry":"cos|ci|preview","action":"<动作名>"}
 * （只有入口与动作名，不含参数、路径、桶名），提供方可据此识别调用来自本技能脚本（如拒绝直接调用、按动作统计调用量）。
 */

import { execFileSync } from 'node:child_process';
import { statSync } from 'node:fs';
import { basename, extname, join } from 'node:path';

export const DEFAULT_PROVIDER_COMMAND = 'tencentcloud-cos-oauth';
// 提供方续期是一次网络请求（tencentcloud-cos-oauth 单次请求超时 15 秒），再留出 Windows 冷启动的余量
const TIMEOUT_MS = 30000;
const MAX_OUTPUT_BYTES = 256 * 1024;
const NAME_PATTERN = /^[a-z][a-z0-9-]{0,63}$/;
const ENTRIES = { 'cos_node.mjs': 'cos', 'ci_api.mjs': 'ci', 'preview_gen.mjs': 'preview' };

let attempted = false;
let lastError = null;

/** 单测用：清除本进程的调用记录 */
export function resetCredentialProvider() {
  attempted = false;
  lastError = null;
}

/** 解析提供方命令；返回 null 表示已关闭 */
export function resolveCredentialProcess(env = process.env) {
  const raw = String(env.TENCENT_COS_CREDENTIAL_PROCESS ?? '').trim();
  if (/^(off|0|false|none)$/i.test(raw)) return null;
  if (!raw) {
    return { command: DEFAULT_PROVIDER_COMMAND, args: ['credential', '--json'], explicit: false };
  }
  let argv = null;
  try {
    argv = raw.startsWith('[') ? JSON.parse(raw) : raw.split(/\s+/);
  } catch { /* 格式错误，下面统一报错 */ }
  if (!Array.isArray(argv) || !argv.length || !argv.every(a => typeof a === 'string' && a)) {
    return { invalid: true };
  }
  return { command: argv[0], args: argv.slice(1), explicit: true };
}

/** 入口与动作名：由脚本文件名与第一个参数得到 */
export function callerContext(argv = process.argv) {
  const entry = ENTRIES[basename(String(argv[1] || ''))];
  if (!entry) return null;
  const action = entry === 'preview' ? 'preview' : String(argv[2] || '');
  return NAME_PATTERN.test(action) ? { entry, action } : { entry };
}

const str = v => (typeof v === 'string' && v.trim() ? v.trim() : '');

/** 取环境变量（Windows 上 env 若是普通对象，键名大小写不固定，如 Path / PATH） */
function envValue(env, name) {
  const key = Object.keys(env).find(k => k.toUpperCase() === name);
  return key ? String(env[key] ?? '') : '';
}

/**
 * Windows：按 PATH + PATHEXT 找命令的完整路径，找不到返回 null。不搜当前目录：cmd.exe 和 Node 在 Windows 上
 * 默认先搜当前目录，工作区里放一个同名 .cmd 就会被执行。命令带路径时按用户配置原样使用。
 */
function findWindowsCommand(command, env) {
  if (/[\\/]/.test(command)) return command;
  const exts = (envValue(env, 'PATHEXT') || '.COM;.EXE;.BAT;.CMD').split(';').filter(Boolean).map(e => e.toUpperCase());
  const candidates = exts.includes(extname(command).toUpperCase()) ? [''] : exts;
  for (const raw of envValue(env, 'PATH').split(';')) {
    const dir = raw.trim().replace(/^"(.*)"$/, '$1');
    if (!dir) continue;
    for (const ext of candidates) {
      const file = join(dir, command + ext);
      try {
        if (statSync(file).isFile()) return file;
      } catch { /* 不存在 */ }
    }
  }
  return null;
}

/**
 * Windows：.cmd / .bat 只能经 cmd.exe 启动（Node 安全限制），整条命令自己拼好再交给 shell，
 * 每段加双引号（路径可含空格）。双引号、% 和换行在 cmd.exe 里无法可靠转义，含有时返回 null。
 */
function windowsCommandLine(argv) {
  if (argv.some(a => /["%\r\n]/.test(a))) return null;
  return argv.map(a => `"${a}"`).join(' ');
}

/**
 * 没有已配置凭证时向提供方取临时密钥，写入 env 的 TENCENT_COS_*（桶与地域都未设置时一并写入默认值）。
 * 每个进程最多执行一次。成功返回 true；失败原因见 credentialProviderHint()。
 */
export function loadProviderCredentials(env, { argv = process.argv, platform = process.platform, timeoutMs = TIMEOUT_MS } = {}) {
  if (attempted) return false;
  attempted = true;
  if (env.TENCENTCLOUD_SECRET_ID || env.TENCENTCLOUD_SECRET_KEY || env.TENCENTCLOUD_TOKEN) return false;
  if (env.TENCENT_COS_SECRET_ID || env.TENCENT_COS_SECRET_KEY) return false;

  const spec = resolveCredentialProcess(env);
  if (!spec) return false;
  if (spec.invalid) {
    lastError = { code: 'InvalidCredentialProcess', error: 'TENCENT_COS_CREDENTIAL_PROCESS 格式不正确' };
    return false;
  }
  const notFound = () => {
    if (spec.explicit) lastError = { code: 'CredentialProcessNotFound', error: `找不到凭证提供方命令 ${spec.command}` };
    return false;
  };
  let command = spec.command;
  let args = spec.args;
  let shell = false;
  if (platform === 'win32') {
    command = findWindowsCommand(spec.command, env);
    if (!command) return notFound();
    if (/\.(cmd|bat)$/i.test(command)) {
      command = windowsCommandLine([command, ...args]);
      if (!command) {
        lastError = { code: 'InvalidCredentialProcess', error: 'TENCENT_COS_CREDENTIAL_PROCESS 含有 cmd.exe 无法安全传递的字符（" % 或换行）' };
        return false;
      }
      args = [];
      shell = true;
    }
  }
  const childEnv = { ...env };
  delete childEnv.TENCENT_COS_CREDENTIAL_CONTEXT;
  const ctx = callerContext(argv);
  if (ctx) childEnv.TENCENT_COS_CREDENTIAL_CONTEXT = JSON.stringify(ctx);

  let stdout = '';
  let exitCode = 0;
  let signal = '';
  try {
    // stderr 不收集：用不到，而且输出过多会触发 maxBuffer，把已拿到的凭证误判为失败
    stdout = execFileSync(command, args, {
      encoding: 'utf-8', env: childEnv, stdio: ['ignore', 'pipe', 'ignore'], timeout: timeoutMs, maxBuffer: MAX_OUTPUT_BYTES, windowsHide: true, shell,
    });
  } catch (err) {
    if (err?.code === 'ENOENT') return notFound();
    if (err?.code === 'ETIMEDOUT') {
      lastError = { code: 'CredentialProcessTimeout', error: `凭证提供方 ${Math.round(timeoutMs / 1000)} 秒内未返回，请稍后重试` };
      return false;
    }
    stdout = err?.stdout ? String(err.stdout) : '';
    exitCode = typeof err?.status === 'number' ? err.status : 1;
    signal = err?.signal ? String(err.signal) : '';
  }

  let payload = null;
  try {
    payload = JSON.parse(stdout.trim());
  } catch { /* 非本协议 */ }
  if (!payload || typeof payload.success !== 'boolean') {
    lastError = exitCode !== 0
      ? { code: 'CredentialProcessFailed', error: `凭证提供方异常退出（${signal ? `信号 ${signal}` : `退出码 ${exitCode}`}）` }
      : { code: 'InvalidCredentialProcessOutput', error: '凭证提供方输出不是约定的 JSON' };
    return false;
  }
  if (exitCode !== 0 || payload.success !== true || !str(payload.secretId) || !str(payload.secretKey)) {
    lastError = { code: str(payload.code) || 'CredentialProcessFailed', error: str(payload.error) || '凭证提供方未返回可用凭证', next: str(payload.next) };
    return false;
  }

  env.TENCENT_COS_SECRET_ID = str(payload.secretId);
  env.TENCENT_COS_SECRET_KEY = str(payload.secretKey);
  env.TENCENT_COS_TOKEN = str(payload.sessionToken) || str(payload.token);
  if (!env.TENCENT_COS_BUCKET && !env.TENCENT_COS_REGION && str(payload.bucket) && str(payload.region)) {
    env.TENCENT_COS_BUCKET = str(payload.bucket);
    env.TENCENT_COS_REGION = str(payload.region);
  }
  return true;
}

/** 提供方失败时附在「缺少凭证」报错后的说明（含下一步命令）；没有失败时为空串 */
export function credentialProviderHint() {
  if (!lastError) return '';
  return `；凭证提供方：${lastError.error}（${lastError.code}）${lastError.next ? `，下一步：${lastError.next}` : ''}`;
}
