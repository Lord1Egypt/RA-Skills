/**
 * 文件存储层 - 技能进化数据持久化
 * 
 * 设计模式：状态外置原则 (State Externalization)
 * 核心原则：文件 > 内存，支持中断恢复
 * 
 * @version v0.3.0
 * @author 王的奴隶 · 严谨专业版
 */

const fs = require('fs').promises;
const path = require('path');

class FileStore {
  constructor(baseDir) {
    this.baseDir = baseDir || path.join(__dirname, '../../data');
  }

  async _ensureDir(dirPath) {
    await fs.mkdir(dirPath, { recursive: true });
  }

  /**
   * 保存进化日志
   * @param {string} skillName - 技能名称
   * @param {Object} logData - 日志数据
   * @returns {Promise<string>} 文件路径
   */
  async saveEvolutionLog(skillName, logData) {
    const logDir = path.join(this.baseDir, 'evolution-log', skillName);
    await this._ensureDir(logDir);

    const timestamp = logData.timestamp || Date.now();
    const fileName = `${timestamp}-evolution.json`;
    const filePath = path.join(logDir, fileName);

    const fullLog = {
      ...logData,
      recordedAt: new Date().toISOString(),
      version: 'v0.3.0'
    };

    await fs.writeFile(filePath, JSON.stringify(fullLog, null, 2));
    return filePath;
  }

  /**
   * 读取进化日志
   * @param {string} skillName - 技能名称
   * @param {number} timestamp - 时间戳（可选）
   * @returns {Promise<Object[]>}
   */
  async getEvolutionLogs(skillName, timestamp = null) {
    const logDir = path.join(this.baseDir, 'evolution-log', skillName);
    try {
      const files = await fs.readdir(logDir);
      const logs = [];

      for (const file of files) {
        if (!file.endsWith('-evolution.json')) continue;
        if (timestamp && !file.startsWith(`${timestamp}`)) continue;

        const filePath = path.join(logDir, file);
        const content = await fs.readFile(filePath, 'utf-8');
        logs.push(JSON.parse(content));
      }

      return logs.sort((a, b) => b.timestamp - a.timestamp);
    } catch (error) {
      if (error.code === 'ENOENT') return [];
      throw error;
    }
  }

  /**
   * 保存版本历史
   * @param {string} skillName - 技能名称
   * @param {Object} versionData - 版本数据
   * @returns {Promise<void>}
   */
  async saveVersionHistory(skillName, versionData) {
    const historyDir = path.join(this.baseDir, 'version-history');
    await this._ensureDir(historyDir);

    const filePath = path.join(historyDir, `${skillName}-versions.json`);

    let history = [];
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      history = JSON.parse(content);
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }

    history.push({
      ...versionData,
      recordedAt: new Date().toISOString()
    });

    await fs.writeFile(filePath, JSON.stringify(history, null, 2));
  }

  /**
   * 读取版本历史
   * @param {string} skillName - 技能名称
   * @returns {Promise<Object[]>}
   */
  async getVersionHistory(skillName) {
    const filePath = path.join(this.baseDir, 'version-history', `${skillName}-versions.json`);
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      if (error.code === 'ENOENT') return [];
      throw error;
    }
  }

  /**
   * 保存状态（支持中断恢复）
   * @param {string} skillName - 技能名称
   * @param {Object} stateData - 状态数据
   * @returns {Promise<void>}
   */
  async saveState(skillName, stateData) {
    const stateDir = path.join(this.baseDir, 'state-store');
    await this._ensureDir(stateDir);

    const filePath = path.join(stateDir, `${skillName}-state.json`);
    const fullState = {
      ...stateData,
      lastUpdated: Date.now(),
      version: 'v0.3.0'
    };

    await fs.writeFile(filePath, JSON.stringify(fullState, null, 2));
  }

  /**
   * 读取状态
   * @param {string} skillName - 技能名称
   * @returns {Promise<Object|null>}
   */
  async getState(skillName) {
    const filePath = path.join(this.baseDir, 'state-store', `${skillName}-state.json`);
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      if (error.code === 'ENOENT') return null;
      throw error;
    }
  }

  /**
   * 删除状态
   * @param {string} skillName - 技能名称
   * @returns {Promise<void>}
   */
  async deleteState(skillName) {
    const filePath = path.join(this.baseDir, 'state-store', `${skillName}-state.json`);
    try {
      await fs.unlink(filePath);
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }
  }

  /**
   * 获取所有技能的状态
   * @returns {Promise<Object[]>}
   */
  async getAllStates() {
    const stateDir = path.join(this.baseDir, 'state-store');
    try {
      const files = await fs.readdir(stateDir);
      const states = [];

      for (const file of files) {
        if (!file.endsWith('-state.json')) continue;
        const filePath = path.join(stateDir, file);
        const content = await fs.readFile(filePath, 'utf-8');
        states.push(JSON.parse(content));
      }

      return states;
    } catch (error) {
      if (error.code === 'ENOENT') return [];
      throw error;
    }
  }

  /**
   * 导出完整数据（用于备份）
   * @param {string} skillName - 技能名称
   * @returns {Promise<Object>}
   */
  async exportData(skillName) {
    const [logs, versions, state] = await Promise.all([
      this.getEvolutionLogs(skillName),
      this.getVersionHistory(skillName),
      this.getState(skillName)
    ]);

    return {
      skillName,
      exportedAt: new Date().toISOString(),
      version: 'v0.3.0',
      data: { logs, versions, state }
    };
  }
}

module.exports = { FileStore };
