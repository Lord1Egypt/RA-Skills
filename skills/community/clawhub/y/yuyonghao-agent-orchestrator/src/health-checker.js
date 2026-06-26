/**
 * HealthChecker - Agent health monitoring
 * Performs heartbeat checks and manages agent health status
 */

const EventEmitter = require('events');

class HealthChecker extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.options = {
      enabled: true,
      interval: 5000,
      timeout: 3000,
      failureThreshold: 3,
      successThreshold: 2,
      ...options
    };

    this.agents = new Map(); // agentId -> health state
    this.isRunning = false;
    this.checkInterval = null;
  }

  async start() {
    if (this.isRunning || !this.options.enabled) return;
    
    this.isRunning = true;
    this.checkInterval = setInterval(() => {
      this._checkAllAgents();
    }, this.options.interval);
    
    this.emit('healthchecker:started');
    console.log('[HealthChecker] Started');
  }

  async stop() {
    if (!this.isRunning) return;
    
    this.isRunning = false;
    
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
    }
    
    this.emit('healthchecker:stopped');
    console.log('[HealthChecker] Stopped');
  }

  registerAgent(agent) {
    this.agents.set(agent.id, {
      agentId: agent.id,
      status: 'unknown',
      consecutiveFailures: 0,
      consecutiveSuccesses: 0,
      lastCheck: null,
      lastSuccess: null,
      lastFailure: null,
      failureReason: null,
      checkHistory: [] // Limited history
    });
    
    this.emit('agent:registered', agent.id);
  }

  unregisterAgent(agentId) {
    this.agents.delete(agentId);
    this.emit('agent:unregistered', agentId);
  }

  async checkAgent(agentId) {
    const state = this.agents.get(agentId);
    if (!state) return null;

    const checkStart = Date.now();
    
    try {
      // Perform health check
      const result = await this._performCheck(agentId);
      
      const checkDuration = Date.now() - checkStart;
      this._recordCheck(state, true, checkDuration);
      
      return result;
    } catch (error) {
      const checkDuration = Date.now() - checkStart;
      this._recordCheck(state, false, checkDuration, error.message);
      
      throw error;
    }
  }

  async _performCheck(agentId) {
    // Simulate health check - in production, this would ping the agent
    // For now, we'll use a simulated check that can be overridden
    return new Promise((resolve, reject) => {
      const checkFn = this._customCheck || this._defaultCheck;
      checkFn(agentId, this.options.timeout)
        .then(resolve)
        .catch(reject);
    });
  }

  async _defaultCheck(agentId, timeout) {
    // Default implementation - simulate a successful check
    // In production, this would make an actual HTTP/RPC call to the agent
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          agentId,
          healthy: true,
          timestamp: Date.now(),
          latency: Math.random() * 100
        });
      }, Math.random() * 50);
    });
  }

  setCustomCheck(fn) {
    this._customCheck = fn;
  }

  _recordCheck(state, success, duration, errorMessage = null) {
    state.lastCheck = Date.now();
    
    // Update history
    state.checkHistory.push({
      success,
      duration,
      timestamp: state.lastCheck,
      error: errorMessage
    });
    
    // Limit history size
    if (state.checkHistory.length > 100) {
      state.checkHistory = state.checkHistory.slice(-50);
    }

    if (success) {
      state.consecutiveSuccesses++;
      state.consecutiveFailures = 0;
      state.lastSuccess = state.lastCheck;
      
      // Mark healthy if threshold reached
      if (state.status !== 'healthy' && state.consecutiveSuccesses >= this.options.successThreshold) {
        state.status = 'healthy';
        this.emit('agent:healthy', state.agentId);
      }
    } else {
      state.consecutiveFailures++;
      state.consecutiveSuccesses = 0;
      state.lastFailure = state.lastCheck;
      state.failureReason = errorMessage;
      
      // Mark unhealthy if threshold reached
      if (state.status !== 'unhealthy' && state.consecutiveFailures >= this.options.failureThreshold) {
        state.status = 'unhealthy';
        this.emit('agent:unhealthy', state.agentId, errorMessage);
      }
    }
  }

  async _checkAllAgents() {
    const checks = [];
    
    for (const [agentId, state] of this.agents) {
      checks.push(this.checkAgent(agentId).catch(error => {
        // Error already recorded in _recordCheck
        return { agentId, error: error.message };
      }));
    }
    
    await Promise.all(checks);
  }

  getHealth(agentId) {
    return this.agents.get(agentId);
  }

  getAllHealth() {
    return Array.from(this.agents.values()).map(state => ({
      agentId: state.agentId,
      status: state.status,
      lastCheck: state.lastCheck,
      lastSuccess: state.lastSuccess,
      lastFailure: state.lastFailure,
      consecutiveFailures: state.consecutiveFailures,
      consecutiveSuccesses: state.consecutiveSuccesses,
      failureReason: state.failureReason,
      checkCount: state.checkHistory.length,
      successRate: this._calculateSuccessRate(state)
    }));
  }

  getHealthyAgents() {
    return Array.from(this.agents.values())
      .filter(state => state.status === 'healthy')
      .map(state => state.agentId);
  }

  getUnhealthyAgents() {
    return Array.from(this.agents.values())
      .filter(state => state.status === 'unhealthy')
      .map(state => state.agentId);
  }

  _calculateSuccessRate(state) {
    if (state.checkHistory.length === 0) return 0;
    const successes = state.checkHistory.filter(h => h.success).length;
    return successes / state.checkHistory.length;
  }

  getStats() {
    const allHealth = this.getAllHealth();
    
    return {
      total: allHealth.length,
      healthy: allHealth.filter(h => h.status === 'healthy').length,
      unhealthy: allHealth.filter(h => h.status === 'unhealthy').length,
      unknown: allHealth.filter(h => h.status === 'unknown').length,
      averageSuccessRate: allHealth.length > 0 
        ? allHealth.reduce((sum, h) => sum + h.successRate, 0) / allHealth.length 
        : 0,
      lastCheck: allHealth.length > 0
        ? Math.max(...allHealth.map(h => h.lastCheck || 0))
        : null
    };
  }

  simulateFailure(agentId, reason = 'Simulated failure') {
    const state = this.agents.get(agentId);
    if (!state) return false;

    this._recordCheck(state, false, 0, reason);
    return true;
  }

  simulateRecovery(agentId) {
    const state = this.agents.get(agentId);
    if (!state) return false;

    this._recordCheck(state, true, 0);
    return true;
  }
}

module.exports = { HealthChecker };
