'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const manifestLib = require('./manifest');

const PHASES = ['setup', 'doctor', 'rollback'];

function parseJsonResult(stdout) {
  const text = String(stdout || '').trim();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch (_) {
    const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
    for (let i = lines.length - 1; i >= 0; i--) {
      if (!lines[i].startsWith('{')) continue;
      try {
        return JSON.parse(lines[i]);
      } catch (_) {
        // Keep looking for the structured result line.
      }
    }
  }
  return null;
}

function runLifecycleScript(scriptPath, args, options) {
  const opts = options || {};
  if (!scriptPath || !fs.existsSync(scriptPath) || !fs.statSync(scriptPath).isFile()) {
    return {
      ok: false,
      skipped: false,
      result: null,
      error: '生命周期脚本不存在: ' + (scriptPath || '未提供'),
      stdout: '',
      stderr: '',
      exitCode: null,
    };
  }
  if (!/\.(?:js|cjs)$/i.test(scriptPath)) {
    return {
      ok: false,
      skipped: false,
      result: null,
      error: '生命周期脚本必须为 Node.js .js/.cjs 文件',
      stdout: '',
      stderr: '',
      exitCode: null,
    };
  }

  const spawn = opts.spawnSync || spawnSync;
  const argv = [scriptPath].concat(Array.isArray(args) ? args : []).concat(['--json']);
  let proc;
  try {
    proc = spawn(process.execPath, argv, {
      cwd: opts.cwd || path.dirname(scriptPath),
      encoding: 'utf8',
      timeout: opts.timeout || 30000,
      maxBuffer: opts.maxBuffer || 4 * 1024 * 1024,
    });
  } catch (error) {
    return {
      ok: false,
      skipped: false,
      result: null,
      error: error.message,
      stdout: '',
      stderr: '',
      exitCode: null,
    };
  }

  const stdout = proc.stdout || '';
  const stderr = proc.stderr || '';
  const parsed = parseJsonResult(stdout);
  const exitCode = proc.status;
  if (proc.error) {
    return { ok: false, skipped: false, result: parsed, error: proc.error.message, stdout, stderr, exitCode };
  }
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    return {
      ok: false,
      skipped: false,
      result: null,
      error: '生命周期脚本未返回合法 JSON' + (stderr ? '：' + stderr.trim() : ''),
      stdout,
      stderr,
      exitCode,
    };
  }
  if (exitCode !== 0) {
    return {
      ok: false,
      skipped: false,
      result: parsed,
      error: parsed.error || stderr.trim() || ('生命周期脚本退出码 ' + exitCode),
      stdout,
      stderr,
      exitCode,
    };
  }
  if (parsed.ok === false) {
    return {
      ok: false,
      skipped: false,
      result: parsed,
      error: parsed.error || '生命周期脚本返回失败',
      stdout,
      stderr,
      exitCode,
    };
  }
  return { ok: true, skipped: false, result: parsed, error: null, stdout, stderr, exitCode };
}

function runPhase(packageDir, manifest, phase, context) {
  if (!PHASES.includes(phase)) {
    return { ok: false, skipped: false, result: null, error: '未知生命周期阶段: ' + phase };
  }
  const ctx = context || {};
  const install = manifest && manifest.install ? manifest.install : {};
  const rel = install[phase];
  if (!rel) {
    return { ok: true, skipped: true, result: null, error: null };
  }
  if (!manifestLib.isSafeRelativePath(rel)) {
    return { ok: false, skipped: false, result: null, error: '生命周期脚本路径不安全: ' + rel };
  }
  const root = path.resolve(packageDir);
  const scriptPath = path.resolve(root, rel);
  const relative = path.relative(root, scriptPath);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    return { ok: false, skipped: false, result: null, error: '生命周期脚本越出包目录: ' + rel };
  }

  const args = [];
  if (ctx.skillDir) args.push('--skill-dir', ctx.skillDir);
  if (ctx.packageDir || packageDir) args.push('--package-dir', ctx.packageDir || packageDir);
  if (ctx.dest) args.push('--dest', ctx.dest);
  if (ctx.snapshot) args.push('--snapshot', ctx.snapshot);
  return runLifecycleScript(scriptPath, args, {
    ...ctx.options,
    cwd: (ctx.options && ctx.options.cwd) || root,
  });
}

module.exports = { PHASES, parseJsonResult, runLifecycleScript, runPhase };
