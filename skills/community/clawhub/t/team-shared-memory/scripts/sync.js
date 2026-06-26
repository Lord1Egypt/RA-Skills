#!/usr/bin/env node
/**
 * Team Memory 同步脚本
 * 多工作区/实例间共享记忆
 * 
 * 用法:
 *   node sync.js --local              # 本地多工作区同步
 *   node sync.js --status             # 查看同步状态
 *   node sync.js --scan <路径>        # 密钥扫描
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const MEMORY_DIR = WORKSPACE + '/memory';
const TEAM_DIR = MEMORY_DIR + '/team';
const AUTO_DIR = MEMORY_DIR + '/auto';
const STATE_FILE = TEAM_DIR + '/.sync-state.json';
const LOCK_FILE = TEAM_DIR + '/.sync-lock';

// 可共享的记忆类型
const SHARED_TYPES = ['project', 'reference'];
const PRIVATE_TYPES = ['user', 'feedback'];

// 确保目录存在
function ensureTeamDir() {
  if (!fs.existsSync(TEAM_DIR)) {
    fs.mkdirSync(TEAM_DIR, { recursive: true });
  }
}

// 读取同步状态
function readState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch (e) {
    return { lastSyncAt: null, syncCount: 0, lastHash: {} };
  }
}

// 保存同步状态
function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// 计算文件 hash
function fileHash(filepath) {
  const content = fs.readFileSync(filepath);
  return crypto.createHash('md5').update(content).digest('hex');
}

// 尝试获取锁
function tryLock() {
  if (fs.existsSync(LOCK_FILE)) {
    try {
      const lock = JSON.parse(fs.readFileSync(LOCK_FILE, 'utf8'));
      const lockAge = Date.now() - lock.startedAt;
      if (lockAge < 5 * 60 * 1000) { // 5 分钟锁
        console.log('[锁] 同步进行中，跳过');
        return false;
      }
    } catch (e) {}
  }
  
  fs.writeFileSync(LOCK_FILE, JSON.stringify({
    pid: process.pid,
    startedAt: Date.now()
  }));
  return true;
}

function releaseLock() {
  try { fs.unlinkSync(LOCK_FILE); } catch (e) {}
}

// 本地同步：将共享记忆复制到 team 目录，反之亦然
function localSync() {
  ensureTeamDir();
  
  const state = readState();
  const syncReport = { timestamp: new Date().toISOString(), pushed: [], pulled: [], conflicts: [] };
  
  // 推送：auto/{project,reference} → team/
  for (const type of SHARED_TYPES) {
    const srcDir = path.join(AUTO_DIR, type);
    const destDir = path.join(TEAM_DIR, type);
    
    if (!fs.existsSync(srcDir)) continue;
    fs.mkdirSync(destDir, { recursive: true });
    
    const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
    
    for (const file of files) {
      const srcFile = path.join(srcDir, file);
      const destFile = path.join(destDir, file);
      const hash = fileHash(srcFile);
      
      // 检查是否变更
      if (state.lastHash[file] === hash && fs.existsSync(destFile)) {
        continue; // 未变更，跳过
      }
      
      // 目标存在且不同 → 冲突
      if (fs.existsSync(destFile)) {
        const destHash = fileHash(destFile);
        if (hash !== destHash) {
          // 以较新的为准
          const srcMtime = fs.statSync(srcFile).mtimeMs;
          const destMtime = fs.statSync(destFile).mtimeMs;
          
          if (srcMtime > destMtime) {
            fs.copyFileSync(srcFile, destFile);
            syncReport.pushed.push(`${type}/${file}`);
          } else {
            fs.copyFileSync(destFile, srcFile);
            syncReport.pulled.push(`${type}/${file}`);
          }
          syncReport.conflicts.push(`${type}/${file}`);
        }
      } else {
        fs.copyFileSync(srcFile, destFile);
        syncReport.pushed.push(`${type}/${file}`);
      }
      
      state.lastHash[file] = hash;
    }
  }
  
  // 拉取：team/ → auto/{project,reference}（新增的文件）
  for (const type of SHARED_TYPES) {
    const srcDir = path.join(TEAM_DIR, type);
    const destDir = path.join(AUTO_DIR, type);
    
    if (!fs.existsSync(srcDir)) continue;
    fs.mkdirSync(destDir, { recursive: true });
    
    const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
    
    for (const file of files) {
      const srcFile = path.join(srcDir, file);
      const destFile = path.join(destDir, file);
      
      if (!fs.existsSync(destFile)) {
        fs.copyFileSync(srcFile, destFile);
        syncReport.pulled.push(`${type}/${file}`);
        state.lastHash[file] = fileHash(srcFile);
      }
    }
  }
  
  // 保存状态
  state.lastSyncAt = Date.now();
  state.syncCount = (state.syncCount || 0) + 1;
  saveState(state);
  
  return syncReport;
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--status')) {
    const state = readState();
    const hoursSince = state.lastSyncAt ? ((Date.now() - state.lastSyncAt) / (1000 * 60 * 60)).toFixed(1) : '从未';
    
    console.log('=== 团队记忆同步状态 ===');
    console.log(`上次同步: ${hoursSince}h 前`);
    console.log(`总同步次数: ${state.syncCount || 0}`);
    console.log(`共享类型: ${SHARED_TYPES.join(', ')}`);
    console.log(`私有类型: ${PRIVATE_TYPES.join(', ')} (不共享)`);
    
    // 统计文件数
    for (const type of [...SHARED_TYPES, ...PRIVATE_TYPES]) {
      const dir = path.join(AUTO_DIR, type);
      const count = fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => f.endsWith('.md')).length : 0;
      console.log(`  ${type}: ${count} 条记忆`);
    }
    return;
  }
  
  // 执行同步
  console.log('=== 开始本地同步 ===\n');
  
  if (tryLock()) {
    try {
      const report = localSync();
      console.log(`\n推送: ${report.pushed.length} 条`);
      console.log(`拉取: ${report.pulled.length} 条`);
      console.log(`冲突: ${report.conflicts.length} 条`);
      console.log('\n=== 同步完成 ===');
    } finally {
      releaseLock();
    }
  }
}

main();
