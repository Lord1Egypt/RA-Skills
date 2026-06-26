/**
 * AgentOrchestrator - Core orchestration engine
 * Manages agents, tasks, and cluster coordination
 */

const EventEmitter = require('events');
const { Scheduler } = require('./scheduler');
const { AgentRegistry } = require('./registry');
const { ResourceManager } = require('./resource-manager');
const { HealthChecker } = require('./health-checker');
const { LoadBalancer } = require('./load-balancer');

class AgentOrchestrator extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.options = {
      cluster: {
        enabled: false,
        nodeId: `node-${Date.now()}`,
        heartbeatInterval: 5000,
        electionTimeout: 10000,
        ...options.cluster
      },
      scheduler: {
        strategy: 'round-robin',
        maxQueueSize: 1000,
        defaultPriority: 'normal',
        ...options.scheduler
      },
      resources: {
        maxAgents: 100,
        maxTasksPerAgent: 10,
        maxMemoryMB: 1024,
        maxCpuPercent: 80,
        ...options.resources
      },
      healthCheck: {
        enabled: true,
        interval: 5000,
        timeout: 3000,
        failureThreshold: 3,
        ...options.healthCheck
      }
    };

    this.isRunning = false;
    this.isLeader = false;
    this.clusterNodes = new Map();
    this.configVersion = 0;
    
    // Initialize components
    this.registry = new AgentRegistry(this.options.resources);
    this.resourceManager = new ResourceManager(this.options.resources);
    this.healthChecker = new HealthChecker(this.options.healthCheck);
    this.loadBalancer = new LoadBalancer(this.options.scheduler.strategy);
    this.scheduler = new Scheduler({
      ...this.options.scheduler,
      registry: this.registry,
      loadBalancer: this.loadBalancer
    });

    this._setupEventHandlers();
    this._setupClusterManagement();
  }

  _setupEventHandlers() {
    // Agent events
    this.registry.on('agent:registered', (agent) => {
      this.emit('agent:registered', agent);
      this.loadBalancer.addAgent(agent);
      this.healthChecker.registerAgent(agent);
      this._broadcastEvent('agent:added', agent);
    });

    this.registry.on('agent:unregistered', (agentId) => {
      this.emit('agent:unregistered', agentId);
      this.loadBalancer.removeAgent(agentId);
      this.healthChecker.unregisterAgent(agentId);
      this._broadcastEvent('agent:removed', { agentId });
    });

    // Health check events
    this.healthChecker.on('agent:healthy', (agentId) => {
      this.emit('agent:healthy', agentId);
      this.registry.updateAgentStatus(agentId, 'healthy');
      this.loadBalancer.markHealthy(agentId);
    });

    this.healthChecker.on('agent:unhealthy', (agentId, reason) => {
      this.emit('agent:unhealthy', agentId, reason);
      this.registry.updateAgentStatus(agentId, 'unhealthy');
      this.loadBalancer.markUnhealthy(agentId);
      this._handleAgentFailure(agentId, reason);
    });

    // Task events
    this.scheduler.on('task:assigned', (task, agentId) => {
      this.emit('task:assigned', task, agentId);
      this.resourceManager.trackTask(agentId, task.id);
    });

    this.scheduler.on('task:completed', (task, result) => {
      this.emit('task:completed', task, result);
      if (task.assignedTo) {
        this.resourceManager.releaseTask(task.assignedTo, task.id);
      }
    });

    this.scheduler.on('task:failed', (task, error) => {
      this.emit('task:failed', task, error);
      if (task.assignedTo) {
        this.resourceManager.releaseTask(task.assignedTo, task.id);
      }
      this._handleTaskFailure(task, error);
    });

    this.scheduler.on('task:timeout', (task) => {
      this.emit('task:timeout', task);
      this._handleTaskTimeout(task);
    });
  }

  _setupClusterManagement() {
    if (!this.options.cluster.enabled) return;

    // Leader election
    this._startLeaderElection();
    
    // Heartbeat for cluster nodes
    this.clusterHeartbeatInterval = setInterval(() => {
      this._sendClusterHeartbeat();
    }, this.options.cluster.heartbeatInterval);

    // Cleanup dead nodes
    this.clusterCleanupInterval = setInterval(() => {
      this._cleanupDeadNodes();
    }, this.options.cluster.heartbeatInterval * 3);
  }

  async start() {
    if (this.isRunning) {
      throw new Error('Orchestrator is already running');
    }

    this.isRunning = true;
    
    await this.scheduler.start();
    await this.healthChecker.start();
    
    this.emit('orchestrator:started', { nodeId: this.options.cluster.nodeId });
    console.log(`[Orchestrator] Started on node ${this.options.cluster.nodeId}`);
    
    return this;
  }

  async stop(graceful = true) {
    if (!this.isRunning) {
      return;
    }

    this.emit('orchestrator:stopping', { graceful });
    
    if (graceful) {
      // Wait for running tasks to complete
      await this.scheduler.waitForRunningTasks(30000);
    }

    this.isRunning = false;
    
    // Stop components
    await this.scheduler.stop();
    await this.healthChecker.stop();
    
    // Clear intervals
    if (this.clusterHeartbeatInterval) {
      clearInterval(this.clusterHeartbeatInterval);
    }
    if (this.clusterCleanupInterval) {
      clearInterval(this.clusterCleanupInterval);
    }
    if (this.leaderElectionTimeout) {
      clearTimeout(this.leaderElectionTimeout);
    }

    this.emit('orchestrator:stopped');
    console.log('[Orchestrator] Stopped');
  }

  // Agent Management
  registerAgent(agentConfig) {
    if (!this.isRunning) {
      throw new Error('Orchestrator is not running');
    }

    // Check resource limits
    if (!this.resourceManager.canAddAgent()) {
      throw new Error('Maximum number of agents reached');
    }

    const agent = this.registry.register(agentConfig);
    this.resourceManager.allocateAgent(agent.id, agent.resources);
    
    console.log(`[Orchestrator] Agent registered: ${agent.id}`);
    return agent;
  }

  unregisterAgent(agentId) {
    const agent = this.registry.get(agentId);
    if (!agent) {
      throw new Error(`Agent not found: ${agentId}`);
    }

    // Cancel running tasks
    const runningTasks = this.scheduler.getRunningTasksForAgent(agentId);
    for (const task of runningTasks) {
      this.scheduler.cancelTask(task.id);
    }

    this.resourceManager.releaseAgent(agentId);
    this.registry.unregister(agentId);
    
    console.log(`[Orchestrator] Agent unregistered: ${agentId}`);
  }

  getAgent(agentId) {
    return this.registry.get(agentId);
  }

  getAllAgents() {
    return this.registry.getAll();
  }

  getAgentsByCapability(capability) {
    return this.registry.getByCapability(capability);
  }

  // Task Management
  async submitTask(taskConfig) {
    if (!this.isRunning) {
      throw new Error('Orchestrator is not running');
    }

    const task = this.scheduler.submit(taskConfig);
    console.log(`[Orchestrator] Task submitted: ${task.id}`);
    return task;
  }

  async submitTaskAndWait(taskConfig, timeout = 60000) {
    const task = await this.submitTask(taskConfig);
    
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error(`Task ${task.id} timed out after ${timeout}ms`));
      }, timeout);

      this.once(`task:completed:${task.id}`, (result) => {
        clearTimeout(timeoutId);
        resolve(result);
      });

      this.once(`task:failed:${task.id}`, (error) => {
        clearTimeout(timeoutId);
        reject(error);
      });
    });
  }

  cancelTask(taskId) {
    return this.scheduler.cancelTask(taskId);
  }

  getTask(taskId) {
    return this.scheduler.getTask(taskId);
  }

  getTaskQueue() {
    return this.scheduler.getQueue();
  }

  // Cluster Management
  joinCluster(nodeInfo) {
    if (!this.options.cluster.enabled) {
      throw new Error('Cluster mode is not enabled');
    }

    const node = {
      id: nodeInfo.id,
      address: nodeInfo.address,
      port: nodeInfo.port,
      lastHeartbeat: Date.now(),
      status: 'active',
      agents: nodeInfo.agents || [],
      load: nodeInfo.load || 0
    };

    this.clusterNodes.set(nodeInfo.id, node);
    this.emit('cluster:node:joined', node);
    
    console.log(`[Orchestrator] Node joined cluster: ${nodeInfo.id}`);
    return node;
  }

  leaveCluster(nodeId) {
    const node = this.clusterNodes.get(nodeId);
    if (node) {
      this.clusterNodes.delete(nodeId);
      this.emit('cluster:node:left', node);
      console.log(`[Orchestrator] Node left cluster: ${nodeId}`);
    }
  }

  getClusterNodes() {
    return Array.from(this.clusterNodes.values());
  }

  getClusterStatus() {
    const agents = this.getAllAgents();
    const tasks = this.scheduler.getAllTasks();
    
    return {
      nodeId: this.options.cluster.nodeId,
      isRunning: this.isRunning,
      isLeader: this.isLeader,
      clusterEnabled: this.options.cluster.enabled,
      clusterSize: this.clusterNodes.size + 1, // +1 for this node
      agents: {
        total: agents.length,
        healthy: agents.filter(a => a.status === 'healthy').length,
        unhealthy: agents.filter(a => a.status === 'unhealthy').length,
        idle: agents.filter(a => a.status === 'idle').length
      },
      tasks: {
        pending: tasks.filter(t => t.status === 'pending').length,
        running: tasks.filter(t => t.status === 'running').length,
        completed: tasks.filter(t => t.status === 'completed').length,
        failed: tasks.filter(t => t.status === 'failed').length
      },
      resources: this.resourceManager.getStats(),
      configVersion: this.configVersion
    };
  }

  updateConfig(newConfig) {
    this.configVersion++;
    Object.assign(this.options, newConfig);
    this.emit('config:updated', this.options);
    this._broadcastEvent('config:changed', { version: this.configVersion });
  }

  // Private methods
  _startLeaderElection() {
    // Simple leader election - first node becomes leader
    // In production, use a proper consensus algorithm like Raft
    this.leaderElectionTimeout = setTimeout(() => {
      if (this.clusterNodes.size === 0) {
        this.isLeader = true;
        this.emit('cluster:leader:elected', { nodeId: this.options.cluster.nodeId });
        console.log(`[Orchestrator] Elected as leader: ${this.options.cluster.nodeId}`);
      }
    }, this.options.cluster.electionTimeout);
  }

  _sendClusterHeartbeat() {
    if (!this.isLeader) return;

    const heartbeat = {
      nodeId: this.options.cluster.nodeId,
      timestamp: Date.now(),
      agents: this.getAllAgents().map(a => ({ id: a.id, status: a.status })),
      load: this.resourceManager.getLoad()
    };

    this.emit('cluster:heartbeat', heartbeat);
  }

  _cleanupDeadNodes() {
    const now = Date.now();
    const timeout = this.options.cluster.heartbeatInterval * 3;

    for (const [nodeId, node] of this.clusterNodes) {
      if (now - node.lastHeartbeat > timeout) {
        console.log(`[Orchestrator] Removing dead node: ${nodeId}`);
        this.leaveCluster(nodeId);
      }
    }
  }

  _broadcastEvent(event, data) {
    if (!this.options.cluster.enabled) return;
    this.emit(`cluster:${event}`, data);
  }

  _handleAgentFailure(agentId, reason) {
    console.log(`[Orchestrator] Handling agent failure: ${agentId}, reason: ${reason}`);
    
    // Get tasks assigned to this agent
    const tasks = this.scheduler.getRunningTasksForAgent(agentId);
    
    for (const task of tasks) {
      // Retry task if possible
      if (task.retries < task.maxRetries) {
        this.scheduler.retryTask(task.id);
      } else {
        this.scheduler.failTask(task.id, new Error(`Agent ${agentId} failed: ${reason}`));
      }
    }

    // Mark agent for recovery
    this.emit('agent:recovery:needed', { agentId, reason });
  }

  _handleTaskFailure(task, error) {
    console.log(`[Orchestrator] Task failed: ${task.id}, error: ${error.message}`);
    
    // Retry if possible
    if (task.retries < task.maxRetries) {
      setTimeout(() => {
        this.scheduler.retryTask(task.id);
      }, 1000 * Math.pow(2, task.retries)); // Exponential backoff
    }
  }

  _handleTaskTimeout(task) {
    console.log(`[Orchestrator] Task timed out: ${task.id}`);
    
    // Release resources
    if (task.assignedTo) {
      this.resourceManager.releaseTask(task.assignedTo, task.id);
    }

    // Retry if possible
    if (task.retries < task.maxRetries) {
      this.scheduler.retryTask(task.id);
    }
  }
}

module.exports = { AgentOrchestrator };