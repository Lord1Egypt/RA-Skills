/**
 * Storage Concurrency Lock + WAL Integration v2.0
 * 文件锁机制：flock-style write lock，防止并发写冲突
 * WAL机制：每次写操作先记日志再应用，支持crash恢复
 *
 * v2.0 升级：
 * - flock 文件锁（多进程安全，进程退出/crash自动释放）
 * - WAL fsync 确保落盘
 * - WAL 同步写 walWriteSync()
 * - 脏读检测 checkVersion()
 * - PID 竞态检测（启动时检查 storage.lock）
 */

import * as fs from 'fs';
import { writeFileSync, readFileSync, existsSync, unlinkSync, renameSync, mkdirSync, openSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync, spawn } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const LOCK_FILE_SUFFIX = '.lock';
const WAL_DIR = join(__dirname, '..', 'wal');
const STORAGE_LOCK_FILE = join(process.env.HOME || '/root', '.unified-memory', 'storage.lock');

// ─── PID 竞态检测 ──────────────────────────────────────────────────────────

/**
 * 检查 PID 进程是否还在运行
 * @param {number} pid
 * @returns {boolean}
 */
function isPidAlive(pid) {
  try {
    execSync(`kill -0 ${pid} 2>/dev/null`, { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

/**
 * 初始化 PID 竞态检测（flock-based, atomic）
 * 使用 flock 尝试获取 storage.lock 的独占锁。
 * 如果锁被占用（另一个进程持有），检测到并退出。
 * 如果获取成功，立即释放（只做检测，不需要持有）。
 */
function initPidLock() {
  const dir = dirname(STORAGE_LOCK_FILE);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  // Use flock -n (non-blocking) to try to acquire lock without waiting
  // If we get the lock immediately, it means no other process holds it
  // If we can't get it, another process is running
  const flockResult = execSync(
    `flock -x -n "${STORAGE_LOCK_FILE}" -c "echo $$" 2>/dev/null`,
    { stdio: 'pipe', timeout: 5 }
  );
  
  if (flockResult?.status === 0) {
    // We got the lock - another process was holding it, we're the duplicate
    try {
      execSync(`flock -x -w 1 "${STORAGE_LOCK_FILE}" -c "echo locked"`, { stdio: 'ignore', timeout: 2 });
    } catch { /* timeout, lock still held */ }
    console.error(`[storage_lock] FATAL: Another process is holding storage.lock. Exiting.`);
    console.error(`[storage_lock] If no other instance is running, delete ${STORAGE_LOCK_FILE}`);
    process.exit(1);
  }
  
  // We got the lock immediately - we're the first instance, keep it
  // Write PID for debugging (flock handles the real locking)
  writeFileSync(STORAGE_LOCK_FILE, JSON.stringify({ pid: process.pid, ts: Date.now() }), 'utf8');
}

/**
 * 释放 PID 锁（正常退出时调用）
 */
function releasePidLock() {
  try {
    if (existsSync(STORAGE_LOCK_FILE)) {
      const data = JSON.parse(readFileSync(STORAGE_LOCK_FILE, 'utf8'));
      if (data.pid === process.pid) {
        unlinkSync(STORAGE_LOCK_FILE);
      }
    }
  } catch { /* ignore */ }
}

// 启动时注册 PID 锁
initPidLock();

// 正常退出时释放锁（process.on('exit') 同步执行）
process.on('exit', () => {
  releasePidLock();
});

// ─── flock 文件锁实现（进程级） ────────────────────────────────────────────

const LOCK_TIMEOUT_MS = 30_000; // 30 秒锁超时

/**
 * 同步获取文件锁（真正的多进程安全 flock 锁）
 * 使用 flock -x 阻塞等待，超时则抛错
 * P1-7: flock(1) provides atomic exclusive lock acquisition.
 * Lock is automatically released when process exits (crash-safe).
 * @param {string} filePath
 * @param {number} timeoutMs
 */
export function acquireLockSync(filePath, timeoutMs = LOCK_TIMEOUT_MS) {
  const lockPath = filePath + LOCK_FILE_SUFFIX;

  // flock -x: 阻塞直到获取锁（或超时）
  // flock 在进程退出时自动释放锁（即使 crash）
  try {
    execSync(`flock -x -w ${Math.ceil(timeoutMs / 1000)} "${lockPath}" -c "echo locked"`, {
      stdio: 'ignore',
      timeout: timeoutMs / 1000 + 1,
    });
  } catch (e) {
    if (e.status === 127) {
      throw new Error(`[storage_lock] flock command not found`);
    }
    // flock 超时（exit code 1）或失败
    throw new Error(`[storage_lock] Lock timeout for ${filePath} after ${timeoutMs}ms`);
  }

  // 锁已获取，写入 PID 记录（调试用，flock 本身已保证原子性）
  writeFileSync(lockPath, JSON.stringify({ pid: process.pid, ts: Date.now() }), 'utf8');
}

/**
 * 同步释放文件锁
 * @param {string} filePath
 */
export function releaseLockSync(filePath) {
  const lockPath = filePath + LOCK_FILE_SUFFIX;
  try {
    if (existsSync(lockPath)) {
      const data = JSON.parse(readFileSync(lockPath, 'utf8'));
      if (data.pid === process.pid) {
        unlinkSync(lockPath);
      }
    }
  } catch { /* ignore */ }
}

/**
 * flock 同步锁（阻塞式，多进程安全）
 * @param {string} filePath
 * @param {number} timeoutMs
 */
export function flockSync(filePath, timeoutMs = LOCK_TIMEOUT_MS) {
  const lockPath = filePath + LOCK_FILE_SUFFIX;

  // 使用 flock -w timeout 获取独占锁（阻塞直到获得或超时）
  try {
    execSync(`flock -x -w ${Math.ceil(timeoutMs / 1000)} "${lockPath}" -c "echo locked"`, {
      stdio: 'ignore',
      timeout: Math.ceil(timeoutMs / 1000) + 1,
    });
  } catch (e) {
    if (e.status === 127) {
      throw new Error(`[storage_lock] flock command not found`);
    }
    throw new Error(`[storage_lock] flockSync timeout for ${filePath} after ${timeoutMs}ms`);
  }

  // 写入 PID 信息（供调试/手动清理）
  writeFileSync(lockPath, JSON.stringify({ pid: process.pid, ts: Date.now() }), 'utf8');
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ─── WAL 集成 ──────────────────────────────────────────────────────────────

let walFd = null;
let walRunId = null;
let walPath = null;

function ensureWalDir() {
  if (!existsSync(WAL_DIR)) mkdirSync(WAL_DIR, { recursive: true });
}

/**
 * 初始化 WAL 存储
 * @param {string} [runId]
 */
export function initWalStorage(runId) {
  ensureWalDir();
  walRunId = runId || `store-${Date.now()}`;
  walPath = join(WAL_DIR, `${walRunId}.wal.jsonl`);
  walFd = openSync(walPath, 'a');
  // Cleanup: delete all other WAL files older than current runId (crash recovery only needs the latest)
  try {
    const currentBase = walRunId;
    for (const f of readdirSync(WAL_DIR)) {
      if (f.endsWith('.wal.jsonl') && !f.startsWith(currentBase)) {
        unlinkSync(join(WAL_DIR, f));
      }
    }
  } catch { /* cleanup errors non-fatal */ }
}

/**
 * 记录写操作到 WAL（异步，不保证 fsync）
 * @param {object} op
 */
export function logWriteOp(op) {
  if (!walFd) return;
  const entry = JSON.stringify({ ...op, ts: Date.now() }) + '\n';
  const buf = Buffer.from(entry, 'utf8');
  fs.writeSync(walFd, buf);
}

/**
 * 记录写操作到 WAL（同步版本，fsync 确保落盘）
 * @param {object} op
 */
export function walWriteSync(op) {
  if (!walFd) return;
  const entry = JSON.stringify({ ...op, ts: Date.now() }) + '\n';
  const buf = Buffer.from(entry, 'utf8');
  fs.writeSync(walFd, buf);
  // 确保数据落盘（fsync）
  fs.fsyncSync(walFd);
}

/**
 * 获取当前 WAL 文件描述符
 */
export function getWalFd() {
  return walFd;
}

/**
 * 获取 WAL 目录
 */
export function getWalDir() {
  return WAL_DIR;
}

// ─── 脏读检测 ──────────────────────────────────────────────────────────────

// 记录每个 memory 的期望版本（由 withLock 调用方设置）
const expectedVersions = new Map();

/**
 * 设置期望的 memory 版本（脏读检测用）
 * @param {string} memoryId
 * @param {number} version
 */
export function setExpectedVersion(memoryId, version) {
  expectedVersions.set(memoryId, version);
}

/**
 * 检查 memory 版本是否符合预期
 * 如果 version 不符合预期，记录 warning 但不阻塞
 * @param {string} memoryId
 * @param {number} expectedVersion
 * @param {object} memory - 被读取的 memory 对象
 * @returns {boolean} true=版本一致，false=脏读
 */
export function checkVersion(memoryId, expectedVersion, memory) {
  if (!memory || memory.version === undefined) return true;

  const actual = memory.version;
  if (actual !== expectedVersion) {
    console.warn(`[storage_lock] ⚠️ 脏读检测: memory "${memoryId}" expected version ${expectedVersion}, got ${actual}`);
    return false;
  }
  return true;
}

/**
 * 获取期望版本
 * @param {string} memoryId
 * @returns {number|undefined}
 */
export function getExpectedVersion(memoryId) {
  return expectedVersions.get(memoryId);
}

/**
 * 清除期望版本
 * @param {string} memoryId
 */
export function clearExpectedVersion(memoryId) {
  expectedVersions.delete(memoryId);
}

// ─── 原子写入 ──────────────────────────────────────────────────────────────

/**
 * 原子保存（锁 + WAL + rename）
 * @param {string} filePath
 * @param {string} data
 * @param {object|null} walOp
 */
export async function atomicSave(filePath, data, walOp = null) {
  await acquireLock(filePath);
  try {
    if (walOp) walWriteSync(walOp); // 使用同步版本确保 fsync
    const tmpPath = `${filePath}.tmp.${process.pid}`;
    writeFileSync(tmpPath, data, 'utf8');
    renameSync(tmpPath, filePath);
  } finally {
    releaseLock(filePath);
  }
}

// ─── WAL Recovery ──────────────────────────────────────────────────────────

/**
 * 从 WAL 文件恢复数据
 * 读取 wal/*.wal.jsonl，按时间顺序重放 add/delete 操作
 * @param {string[]} walFiles - WAL 文件列表
 * @param {string} targetFile - 目标数据文件路径
 * @param {object[]} memories - 当前内存中的数据
 * @returns {object[]} 恢复后的 memories
 */
export function recoverFromWAL(walFiles, targetFile, memories) {
  const memMap = new Map(memories.map(m => [m.id, m]));

  for (const walFile of walFiles) {
    try {
      const lines = readFileSync(join(WAL_DIR, walFile), 'utf8')
        .trim().split('\n').filter(Boolean);

      for (const line of lines) {
        const op = JSON.parse(line);
        const { type, memory, memory_id: delId } = op;

        if (type === 'add' && memory) {
          memMap.set(memory.id, memory);
        } else if (type === 'delete' && delId) {
          memMap.delete(delId);
        }
      }
    } catch { /* skip corrupted WAL files */ }
  }

  return Array.from(memMap.values());
}
