/**
 * Scheduler - Task scheduling and queue management
 * Handles task assignment, prioritization, and execution
 */

const EventEmitter = require('events');
const { v4: uuidv4 } = require('./utils');

const PRIORITY_LEVELS = {
  'critical': 4,
  'high': 3,
  'normal': 2,
  'low': 1
};

class Scheduler extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.options = {
      strategy: 'round-robin',
      maxQueueSize: 1000,
      defaultPriority: 'normal',
      maxRetries: 3,
      retryDelay: 5000,
      taskTimeout: 60000,
      pollInterval: 100,
      ...options
    };

    this.registry = options.registry;
    this.loadBalancer = options.loadBalancer;
    
    this.taskQueue = []; // Priority queue
    this.runningTasks = new Map();
    this.completedTasks = new Map();
    this.taskHistory = []; // Limited history
    this.isRunning = false;
    this.pollTimer = null;
    this.taskTimers = new Map(); // Timeout timers
  }

  async start() {
    if (this.isRunning) return;
    
    this.isRunning = true;
    this._startPolling();
    this.emit('scheduler:started');
    console.log('[Scheduler] Started');
  }

  async stop() {
    this.isRunning = false;
    
    if (this.pollTimer) {
      clearTimeout(this.pollTimer);
      this.pollTimer = null;
    }

    // Clear all task timeouts
    for (const timer of this.taskTimers.values()) {
      clearTimeout(timer);
    }
    this.taskTimers.clear();

    this.emit('scheduler:stopped');
    console.log('[Scheduler] Stopped');
  }

  submit(config) {
    if (this.taskQueue.length >= this.options.maxQueueSize) {
      throw new Error('Task queue is full');
    }

    const task = {
      id: config.id || uuidv4(),
      type: config.type,
      priority: config.priority || this.options.defaultPriority,
      priorityLevel: PRIORITY_LEVELS[config.priority] || PRIORITY_LEVELS.normal,
      payload: config.payload || {},
      requirements: config.requirements || {},
      maxRetries: config.maxRetries || this.options.maxRetries,
      retries: 0,
      timeout: config.timeout || this.options.taskTimeout,
      status: 'pending',
      createdAt: Date.now(),
      startedAt: null,
      completedAt: null,
      assignedTo: null,
      result: null,
      error: null
    };

    // Insert into priority queue
    this._insertIntoQueue(task);
    
    this.emit('task:submitted', task);
    console.log(`[Scheduler] Task submitted: ${task.id} (priority: ${task.priority})`);
    
    return task;
  }

  _insertIntoQueue(task) {
    // Insert based on priority (higher priority first)
    let inserted = false;
    for (let i = 0; i < this.taskQueue.length; i++) {
      if (task.priorityLevel > this.taskQueue[i].priorityLevel) {
        this.taskQueue.splice(i, 0, task);
        inserted = true;
        break;
      }
    }
    if (!inserted) {
      this.taskQueue.push(task);
    }
  }

  cancelTask(taskId) {
    // Check pending queue
    const queueIndex = this.taskQueue.findIndex(t => t.id === taskId);
    if (queueIndex !== -1) {
      const task = this.taskQueue.splice(queueIndex, 1)[0];
      task.status = 'cancelled';
      task.completedAt = Date.now();
      this._addToHistory(task);
      this.emit('task:cancelled', task);
      return true;
    }

    // Check running tasks
    const runningTask = this.runningTasks.get(taskId);
    if (runningTask) {
      runningTask.status = 'cancelled';
      runningTask.completedAt = Date.now();
      
      // Clear timeout
      const timer = this.taskTimers.get(taskId);
      if (timer) {
        clearTimeout(timer);
        this.taskTimers.delete(taskId);
      }

      this.runningTasks.delete(taskId);
      this._addToHistory(runningTask);
      this.emit('task:cancelled', runningTask);
      
      // Notify agent
      this.emit('task:cancel', runningTask);
      return true;
    }

    return false;
  }

  getTask(taskId) {
    // Check queue
    const queued = this.taskQueue.find(t => t.id === taskId);
    if (queued) return queued;

    // Check running
    const running = this.runningTasks.get(taskId);
    if (running) return running;

    // Check completed
    return this.completedTasks.get(taskId);
  }

  getQueue() {
    return [...this.taskQueue];
  }

  getRunningTasks() {
    return Array.from(this.runningTasks.values());
  }

  getRunningTasksForAgent(agentId) {
    return this.getRunningTasks().filter(t => t.assignedTo === agentId);
  }

  getAllTasks() {
    return [
      ...this.taskQueue,
      ...this.runningTasks.values(),
      ...this.completedTasks.values()
    ];
  }

  getTaskHistory(limit = 100) {
    return this.taskHistory.slice(-limit);
  }

  retryTask(taskId) {
    const task = this.completedTasks.get(taskId);
    if (!task) return false;

    if (task.retries >= task.maxRetries) {
      return false;
    }

    // Reset task state
    task.status = 'pending';
    task.retries++;
    task.assignedTo = null;
    task.startedAt = null;
    task.completedAt = null;
    task.error = null;
    
    this.completedTasks.delete(taskId);
    this._insertIntoQueue(task);
    
    this.emit('task:retry', task);
    console.log(`[Scheduler] Task retry: ${task.id} (attempt ${task.retries})`);
    
    return true;
  }

  failTask(taskId, error) {
    const task = this.runningTasks.get(taskId) || this.taskQueue.find(t => t.id === taskId);
    if (!task) return false;

    task.status = 'failed';
    task.error = error.message || error;
    task.completedAt = Date.now();

    // Remove from running
    this.runningTasks.delete(taskId);
    
    // Clear timeout
    const timer = this.taskTimers.get(taskId);
    if (timer) {
      clearTimeout(timer);
      this.taskTimers.delete(taskId);
    }

    this._addToHistory(task);
    this.emit('task:failed', task, error);
    
    return true;
  }

  completeTask(taskId, result) {
    const task = this.runningTasks.get(taskId);
    if (!task) return false;

    task.status = 'completed';
    task.result = result;
    task.completedAt = Date.now();

    // Remove from running
    this.runningTasks.delete(taskId);
    
    // Clear timeout
    const timer = this.taskTimers.get(taskId);
    if (timer) {
      clearTimeout(timer);
      this.taskTimers.delete(taskId);
    }

    this.completedTasks.set(taskId, task);
    this._addToHistory(task);
    this.emit('task:completed', task, result);
    
    return true;
  }

  async waitForRunningTasks(timeout = 30000) {
    const startTime = Date.now();
    
    while (this.runningTasks.size > 0) {
      if (Date.now() - startTime > timeout) {
        throw new Error('Timeout waiting for running tasks');
      }
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  _startPolling() {
    if (!this.isRunning) return;

    this._processQueue();
    
    this.pollTimer = setTimeout(() => {
      this._startPolling();
    }, this.options.pollInterval);
  }

  _processQueue() {
    if (this.taskQueue.length === 0) return;
    if (!this.registry || !this.loadBalancer) return;

    // Get available agents
    const availableAgents = this.registry.getAvailableAgents();
    if (availableAgents.length === 0) return;

    // Process tasks
    const tasksToProcess = [];
    
    for (let i = this.taskQueue.length - 1; i >= 0; i--) {
      const task = this.taskQueue[i];
      
      // Find suitable agents
      let suitableAgents = availableAgents;
      
      if (task.requirements.capabilities) {
        suitableAgents = availableAgents.filter(agent => 
          task.requirements.capabilities.every(cap => 
            agent.capabilities.includes(cap)
          )
        );
      }

      if (suitableAgents.length === 0) continue;

      // Select agent using load balancer
      const selectedAgent = this.loadBalancer.select(suitableAgents);
      if (!selectedAgent) continue;

      // Assign task
      task.status = 'running';
      task.assignedTo = selectedAgent.id;
      task.startedAt = Date.now();
      
      // Remove from queue
      this.taskQueue.splice(i, 1);
      
      // Add to running
      this.runningTasks.set(task.id, task);
      
      // Set timeout
      this._setTaskTimeout(task);
      
      this.emit('task:assigned', task, selectedAgent.id);
      console.log(`[Scheduler] Task assigned: ${task.id} -> ${selectedAgent.id}`);
      
      // Update agent load
      selectedAgent.currentLoad++;
    }
  }

  _setTaskTimeout(task) {
    const timer = setTimeout(() => {
      if (this.runningTasks.has(task.id)) {
        const runningTask = this.runningTasks.get(task.id);
        runningTask.status = 'timeout';
        runningTask.completedAt = Date.now();
        
        this.runningTasks.delete(task.id);
        this.taskTimers.delete(task.id);
        this._addToHistory(runningTask);
        
        this.emit('task:timeout', runningTask);
        console.log(`[Scheduler] Task timed out: ${task.id}`);
      }
    }, task.timeout);
    
    this.taskTimers.set(task.id, timer);
  }

  _addToHistory(task) {
    this.taskHistory.push({
      id: task.id,
      type: task.type,
      status: task.status,
      priority: task.priority,
      assignedTo: task.assignedTo,
      createdAt: task.createdAt,
      startedAt: task.startedAt,
      completedAt: task.completedAt,
      duration: task.completedAt - task.startedAt,
      retries: task.retries
    });

    // Limit history size
    if (this.taskHistory.length > 1000) {
      this.taskHistory = this.taskHistory.slice(-500);
    }
  }

  getStats() {
    return {
      queueSize: this.taskQueue.length,
      runningCount: this.runningTasks.size,
      completedCount: this.completedTasks.size,
      historySize: this.taskHistory.length,
      byPriority: {
        critical: this.taskQueue.filter(t => t.priority === 'critical').length,
        high: this.taskQueue.filter(t => t.priority === 'high').length,
        normal: this.taskQueue.filter(t => t.priority === 'normal').length,
        low: this.taskQueue.filter(t => t.priority === 'low').length
      },
      byStatus: {
        pending: this.taskQueue.length,
        running: this.runningTasks.size,
        completed: this.completedTasks.size
      }
    };
  }
}

module.exports = { Scheduler, PRIORITY_LEVELS };