/**
 * Multi-Agent Orchestrator
 * Manages agent collaboration and task distribution
 */

const { createAgent } = require('./agent-roles');

class MultiAgentOrchestrator {
  constructor(options = {}) {
    this.verbose = options.verbose || false;
    this.agents = [];
    this.taskQueue = [];
    this.completedTasks = [];
    this.failedTasks = [];
    this.maxRetries = options.maxRetries || 3;
  }

  /**
   * Initialize agents with specified roles
   */
  initializeAgents(roles = ['planner', 'executor', 'reviewer'], options = {}) {
    this.agents = [];
    
    for (const role of roles) {
      try {
        const agent = createAgent(role, options);
        this.agents.push({
          id: `agent-${this.agents.length + 1}`,
          role: agent,
          status: 'idle',
          currentTask: null
        });
        
        if (this.verbose) {
          console.log(`[Orchestrator] Initialized ${role} agent`);
        }
      } catch (error) {
        console.error(`[Orchestrator] Failed to initialize ${role}: ${error.message}`);
      }
    }
    
    if (this.verbose) {
      console.log(`[Orchestrator] Initialized ${this.agents.length} agents`);
    }
    
    return this.agents;
  }

  /**
   * Execute a task using multi-agent collaboration
   */
  async executeTask(task, options = {}) {
    const {
      mode = 'collaborative', // 'collaborative', 'sequential', 'parallel'
      roles = ['planner', 'executor', 'reviewer'],
      timeout = 60000
    } = options;

    if (this.verbose) {
      console.log(`\n[Orchestrator] Starting task: ${task.substring(0, 100)}...`);
      console.log(`[Orchestrator] Mode: ${mode}`);
      console.log(`[Orchestrator] Roles: ${roles.join(', ')}`);
    }

    const startTime = Date.now();
    const context = {
      availableAgents: this.agents,
      startTime,
      timeout,
      ...options.context
    };

    try {
      let result;
      
      if (mode === 'collaborative') {
        result = await this.executeCollaborative(task, context);
      } else if (mode === 'sequential') {
        result = await this.executeSequential(task, roles, context);
      } else if (mode === 'parallel') {
        result = await this.executeParallel(task, roles, context);
      } else {
        throw new Error(`Unknown execution mode: ${mode}`);
      }

      const duration = Date.now() - startTime;
      result.duration = duration;
      result.mode = mode;

      if (result.success) {
        this.completedTasks.push({ task, result, duration });
      } else {
        this.failedTasks.push({ task, result, duration });
      }

      if (this.verbose) {
        console.log(`\n[Orchestrator] Task ${result.success ? 'completed' : 'failed'} in ${duration}ms`);
      }

      return result;
    } catch (error) {
      const duration = Date.now() - startTime;
      const result = {
        success: false,
        error: error.message,
        duration,
        mode
      };
      this.failedTasks.push({ task, result, duration });
      
      if (this.verbose) {
        console.error(`[Orchestrator] Task failed with error: ${error.message}`);
      }
      
      return result;
    }
  }

