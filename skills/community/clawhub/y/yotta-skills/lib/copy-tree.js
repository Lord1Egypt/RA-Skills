'use strict';

/**
 * 安装落位的复制原语（单一真源）。
 *
 * 口径（2026-10-01，与元造 0.1.3 的安装器修复对齐）：
 * - 顶层开发文件 / 目录（package.json / bin / node_modules / .git）只在**安装包顶层**跳过；
 *   技能包内嵌套的同名载荷（如 template/package.json、template/bin/install.js）必须保留。
 * - 缓存 / 编译产物（__pycache__ / .pytest_cache / .mypy_cache / *.pyc / *.pyo）任意层级都跳过。
 */

const fs = require('fs');
const path = require('path');
const linkSafety = require('./link-safety');

const COPY_SKIP = new Set(['package.json', 'bin', 'node_modules', '.git']);

function shouldSkipCache(name, isFile) {
  if (name === '__pycache__' || name === '.pytest_cache' || name === '.mypy_cache') return true;
  if (isFile && (name.endsWith('.pyc') || name.endsWith('.pyo'))) return true;
  return false;
}

function copyDir(src, dst, skip, topLevel) {
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (topLevel && skip.has(entry.name)) continue;
    if (shouldSkipCache(entry.name, entry.isFile())) continue;
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) {
      if (linkSafety.isDirectLink(d)) {
        throw new linkSafety.TargetError('目标目录包含符号链接或 junction，拒绝写入: ' + d);
      }
      fs.mkdirSync(d, { recursive: true });
      if (linkSafety.isDirectLink(d)) {
        throw new linkSafety.TargetError('目标目录包含符号链接或 junction，拒绝写入: ' + d);
      }
      copyDir(s, d, skip, false);
    } else if (entry.isFile()) {
      if (linkSafety.isDirectLink(d)) {
        throw new linkSafety.TargetError('目标文件是符号链接，拒绝写入: ' + d);
      }
      fs.copyFileSync(s, d);
    }
  }
}

module.exports = { COPY_SKIP, shouldSkipCache, copyDir };
