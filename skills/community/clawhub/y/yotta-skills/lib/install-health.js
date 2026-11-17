'use strict';
const fs = require('fs');
const path = require('path');
const manifestLib = require('./manifest');
const scanLib = require('./skills-scan');

function addCheck(checks, id, ok, message, severity, hint) {
  checks.push({
    id,
    ok: !!ok,
    severity: severity || (ok ? 'info' : 'error'),
    message,
    hint: hint || null,
  });
}

function readManifest(target, slug) {
  const file = path.join(target, manifestLib.MANIFEST_FILE);
  if (!fs.existsSync(file)) return { value: null, error: null };
  try {
    return { value: JSON.parse(fs.readFileSync(file, 'utf8')), error: null };
  } catch (error) {
    return { value: null, error: '无法解析 skill-manifest.json: ' + error.message };
  }
}

/** 优先读取目标目录对应的副本版本，旧注册表缺少 variants 时回退聚合版本。 */
function registryVersionForTarget(record, target) {
  const variants = Array.isArray(record.variants) ? record.variants : [];
  const normalizedTarget = path.resolve(target);
  const exact = variants.find((variant) => {
    if (!variant || !variant.dir) return false;
    return path.resolve(variant.dir) === normalizedTarget;
  });
  if (exact && exact.version) {
    return { version: String(exact.version).trim(), scope: 'target' };
  }
  return { version: record.version ? String(record.version).trim() : '', scope: 'aggregate' };
}

function checkInstalledSkill(context) {
  const ctx = context || {};
  const slug = String(ctx.slug || '');
  const target = ctx.target ? path.resolve(ctx.target) : '';
  const checks = [];
  const errors = [];
  const warnings = [];
  const fixes = [];
  let version = null;

  if (!slug) {
    addCheck(checks, 'slug', false, '缺少技能 slug');
    errors.push('缺少技能 slug');
  }
  if (!target || !fs.existsSync(target) || !fs.statSync(target).isDirectory()) {
    addCheck(checks, 'target', false, '技能目录不存在' + (target ? ': ' + target : ''));
    errors.push('技能目录不存在' + (target ? ': ' + target : ''));
    return { ok: false, slug, version, checks, errors, warnings, fixes };
  }
  addCheck(checks, 'target', true, '技能目录存在');

  const skillFile = path.join(target, 'SKILL.md');
  let text = null;
  try {
    text = fs.readFileSync(skillFile, 'utf8');
    addCheck(checks, 'skill_file', true, 'SKILL.md 可读');
  } catch (error) {
    addCheck(checks, 'skill_file', false, 'SKILL.md 不可读: ' + error.message);
    errors.push('SKILL.md 不可读: ' + error.message);
  }

  let frontmatter = null;
  if (text !== null) {
    frontmatter = scanLib.parseFrontmatter(text);
    if (!frontmatter) {
      addCheck(checks, 'frontmatter', false, 'SKILL.md 缺少有效 frontmatter');
      errors.push('SKILL.md 缺少有效 frontmatter');
    } else {
      addCheck(checks, 'frontmatter', true, 'SKILL.md frontmatter 有效');
      if (frontmatter.name !== slug) {
        addCheck(checks, 'slug_identity', false, 'SKILL.md name 与目标 slug 不一致');
        errors.push('SKILL.md name 与目标 slug 不一致');
      } else {
        addCheck(checks, 'slug_identity', true, 'SKILL.md slug 一致');
      }
      version = frontmatter.version ? String(frontmatter.version).trim() : null;
      if (!version || !/^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$/.test(version)) {
        addCheck(checks, 'version_format', false, 'SKILL.md 版本号非法');
        errors.push('SKILL.md 版本号非法');
      } else {
        addCheck(checks, 'version_format', true, 'SKILL.md 版本号有效');
      }
    }
  }

  if (ctx.expectedVersion && version && version !== ctx.expectedVersion) {
    addCheck(checks, 'version_match', false, '版本不一致：已安装 v' + version + '，期望 v' + ctx.expectedVersion);
    errors.push('版本不一致：已安装 v' + version + '，期望 v' + ctx.expectedVersion);
  } else if (ctx.expectedVersion && version) {
    addCheck(checks, 'version_match', true, '版本与期望一致');
  }

  const loadedManifest = readManifest(target, slug);
  if (loadedManifest.error) {
    addCheck(checks, 'manifest', false, loadedManifest.error);
    errors.push(loadedManifest.error);
  } else if (loadedManifest.value) {
    if (loadedManifest.value.trust !== 'yottameta') {
      addCheck(checks, 'manifest_trust', false, 'manifest trust 必须为 yottameta');
      errors.push('manifest trust 必须为 yottameta');
    } else {
      addCheck(checks, 'manifest_trust', true, 'manifest trust 为 yottameta');
    }
    const validation = manifestLib.validateManifest(loadedManifest.value, {
      skill: {
        slug,
        pkg: ctx.expectedPackage || loadedManifest.value.package,
        version: version || loadedManifest.value.version,
      },
      pkgDir: target,
      requirePackageJson: false,
    });
    if (!validation.ok) {
      addCheck(checks, 'manifest', false, 'manifest 校验失败: ' + validation.errors.join('; '));
      errors.push.apply(errors, validation.errors);
    } else {
      addCheck(checks, 'manifest', true, 'manifest 校验通过');
    }
  } else {
    addCheck(checks, 'manifest', true, '未提供 skill-manifest.json，使用家族默认契约');
  }

  if (ctx.registry) {
    const record = ctx.registry.skills && ctx.registry.skills[slug];
    if (!record || record.status === 'gone') {
      addCheck(checks, 'registry', false, '注册表未记录当前技能', 'warning');
      warnings.push('注册表未记录当前技能');
      fixes.push('运行 yotta-skills --reindex 重扫注册表');
    } else {
      const registryVersion = registryVersionForTarget(record, target);
      if (version && registryVersion.version && registryVersion.version !== version) {
        const scopeText = registryVersion.scope === 'target' ? '注册表版本（目标副本）' : '注册表版本（聚合）';
        addCheck(
          checks,
          'registry',
          false,
          scopeText + ' v' + registryVersion.version + ' 与已安装 v' + version + ' 不一致',
          'warning',
        );
        warnings.push(scopeText + ' v' + registryVersion.version + ' 与已安装 v' + version + ' 不一致');
        fixes.push('运行 yotta-skills --reindex 重扫注册表');
      } else {
        addCheck(checks, 'registry', true, '注册表记录一致');
      }
    }
  }

  return {
    ok: errors.length === 0,
    slug,
    version,
    checks,
    errors,
    warnings,
    fixes: Array.from(new Set(fixes)),
  };
}

module.exports = { checkInstalledSkill };
