'use strict';
/**
 * yotta-skills 受信校验器（元信）记录与身份校验（v0.19.13）。
 *
 * 背景：旧实现用「本地技能注册表里 slug=yotta-verify 的 source_dirs」发现校验器，
 * 而注册表身份来自被扫描技能自己 SKILL.md frontmatter 的 `name` —— 任意目录只要自称
 * `yotta-verify` 并提供 `scripts/yotta_verify.py`，就会被当作扫描引擎执行
 * （可执行任意代码，并可伪造 `SAFE TO INSTALL` 结论）。
 *
 * 新模型：
 *   1. 只有「安装管线校验通过后写入的安装记录」才算受信来源（路径 + SHA-256 双绑定）；
 *   2. 记录缺失 / 摘要不符 / 身份不符 / 路径经符号链接跳转 → 一律 fail-closed，
 *      交由上层走自举安装（从 npm 重新装一份干净的元信）；
 *   3. 用户显式指定（`--verify` / `YOTTA_SKILLS_VERIFY`）保留为人工可信路径，不参与本校验。
 *
 * 零依赖：只用 Node.js 标准库。
 */
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const RECORD_FILE_NAME = 'trusted-verifier.json';
const REGISTRY_DIR_NAME = '.yottaskills';
const EXPECTED = {
  slug: 'yotta-verify',
  pkg: '@yottameta/yotta-verify',
  trust: 'yottameta',
};

/** 安装记录路径：与注册表同目录（支持 YOTTA_SKILLS_REGISTRY_FILE 多 agent 隔离）。 */
function recordPath(registryFile) {
  if (registryFile) return path.join(path.dirname(path.resolve(registryFile)), RECORD_FILE_NAME);
  const override = String(process.env.YOTTA_SKILLS_REGISTRY_FILE || '').trim();
  if (override) return path.join(path.dirname(path.resolve(override)), RECORD_FILE_NAME);
  return path.join(os.homedir(), REGISTRY_DIR_NAME, RECORD_FILE_NAME);
}

function sha256File(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function loadRecord(registryFile) {
  try {
    const value = JSON.parse(fs.readFileSync(recordPath(registryFile), 'utf8'));
    return (value && typeof value === 'object') ? value : null;
  } catch (_) {
    return null;
  }
}

function saveRecord(record, registryFile) {
  const file = recordPath(registryFile);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(record, null, 2) + '\n', 'utf8');
  return file;
}

function frontmatterValue(skillFile, key) {
  let text;
  try {
    text = fs.readFileSync(skillFile, 'utf8');
  } catch (_) {
    return null;
  }
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return null;
  const re = new RegExp('^' + key + ':\\s*(.+?)\\s*$', 'm');
  const hit = m[1].match(re);
  return hit ? hit[1].replace(/^["']|["']$/g, '') : null;
}

/**
 * 检查候选引擎是否「长得像」一份元信包（不做信任判定）：
 * 路径不能经符号链接跳转；包内必须有 SKILL.md + skill-manifest.json，
 * 且 slug / package / trust / 版本与 SKILL.md 一致。
 */
function inspectPackage(enginePath) {
  if (!enginePath) return { ok: false, reason: '未指定引擎路径' };
  const resolved = path.resolve(String(enginePath));
  let real;
  try {
    if (!fs.statSync(resolved).isFile()) return { ok: false, reason: '引擎路径不是文件' };
    real = fs.realpathSync(resolved);
  } catch (_) {
    return { ok: false, reason: '引擎文件不存在' };
  }
  if (real !== resolved) return { ok: false, reason: '引擎路径经符号链接跳转，拒绝' };

  const skillDir = path.dirname(path.dirname(resolved));
  const skillFile = path.join(skillDir, 'SKILL.md');
  const manifestFile = path.join(skillDir, 'skill-manifest.json');
  if (!fs.existsSync(skillFile)) return { ok: false, reason: '缺少 SKILL.md' };
  if (!fs.existsSync(manifestFile)) return { ok: false, reason: '缺少 skill-manifest.json' };

  const skillName = frontmatterValue(skillFile, 'name');
  if (skillName !== EXPECTED.slug) {
    return { ok: false, reason: 'SKILL.md name 不是 ' + EXPECTED.slug };
  }
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
  } catch (_) {
    return { ok: false, reason: 'skill-manifest.json 解析失败' };
  }
  if (manifest.slug !== EXPECTED.slug) return { ok: false, reason: 'manifest slug 不符' };
  if (manifest.package !== EXPECTED.pkg) return { ok: false, reason: 'manifest package 不符' };
  if (manifest.trust !== EXPECTED.trust) return { ok: false, reason: 'manifest trust 不符' };
  const skillVersion = frontmatterValue(skillFile, 'version');
  if (!skillVersion || manifest.version !== skillVersion) {
    return { ok: false, reason: 'manifest 与 SKILL.md 版本不一致' };
  }

  return {
    ok: true,
    path: resolved,
    reason: null,
    info: {
      slug: manifest.slug,
      package: manifest.package,
      version: manifest.version,
      skillDir: skillDir,
      sha256: sha256File(resolved),
    },
  };
}

/** 身份 + 摘要双绑定校验：options.record 为安装记录（缺失即 fail-closed）。 */
function verifyEngine(enginePath, options) {
  const opts = options || {};
  const inspected = inspectPackage(enginePath);
  if (!inspected.ok) return inspected;
  const record = opts.record;
  if (opts.requireRecord === false) return inspected;
  if (!record || !record.path || !record.sha256) {
    return { ok: false, reason: '缺少受信安装记录（fail-closed）' };
  }
  if (path.resolve(String(record.path)) !== inspected.path) {
    return { ok: false, reason: '安装记录路径与候选引擎不一致' };
  }
  if (String(record.sha256).toLowerCase() !== inspected.info.sha256.toLowerCase()) {
    return { ok: false, reason: '引擎摘要与安装记录不一致' };
  }
  return inspected;
}

module.exports = {
  RECORD_FILE_NAME,
  EXPECTED,
  recordPath,
  sha256File,
  loadRecord,
  saveRecord,
  inspectPackage,
  verifyEngine,
};
