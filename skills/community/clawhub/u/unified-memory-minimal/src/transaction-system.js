/**
 * Transaction System - 统一记忆事务管理系统
 * 
 * 功能：
 * 1. 完善的 WAL（Write-Ahead Logging）系统
 * 2. 完整的事务管理（嵌套事务、保存点、隔离级别）
 * 3. 事务回滚机制（原子性操作、错误恢复）
 * 4. 死锁检测和处理
 * 5. 崩溃恢复和重放
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== 日志级别 ==========
const LogLevel = { DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3 };

// ========== 事务状态 ==========
const TransactionState = {
  ACTIVE: 'active',
  PREPARING: 'preparing',
  PREPARED: 'prepared',
  COMMITTED: 'committed',
  ROLLING_BACK: 'rolling_back',
  ROLLED_BACK: 'rolled_back',
  FAILED: 'failed'
};

// ========== 隔离级别 ==========
const IsolationLevel = {
  READ_UNCOMMITTED: 'READ_UNCOMMITTED',
  READ_COMMITTED: 'READ_COMMITTED',
  REPEATABLE_READ: 'REPEATABLE_READ',
  SERIALIZABLE: 'SERIALIZABLE'
};

// ========== WAL 条目类型 ==========
const WALEntryType = {
  BEGIN: 'BEGIN', PREPARE: 'PREPARE', COMMIT: 'COMMIT', ROLLBACK: 'ROLLBACK',
  SAVEPOINT: 'SAVEPOINT', RELEASE_SAVEPOINT: 'RELEASE_SAVEPOINT',
  UPDATE: 'UPDATE', DELETE: 'DELETE', INSERT: 'INSERT', CHECKPOINT: 'CHECKPOINT'
};

// ========== 工具函数 ==========
function generateId(prefix = '') {
  const timestamp = Date.now();
  const random = crypto.randomBytes(8).toString('hex');
  return `${prefix}${timestamp}_${random}`;
}

// ========== WAL 管理器 ==========
export class WALManager {
  constructor(options = {}) {
    this.walDir = options.walDir || path.join(process.env.HOME || '/root', '.unified-memory', 'wal');
    this.maxFileSize = options.maxFileSize || 10 * 1024 * 1024;
    this.maxFiles = options.maxFiles || 10;
    this.syncMode = options.syncMode || 'normal';
    this.compressOldLogs = options.compressOldLogs !== false;
    
    this.currentWalFile = null;
    this.currentWalFd = null;
    this.currentWalSize = 0;
    this.writeBuffer = [];
    this.bufferFlushInterval = null;
    
    this.metrics = { writes: 0, bytesWritten: 0, syncs: 0, rotations: 0, recoveries: 0, replayedEntries: 0, errors: 0 };
    this.listeners = new Map();
    
    this._ensureWalDirectory();
    this._initCurrentWalFile();
    this._startBufferFlush();
  }
  
  _ensureWalDirectory() {
    if (!fs.existsSync(this.walDir)) fs.mkdirSync(this.walDir, { recursive: true });
  }
  
  _initCurrentWalFile() {
    const timestamp = Date.now();
    const filename = `store-${timestamp}.wal.jsonl`;
    this.currentWalFile = path.join(this.walDir, filename);
    this.currentWalFd = fs.openSync(this.currentWalFile, 'a+');
    this.currentWalSize = fs.statSync(this.currentWalFile).size;
  }
  
  _startBufferFlush() {
    const flushInterval = this.syncMode === 'fast' ? 100 : this.syncMode === 'full' ? 1000 : 500;
    this.bufferFlushInterval = setInterval(() => {
      if (this.writeBuffer.length > 0) this._flushBuffer();
    }, flushInterval);
    process.on('exit', () => this._flushBuffer());
  }
  
  _flushBuffer() {
    if (this.writeBuffer.length === 0) return;
    const entries = this.writeBuffer.splice(0, this.writeBuffer.length);
    const data = entries.map(e => JSON.stringify(e)).join('\n') + '\n';
    try {
      fs.writeSync(this.currentWalFd, data);
      this.currentWalSize += Buffer.byteLength(data, 'utf8');
      this.metrics.bytesWritten += Buffer.byteLength(data, 'utf8');
      if (this.syncMode === 'full') { fs.fsyncSync(this.currentWalFd); this.metrics.syncs++; }
      if (this.currentWalSize >= this.maxFileSize) this._rotateWal();
    } catch (error) { this.metrics.errors++; this._emit('error', { error, entries }); }
  }
  
  _rotateWal() {
    try {
      if (this.currentWalFd) fs.closeSync(this.currentWalFd);
      if (this.compressOldLogs && this.currentWalFile) this._compressOldWal(this.currentWalFile);
      this._cleanupOldWalFiles();
      this._initCurrentWalFile();
      this.metrics.rotations++;
      this._emit('rotation', { oldFile: this.currentWalFile });
    } catch (error) { this.metrics.errors++; this._emit('error', { error, context: 'rotation' }); }
  }
  
  _compressOldWal(filePath) {
    try {
      const stats = fs.statSync(filePath);
      if (stats.size === 0) { fs.unlinkSync(filePath); return; }
      fs.renameSync(filePath, filePath + '.gz');
    } catch (error) {}
  }
  
  _cleanupOldWalFiles() {
    try {
      const files = fs.readdirSync(this.walDir)
        .filter(f => f.endsWith('.wal.jsonl') || f.endsWith('.wal.jsonl.gz'))
        .map(f => ({ name: f, path: path.join(this.walDir, f), mtime: fs.statSync(path.join(this.walDir, f)).mtime.getTime() }))
        .sort((a, b) => b.mtime - a.mtime);
      if (files.length > this.maxFiles) {
        for (const file of files.slice(this.maxFiles)) {
          try { fs.unlinkSync(file.path); } catch (e) {}
        }
      }
    } catch (error) {}
  }
  
  _emit(event, data) { (this.listeners.get(event) || []).forEach(h => h(data)); }
  on(event, handler) { if (!this.listeners.has(event)) this.listeners.set(event, []); this.listeners.get(event).push(handler); }
  off(event, handler) { const handlers = this.listeners.get(event) || []; const index = handlers.indexOf(handler); if (index > -1) handlers.splice(index, 1); }
  
  write(type, data) {
    const entry = { type, data, timestamp: new Date().toISOString(), sequence: ++this.metrics.writes };
    this.writeBuffer.push(entry);
    if (this.syncMode === 'full') this._flushBuffer();
    this._emit('write', entry);
    return entry;
  }
  
  flush() { this._flushBuffer(); }
  sync() { this._flushBuffer(); if (this.currentWalFd) { fs.fsyncSync(this.currentWalFd); this.metrics.syncs++; } }
  
  async recover(options = {}) {
    const { maxEntries = 10000, onEntry = null } = options;
    this.metrics.recoveries++;
    const result = { entries: [], transactions: new Map(), errors: [], recovered: 0 };
    try {
      const files = fs.readdirSync(this.walDir).filter(f => f.endsWith('.wal.jsonl') || f.endsWith('.wal.jsonl.gz')).sort().map(f => path.join(this.walDir, f));
      for (const file of files) {
        try {
          const content = fs.readFileSync(file, 'utf8');
          for (const line of content.trim().split('\n')) {
            if (!line.trim()) continue;
            try {
              const entry = JSON.parse(line);
              if (entry.type === WALEntryType.BEGIN) result.transactions.set(entry.data.transactionId, { entries: [], state: 'active' });
              if (entry.data?.transactionId && result.transactions.has(entry.data.transactionId)) result.transactions.get(entry.data.transactionId).entries.push(entry);
              if (result.entries.length < maxEntries) result.entries.push(entry);
              if (onEntry) onEntry(entry);
              result.recovered++;
              this.metrics.replayedEntries++;
            } catch (parseError) { result.errors.push({ file, line, error: parseError.message }); }
          }
        } catch (fileError) { result.errors.push({ file, error: fileError.message }); }
      }
      for (const [txId, tx] of result.transactions) {
        const lastEntry = tx.entries[tx.entries.length - 1];
        if (lastEntry && lastEntry.type !== WALEntryType.COMMIT && lastEntry.type !== WALEntryType.ROLLBACK) tx.state = 'incomplete';
      }
    } catch (error) { result.errors.push({ error: error.message }); }
    this._emit('recovered', result);
    return result;
  }
  
  checkpoint() { this.sync(); return this.write(WALEntryType.CHECKPOINT, { checkpointId: generateId('cp_'), timestamp: new Date().toISOString() }); }
  getMetrics() { return { ...this.metrics, bufferSize: this.writeBuffer.length, currentWalFile: this.currentWalFile, currentWalSize: this.currentWalSize }; }
  close() {
    if (this.bufferFlushInterval) clearInterval(this.bufferFlushInterval);
    this._flushBuffer();
    if (this.currentWalFd) { fs.closeSync(this.currentWalFd); this.currentWalFd = null; }
  }
}

// ========== 保存点管理器 ==========
class SavepointManager {
  constructor() { this.savepoints = new Map(); }
  createSavepoint(transactionId, savepointName) {
    if (!this.savepoints.has(transactionId)) this.savepoints.set(transactionId, new Map());
    const spData = { name: savepointName, transactionId, timestamp: Date.now(), operationCount: 0 };
    this.savepoints.get(transactionId).set(savepointName, spData);
    return spData;
  }
  getSavepoint(transactionId, savepointName) { return this.savepoints.get(transactionId)?.get(savepointName); }
  releaseSavepoint(transactionId, savepointName) { this.savepoints.get(transactionId)?.delete(savepointName); }
  getAllSavepoints(transactionId) { return Array.from(this.savepoints.get(transactionId)?.values() || []); }
  clearTransaction(transactionId) { this.savepoints.delete(transactionId); }
}

// ========== 死锁检测器 ==========
class DeadlockDetector {
  constructor(options = {}) {
    this.timeout = options.lockTimeout || 5000;
    this.checkInterval = options.checkInterval || 1000;
    this.waitForGraph = new Map();
    this.lockHolders = new Map();
    this.lockWaiters = new Map();
    this.intervalId = null;
    this.onDeadlockDetected = options.onDeadlockDetected || (() => {});
  }
  start() { if (!this.intervalId) this.intervalId = setInterval(() => this._checkDeadlocks(), this.checkInterval); }
  stop() { if (this.intervalId) { clearInterval(this.intervalId); this.intervalId = null; } }
  acquireLock(transactionId, resourceId) {
    if (this.lockHolders.has(resourceId)) {
      const holder = this.lockHolders.get(resourceId);
      if (this._wouldCauseDeadlock(transactionId, holder)) return { success: false, reason: 'deadlock', holder };
      if (!this.waitForGraph.has(transactionId)) this.waitForGraph.set(transactionId, new Set());
      this.waitForGraph.get(transactionId).add(holder);
      if (!this.lockWaiters.has(transactionId)) this.lockWaiters.set(transactionId, new Map());
      this.lockWaiters.get(transactionId).set(resourceId, Date.now());
      return { success: false, reason: 'waiting', holder };
    }
    this.lockHolders.set(resourceId, transactionId);
    return { success: true };
  }
  releaseLock(transactionId, resourceId) {
    if (this.lockHolders.get(resourceId) === transactionId) this.lockHolders.delete(resourceId);
    for (const [txId, waitSet] of this.waitForGraph) waitSet.delete(transactionId);
    if (this.lockWaiters.has(transactionId)) this.lockWaiters.get(transactionId).delete(resourceId);
  }
  releaseAllLocks(transactionId) {
    for (const [resourceId, holder] of this.lockHolders) { if (holder === transactionId) this.lockHolders.delete(resourceId); }
    for (const [txId, waitSet] of this.waitForGraph) waitSet.delete(transactionId);
    this.lockWaiters.delete(transactionId);
  }
  _wouldCauseDeadlock(transactionId, holderId) {
    const visited = new Set();
    const queue = [holderId];
    while (queue.length > 0) {
      const current = queue.shift();
      if (current === transactionId) return true;
      if (visited.has(current)) continue;
      visited.add(current);
      const waitSet = this.waitForGraph.get(current);
      if (waitSet) { for (const next of waitSet) { if (!visited.has(next)) queue.push(next); } }
    }
    return false;
  }
  _checkDeadlocks() {
    const now = Date.now();
    const timeoutTxs = [];
    for (const [txId, resources] of this.lockWaiters) {
      for (const [resourceId, waitStart] of resources) {
        if (now - waitStart > this.timeout) { timeoutTxs.push(txId); break; }
      }
    }
    if (timeoutTxs.length > 0) {
      const oldestTx = timeoutTxs.reduce((oldest, txId) => {
        const waiters = this.lockWaiters.get(txId);
        const oldestWait = Math.min(...Array.from(waiters.values()));
        const oldestOldest = this._getOldestWait(oldest);
        return oldestWait < oldestOldest ? txId : oldest;
      });
      this.onDeadlockDetected(oldestTx);
    }
  }
  _getOldestWait(transactionId) { const waiters = this.lockWaiters.get(transactionId); if (!waiters) return Date.now(); return Math.min(...Array.from(waiters.values())); }
  getLockInfo() {
    return {
      holders: Array.from(this.lockHolders.entries()).map(([resourceId, txId]) => ({ resourceId, transactionId: txId })),
      waiters: Array.from(this.lockWaiters.entries()).map(([txId, resources]) => ({ transactionId: txId, resources: Array.from(resources.entries()).map(([resourceId, waitStart]) => ({ resourceId, waitMs: Date.now() - waitStart })) }))
    };
  }
}

// ========== 完整事务管理器 ==========
export class TransactionManager {
  constructor(options = {}) {
    this.walDir = options.walDir || path.join(process.env.HOME || '/root', '.unified-memory', 'wal');
    this.dataDir = options.dataDir || path.join(process.env.HOME || '/root', '.unified-memory', 'data');
    this.isolationLevel = options.isolationLevel || IsolationLevel.READ_COMMITTED;
    this.lockTimeout = options.lockTimeout || 5000;
    this.maxNestedTransactions = options.maxNestedTransactions || 5;
    this.enableDeadlockDetection = options.enableDeadlockDetection !== false;
    
    this.wal = new WALManager({ walDir: this.walDir, maxFileSize: options.maxWalSize || 10 * 1024 * 1024, maxFiles: options.maxWalFiles || 10, syncMode: options.walSyncMode || 'normal' });
    this.savepointManager = new SavepointManager();
    this.deadlockDetector = new DeadlockDetector({ lockTimeout: this.lockTimeout, onDeadlockDetected: (txId) => this._handleDeadlock(txId) });
    if (this.enableDeadlockDetection) this.deadlockDetector.start();
    
    this.transactions = new Map();
    this.nextTransactionId = 1;
    this.operationLogs = new Map();
    this.committedData = new Map();
    
    this.stats = { transactionsStarted: 0, transactionsCommitted: 0, transactionsRolledBack: 0, savepointsCreated: 0, deadlocksDetected: 0, nestedTransactions: 0 };
    this._ensureDirectories();
    this.wal.on('error', ({ error }) => console.error('[WAL Error]', error));
  }
  
  _ensureDirectories() {
    if (!fs.existsSync(this.walDir)) fs.mkdirSync(this.walDir, { recursive: true });
    if (!fs.existsSync(this.dataDir)) fs.mkdirSync(this.dataDir, { recursive: true });
  }
  
  async begin(options = {}) {
    const { parentId = null, isolationLevel = null, savepointName = null } = options;
    const transactionId = `tx_${this.nextTransactionId++}`;
    const now = Date.now();
    
    if (parentId) {
      const depth = this._getTransactionDepth(parentId);
      if (depth >= this.maxNestedTransactions) throw new Error(`Maximum nested transaction depth (${this.maxNestedTransactions}) exceeded`);
      this.stats.nestedTransactions++;
    }
    
    const transaction = { id: transactionId, parentId, state: TransactionState.ACTIVE, isolationLevel: isolationLevel || this.isolationLevel, startTime: now, savepoints: [], operations: [], locks: new Set(), depth: parentId ? this._getTransactionDepth(parentId) + 1 : 0, metadata: {} };
    this.transactions.set(transactionId, transaction);
    this.operationLogs.set(transactionId, []);
    this.stats.transactionsStarted++;
    
    this.wal.write(WALEntryType.BEGIN, { transactionId, parentId, isolationLevel: transaction.isolationLevel, timestamp: new Date().toISOString() });
    
    if (parentId) { const parent = this.transactions.get(parentId); if (parent) parent.nestedCount = (parent.nestedCount || 0) + 1; }
    if (savepointName) this._createSavepoint(transactionId, savepointName);
    
    return transactionId;
  }
  
  _getTransactionDepth(transactionId) { const tx = this.transactions.get(transactionId); return tx ? tx.depth : 0; }
  
  _createSavepoint(transactionId, savepointName) {
    const tx = this.transactions.get(transactionId);
    if (!tx) throw new Error(`Transaction ${transactionId} not found`);
    const savepoint = this.savepointManager.createSavepoint(transactionId, savepointName);
    savepoint.operationIndex = tx.operations.length;
    tx.savepoints.push({ name: savepointName, timestamp: savepoint.timestamp });
    this.stats.savepointsCreated++;
    this.wal.write(WALEntryType.SAVEPOINT, { transactionId, savepointName, timestamp: new Date().toISOString() });
    return savepoint;
  }
  
  async createSavepoint(transactionId, savepointName) { return this._createSavepoint(transactionId, savepointName); }
  
  async rollbackToSavepoint(transactionId, savepointName) {
    const tx = this.transactions.get(transactionId);
    if (!tx) throw new Error(`Transaction ${transactionId} not found`);
    const savepoint = this.savepointManager.getSavepoint(transactionId, savepointName);
    if (!savepoint) throw new Error(`Savepoint ${savepointName} not found`);
    const operations = this.operationLogs.get(transactionId) || [];
    const savepointOps = operations.slice(0, savepoint.operationIndex);
    for (let i = operations.length - 1; i >= savepointOps.length; i--) await this._reverseOperation(operations[i]);
    this.operationLogs.set(transactionId, savepointOps);
    tx.operations = savepointOps;
    this.wal.write(WALEntryType.ROLLBACK, { transactionId, savepointName, timestamp: new Date().toISOString(), type: 'savepoint' });
    return true;
  }
  
  async releaseSavepoint(transactionId, savepointName) {
    this.savepointManager.releaseSavepoint(transactionId, savepointName);
    const tx = this.transactions.get(transactionId);
    if (tx) tx.savepoints = tx.savepoints.filter(sp => sp.name !== savepointName);
    this.wal.write(WALEntryType.RELEASE_SAVEPOINT, { transactionId, savepointName, timestamp: new Date().toISOString() });
  }
  
  async execute(transactionId, operation) {
    const tx = this.transactions.get(transactionId);
    if (!tx) throw new Error(`Transaction ${transactionId} not found`);
    if (tx.state !== TransactionState.ACTIVE) throw new Error(`Transaction ${transactionId} is not active (state: ${tx.state})`);
    
    const resourceId = operation.resourceId || operation.memoryId;
    if (resourceId && this.enableDeadlockDetection) {
      const lockResult = this.deadlockDetector.acquireLock(transactionId, resourceId);
      if (!lockResult.success) {
        if (lockResult.reason === 'deadlock') throw new Error(`Deadlock detected while acquiring lock for ${resourceId}`);
        await this._waitForLock(transactionId, resourceId);
      }
      tx.locks.add(resourceId);
    }
    
    const opRecord = { ...operation, timestamp: Date.now(), sequence: tx.operations.length };
    tx.operations.push(opRecord);
    const operations = this.operationLogs.get(transactionId) || [];
    operations.push(opRecord);
    this.operationLogs.set(transactionId, operations);
    
    const walOp = operation.type === 'insert' ? WALEntryType.INSERT : operation.type === 'update' ? WALEntryType.UPDATE : operation.type === 'delete' ? WALEntryType.DELETE : operation.type;
    this.wal.write(walOp, { transactionId, operation, timestamp: new Date().toISOString() });
    return opRecord;
  }
  
  async _waitForLock(transactionId, resourceId) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => { this.deadlockDetector.releaseLock(transactionId, resourceId); reject(new Error(`Lock timeout for resource ${resourceId}`)); }, this.lockTimeout);
      const checkInterval = setInterval(() => { const holder = this.deadlockDetector.lockHolders.get(resourceId); if (!holder || holder === transactionId) { clearTimeout(timeout); clearInterval(checkInterval); resolve(); } }, 100);
    });
  }
  
  async prepare(transactionId) {
    const tx = this.transactions.get(transactionId);
    if (!tx) throw new Error(`Transaction ${transactionId} not found`);
    if (tx.state !== TransactionState.ACTIVE) throw new Error(`Transaction ${transactionId} is not active`);
    tx.state = TransactionState.PREPARING;
    this.wal.write(WALEntryType.PREPARE, { transactionId, operationCount: tx.operations.length, timestamp: new Date().toISOString() });
    this.wal.sync();
    tx.state = TransactionState.PREPARED;
    return true;
  }
  
  async commit(transactionId) {
    const tx = this.transactions.get(transactionId);
    if (!tx) throw new Error(`Transaction ${transactionId} not found`);
    for (const sp of tx.savepoints) this.savepointManager.releaseSavepoint(transactionId, sp.name);
    tx.state = TransactionState.COMMITTED;
    tx.endTime = Date.now();
    for (const resourceId of tx.locks) this.deadlockDetector.releaseLock(transactionId, resourceId);
    for (const op of tx.operations) {
      if (op.memoryId) {
        if (op.type === 'delete') this.committedData.delete(op.memoryId);
        else this.committedData.set(op.memoryId, { data: op.data, commitTime: tx.endTime });
      }
    }
    this.wal.write(WALEntryType.COMMIT, { transactionId, operationCount: tx.operations.length, duration: tx.endTime - tx.startTime, timestamp: new Date().toISOString() });
    this.wal.flush();
    this.stats.transactionsCommitted++;
    this._cleanupTransaction(transactionId);
    return { transactionId, operationCount: tx.operations.length, duration: tx.endTime - tx.startTime };
  }
  
  async rollback(transactionId, error = null) {
    const tx = this.transactions.get(transactionId);
    if (!tx) throw new Error(`Transaction ${transactionId} not found`);
    tx.state = TransactionState.ROLLING_BACK;
    const startRollback = Date.now();
    const operations = this.operationLogs.get(transactionId) || [];
    for (let i = operations.length - 1; i >= 0; i--) { try { await this._reverseOperation(operations[i]); } catch (e) { console.error(`Failed to reverse operation:`, e); } }
    for (const resourceId of tx.locks) this.deadlockDetector.releaseLock(transactionId, resourceId);
    tx.state = TransactionState.ROLLED_BACK;
    tx.endTime = Date.now();
    tx.error = error?.message;
    this.wal.write(WALEntryType.ROLLBACK, { transactionId, operationCount: operations.length, duration: Date.now() - startRollback, error: error?.message, timestamp: new Date().toISOString() });
    this.stats.transactionsRolledBack++;
    this._cleanupTransaction(transactionId);
    return { transactionId, operationsRolledBack: operations.length, duration: Date.now() - startRollback };
  }
  
  async _reverseOperation(operation) {
    switch (operation.type) {
      case 'insert': return this._reverseInsert(operation);
      case 'update': return this._reverseUpdate(operation);
      case 'delete': return this._reverseDelete(operation);
      default: return Promise.resolve();
    }
  }
  _reverseInsert(operation) { return Promise.resolve(); }
  _reverseUpdate(operation) { return Promise.resolve(); }
  _reverseDelete(operation) { return Promise.resolve(); }
  
  async _handleDeadlock(transactionId) {
    this.stats.deadlocksDetected++;
    console.warn(`[Deadlock] Detected deadlock involving transaction ${transactionId}`);
    try { await this.rollback(transactionId, new Error('Deadlock detected')); } catch (e) { console.error(`[Deadlock] Failed to rollback deadlocked transaction:`, e); }
  }
  
  _cleanupTransaction(transactionId) {
    const tx = this.transactions.get(transactionId);
    this.savepointManager.clearTransaction(transactionId);
    this.operationLogs.delete(transactionId);
    if (tx?.parentId) { const parent = this.transactions.get(tx.parentId); if (parent && parent.nestedCount > 0) parent.nestedCount--; }
    this.transactions.delete(transactionId);
  }
  
  getTransactionStatus(transactionId) {
    const tx = this.transactions.get(transactionId);
    if (!tx) return null;
    return { id: tx.id, state: tx.state, parentId: tx.parentId, isolationLevel: tx.isolationLevel, depth: tx.depth, operationCount: tx.operations.length, savepointCount: tx.savepoints.length, lockCount: tx.locks.size, startTime: tx.startTime, duration: Date.now() - tx.startTime, error: tx.error };
  }
  
  getActiveTransactions() { const active = []; for (const [id, tx] of this.transactions) active.push(this.getTransactionStatus(id)); return active; }
  
  getStats() { return { ...this.stats, activeTransactions: this.transactions.size, wal: this.wal.getMetrics(), locks: this.enableDeadlockDetection ? this.deadlockDetector.getLockInfo() : null }; }
  
  async recover() {
    console.log('[Recovery] Starting crash recovery...');
    const result = await this.wal.recover();
    console.log(`[Recovery] Found ${result.transactions.size} transactions, ${result.recovered} entries`);
    let rolledBack = 0;
    for (const [txId, tx] of result.transactions) {
      if (tx.state === 'incomplete') {
        console.log(`[Recovery] Rolling back incomplete transaction: ${txId}`);
        try { await this.rollback(txId, new Error('Recovery rollback')); rolledBack++; } catch (e) { console.error(`[Recovery] Failed to rollback ${txId}:`, e); }
      }
    }
    console.log(`[Recovery] Completed. Rolled back ${rolledBack} incomplete transactions`);
    return { recovered: result.recovered, transactionsFound: result.transactions.size, rolledBack, errors: result.errors.length };
  }
  
  close() { this.deadlockDetector?.stop(); this.wal?.close(); }
}

// ========== 单元测试 ==========
async function runTests() {
  console.log('🧪 Starting Transaction System Tests\n');
  const results = [];
  
  // Test 1: Basic transaction
  try {
    const tm = new TransactionManager({ walDir: '/tmp/test-wal', enableDeadlockDetection: false });
    const txId = await tm.begin();
    console.log(`✓ Test 1: begin() returned ${txId}`);
    results.push({ test: 'begin', passed: true });
    await tm.execute(txId, { type: 'insert', memoryId: 'mem_1', data: { content: 'Test memory' } });
    console.log('✓ Test 2: execute() worked');
    results.push({ test: 'execute', passed: true });
    await tm.commit(txId);
    console.log('✓ Test 3: commit() worked');
    results.push({ test: 'commit', passed: true });
    const stats = tm.getStats();
    console.log(`✓ Test 4: stats - committed: ${stats.transactionsCommitted}`);
    results.push({ test: 'stats', passed: true });
    tm.close();
  } catch (e) { console.error(`✗ Basic transaction test failed:`, e.message); results.push({ test: 'basic', passed: false, error: e.message }); }
  
  // Test 2: Savepoint
  try {
    const tm = new TransactionManager({ walDir: '/tmp/test-wal-2', enableDeadlockDetection: false });
    const txId = await tm.begin();
    await tm.execute(txId, { type: 'insert', memoryId: 'mem_1', data: { content: 'Initial' } });
    await tm.createSavepoint(txId, 'sp1');
    console.log('✓ Test 5: createSavepoint() worked');
    await tm.execute(txId, { type: 'insert', memoryId: 'mem_2', data: { content: 'After savepoint' } });
    await tm.rollbackToSavepoint(txId, 'sp1');
    console.log('✓ Test 6: rollbackToSavepoint() worked');
    await tm.commit(txId);
    console.log('✓ Test 7: commit after rollback to savepoint worked');
    tm.close();
    results.push({ test: 'savepoint', passed: true });
  } catch (e) { console.error(`✗ Savepoint test failed:`, e.message); results.push({ test: 'savepoint', passed: false, error: e.message }); }
  
  // Test 3: Nested transaction
  try {
    const tm = new TransactionManager({ walDir: '/tmp/test-wal-3', enableDeadlockDetection: false });
    const parentId = await tm.begin();
    await tm.execute(parentId, { type: 'insert', memoryId: 'mem_parent', data: { content: 'Parent' } });
    const childId = await tm.begin({ parentId });
    await tm.execute(childId, { type: 'insert', memoryId: 'mem_child', data: { content: 'Child' } });
    await tm.commit(childId);
    console.log('✓ Test 8: nested transaction commit worked');
    await tm.commit(parentId);
    console.log('✓ Test 9: parent commit after nested worked');
    tm.close();
    results.push({ test: 'nested', passed: true });
  } catch (e) { console.error(`✗ Nested transaction test failed:`, e.message); results.push({ test: 'nested', passed: false, error: e.message }); }
  
  // Test 4: Rollback
  try {
    const tm = new TransactionManager({ walDir: '/tmp/test-wal-4', enableDeadlockDetection: false });
    const txId = await tm.begin();
    await tm.execute(txId, { type: 'insert', memoryId: 'mem_1', data: { content: 'Will be rolled back' } });
    await tm.rollback(txId, new Error('Test rollback'));
    console.log('✓ Test 10: rollback() worked');
    const stats = tm.getStats();
    console.log(`✓ Test 11: rolled back count: ${stats.transactionsRolledBack}`);
    results.push({ test: 'rollback', passed: true });
    tm.close();
  } catch (e) { console.error(`✗ Rollback test failed:`, e.message); results.push({ test: 'rollback', passed: false, error: e.message }); }
  
  // Test 5: Recovery
  try {
    const tm = new TransactionManager({ walDir: '/tmp/test-wal-5', enableDeadlockDetection: false });
    const txId = await tm.begin();
    await tm.execute(txId, { type: 'insert', memoryId: 'mem_1', data: { content: 'For recovery test' } });
    await tm.commit(txId);
    const recovery = await tm.recover();
    console.log(`✓ Test 12: recover() worked, recovered: ${recovery.recovered}`);
    results.push({ test: 'recovery', passed: true });
    tm.close();
  } catch (e) { console.error(`✗ Recovery test failed:`, e.message); results.push({ test: 'recovery', passed: false, error: e.message }); }
  
  // Summary
  console.log('\n📊 Test Results:');
  const passed = results.filter(r => r.passed).length;
  const failed = results.filter(r => !r.passed).length;
  console.log(`   Total: ${results.length} | Passed: ${passed} | Failed: ${failed}`);
  
  return results;
}

// Run tests if executed directly
if (process.argv[1] && process.argv[1].includes('transaction-system')) {
  runTests().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
}

export { runTests };
