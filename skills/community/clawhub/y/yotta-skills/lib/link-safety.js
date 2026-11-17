'use strict';

/**
 * 安装目标链接防护（元阁 install / update 单一真源）。
 *
 * 规则：
 * - 普通目录 / 不存在的目标：按原路径安装。
 * - 受管 Hub 链接（目标 basename = slug，父目录含 .yotta-hub.json / .yotta-links.json）：
 *   解析 realpath，在真实目录上更新，保留链接。
 * - 任意其他链接（含 Windows junction / reparse point）：fail-closed。
 * - 已存在的目标树里发现任意嵌套链接：fail-closed，避免复制 / 快照 / 回滚写穿。
 */

const fs = require('fs');
const path = require('path');

class TargetError extends Error {
  constructor(message) {
    super(message);
    this.name = 'TargetError';
    this.code = 'TARGET';
  }
}

function normalized(value) {
  return process.platform === 'win32'
    ? path.resolve(value).toLowerCase()
    : path.resolve(value);
}

function isDirectLink(target) {
  let stat = null;
  try {
    stat = fs.lstatSync(target);
  } catch (_) {
    return false;
  }
  if (stat.isSymbolicLink()) return true;
  try {
    const real = fs.realpathSync(target);
    const parentReal = fs.realpathSync(path.dirname(target));
    return normalized(real) !== normalized(path.join(parentReal, path.basename(target)));
  } catch (_) {
    return false;
  }
}

function isManagedHubTarget(target, slug) {
  if (!isDirectLink(target)) return false;
  try {
    const real = fs.realpathSync(target);
    if (path.basename(real) !== slug) return false;
    const parent = path.dirname(real);
    return fs.existsSync(path.join(parent, '.yotta-hub.json'))
      || fs.existsSync(path.join(parent, '.yotta-links.json'));
  } catch (_) {
    return false;
  }
}

function assertNoNestedLinks(root) {
  let stat = null;
  try {
    stat = fs.lstatSync(root);
  } catch (_) {
    return;
  }
  if (!stat.isDirectory()) return;
  for (const name of fs.readdirSync(root)) {
    const current = path.join(root, name);
    if (isDirectLink(current)) {
      throw new TargetError('目标目录包含符号链接或 junction，拒绝写入: ' + current);
    }
    assertNoNestedLinks(current);
  }
}

function resolveInstallTarget(target, slug) {
  const requested = path.resolve(target);
  let stat = null;
  try {
    stat = fs.lstatSync(requested);
  } catch (_) {
    return { target: requested, viaLink: false };
  }
  if (stat.isSymbolicLink() || isDirectLink(requested)) {
    if (!isManagedHubTarget(requested, slug)) {
      throw new TargetError('目标目录是符号链接或 junction，拒绝跟随: ' + requested);
    }
    const real = fs.realpathSync(requested);
    assertNoNestedLinks(real);
    return { target: real, viaLink: true };
  }
  if (!stat.isDirectory()) {
    throw new TargetError('目标路径已存在且不是目录: ' + requested);
  }
  assertNoNestedLinks(requested);
  return { target: requested, viaLink: false };
}

module.exports = {
  TargetError,
  isDirectLink,
  isManagedHubTarget,
  assertNoNestedLinks,
  resolveInstallTarget,
};
