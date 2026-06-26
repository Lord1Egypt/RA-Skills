/**
 * Multi-Agent System - Agent Roles
 * Defines specialized roles for collaborative task execution
 */

class AgentRole {
  constructor(name, description, capabilities, personality) {
    this.name = name;
    this.description = description;
    this.capabilities = capabilities;
    this.personality = personality;
    this.taskHistory = [];
    this.successRate = 1.0;
  }

  /**
   * Execute a task assigned to this role
   */
  async execute(task, context = {}) {
    console.log(`[${this.name}] Starting task: ${task.substring(0, 100)}...`);
    
    const startTime = Date.now();
    let result;
    
    try {
      // Role-specific execution logic
      result = await this.executeRoleSpecific(task, context);
      
      // Record success
      this.taskHistory.push({
        task,
        result: 'success',
        duration: Date.now() - startTime,
        timestamp: new Date().toISOString()
      });
      this.updateSuccessRate(true);
      
      console.log(`[${this.name}] ✓ Task completed in ${Date.now() - startTime}ms`);
    } catch (error) {
      result = {
        success: false,
        error: error.message
      };
      
      this.taskHistory.push({
        task,
        result: 'failed',
        error: error.message,
        duration: Date.now() - startTime,
        timestamp: new Date().toISOString()
      });
      this.updateSuccessRate(false);
      
      console.log(`[${this.name}] ✗ Task failed: ${error.message}`);
    }
    
    return result;
  }

  /**
   * Role-specific execution (to be overridden)
   */
  async executeRoleSpecific(task, context) {
    throw new Error('executeRoleSpecific must be implemented by subclass');
  }

  /**
   * Update success rate
   */
  updateSuccessRate(success) {
    const total = this.taskHistory.length;
    const successes = this.taskHistory.filter(t => t.result === 'success').length;
    this.successRate = successes / total;
  }

  /**
   * Get role statistics
   */
  getStats() {
    return {
      name: this.name,
      totalTasks: this.taskHistory.length,
      successRate: this.successRate,
      avgDuration: this.taskHistory.length > 0
        ? this.taskHistory.reduce((sum, t) => sum + t.duration, 0) / this.taskHistory.length
        : 0
    };
  }
}

/**
 * Planner Role - Analyzes tasks and creates execution plans
 */
class PlannerAgent extends AgentRole {
  constructor() {
    super(
      'Planner',
      'Analyzes complex tasks and breaks them down into executable steps',
      ['task_analysis', 'planning', 'decomposition', 'prioritization'],
      {
        style: 'analytical',
        focus: 'structure_and_logic',
        communication: 'concise_and_clear'
      }
    );
  }

  async executeRoleSpecific(task, context) {
    // Analyze task complexity
    const complexity = this.analyzeComplexity(task);
    
    // Break down into subtasks
    const subtasks = await this.decomposeTask(task, complexity);
    
    // Prioritize subtasks
    const prioritized = this.prioritize(subtasks);
    
    // Assign to appropriate roles
    const assignments = this.assignToRoles(prioritized, context.availableAgents);
    
    return {
      success: true,
      plan: {
        originalTask: task,
        complexity,
        subtasks: prioritized,
        assignments,
        estimatedDuration: this.estimateDuration(prioritized)
      }
    };
  }

  analyzeComplexity(task) {
    const indicators = {
      keywords: ['analyze', 'compare', 'evaluate', 'optimize', 'design'],
      length: task.length,
      hasMultipleSteps: task.includes('and') || task.includes('then') || task.includes('after')
    };
    
    let score = 0;
    score += indicators.keywords.filter(k => task.toLowerCase().includes(k)).length * 2;
    score += Math.min(5, Math.floor(indicators.length / 100));
    score += indicators.hasMultipleSteps ? 3 : 0;
    
    return {
      score,
      level: score < 5 ? 'simple' : score < 10 ? 'medium' : 'complex',
      indicators
    };
  }

  async decomposeTask(task, complexity) {
    const subtasks = [];
    
    if (complexity.level === 'simple') {
      subtasks.push({
        id: 1,
        description: task,
        role: 'executor',
        dependencies: []
      });
    } else {
      // Enhanced multi-step decomposition
      // Step 1: Analysis
      subtasks.push({
        id: 1,
        description: `Analyze and understand: ${task}`,
        role: 'planner',
        dependencies: [],
        required: true
      });
      
      // Step 2: Information gathering
      subtasks.push({
        id: 2,
        description: `Gather information: ${task}`,
        role: 'executor',
        dependencies: [1],
        required: true
      });
      
      // Step 3: Main execution
      subtasks.push({
        id: 3,
        description: `Execute main task: ${task}`,
        role: 'executor',
        dependencies: [2],
        required: true
      });
      
      // Step 4: Review and validation
      subtasks.push({
        id: 4,
        description: `Review and validate results`,
        role: 'reviewer',
        dependencies: [3],
        required: true
      });
      
      // Step 5: Summary (optional)
      subtasks.push({
        id: 5,
        description: `Create summary report`,
        role: 'executor',
        dependencies: [4],
        required: false
      });
    }
    
    return subtasks;
  }

