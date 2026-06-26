/**
 * Agent Orchestrator - Main Entry Point
 * Production-grade Agent orchestration system
 */

const { AgentOrchestrator } = require('./orchestrator');
const { Scheduler } = require('./scheduler');
const { AgentRegistry } = require('./registry');
const { ResourceManager } = require('./resource-manager');
const { HealthChecker } = require('./health-checker');
const { LoadBalancer } = require('./load-balancer');

module.exports = {
  AgentOrchestrator,
  Scheduler,
  AgentRegistry,
  ResourceManager,
  HealthChecker,
  LoadBalancer
};

// If run directly, create a demo instance
if (require.main === module) {
  const orchestrator = new AgentOrchestrator({
    cluster: { enabled: true, nodeId: 'demo-node' },
    scheduler: { strategy: 'round-robin' },
    resources: { maxAgents: 10, maxTasksPerAgent: 5 }
  });

  console.log('Agent Orchestrator Demo Started');
  console.log('Status:', orchestrator.getClusterStatus());
}
