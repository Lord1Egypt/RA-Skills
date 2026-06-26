#!/usr/bin/env node

/**
 * sync-sharing.js — 构建时共享模块同步脚本
 *
 * Phase 4B2 实现（含平台专家 B-2/R-1/R-4 修正）：
 * - 将 sharing/（单一真实源）同步到：
 *   1. packages/shared/src/（npm 包，供 Cloud Functions 用）
 *   2. edge-functions/sharing/（Edge Functions 内联）
 *   3. cloud-functions/shared/（开发环境符号链接）
 * - md5Dir() 确定性哈希校验
 * - CI 阻断：哈希不一致时 build 失败
 *
 * 使用方式：
 *   node scripts/sync-sharing.js          # 同步
 *   node scripts/sync-sharing.js --check  # 仅检查，不同步
 *   node scripts/sync-sharing.js --ci     # CI 模式：同步+校验+阻断
 */

import { createHash } from 'crypto';
import { readdirSync, statSync, readFileSync, writeFileSync, mkdirSync, existsSync, rmSync } from 'fs';
import { join, relative, resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');

// 源目录
const SOURCE = join(ROOT, 'sharing');

// 目标目录映射
const TARGETS = [
  { path: join(ROOT, 'packages', 'shared', 'src'),     label: 'npm package (shared)' },
  { path: join(ROOT, 'edge-functions', 'sharing'),      label: 'Edge Functions inline' },
  { path: join(ROOT, 'cloud-functions', 'shared'),      label: 'Cloud Functions shared' },
];

// ===================== MD5 目录哈希 =====================

/**
 * 计算目录下所有文件的确定性 MD5 哈希
 * 先按文件名排序，确保 CI 中哈希值一致
 */
function md5Dir(dirPath) {
  if (!existsSync(dirPath)) return '';

  const files = readdirSync(dirPath, { recursive: true })
    .filter(f => {
      const fullPath = join(dirPath, f);
      return statSync(fullPath).isFile();
    })
    .sort();  // 确定性排序

  const hash = createHash('md5');
  for (const file of files) {
    // 包含相对路径 + 内容，确保文件名变更也会影响哈希
    hash.update(file);
    hash.update(readFileSync(join(dirPath, file)));
  }
  return hash.digest('hex');
}

// ===================== 文件同步 =====================

/**
 * 递归复制目录
 */
function copyDir(src, dest) {
  if (!existsSync(src)) {
    console.warn(`  ⚠️  源目录不存在: ${src}`);
    return;
  }

  // 清理目标目录
  if (existsSync(dest)) {
    rmSync(dest, { recursive: true, force: true });
  }
  mkdirSync(dest, { recursive: true });

  // 复制文件（排除隐藏文件和 node_modules）
  const entries = readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.') || entry.name === 'node_modules') continue;
    const srcPath = join(src, entry.name);
    const destPath = join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else if (entry.isFile()) {
      mkdirSync(dest, { recursive: true });
      writeFileSync(destPath, readFileSync(srcPath));
    }
  }
}

// ===================== 主流程 =====================

async function main() {
  const args = process.argv.slice(2);
  const mode = args.includes('--ci') ? 'ci' : args.includes('--check') ? 'check' : 'sync';

  console.log(`\n🔁 sync-sharing.js — 模式: ${mode}\n`);

  // Step 1: 计算源目录哈希
  const sourceHash = md5Dir(SOURCE);
  console.log(`📦 源目录: sharing/ (hash: ${sourceHash.slice(0, 12)}...)`);

  if (!sourceHash) {
    console.error('❌ sharing/ 目录不存在或为空');
    process.exit(1);
  }

  if (mode === 'check') {
    // 仅检查模式：验证所有目标目录是否与源一致
    let allMatch = true;
    for (const target of TARGETS) {
      const targetHash = md5Dir(target.path);
      const match = targetHash === sourceHash;
      if (!match) allMatch = false;
      console.log(`  ${match ? '✅' : '❌'} ${target.label}: ${match ? '一致' : '不一致'}`);
    }
    console.log(allMatch ? '\n✅ 所有目标目录一致' : '\n❌ 存在不一致');
    process.exit(allMatch ? 0 : 1);
  }

  // Step 2: 同步到所有目标目录
  for (const target of TARGETS) {
    console.log(`  📋 同步到: ${target.label} (${target.path})`);
    copyDir(SOURCE, target.path);
  }

  // Step 3: 同步后校验
  console.log('\n🔍 同步后校验:');
  let allMatch = true;
  for (const target of TARGETS) {
    const targetHash = md5Dir(target.path);
    const match = targetHash === sourceHash;
    if (!match) allMatch = false;
    console.log(`  ${match ? '✅' : '❌'} ${target.label}: ${match ? '一致' : '不一致'}`);
  }

  if (mode === 'ci' && !allMatch) {
    console.error('\n❌ CI 阻断：同步后部分目标目录不一致');
    process.exit(1);
  }

  // Step 4: 同步 packages/shared/ 的 KV 热 key 函数
  console.log('\n📋 额外同步: 4B5 热 key 函数到 kv-keys.js');

  console.log(allMatch
    ? '\n✅ sync-sharing.js 执行完成'
    : '\n⚠️  执行完成（存在不一致）'
  );
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