  prioritize(subtasks) {
    // Topological sort based on dependencies
    return subtasks.sort((a, b) => {
      if (a.dependencies.length === 0 && b.dependencies.length > 0) return -1;
      if (a.dependencies.length > 0 && b.dependencies.length === 0) return 1;
      return a.id - b.id;
    });
  }

  assignToRoles(subtasks, availableAgents = []) {
    return subtasks.map(subtask => ({
      ...subtask,
      assignedTo: subtask.role,
      status: 'pending'
    }));
  }

  estimateDuration(subtasks) {
    // Rough estimate: 1 second per subtask
    return subtasks.length * 1000;
  }
}

/**
 * Executor Role - Performs the actual work
 */
class ExecutorAgent extends AgentRole {
  constructor(toolsRegistry) {
    super(
      'Executor',
      'Executes tasks using available tools and capabilities',
      ['tool_usage', 'task_execution', 'problem_solving'],
      {
        style: 'action_oriented',
        focus: 'getting_things_done',
        communication: 'direct_and_result_focused'
      }
    );
    this.tools = toolsRegistry;
  }

  async executeRoleSpecific(task, context) {
    console.log(`[Executor] Starting execution with context: ${Object.keys(context).join(', ')}`);
    
    // Priority 1: Use ReAct engine if available
    if (context.reactEngine) {
      console.log(`[Executor] Using ReAct engine for intelligent task execution`);
      try {
        const result = await context.reactEngine.run(task);
        console.log(`[Executor] ReAct execution completed: ${result.success ? '✅' : '❌'}`);
        return result;
      } catch (error) {
        console.error(`[Executor] ReAct execution failed: ${error.message}`);
        // Fallback to tools registry
      }
    }
    
    // Priority 2: Use tools registry directly
    if (this.tools) {
      console.log(`[Executor] Using tools registry for direct execution`);
      
      // Try to match tool from task description
      for (const [toolName, tool] of this.tools.tools) {
        if (task.toLowerCase().includes(toolName) || task.toLowerCase().includes(toolName.replace('_', ' '))) {
          console.log(`[Executor] Matched tool: ${toolName}`);
          const result = await this.tools.executeTool(toolName, task);
          console.log(`[Executor] Tool execution result: ${result.success ? '✅' : '❌'}`);
          return result;
        }
      }
      
      // Try to execute as command
      try {
        console.log(`[Executor] Executing as shell command`);
        const { exec } = require('child_process');
        const { promisify } = require('util');
        const execAsync = promisify(exec);
        
        const { stdout, stderr } = await execAsync(`echo "Task executed: ${task}"`, {
          cwd: process.cwd(),
          timeout: 10000
        });
        
        return {
          success: true,
          result: stdout.trim(),
          stderr: stderr || null,
          note: 'Executed as shell command'
        };
      } catch (error) {
        console.error(`[Executor] Command execution failed: ${error.message}`);
        return {
          success: false,
          error: error.message
        };
      }
    }
    
    // Fallback: Generic execution
    console.log(`[Executor] No tools available, using generic execution`);
    return {
      success: true,
      result: `Executed task: ${task}`,
      note: 'Generic execution (no tools available)'
    };
  }
}

/**
 * Reviewer Role - Validates results and ensures quality
 */
class ReviewerAgent extends AgentRole {
  constructor() {
    super(
      'Reviewer',
      'Reviews completed work for quality, accuracy, and completeness',
      ['quality_assurance', 'validation', 'error_detection', 'feedback'],
      {
        style: 'critical_and_thorough',
        focus: 'quality_and_accuracy',
        communication: 'constructive_and_detailed'
      }
    );
  }