  /**
   * Collaborative execution: Plan → Execute → Review
   */
  async executeCollaborative(task, context) {
    const planner = this.agents.find(a => a.role.name === 'Planner');
    const executor = this.agents.find(a => a.role.name === 'Executor');
    const reviewer = this.agents.find(a => a.role.name === 'Reviewer');

    const results = {
      planning: null,
      execution: [],
      review: null,
      success: false
    };

    // Step 1: Planning
    if (planner) {
      if (this.verbose) console.log('\n[Phase 1] Planning...');
      planner.status = 'busy';
      results.planning = await planner.role.execute(task, context);
      planner.status = 'idle';
      
      if (!results.planning.success) {
        return { ...results, success: false, error: 'Planning failed' };
      }
    }

    // Step 2: Execution
    if (executor) {
      if (this.verbose) console.log('\n[Phase 2] Executing...');
      
      const plan = results.planning?.result?.plan;
      const tasksToExecute = plan?.assignments || [{ description: task, role: 'executor', required: true }];
      
      if (this.verbose) console.log(`[Executor] Will execute ${tasksToExecute.length} subtask(s)`);
      
      for (const subtask of tasksToExecute) {
        executor.status = 'busy';
        const execResult = await executor.role.execute(subtask.description, {
          ...context,
          previousResults: results.execution,
          qualityCriteria: context.qualityCriteria || ['success', 'complete']
        });
        executor.status = 'idle';
        
        results.execution.push({
          task: subtask.description,
          assignedRole: subtask.role,
          required: subtask.required !== false,
          ...execResult
        });
        
        if (!execResult.success && subtask.required !== false) {
          if (this.verbose) console.log(`[Executor] Critical task failed: ${subtask.description}`);
        }
      }
    }

    // Step 3: Review
    if (reviewer) {
      if (this.verbose) console.log('\n[Phase 3] Reviewing...');
      reviewer.status = 'busy';
      
      // Ensure we have execution results to review
      const resultsToReview = results.execution && results.execution.length > 0 ? results.execution : [];
      
      if (this.verbose) console.log(`[Reviewer] Reviewing ${resultsToReview.length} execution result(s)`);
      
      results.review = await reviewer.role.execute(task, {
        ...context,
        previousResults: resultsToReview,
        qualityCriteria: context.qualityCriteria || ['success', 'complete', 'fast']
      });
      reviewer.status = 'idle';
      
      results.success = results.review.approved !== false;
    } else {
      // No reviewer, check execution success
      const successfulExecutions = results.execution ? results.execution.filter(r => r.success).length : 0;
      const totalExecutions = results.execution ? results.execution.length : 0;
      results.success = totalExecutions > 0 && successfulExecutions === totalExecutions;
    }

    return results;
  }

  /**
   * Sequential execution: Execute tasks one by one
   */
  async executeSequential(task, roles, context) {
    const results = [];
    
    for (const roleName of roles) {
      const agent = this.agents.find(a => a.role.name.toLowerCase() === roleName.toLowerCase());
      
      if (!agent) {
        if (this.verbose) console.log(`[Orchestrator] Agent not found: ${roleName}`);
        continue;
      }
      
      if (this.verbose) console.log(`\n[Sequential] ${roleName} executing...`);
      
      agent.status = 'busy';
      const result = await agent.role.execute(task, {
        ...context,
        previousResults: results
      });
      agent.status = 'idle';
      
      results.push({
        role: roleName,
        ...result
      });
    }
    
    return {
      success: results.every(r => r.success),
      results,
      totalSteps: results.length
    };
  }

  /**
   * Parallel execution: Execute tasks concurrently
   */
  async executeParallel(task, roles, context) {
    const executionPromises = roles.map(async (roleName) => {
      const agent = this.agents.find(a => a.role.name.toLowerCase() === roleName.toLowerCase());
      
      if (!agent) {
        return { role: roleName, success: false, error: 'Agent not found' };
      }
      
      agent.status = 'busy';
      try {
        const result = await agent.role.execute(task, context);
        agent.status = 'idle';
        return { role: roleName, ...result };
      } catch (error) {
        agent.status = 'idle';
        return { role: roleName, success: false, error: error.message };
      }
    });
    
    const results = await Promise.all(executionPromises);
    
    return {
      success: results.some(r => r.success), // At least one succeeds
      results,
      parallel: true
    };
  }

  /**
   * Get orchestrator statistics
   */
  getStats() {
    const totalTasks = this.completedTasks.length + this.failedTasks.length;
    const successRate = totalTasks > 0 ? this.completedTasks.length / totalTasks : 0;
    
    const agentStats = this.agents.map(agent => ({
      id: agent.id,
      role: agent.role.name,
      status: agent.status,
      ...agent.role.getStats()
    }));
    
    return {
      totalAgents: this.agents.length,
      totalTasks,
      completedTasks: this.completedTasks.length,
      failedTasks: this.failedTasks.length,
      successRate,
      agents: agentStats
    };
  }

  /**
   * Reset orchestrator state
   */
  reset() {
    this.taskQueue = [];
    this.completedTasks = [];
    this.failedTasks = [];
    
    for (const agent of this.agents) {
      agent.status = 'idle';
      agent.currentTask = null;
    }
    
    if (this.verbose) {
      console.log('[Orchestrator] Reset complete');
    }
  }
}

module.exports = { MultiAgentOrchestrator };
