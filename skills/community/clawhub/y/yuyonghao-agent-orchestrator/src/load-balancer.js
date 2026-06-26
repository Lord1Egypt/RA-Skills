/**
 * LoadBalancer - Load balancing strategies for task distribution
 * Supports Round Robin, Least Connections, and custom strategies
 */

const EventEmitter = require('events');

class LoadBalancer extends EventEmitter {
  constructor(strategy = 'round-robin') {
    super();
    
    this.strategy = strategy;
    this.agents = new Map(); // agentId -> agent info
    this.agentList = []; // Ordered list for round-robin
    this.currentIndex = 0;
    this.weights = new Map(); // For weighted strategies
  }

  addAgent(agent) {
    this.agents.set(agent.id, {
      id: agent.id,
      capabilities: agent.capabilities || [],
      currentLoad: agent.currentLoad || 0,
      maxConcurrent: agent.resources?.maxConcurrent || 5,
      healthy: true,
      weight: 1,
      lastUsed: 0
    });
    
    this._rebuildAgentList();
    this.emit('agent:added', agent.id);
  }

  removeAgent(agentId) {
    this.agents.delete(agentId);
    this._rebuildAgentList();
    this.emit('agent:removed', agentId);
  }

  updateAgent(agent) {
    const existing = this.agents.get(agent.id);
    if (existing) {
      existing.currentLoad = agent.currentLoad || existing.currentLoad;
      existing.maxConcurrent = agent.resources?.maxConcurrent || existing.maxConcurrent;
      existing.capabilities = agent.capabilities || existing.capabilities;
    }
  }

  markHealthy(agentId) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.healthy = true;
      this.emit('agent:healthy', agentId);
    }
  }

  markUnhealthy(agentId) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.healthy = false;
      this.emit('agent:unhealthy', agentId);
    }
  }

  setWeight(agentId, weight) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.weight = weight;
      this.weights.set(agentId, weight);
    }
  }

  setStrategy(strategy) {
    const validStrategies = ['round-robin', 'least-connections', 'weighted-round-robin', 'random', 'first-available'];
    if (!validStrategies.includes(strategy)) {
      throw new Error(`Invalid strategy: ${strategy}. Valid strategies: ${validStrategies.join(', ')}`);
    }
    
    this.strategy = strategy;
    this.emit('strategy:changed', strategy);
  }

  select(availableAgents) {
    if (!availableAgents || availableAgents.length === 0) {
      return null;
    }

    // Filter to only healthy agents
    const healthyAgents = availableAgents.filter(a => {
      const agent = this.agents.get(a.id);
      return agent && agent.healthy;
    });

    if (healthyAgents.length === 0) {
      return null;
    }

    switch (this.strategy) {
      case 'round-robin':
        return this._roundRobin(healthyAgents);
      case 'least-connections':
        return this._leastConnections(healthyAgents);
      case 'weighted-round-robin':
        return this._weightedRoundRobin(healthyAgents);
      case 'random':
        return this._random(healthyAgents);
      case 'first-available':
        return this._firstAvailable(healthyAgents);
      default:
        return this._roundRobin(healthyAgents);
    }
  }

  _roundRobin(agents) {
    // Find the next available agent in round-robin order
    const startIndex = this.currentIndex;
    
    do {
      const agentId = this.agentList[this.currentIndex];
      this.currentIndex = (this.currentIndex + 1) % this.agentList.length;
      
      const agent = agents.find(a => a.id === agentId);
      if (agent) {
        const lbAgent = this.agents.get(agent.id);
        if (lbAgent) {
          lbAgent.lastUsed = Date.now();
        }
        return agent;
      }
    } while (this.currentIndex !== startIndex);
    
    return null;
  }

  _leastConnections(agents) {
    // Select agent with lowest load ratio
    return agents.reduce((best, current) => {
      const bestLoad = best.currentLoad / (best.resources?.maxConcurrent || 5);
      const currentLoad = current.currentLoad / (current.resources?.maxConcurrent || 5);
      return currentLoad < bestLoad ? current : best;
    });
  }

  _weightedRoundRobin(agents) {
    // Simple weighted round-robin
    const weightedList = [];
    
    for (const agent of agents) {
      const lbAgent = this.agents.get(agent.id);
      const weight = lbAgent?.weight || 1;
      for (let i = 0; i < weight; i++) {
        weightedList.push(agent);
      }
    }
    
    if (weightedList.length === 0) return null;
    
    const selected = weightedList[this.currentIndex % weightedList.length];
    this.currentIndex++;
    
    const lbAgent = this.agents.get(selected.id);
    if (lbAgent) {
      lbAgent.lastUsed = Date.now();
    }
    
    return selected;
  }

  _random(agents) {
    const index = Math.floor(Math.random() * agents.length);
    return agents[index];
  }

  _firstAvailable(agents) {
    return agents[0];
  }

  _rebuildAgentList() {
    this.agentList = Array.from(this.agents.keys());
  }

  getStats() {
    const agents = Array.from(this.agents.values());
    
    return {
      strategy: this.strategy,
      totalAgents: agents.length,
      healthyAgents: agents.filter(a => a.healthy).length,
      unhealthyAgents: agents.filter(a => !a.healthy).length,
      averageLoad: agents.length > 0 
        ? agents.reduce((sum, a) => sum + (a.currentLoad / a.maxConcurrent), 0) / agents.length 
        : 0,
      agents: agents.map(a => ({
        id: a.id,
        healthy: a.healthy,
        load: a.currentLoad,
        maxConcurrent: a.maxConcurrent,
        utilization: a.currentLoad / a.maxConcurrent,
        weight: a.weight,
        lastUsed: a.lastUsed
      }))
    };
  }

  getAgentLoad(agentId) {
    const agent = this.agents.get(agentId);
    if (!agent) return null;
    
    return {
      id: agent.id,
      currentLoad: agent.currentLoad,
      maxConcurrent: agent.maxConcurrent,
      utilization: agent.currentLoad / agent.maxConcurrent,
      healthy: agent.healthy
    };
  }

  // Custom strategy support
  setCustomSelector(selectorFn) {
    this._customSelector = selectorFn;
    this.strategy = 'custom';
  }

  _custom(agents) {
    if (this._customSelector) {
      return this._customSelector(agents, this.agents);
    }
    return this._roundRobin(agents);
  }
}

module.exports = { LoadBalancer };