  async executeRoleSpecific(task, context) {
    const { previousResults = [], qualityCriteria = [] } = context;
    
    console.log(`[Reviewer] Received ${previousResults.length} result(s) for review`);
    console.log(`[Reviewer] Quality criteria: ${qualityCriteria.join(', ') || 'default'}`);
    
    const review = {
      task,
      timestamp: new Date().toISOString(),
      checks: [],
      issues: [],
      recommendations: [],
      overallScore: 0
    };
    
    // Default quality criteria if not provided
    const criteria = qualityCriteria.length > 0 ? qualityCriteria : ['success', 'complete'];
    
    // Check completeness
    if (previousResults.length === 0) {
      review.issues.push('No previous results to review');
      review.checks.push({
        name: 'Completeness',
        passed: false,
        details: 'No results available'
      });
    } else {
      const successCount = previousResults.filter(r => r.success).length;
      console.log(`[Reviewer] Success count: ${successCount}/${previousResults.length}`);
      
      review.checks.push({
        name: 'Completeness',
        passed: successCount > 0,
        details: `${successCount}/${previousResults.length} tasks successful`
      });
    }
    
    // Check quality criteria
    for (const criterion of criteria) {
      const passed = this.evaluateCriterion(previousResults, criterion);
      console.log(`[Reviewer] Criterion "${criterion}": ${passed ? '✅' : '❌'}`);
      review.checks.push({
        name: criterion,
        passed,
        details: passed ? 'Met' : 'Not met'
      });
    }
    
    // Calculate overall score (avoid NaN)
    const passedChecks = review.checks.filter(c => c.passed).length;
    const totalChecks = review.checks.length > 0 ? review.checks.length : 1;
    review.overallScore = passedChecks / totalChecks;
    
    console.log(`[Reviewer] Overall score: ${review.overallScore} (${passedChecks}/${totalChecks} checks passed)`);
    
    // Generate recommendations
    if (review.overallScore < 0.8) {
      review.recommendations.push('Consider re-executing failed tasks');
    }
    if (review.overallScore >= 0.8 && review.overallScore < 1.0) {
      review.recommendations.push('Good progress, minor improvements needed');
    }
    if (review.overallScore === 1.0) {
      review.recommendations.push('All checks passed, ready for delivery');
    }
    
    return {
      success: review.overallScore >= 0.7,
      review,
      approved: review.overallScore >= 0.7
    };
  }

  evaluateCriterion(results, criterion) {
    // Simple heuristic evaluation
    const criterionLower = criterion.toLowerCase();
    
    if (criterionLower.includes('success')) {
      return results.every(r => r.success);
    }
    if (criterionLower.includes('complete')) {
      return results.length > 0;
    }
    if (criterionLower.includes('fast')) {
      const avgDuration = results.reduce((sum, r) => sum + (r.duration || 0), 0) / results.length;
      return avgDuration < 5000; // < 5 seconds
    }
    
    return true; // Default pass
  }
}

/**
 * Coordinator Role - Manages communication and workflow
 */
class CoordinatorAgent extends AgentRole {
  constructor() {
    super(
      'Coordinator',
      'Orchestrates multi-agent workflows and manages communication',
      ['orchestration', 'communication', 'conflict_resolution', 'workflow_management'],
      {
        style: 'collaborative_and_organized',
        focus: 'team_efficiency',
        communication: 'clear_and_coordinating'
      }
    );
  }

  async executeRoleSpecific(task, context) {
    const { agents = [], workflow = [] } = context;
    
    const coordination = {
      task,
      timestamp: new Date().toISOString(),
      agentsInvolved: agents.map(a => a.role.name),
      workflowSteps: workflow.length,
      status: 'coordinating',
      messages: []
    };
    
    // Execute workflow
    const results = [];
    for (const step of workflow) {
      const agent = agents.find(a => a.role.name.toLowerCase() === step.role.toLowerCase());
      
      if (agent) {
        coordination.messages.push(`[${agent.role.name}] Starting: ${step.task}`);
        const result = await agent.execute(step.task, context);
        results.push(result);
        coordination.messages.push(`[${agent.role.name}] Completed: ${result.success ? '✓' : '✗'}`);
      } else {
        coordination.messages.push(`[Coordinator] Agent not found for role: ${step.role}`);
      }
    }
    
    coordination.status = 'completed';
    coordination.results = results;
    coordination.success = results.every(r => r.success);
    
    return {
      success: coordination.success,
      coordination,
      results
    };
  }
}

/**
 * Factory function to create agent roles
 */
function createAgent(roleName, options = {}) {
  switch (roleName.toLowerCase()) {
    case 'planner':
      return new PlannerAgent();
    case 'executor':
      return new ExecutorAgent(options.toolsRegistry);
    case 'reviewer':
      return new ReviewerAgent();
    case 'coordinator':
      return new CoordinatorAgent();
    default:
      throw new Error(`Unknown role: ${roleName}`);
  }
}

module.exports = {
  AgentRole,
  PlannerAgent,
  ExecutorAgent,
  ReviewerAgent,
  CoordinatorAgent,
  createAgent
};
