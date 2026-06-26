/**
 * Report Generator - Generate reliability reports
 */

class ReportGenerator {
  constructor(options = {}) {
    this.options = {
      format: options.format || 'markdown',
      includeCharts: options.includeCharts !== false,
      detailLevel: options.detailLevel || 'standard'
    };
  }

  generate(monitor) {
    const stats = monitor.getStats();
    
    if (this.options.format === 'markdown') {
      return this.generateMarkdown(stats);
    }
    
    return this.generateJSON(stats);
  }

  generateMarkdown(stats) {
    let report = `# Reliability Report\n\n`;
    
    report += `## Summary\n`;
    report += `- **Overall Success Rate**: ${(stats.successRate * 100).toFixed(2)}%\n`;
    report += `- **Total Executions**: ${stats.total}\n`;
    report += `- **Successful**: ${stats.successful}\n`;
    report += `- **Failed**: ${stats.failed}\n\n`;
    
    report += `## Error Rate by Step\n`;
    for (const [step, rate] of Object.entries(stats.byStep || {})) {
      report += `- ${step}: ${(rate * 100).toFixed(2)}%\n`;
    }
    
    return report;
  }

  generateJSON(stats) {
    return JSON.stringify(stats, null, 2);
  }
}

module.exports = ReportGenerator;
