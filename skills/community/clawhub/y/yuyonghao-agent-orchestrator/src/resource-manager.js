/**
 * ResourceManager - Resource allocation and monitoring
 * Manages CPU, memory, and concurrency limits
 */

const EventEmitter = require('events');

class ResourceManager extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.options = {
      maxAgents: 100,
      maxTasksPerAgent: 10,
      maxMemoryMB: 1024,
      maxCpuPercent: 80,
      ...options
    };

    // Resource tracking
    this.agentResources = new Map(); // agentId -> { memory, cpu, tasks }
    this.taskResources = new Map(); // taskId -> { agentId, memory, cpu }
    
    // Current usage
    this.totalMemoryUsed = 0;
    this.totalCpuUsed = 0;
    this.totalTasks = 0;
    
    // Stats
    this.stats = {
      peakMemory: 0,
      peakCpu: 0,
      peakTasks: 0,
      totalAllocated: 0,
      totalReleased: 0
    };
  }

  canAddAgent() {
    return this.agentResources.size < this.options.maxAgents;
  }

  allocateAgent(agentId, resources = {}) {
    if (this.agentResources.has(agentId)) {
      throw new Error(`Agent already allocated: ${agentId}`);
    }

    const agentRes = {
      maxConcurrent: resources.maxConcurrent || 5,
      memoryMB: resources.memoryMB || 256,
      cpuPercent: resources.cpuPercent || 20,
      tasks: new Set(),
      memoryUsed: 0,
      cpuUsed: 0
    };

    this.agentResources.set(agentId, agentRes);
    this.stats.totalAllocated++;
    
    this.emit('agent:allocated', { agentId, resources: agentRes });
    return agentRes;
  }

  releaseAgent(agentId) {
    const agentRes = this.agentResources.get(agentId);
    if (!agentRes) return false;

    // Release all tasks
    for (const taskId of agentRes.tasks) {
      this.releaseTask(agentId, taskId);
    }

    this.agentResources.delete(agentId);
    this.stats.totalReleased++;
    
    this.emit('agent:released', { agentId });
    return true;
  }

  canAllocateTask(agentId, resources = {}) {
    const agentRes = this.agentResources.get(agentId);
    if (!agentRes) return false;

    // Check concurrency
    if (agentRes.tasks.size >= agentRes.maxConcurrent) {
      return false;
    }

    if (agentRes.tasks.size >= this.options.maxTasksPerAgent) {
      return false;
    }

    // Check memory
    const memoryNeeded = resources.memoryMB || 64;
    if (this.totalMemoryUsed + memoryNeeded > this.options.maxMemoryMB) {
      return false;
    }

    // Check CPU
    const cpuNeeded = resources.cpuPercent || 10;
    if (this.totalCpuUsed + cpuNeeded > this.options.maxCpuPercent) {
      return false;
    }

    return true;
  }

  trackTask(agentId, taskId, resources = {}) {
    const agentRes = this.agentResources.get(agentId);
    if (!agentRes) {
      throw new Error(`Agent not found: ${agentId}`);
    }

    const memoryNeeded = resources.memoryMB || 64;
    const cpuNeeded = resources.cpuPercent || 10;

    agentRes.tasks.add(taskId);
    agentRes.memoryUsed += memoryNeeded;
    agentRes.cpuUsed += cpuNeeded;

    this.taskResources.set(taskId, {
      agentId,
      memoryMB: memoryNeeded,
      cpuPercent: cpuNeeded
    });

    this.totalMemoryUsed += memoryNeeded;
    this.totalCpuUsed += cpuNeeded;
    this.totalTasks++;

    // Update peak stats
    this.stats.peakMemory = Math.max(this.stats.peakMemory, this.totalMemoryUsed);
    this.stats.peakCpu = Math.max(this.stats.peakCpu, this.totalCpuUsed);
    this.stats.peakTasks = Math.max(this.stats.peakTasks, this.totalTasks);

    this.emit('task:allocated', { 
      agentId, 
      taskId, 
      resources: { memoryMB: memoryNeeded, cpuPercent: cpuNeeded }
    });

    return true;
  }

  releaseTask(agentId, taskId) {
    const agentRes = this.agentResources.get(agentId);
    if (!agentRes) return false;

    if (!agentRes.tasks.has(taskId)) return false;

    const taskRes = this.taskResources.get(taskId);
    if (!taskRes) return false;

    agentRes.tasks.delete(taskId);
    agentRes.memoryUsed -= taskRes.memoryMB;
    agentRes.cpuUsed -= taskRes.cpuPercent;

    this.totalMemoryUsed -= taskRes.memoryMB;
    this.totalCpuUsed -= taskRes.cpuPercent;
    this.totalTasks--;

    this.taskResources.delete(taskId);

    this.emit('task:released', { agentId, taskId });
    return true;
  }

  getAgentResources(agentId) {
    const agentRes = this.agentResources.get(agentId);
    if (!agentRes) return null;

    return {
      maxConcurrent: agentRes.maxConcurrent,
      memoryMB: agentRes.memoryMB,
      cpuPercent: agentRes.cpuPercent,
      tasksRunning: agentRes.tasks.size,
      memoryUsed: agentRes.memoryUsed,
      cpuUsed: agentRes.cpuUsed,
      utilization: {
        tasks: agentRes.tasks.size / agentRes.maxConcurrent,
        memory: agentRes.memoryUsed / agentRes.memoryMB,
        cpu: agentRes.cpuUsed / agentRes.cpuPercent
      }
    };
  }

  getTaskResources(taskId) {
    return this.taskResources.get(taskId);
  }

  getLoad() {
    const agentCount = this.agentResources.size;
    if (agentCount === 0) return 0;

    const totalCapacity = agentCount * this.options.maxTasksPerAgent;
    return this.totalTasks / totalCapacity;
  }

  getStats() {
    const agentCount = this.agentResources.size;
    
    return {
      agents: {
        total: agentCount,
        max: this.options.maxAgents,
        utilization: agentCount / this.options.maxAgents
      },
      tasks: {
        running: this.totalTasks,
        max: agentCount * this.options.maxTasksPerAgent,
        utilization: agentCount > 0 ? this.totalTasks / (agentCount * this.options.maxTasksPerAgent) : 0
      },
      memory: {
        used: this.totalMemoryUsed,
        max: this.options.maxMemoryMB,
        utilization: this.totalMemoryUsed / this.options.maxMemoryMB,
        peak: this.stats.peakMemory
      },
      cpu: {
        used: this.totalCpuUsed,
        max: this.options.maxCpuPercent,
        utilization: this.totalCpuUsed / this.options.maxCpuPercent,
        peak: this.stats.peakCpu
      },
      peakTasks: this.stats.peakTasks,
      totalAllocated: this.stats.totalAllocated,
      totalReleased: this.stats.totalReleased
    };
  }

  getAgentStats(agentId) {
    const agentRes = this.agentResources.get(agentId);
    if (!agentRes) return null;

    return {
      id: agentId,
      resources: {
        maxConcurrent: agentRes.maxConcurrent,
        memoryMB: agentRes.memoryMB,
        cpuPercent: agentRes.cpuPercent
      },
      usage: {
        tasks: agentRes.tasks.size,
        memoryMB: agentRes.memoryUsed,
        cpuPercent: agentRes.cpuUsed
      },
      utilization: {
        tasks: agentRes.tasks.size / agentRes.maxConcurrent,
        memory: agentRes.memoryUsed / agentRes.memoryMB,
        cpu: agentRes.cpuUsed / agentRes.cpuPercent
      },
      taskIds: Array.from(agentRes.tasks)
    };
  }

  getAllAgentStats() {
    return Array.from(this.agentResources.keys()).map(id => this.getAgentStats(id));
  }

  resetStats() {
    this.stats = {
      peakMemory: this.totalMemoryUsed,
      peakCpu: this.totalCpuUsed,
      peakTasks: this.totalTasks,
      totalAllocated: this.stats.totalAllocated,
      totalReleased: this.stats.totalReleased
    };
  }

  checkLimits() {
    const stats = this.getStats();
    const violations = [];

    if (stats.agents.utilization > 0.9) {
      violations.push({
        type: 'agents',
        message: 'Agent limit approaching',
        utilization: stats.agents.utilization
      });
    }

    if (stats.memory.utilization > 0.9) {
      violations.push({
        type: 'memory',
        message: 'Memory limit approaching',
        utilization: stats.memory.utilization
      });
    }

    if (stats.cpu.utilization > 0.9) {
      violations.push({
        type: 'cpu',
        message: 'CPU limit approaching',
        utilization: stats.cpu.utilization
      });
    }

    if (violations.length > 0) {
      this.emit('limits:approaching', violations);
    }

    return violations;
  }
}

module.exports = { ResourceManager };