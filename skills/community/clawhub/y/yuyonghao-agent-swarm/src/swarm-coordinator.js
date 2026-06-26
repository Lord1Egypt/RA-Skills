/**
 * Swarm Coordinator - 群体协调器
 * 管理群体生命周期、成员发现和通信
 */

export class SwarmCoordinator {
  constructor(options = {}) {
    this.options = {
      maxAgents: options.maxAgents || 100,
      consensusThreshold: options.consensusThreshold || 0.7,
      communicationProtocol: options.communicationProtocol || 'broadcast',
      ...options
    };
    this.swarms = new Map();
    this.agents = new Map();
  }

  createSwarm(config = {}) {
    const swarmId = `swarm-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const swarm = {
      id: swarmId,
      name: config.name || 'unnamed-swarm',
      specialization: config.specialization || 'general',
      agents: new Set(),
      status: 'active',
      createdAt: Date.now(),
      tasks: []
    };
    this.swarms.set(swarmId, swarm);
    return swarmId;
  }

  destroySwarm(swarmId) {
    const swarm = this.swarms.get(swarmId);
    if (!swarm) return false;
    
    swarm.agents.forEach(agentId => {
      const agent = this.agents.get(agentId);
      if (agent) agent.swarmId = null;
    });
    
    this.swarms.delete(swarmId);
    return true;
  }

  addAgent(swarmId, agentConfig) {
    const swarm = this.swarms.get(swarmId);
    if (!swarm) throw new Error(`Swarm ${swarmId} not found`);
    if (swarm.agents.size >= this.options.maxAgents) {
      throw new Error('Swarm capacity exceeded');
    }

    const agent = {
      id: agentConfig.id || `agent-${Date.now()}`,
      swarmId,
      capabilities: agentConfig.capabilities || [],
      capacity: agentConfig.capacity || 1,
      load: 0,
      status: 'idle',
      registeredAt: Date.now()
    };
    
    this.agents.set(agent.id, agent);
    swarm.agents.add(agent.id);
    return agent.id;
  }

  removeAgent(agentId) {
    const agent = this.agents.get(agentId);
    if (!agent) return false;
    
    const swarm = this.swarms.get(agent.swarmId);
    if (swarm) swarm.agents.delete(agentId);
    
    this.agents.delete(agentId);
    return true;
  }

  async executeTask(swarmId, taskConfig) {
    const swarm = this.swarms.get(swarmId);
    if (!swarm) throw new Error(`Swarm ${swarmId} not found`);

    const task = {
      id: `task-${Date.now()}`,
      type: taskConfig.type,
      input: taskConfig.input,
      status: 'pending',
      createdAt: Date.now()
    };

    swarm.tasks.push(task);
    
    const availableAgents = swarm.agents.size;
    if (availableAgents === 0) {
      throw new Error('No agents available in swarm');
    }

    task.status = 'executing';
    
    const results = await this.distributeTask(swarm, task, taskConfig.shardStrategy);
    
    task.status = 'completed';
    task.completedAt = Date.now();
    
    return {
      taskId: task.id,
      results,
      agentCount: availableAgents,
      duration: task.completedAt - task.createdAt
    };
  }

  async distributeTask(swarm, task, strategy) {
    const agentIds = Array.from(swarm.agents);
    const results = [];

    if (strategy === 'parallel') {
      const promises = agentIds.map(agentId => 
        this.executeOnAgent(agentId, task)
      );
      const agentResults = await Promise.allSettled(promises);
      results.push(...agentResults.map(r => 
        r.status === 'fulfilled' ? r.value : { error: r.reason }
      ));
    } else {
      for (const agentId of agentIds) {
        try {
          const result = await this.executeOnAgent(agentId, task);
          results.push(result);
        } catch (error) {
          results.push({ error: error.message });
        }
      }
    }

    return results;
  }

  async executeOnAgent(agentId, task) {
    const agent = this.agents.get(agentId);
    if (!agent) throw new Error(`Agent ${agentId} not found`);
    
    agent.status = 'busy';
    agent.load++;
    
    await new Promise(resolve => setTimeout(resolve, 100));
    
    agent.status = 'idle';
    
    return {
      agentId,
      taskId: task.id,
      output: `Processed by ${agentId}`,
      timestamp: Date.now()
    };
  }

  getSwarmStatus(swarmId) {
    const swarm = this.swarms.get(swarmId);
    if (!swarm) return null;

    const agentStatuses = Array.from(swarm.agents).map(id => {
      const agent = this.agents.get(id);
      return agent ? { id: agent.id, status: agent.status, load: agent.load } : null;
    }).filter(Boolean);

    return {
      id: swarm.id,
      name: swarm.name,
      agentCount: swarm.agents.size,
      agents: agentStatuses,
      taskCount: swarm.tasks.length,
      status: swarm.status,
      createdAt: swarm.createdAt
    };
  }

  getAllSwarms() {
    return Array.from(this.swarms.keys()).map(id => this.getSwarmStatus(id));
  }
}

export default SwarmCoordinator;
