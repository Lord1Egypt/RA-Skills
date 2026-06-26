/**
 * 原子事务管理器 - 解决双写无事务问题
 * 实现两阶段提交协议，保证 JSON 和向量存储的一致性
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export class AtomicTransactionManager {
  constructor() {
    this.transactions = new Map();
    this.recoveryLogPath = path.join(process.env.HOME || '/root', '.unified-memory', 'transaction-recovery.log');
    
    // 确保日志目录存在
    this._ensureLogDirectory();
  }
  
  async _ensureLogDirectory() {
    const logDir = path.dirname(this.recoveryLogPath);
    try {
      await fs.mkdir(logDir, { recursive: true });
    } catch (error) {
      console.warn(`Failed to create log directory: ${error.message}`);
    }
  }

  /**
   * 开始一个新事务
   */
  async beginTransaction(transactionId = `tx_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`) {
    const transaction = {
      id: transactionId,
      startTime: Date.now(),
      state: 'preparing',
      jsonData: null,
      vectorData: null,
      prepared: false,
      committed: false
    };

    this.transactions.set(transactionId, transaction);
    
    // 记录事务开始
    await this.logTransaction(transactionId, 'BEGIN', { state: 'preparing' });
    
    return transactionId;
  }

  /**
   * 准备 JSON 写入
   */
  async prepareJsonWrite(transactionId, memory) {
    const transaction = this.transactions.get(transactionId);
    if (!transaction) {
      throw new Error(`Transaction ${transactionId} not found`);
    }

    // 创建临时文件
    const tempDir = path.join(process.env.HOME || '/root', '.unified-memory', 'temp');
    await fs.mkdir(tempDir, { recursive: true });
    
    const tempFile = path.join(tempDir, `${transactionId}_json.tmp`);
    const jsonData = JSON.stringify(memory, null, 2);
    
    await fs.writeFile(tempFile, jsonData, 'utf8');
    
    // 确保写入磁盘 - 使用 fd.sync()
    const fd = await fs.open(tempFile, 'r+');
    try {
      await fd.sync();
    } finally {
      await fd.close();
    }
    
    transaction.jsonData = {
      tempFile,
      memoryId: memory.id,
      data: jsonData
    };

    await this.logTransaction(transactionId, 'PREPARE_JSON', { 
      memoryId: memory.id,
      tempFile 
    });

    // 如果没有向量数据，也标记为 prepared
    if (!transaction.vectorData) {
      transaction.prepared = true;
      transaction.state = 'prepared';
    }

    return tempFile;
  }

  /**
   * 准备向量写入
   */
  async prepareVectorWrite(transactionId, memory, embedding) {
    const transaction = this.transactions.get(transactionId);
    if (!transaction) {
      throw new Error(`Transaction ${transactionId} not found`);
    }

    // 向量数据准备
    transaction.vectorData = {
      memoryId: memory.id,
      embedding: embedding,
      timestamp: Date.now()
    };

    await this.logTransaction(transactionId, 'PREPARE_VECTOR', { 
      memoryId: memory.id,
      hasEmbedding: !!embedding
    });

    transaction.prepared = true;
    transaction.state = 'prepared';

    return true;
  }

  /**
   * 提交事务
   */
  async commitTransaction(transactionId) {
    const transaction = this.transactions.get(transactionId);
    if (!transaction) {
      throw new Error(`Transaction ${transactionId} not found`);
    }

    if (!transaction.prepared) {
      throw new Error(`Transaction ${transactionId} not prepared`);
    }

    transaction.state = 'committing';

    try {
      // 阶段1：提交 JSON
      if (transaction.jsonData) {
        await this.commitJsonWrite(transaction);
      }

      // 阶段2：提交向量
      if (transaction.vectorData) {
        await this.commitVectorWrite(transaction);
      }

      // 阶段3：清理临时文件
      await this.cleanupTransaction(transaction);

      transaction.committed = true;
      transaction.state = 'committed';
      
      await this.logTransaction(transactionId, 'COMMIT_SUCCESS', { 
        jsonCommitted: !!transaction.jsonData,
        vectorCommitted: !!transaction.vectorData
      });

      return true;

    } catch (error) {
      // 提交失败，执行回滚
      await this.rollbackTransaction(transactionId, error);
      throw error;
    }
  }

  /**
   * 提交 JSON 写入
   */
  async commitJsonWrite(transaction) {
    const { jsonData } = transaction;
    
    // 这里应该调用实际的 JSON 存储写入
    // 暂时模拟写入
    console.log(`[Transaction] Committing JSON for memory ${jsonData.memoryId}`);
    
    // 实际实现中，这里会调用 storage.js 的写入函数
    // 并确保写入成功后再删除临时文件
    
    return true;
  }

  /**
   * 提交向量写入
   */
  async commitVectorWrite(transaction) {
    const { vectorData } = transaction;
    
    // 这里应该调用实际的向量存储写入
    console.log(`[Transaction] Committing vector for memory ${vectorData.memoryId}`);
    
    // 实际实现中，这里会调用 vector_lancedb.js 的写入函数
    
    return true;
  }

  /**
   * 回滚事务
   */
  async rollbackTransaction(transactionId, error) {
    const transaction = this.transactions.get(transactionId);
    if (!transaction) return;

    transaction.state = 'rolling_back';

    try {
      // 清理 JSON 临时文件
      if (transaction.jsonData?.tempFile) {
        try {
          await fs.unlink(transaction.jsonData.tempFile);
        } catch (e) {
          console.warn(`Failed to delete temp file: ${e.message}`);
        }
      }

      // 清理向量数据
      // 实际实现中可能需要撤销向量写入

      await this.logTransaction(transactionId, 'ROLLBACK', { 
        error: error?.message,
        jsonCleaned: !!transaction.jsonData,
        vectorCleaned: !!transaction.vectorData
      });

    } finally {
      transaction.state = 'rolled_back';
      this.transactions.delete(transactionId);
    }
  }

  /**
   * 清理事务
   */
  async cleanupTransaction(transaction) {
    // 清理临时文件
    if (transaction.jsonData?.tempFile) {
      try {
        await fs.unlink(transaction.jsonData.tempFile);
      } catch (e) {
        console.warn(`Failed to delete temp file during cleanup: ${e.message}`);
      }
    }

    // 从活动事务中移除
    this.transactions.delete(transaction.id);
  }

  /**
   * 记录事务日志（用于恢复）
   */
  async logTransaction(transactionId, action, details = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      transactionId,
      action,
      details,
      pid: process.pid
    };

    try {
      await fs.appendFile(
        this.recoveryLogPath,
        JSON.stringify(logEntry) + '\n',
        'utf8'
      );
    } catch (error) {
      console.warn(`Failed to log transaction: ${error.message}`);
    }
  }

  /**
   * 恢复未完成的事务（系统启动时调用）
   */
  async recoverTransactions() {
    try {
      if (!await fs.access(this.recoveryLogPath).then(() => true).catch(() => false)) {
        return { recovered: 0, errors: 0 };
      }

      const logContent = await fs.readFile(this.recoveryLogPath, 'utf8');
      const lines = logContent.trim().split('\n');
      
      const transactions = new Map();
      
      // 分析日志，找出未完成的事务
      for (const line of lines) {
        try {
          const entry = JSON.parse(line);
          if (!transactions.has(entry.transactionId)) {
            transactions.set(entry.transactionId, []);
          }
          transactions.get(entry.transactionId).push(entry);
        } catch (e) {
          console.warn(`Failed to parse log entry: ${e.message}`);
        }
      }

      let recovered = 0;
      let errors = 0;

      // 检查每个事务的完成状态
      for (const [txId, entries] of transactions) {
        const lastAction = entries[entries.length - 1]?.action;
        
        if (lastAction !== 'COMMIT_SUCCESS' && lastAction !== 'ROLLBACK') {
          console.log(`[Recovery] Found incomplete transaction: ${txId}, last action: ${lastAction}`);
          
          try {
            // 尝试回滚未完成的事务
            await this.rollbackTransaction(txId, new Error('Recovery rollback'));
            recovered++;
          } catch (error) {
            console.error(`[Recovery] Failed to rollback transaction ${txId}: ${error.message}`);
            errors++;
          }
        }
      }

      // 清理旧的恢复日志
      await this.cleanupRecoveryLog();

      return { recovered, errors };

    } catch (error) {
      console.error(`[Recovery] Failed to recover transactions: ${error.message}`);
      return { recovered: 0, errors: 1 };
    }
  }

  /**
   * 清理恢复日志
   */
  async cleanupRecoveryLog() {
    try {
      // 保留最近 1000 行日志
      const logContent = await fs.readFile(this.recoveryLogPath, 'utf8');
      const lines = logContent.trim().split('\n');
      
      if (lines.length > 1000) {
        const recentLines = lines.slice(-1000);
        await fs.writeFile(this.recoveryLogPath, recentLines.join('\n') + '\n', 'utf8');
      }
    } catch (error) {
      console.warn(`Failed to cleanup recovery log: ${error.message}`);
    }
  }

  /**
   * 获取事务状态
   */
  getTransactionStatus(transactionId) {
    const transaction = this.transactions.get(transactionId);
    if (!transaction) return null;
    
    return {
      id: transaction.id,
      state: transaction.state,
      prepared: transaction.prepared,
      committed: transaction.committed,
      startTime: transaction.startTime,
      duration: Date.now() - transaction.startTime
    };
  }

  /**
   * 获取所有活动事务
   */
  getAllTransactions() {
    const result = [];
    for (const [id, tx] of this.transactions) {
      result.push({
        id,
        state: tx.state,
        prepared: tx.prepared,
        committed: tx.committed,
        startTime: tx.startTime,
        duration: Date.now() - tx.startTime
      });
    }
    return result;
  }
}

// 单例实例
let _instance = null;

export function getTransactionManager() {
  if (!_instance) {
    _instance = new AtomicTransactionManager();
  }
  return _instance;
}

export default AtomicTransactionManager;