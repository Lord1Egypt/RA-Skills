/**
 * Agent Reliability Framework
 * Main entry point
 */

const ReliabilityMonitor = require('./reliability-monitor');
const FallbackManager = require('./fallback-manager');
const ConfidenceCalculator = require('./confidence-calculator');
const VotingConsensus = require('./voting-consensus');
const ReportGenerator = require('./report-generator');

module.exports = {
  ReliabilityMonitor,
  FallbackManager,
  ConfidenceCalculator,
  VotingConsensus,
  ReportGenerator,
  
  // Convenience factory functions
  createMonitor(options) {
    return new ReliabilityMonitor(options);
  },
  
  createFallback(options) {
    return new FallbackManager(options);
  },
  
  createConsensus(options) {
    return new VotingConsensus(options);
  },
  
  createReportGenerator(options) {
    return new ReportGenerator(options);
  }
};
