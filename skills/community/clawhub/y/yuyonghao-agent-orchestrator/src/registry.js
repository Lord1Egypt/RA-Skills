/**
 * AgentRegistry - Agent registration and discovery
 * Manages agent lifecycle and capability indexing
 */

const EventEmitter = require('events');

class AgentRegistry extends EventEmitter {
  constructor(options = {}) {
    super();
    this.agents = new Map();
    this.capabilityIndex = new Map(); // capability -> Set(agentIds)
    this.options = {
      maxAgents: 100,
      ...options
    };
  }

  register(config) {
    if (this.agents.size >= this.options.maxAgents) {
      throw new Error(`Maximum agent limit reached: ${this.options.maxAgents}`);
    }

    if (!config.id) {
      throw new Error('Agent ID is required');
    }

    if (this.agents.has(config.id)) {
      throw new Error(`Agent already registered: ${config.id}`);
    }

    const agent = {
      id: config.id,
      capabilities: config.capabilities || [],
      resources: {
        maxConcurrent: config.resources?.maxConcurrent || 5,
        memoryMB: config.resources?.memoryMB || 256,
        cpuPercent: config.resources?.cpuPercent || 20,
        ...config.resources
      },
      metadata: config.metadata || {},
      status: 'idle',
      registeredAt: Date.now(),
      lastSeen: Date.now(),
      tasksCompleted: 0,
      tasksFailed: 0,
      currentLoad: 0
    };

    this.agents.set(agent.id, agent);

    // Index capabilities
    for (const capability of agent.capabilities) {
      if (!this.capabilityIndex.has(capability)) {
        this.capabilityIndex.set(capability, new Set());
      }
      this.capabilityIndex.get(capability).add(agent.id);
    }

    this.emit('agent:registered', agent);
    return agent;
  }

  unregister(agentId) {
    const agent = this.agents.get(agentId);
    if (!agent) {
      return false;
    }

    // Remove from capability index
    for (const capability of agent.capabilities) {
      const agents = this.capabilityIndex.get(capability);
      if (agents) {
        agents.delete(agentId);
        if (agents.size === 0) {
          this.capabilityIndex.delete(capability);
        }
      }
    }

    this.agents.delete(agentId);
    this.emit('agent:unregistered', agentId);
    return true;
  }

  get(agentId) {
    return this.agents.get(agentId);
  }

  getAll() {
    return Array.from(this.agents.values());
  }

  getByCapability(capability) {
    const agentIds = this.capabilityIndex.get(capability);
    if (!agentIds) {
      return [];
    }
    return Array.from(agentIds).map(id => this.agents.get(id)).filter(Boolean);
  }

  getByCapabilities(capabilities, matchAll = true) {
    if (!capabilities || capabilities.length === 0) {
      return this.getAll();
    }

    if (matchAll) {
      // Agent must have all capabilities
      let result = new Set(this.getByCapability(capabilities[0]).map(a => a.id));
      for (let i = 1; i < capabilities.length; i++) {
        const agents = new Set(this.getByCapability(capabilities[i]).map(a => a.id));
        result = new Set([...result].filter(id => agents.has(id)));
      }
      return Array.from(result).map(id => this.agents.get(id)).filter(Boolean);
    } else {
      // Agent must have at least one capability
      const result = new Set();
      for (const capability of capabilities) {
        const agents = this.getByCapability(capability);
        for (const agent of agents) {
          result.add(agent.id);
        }
      }
      return Array.from(result).map(id => this.agents.get(id)).filter(Boolean);
    }
  }

  updateAgentStatus(agentId, status) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.status = status;
      agent.lastSeen = Date.now();
      this.emit('agent:status:changed', { agentId, status });
    }
  }

  updateAgentLoad(agentId, load) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.currentLoad = load;
      agent.lastSeen = Date.now();
    }
  }

  incrementTaskCount(agentId, success = true) {
    const agent = this.agents.get(agentId);
    if (agent) {
      if (success) {
        agent.tasksCompleted++;
      } else {
        agent.tasksFailed++;
      }
    }
  }

  getHealthyAgents() {
    return this.getAll().filter(agent => agent.status === 'healthy');
  }

  getAvailableAgents() {
    return this.getAll().filter(agent => 
      agent.status === 'healthy' && 
      agent.currentLoad < agent.resources.maxConcurrent
    );
  }

  getStats() {
    const agents = this.getAll();
    return {
      total: agents.length,
      byStatus: {
        healthy: agents.filter(a => a.status === 'healthy').length,
        unhealthy: agents.filter(a => a.status === 'unhealthy').length,
        idle: agents.filter(a => a.status === 'idle').length
      },
      byCapability: Array.from(this.capabilityIndex.entries()).map(([cap, ids]) => ({
        capability: cap,
        count: ids.size
      })),
      totalTasksCompleted: agents.reduce((sum, a) => sum + a.tasksCompleted, 0),
      totalTasksFailed: agents.reduce((sum, a) => sum + a.tasksFailed, 0)
    };
  }

  hasCapability(agentId, capability) {
    const agent = this.agents.get(agentId);
    return agent && agent.capabilities.includes(capability);
  }

  getCapabilities(agentId) {
    const agent = this.agents.get(agentId);
    return agent ? agent.capabilities : [];
  }

  updateCapabilities(agentId, capabilities) {
    const agent = this.agents.get(agentId);
    if (!agent) {
      throw new Error(`Agent not found: ${agentId}`);
    }

    // Remove old capabilities from index
    for (const capability of agent.capabilities) {
      const agents = this.capabilityIndex.get(capability);
      if (agents) {
        agents.delete(agentId);
      }
    }

    // Update capabilities
    agent.capabilities = capabilities;

    // Add new capabilities to index
    for (const capability of capabilities) {
      if (!this.capabilityIndex.has(capability)) {
        this.capabilityIndex.set(capability, new Set());
      }
      this.capabilityIndex.get(capability).add(agentId);
    }

    this.emit('agent:capabilities:updated', { agentId, capabilities });
  }
}

module.exports = { AgentRegistry };
