/**
 * 认一下这个命令跑在哪个 AI 助手里，网站授权页上显示「Claude Code 发起的登录」「Codex 发起的登录」，方便用户核对。
 *
 * 两条线索，先看进程树、再看环境变量：
 *   · 进程树：从父进程往上找，最近的那个认得出的程序就是它。Claude Code 跑在 Cursor 的
 *     终端里，往上既有 claude 又有 Cursor，算 Claude Code 才对 —— 所以按远近、不按名单顺序
 *   · 环境变量：npm 装的 Claude Code、Codex 进程名就是 node，进程树认不出来，靠它们自己
 *     给子进程留的变量兜底。WorkBuddy 这类桌面应用不确定留什么变量，主要靠进程树
 *
 * 认不出来就返回空串，授权页显示「命令行」。这里出任何错都不能影响登录，一律吞掉。
 * 用户想纠正的话设 STUDIO_AGENT=<名字>，优先级最高。
 */
import { execFileSync } from 'node:child_process';

// 进程路径里出现这些字样就认作对应的助手。按可执行文件的路径匹配（macOS 上是完整路径，
// Linux 上是进程名），不看命令行参数：参数里带着项目路径，项目叫 codex-demo 就认错了
const PROCESS_PATTERNS = [
  ['workbuddy', /workbuddy/i],
  // 阿里的 QwenWork / QoderWork 桌面端，要排在 qoder 前面
  ['qwenwork', /qwen[ _-]?work/i],
  ['qoderwork', /qoder[ _-]?work/i],
  ['codebuddy', /codebuddy/i],
  ['claude-code', /(^|\/)claude(\.app\/|$)|\/claude-code\//i],
  ['codex', /(^|\/)codex(\.app\/|$)|(^|\/)codex-[a-z0-9-]+$/i],
  ['cursor', /(^|\/)cursor(\.app\/|[ -]|$)/i],
  ['trae', /(^|\/)trae( cn)?(\.app\/|$)/i],
  ['qoder', /(^|\/)qoder(\.app\/|$)/i],
  ['windsurf', /(^|\/)windsurf(\.app\/|$)/i],
  ['kiro', /(^|\/)kiro(\.app\/|$)/i],
  ['gemini', /(^|\/)gemini$/i],
  ['opencode', /(^|\/)opencode$/i],
  ['qwen-code', /(^|\/)qwen$/i],
];

function fromEnv(env) {
  const has = (re) => Object.keys(env).some((k) => re.test(k));
  if (env.CLAUDECODE || env.CLAUDE_CODE_ENTRYPOINT) return 'claude-code';
  if (env.CODEX_SANDBOX || env.CODEX_THREAD_ID || env.CODEX_SANDBOX_NETWORK_DISABLED) return 'codex';
  if (has(/^WORKBUDDY_/)) return 'workbuddy';
  if (has(/^CODEBUDDY_/)) return 'codebuddy';
  if (has(/^QWEN_?WORK/i)) return 'qwenwork';
  if (has(/^QODER_?WORK/i)) return 'qoderwork';
  if (env.CURSOR_AGENT || env.CURSOR_TRACE_ID) return 'cursor';
  if (env.GEMINI_CLI) return 'gemini';
  if (env.OPENCODE) return 'opencode';
  // 新出的约定：AI_AGENT=claude-code_2-1-304_agent 这样，取第一段
  const generic = /^[a-z][a-z0-9-]{1,31}/i.exec(String(env.AI_AGENT || ''));
  return generic ? generic[0].toLowerCase() : '';
}

/** 父进程链上每一级的可执行文件路径，最近的在前。Windows 上没有 ps，返回空 */
function ancestors() {
  if (process.platform === 'win32') return [];
  const out = execFileSync('ps', ['-A', '-o', 'pid=,ppid=,comm='], {
    encoding: 'utf8',
    timeout: 3000,
    stdio: ['ignore', 'pipe', 'ignore'],
  });
  const table = new Map();
  for (const line of out.split('\n')) {
    const m = /^\s*(\d+)\s+(\d+)\s+(.*)$/.exec(line);
    if (m) table.set(Number(m[1]), { ppid: Number(m[2]), comm: m[3].trim() });
  }
  const chain = [];
  let pid = process.ppid;
  for (let i = 0; i < 30 && pid > 1 && table.has(pid); i += 1) {
    const row = table.get(pid);
    chain.push(row.comm);
    pid = row.ppid;
  }
  return chain;
}

export function fromProcessChain(chain) {
  for (const comm of chain) {
    for (const [name, re] of PROCESS_PATTERNS) {
      if (re.test(comm)) return name;
    }
  }
  return '';
}

let cached;

export function detectAgent(env = process.env) {
  if (cached !== undefined) return cached;
  const override = String(env.STUDIO_AGENT || '').trim().toLowerCase();
  let found = /^[a-z][a-z0-9-]{0,31}$/.test(override) ? override : '';
  if (!found) {
    try {
      found = fromProcessChain(ancestors());
    } catch {
      // ps 被沙箱拦了之类，退回环境变量
    }
  }
  if (!found) found = fromEnv(env);
  cached = found;
  return found;
}

export { fromEnv };
