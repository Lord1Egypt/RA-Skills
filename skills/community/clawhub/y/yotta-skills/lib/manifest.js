'use strict';
const fs = require('fs');
const path = require('path');

const MANIFEST_FILE = 'skill-manifest.json';

function defaultManifest(skill) {
  return {
    manifestVersion: 1,
    slug: skill.slug,
    name: skill.name,
    package: skill.pkg,
    version: skill.version,
    trust: 'yottameta',
    install: {
      idempotent: true,
      network: 'registry',
    },
    permissions: {
      filesystem: 'user-skills-dir',
      network: 'registry',
      process: 'child-process',
      note: '仅调用本包内安装与自检脚本；默认无自定义脚本。',
    },
    auto_apply: {
      mode: 'route',
      note: '元阁只给路由建议；安装与调用均由用户确认后执行，不自动调用。',
    },
  };
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function readSkillVersion(pkgDir) {
  try {
    const text = fs.readFileSync(path.join(pkgDir, 'SKILL.md'), 'utf8');
    const match = text.match(/^version:\s*([0-9]+\.[0-9]+\.[0-9]+)/m);
    return match ? match[1] : null;
  } catch (_) {
    return null;
  }
}

function isSafeRelativePath(value) {
  if (typeof value !== 'string' || value.trim() === '') return false;
  if (path.isAbsolute(value) || /^[A-Za-z]:[\\/]/.test(value)) return false;
  const parts = value.split(/[\\/]+/);
  return !parts.includes('..');
}

function validateManifest(manifest, context) {
  const errors = [];
  const skill = context.skill;
  const pkgDir = context.pkgDir;
  const required = ['manifestVersion', 'slug', 'name', 'package', 'version', 'trust', 'install', 'permissions'];
  for (const key of required) {
    if (manifest[key] === undefined) errors.push('缺少字段: ' + key);
  }
  if (manifest.manifestVersion !== 1) errors.push('manifestVersion 必须为 1');
  if (manifest.slug !== skill.slug) errors.push('slug 与清单不一致');
  if (manifest.package !== skill.pkg) errors.push('package 与清单不一致');
  if (!/^[a-z0-9][a-z0-9-]*$/.test(String(manifest.slug || ''))) errors.push('slug 格式非法');
  if (!/^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$/.test(String(manifest.version || ''))) {
    errors.push('version 格式非法');
  }
  if (!['yottameta', 'third-party-verified', 'unknown'].includes(manifest.trust)) errors.push('trust 非法');
  if (!manifest.install || manifest.install.idempotent !== true) errors.push('install.idempotent 必须为 true');
  if (!manifest.permissions || typeof manifest.permissions !== 'object') errors.push('permissions 缺失');
  if (manifest.permissions && !['none', 'user-skills-dir', 'project-dir', 'user-config', 'other'].includes(manifest.permissions.filesystem)) {
    errors.push('permissions.filesystem 非法');
  }
  if (manifest.permissions && !['none', 'registry', 'allowlist', 'other'].includes(manifest.permissions.network)) {
    errors.push('permissions.network 非法');
  }

  let packageMeta = null;
  const packageJsonPath = path.join(pkgDir, 'package.json');
  if (fs.existsSync(packageJsonPath)) {
    try {
      packageMeta = readJson(packageJsonPath);
    } catch (error) {
      errors.push('无法读取 package.json: ' + error.message);
    }
  } else if (context.requirePackageJson !== false) {
    errors.push('无法读取 package.json: 文件不存在');
  }
  if (packageMeta && packageMeta.name !== skill.pkg) errors.push('package.json.name 与清单不一致');
  if (packageMeta && packageMeta.version !== manifest.version) {
    errors.push('package.json.version 与 manifest.version 不一致');
  }
  const skillVersion = readSkillVersion(pkgDir);
  if (skillVersion !== manifest.version) errors.push('SKILL.md.version 与 manifest.version 不一致');
  for (const key of ['setup', 'doctor', 'rollback']) {
    const rel = manifest.install && manifest.install[key];
    if (rel !== undefined && !isSafeRelativePath(rel)) errors.push('install.' + key + ' 路径不安全');
  }
  return { ok: errors.length === 0, errors };
}

function loadManifest(context) {
  const file = path.join(context.pkgDir, MANIFEST_FILE);
  if (!fs.existsSync(file)) {
    return {
      manifest: defaultManifest(context.skill),
      source: 'family-default',
      errors: [],
    };
  }

  let value;
  try {
    value = readJson(file);
  } catch (error) {
    return {
      manifest: null,
      source: 'package',
      errors: ['无法解析 skill-manifest.json: ' + error.message],
    };
  }
  const validation = validateManifest(value, context);
  return {
    manifest: value,
    source: 'package',
    errors: validation.errors,
  };
}

module.exports = {
  MANIFEST_FILE,
  defaultManifest,
  loadManifest,
  validateManifest,
  isSafeRelativePath,
};
