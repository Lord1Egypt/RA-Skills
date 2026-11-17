'use strict';
const fs = require('fs');
const path = require('path');

const OFFICIAL_REGISTRY = 'https://registry.npmjs.org/';
const FALLBACK_HINT =
  '提示：镜像同步延迟时可用官方源重试 —— 设置环境变量 npm_config_registry=' + OFFICIAL_REGISTRY +
  '，或 YOTTA_SKILLS_NPM_FLAGS=--registry=' + OFFICIAL_REGISTRY;

function isNotFound(raw) {
  const text = String(raw || '');
  return /\bE404\b/.test(text) || /\b404 Not Found\b/i.test(text) || /could not be found/i.test(text);
}

function hasRegistryFlag(args) {
  return (args || []).some((arg) => arg === '--registry' || String(arg).startsWith('--registry='));
}

function briefOf(raw) {
  const lines = String(raw || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  return lines.slice(-4).join(' | ');
}

/** 把 spawn 层错误（如 ENOENT：npm 缺失）并入原始错误文本，供上层人话提示识别。 */
function rawOf(result) {
  if (result && result.error && result.error.message) return String(result.error.message).trim();
  return String((result && result.stderr) || (result && result.stdout) || 'npm pack 失败').trim();
}

function findTarball(stdout, packDir, readdirSync) {
  const lines = String(stdout || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  let tarball = null;
  for (const line of lines) if (/\.tgz$/.test(line)) tarball = line;
  if (tarball) return tarball;
  try {
    const found = readdirSync(packDir).filter((name) => name.endsWith('.tgz'));
    if (found.length === 1) return found[0];
  } catch (_) {
    /* ignore */
  }
  return null;
}

/**
 * 创建 npm pack 执行器。
 *
 * 默认源（国内镜像）拉不到 tarball 时会报 404 —— 此时自动改用官方源重试一次，
 * 并把 registryFallback 标记回传给安装管线（写入证据）。用户已显式指定 registry、
 * 或设置 YOTTA_SKILLS_NO_FALLBACK=1 时不重试。
 */
function createPackRunner(deps) {
  const spawnSync = deps.spawnSync;
  const specOf = deps.specOf;
  const resolveNpm = deps.resolveNpm;
  const readdirSync = deps.readdirSync || fs.readdirSync;
  const fallbackDisabled = deps.fallbackDisabled || (() => process.env.YOTTA_SKILLS_NO_FALLBACK === '1');

  return function runNpmPack(skill, opts, packDir) {
    const spec = specOf(skill, opts.pin);
    const baseArgs = ['pack', spec, '--pack-destination', packDir];
    const flags = (process.env.YOTTA_SKILLS_NPM_FLAGS || '').trim();
    if (flags) baseArgs.push(...flags.split(/\s+/));
    const npm = resolveNpm(opts);
    const attempt = (args) => spawnSync(npm.bin, [...npm.prefix, ...args], {
      encoding: 'utf8',
      timeout: 180000,
      maxBuffer: 64 * 1024 * 1024,
      shell: npm.shell,
      // 0.29.5 S4：显式继承调用方环境（YOTTA_SKILLS_REGISTRY_FILE / YOTTA_SKILLS_MANIFEST /
      // npm_config_* 等必须传到 npm / npx 子进程；此前依赖 spawnSync 默认继承，行为不变）。
      env: process.env,
    });

    let result = attempt(baseArgs);
    let registryFallback = false;
    if (result.status !== 0) {
      const raw = rawOf(result);
      if (!fallbackDisabled() && !hasRegistryFlag(baseArgs) && isNotFound(raw)) {
        result = attempt([...baseArgs, '--registry', OFFICIAL_REGISTRY]);
        registryFallback = result.status === 0;
      }
    }
    if (result.status !== 0) {
      const raw = rawOf(result);
      const brief = briefOf(raw) || 'npm pack 失败';
      const hint = isNotFound(raw) ? '\n  ' + FALLBACK_HINT : '';
      return { error: brief + hint, detail: raw };
    }
    const tarball = findTarball(result.stdout, packDir, readdirSync);
    if (!tarball) return { error: '未找到 npm pack 产物（' + spec + '）' };
    const versionMatch = String(tarball).match(/-([0-9]+\.[0-9]+\.[0-9]+)\.tgz$/);
    return {
      tarball: path.join(packDir, tarball),
      resolved: versionMatch ? versionMatch[1] : null,
      spec,
      registryFallback,
    };
  };
}

module.exports = {
  OFFICIAL_REGISTRY,
  FALLBACK_HINT,
  isNotFound,
  hasRegistryFlag,
  createPackRunner,
};
