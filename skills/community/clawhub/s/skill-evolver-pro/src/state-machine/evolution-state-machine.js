/**
 * 技能进化状态机 - 管理技能进化流程的状态转换
 * 
 * 设计模式：状态机模式 (State Machine Pattern)
 * 核心原则：状态外置 (State Externalization) - 状态持久化到文件，支持中断恢复
 * 
 * @version v0.3.0
 * @author 王的奴隶 · 严谨专业版
 */

const fs = require('fs').promises;
const path = require('path');
const EventEmitter = require('events');

// ============================================================================
// 状态定义
// ============================================================================

const STATES = {
  IDLE: 'IDLE',                    // 空闲，等待触发
  ANALYZING: 'ANALYZING',          // 分析技能使用数据
  PLANNING: 'PLANNING',            // 生成进化计划
  IMPLEMENTING: 'IMPLEMENTING',    // 实施优化
  TESTING: 'TESTING',              // 验证优化效果
  DEPLOYING: 'DEPLOYING',          // 部署新版本
  COMPLETED: 'COMPLETED',          // 进化完成
  FAILED: 'FAILED'                 // 进化失败（可重试）
};

// ============================================================================
// 状态转换规则
// ============================================================================

const TRANSITIONS = {
  [STATES.IDLE]: [STATES.ANALYZING, STATES.FAILED],
  [STATES.ANALYZING]: [STATES.PLANNING, STATES.FAILED],
  [STATES.PLANNING]: [STATES.IMPLEMENTING, STATES.FAILED],
  [STATES.IMPLEMENTING]: [STATES.TESTING, STATES.FAILED],
  [STATES.TESTING]: [STATES.DEPLOYING, STATES.IMPLEMENTING, STATES.FAILED],
  [STATES.DEPLOYING]: [STATES.COMPLETED, STATES.FAILED],
  [STATES.COMPLETED]: [STATES.IDLE],
  [STATES.FAILED]: [STATES.IDLE, STATES.ANALYZING]
};

// ============================================================================
// 状态机类
// ============================================================================

class EvolutionStateMachine extends EventEmitter {
  constructor(skillName, options = {}) {
    super();
    this.skillName = skillName;
    this.dataDir = options.dataDir || path.join(__dirname, '../../data');
    this.timeoutMs = options.timeoutMs || 300000;
    this.currentState = STATES.IDLE;
    this.stateHistory = [];
    this.stateStartTime = null;
    this.transitionCallbacks = {};
  }

  _getStateFilePath() {
    return path.join(this.dataDir, 'state-store', `${this.skillName}-state.json`);
  }

  _getHistoryFilePath() {
    return path.join(this.dataDir, 'evolution-log', this.skillName, 'state-history.json');
  }

  async _ensureDirectories() {
    const dirs = [
      path.join(this.dataDir, 'state-store'),
      path.join(this.dataDir, 'evolution-log', this.skillName)
    ];
    for (const dir of dirs) {
      await fs.mkdir(dir, { recursive: true });
    }
  }

  async readPersistedState() {
    try {
      const stateFile = this._getStateFilePath();
      const data = await fs.readFile(stateFile, 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      if (error.code === 'ENOENT') return null;
      throw error;
    }
  }

  async persistState() {
    await this._ensureDirectories();
    const stateData = {
      skillName: this.skillName,
      currentState: this.currentState,
      stateStartTime: this.stateStartTime,
      stateHistory: this.stateHistory,
      lastUpdated: Date.now()
    };
    await fs.writeFile(this._getStateFilePath(), JSON.stringify(stateData, null, 2));
  }

  isTimeout() {
    if (!this.stateStartTime) return false;
    return Date.now() - this.stateStartTime > this.timeoutMs;
  }

  getCurrentState() {
    return this.currentState;
  }

  getStateHistory() {
    return [...this.stateHistory];
  }

  isValidTransition(fromState, toState) {
    const allowedTransitions = TRANSITIONS[fromState];
    return allowedTransitions && allowedTransitions.includes(toState);
  }

  onTransition(fromState, toState, callback) {
    const key = `${fromState}->${toState}`;
    if (!this.transitionCallbacks[key]) {
      this.transitionCallbacks[key] = [];
    }
    this.transitionCallbacks[key].push(callback);
  }

  async transition(nextState, data = {}) {
    const previousState = this.currentState;

    if (!this.isValidTransition(previousState, nextState)) {
      const error = new Error(
        `Invalid transition: ${previousState} → ${nextState}. ` +
        `Allowed: ${TRANSITIONS[previousState]?.join(', ') || 'none'}`
      );
      this.emit('transition:error', { from: previousState, to: nextState, error });
      throw error;
    }

    const key = `${previousState}->${nextState}`;
    if (this.transitionCallbacks[key]) {
      for (const callback of this.transitionCallbacks[key]) {
        await callback(data);
      }
    }

    this.currentState = nextState;
    this.stateStartTime = Date.now();
    this.stateHistory.push({ from: previousState, to: nextState, timestamp: Date.now(), data });

    await this.persistState();

    this.emit('stateChange', { from: previousState, to: nextState, data });
    this.emit(`state:${nextState}`, data);

    return true;
  }

  async start(options = {}) {
    if (this.currentState !== STATES.IDLE) {
      throw new Error(`Cannot start from state: ${this.currentState}`);
    }
    await this.transition(STATES.ANALYZING, { ...options, action: 'start' });
  }

  async resume() {
    const persistedState = await this.readPersistedState();
    if (!persistedState) throw new Error('No persisted state found');

    this.currentState = persistedState.currentState;
    this.stateStartTime = persistedState.stateStartTime;
    this.stateHistory = persistedState.stateHistory || [];

    this.emit('resumed', { state: this.currentState, history: this.stateHistory });
    return this.currentState;
  }

  async complete(data = {}) {
    if (this.currentState !== STATES.DEPLOYING) {
      throw new Error(`Cannot complete from state: ${this.currentState}`);
    }
    await this.transition(STATES.COMPLETED, { ...data, action: 'complete' });
    setTimeout(() => this.transition(STATES.IDLE, { action: 'reset' }), 1000);
  }

  async fail(error) {
    const previousState = this.currentState;
    await this.transition(STATES.FAILED, { error: error.message || error, action: 'fail' });
    this.emit('failed', { from: previousState, error });
  }

  async reset() {
    this.currentState = STATES.IDLE;
    this.stateHistory = [];
    this.stateStartTime = null;
    await this.persistState();
    this.emit('reset', {});
  }

  getInfo() {
    return {
      skillName: this.skillName,
      currentState: this.currentState,
      stateStartTime: this.stateStartTime,
      historyLength: this.stateHistory.length,
      isTimeout: this.isTimeout(),
      allowedTransitions: TRANSITIONS[this.currentState] || []
    };
  }
}

module.exports = { EvolutionStateMachine, STATES, TRANSITIONS };
