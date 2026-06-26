/**
 * Refactoring Engine - 重构引擎
 * 生成重构建议
 */

class RefactoringEngine {
  constructor(options = {}) {
    this.options = options;
  }

  /**
   * 生成重构方案
   * @param {Object} analysis - 分析结果
   * @returns {Object} 重构方案
   */
  generateRefactoringPlan(analysis) {
    const changes = [];

    for (const issue of analysis.issues) {
      const change = this.generateChange(issue, analysis);
      if (change) {
        changes.push(change);
      }
    }

    return {
      filePath: analysis.filePath,
      changes,
      summary: {
        totalChanges: changes.length,
        breakingChanges: changes.filter(c => c.breaking).length,
        safeChanges: changes.filter(c => !c.breaking).length
      }
    };
  }

  /**
   * 为单个问题生成变更
   */
  generateChange(issue, analysis) {
    switch (issue.type) {
      case 'long-function':
        return this.generateExtractFunctionChange(issue, analysis);
      
      case 'too-many-parameters':
        return this.generateParameterObjectChange(issue, analysis);
      
      case 'deep-nesting':
        return this.generateSimplifyNestingChange(issue, analysis);
      
      case 'high-complexity':
        return this.generateReduceComplexityChange(issue, analysis);
      
      case 'magic-number':
        return this.generateExtractConstantChange(issue, analysis);
      
      default:
        return null;
    }
  }

  /**
   * 提取函数重构
   */
  generateExtractFunctionChange(issue, analysis) {
    const funcName = issue.message.match(/"([^"]+)"/)?.[1] || 'function';
    
    return {
      type: 'extract-function',
      description: `Extract parts of "${funcName}" into smaller functions`,
      breaking: false,
      location: issue.location,
      original: issue.message,
      suggestion: `Split ${funcName} into smaller, focused functions`,
      actions: [
        {
          type: 'extract',
          target: funcName,
          description: 'Extract cohesive code blocks into new functions'
        }
      ]
    };
  }

  /**
   * 参数对象重构
   */
  generateParameterObjectChange(issue, analysis) {
    const funcName = issue.message.match(/"([^"]+)"/)?.[1] || 'function';
    
    return {
      type: 'parameter-object',
      description: `Convert parameters of "${funcName}" to options object`,
      breaking: true,
      location: issue.location,
      original: issue.message,
      suggestion: `Replace multiple parameters with a single options object`,
      actions: [
        {
          type: 'replace',
          target: funcName,
          description: 'Convert to destructured parameter object'
        }
      ]
    };
  }

  /**
   * 简化嵌套重构
   */
  generateSimplifyNestingChange(issue, analysis) {
    const funcName = issue.message.match(/"([^"]+)"/)?.[1] || 'function';
    
    return {
      type: 'simplify-nesting',
      description: `Reduce nesting depth in "${funcName}"`,
      breaking: false,
      location: issue.location,
      original: issue.message,
      suggestion: 'Use early returns and extract nested logic',
      actions: [
        {
          type: 'refactor',
          target: funcName,
          description: 'Apply guard clauses and extract nested conditions'
        }
      ]
    };
  }

  /**
   * 降低复杂度重构
   */
  generateReduceComplexityChange(issue, analysis) {
    const funcName = issue.message.match(/"([^"]+)"/)?.[1] || 'function';
    
    return {
      type: 'reduce-complexity',
      description: `Simplify complex logic in "${funcName}"`,
      breaking: false,
      location: issue.location,
      original: issue.message,
      suggestion: 'Extract conditions into helper functions or use lookup tables',
      actions: [
        {
          type: 'refactor',
          target: funcName,
          description: 'Extract complex conditions into named functions'
        }
      ]
    };
  }

  /**
   * 提取常量重构
   */
  generateExtractConstantChange(issue, analysis) {
    const value = issue.message.match(/:\s*(\d+)/)?.[1] || 'VALUE';
    const constName = this.generateConstantName(value);
    
    return {
      type: 'extract-constant',
      description: `Extract magic number ${value} to constant`,
      breaking: false,
      location: issue.location,
      original: issue.message,
      suggestion: `Define const ${constName} = ${value};`,
      actions: [
        {
          type: 'add',
          target: 'constants',
          description: `Add constant declaration: const ${constName} = ${value};`
        },
        {
          type: 'replace',
          target: issue.location,
          description: `Replace ${value} with ${constName}`
        }
      ]
    };
  }

  /**
   * 生成常量名称
   */
  generateConstantName(value) {
    const num = parseInt(value);
    if (num === 60) return 'SECONDS_PER_MINUTE';
    if (num === 60 * 60) return 'SECONDS_PER_HOUR';
    if (num === 24 * 60 * 60) return 'SECONDS_PER_DAY';
    if (num === 1024) return 'KB';
    if (num === 1024 * 1024) return 'MB';
    if (num === 1000) return 'MS_PER_SECOND';
    if (num === 1000 * 60) return 'MS_PER_MINUTE';
    if (num === 1000 * 60 * 60) return 'MS_PER_HOUR';
    return `CONSTANT_${value}`;
  }

  /**
   * 导出重构方案
   */
  exportPlan(plan, format = 'json') {
    if (format === 'json') {
      return JSON.stringify(plan, null, 2);
    }
    
    if (format === 'markdown') {
      let md = `# Refactoring Plan for ${plan.filePath}\n\n`;
      md += `## Summary\n`;
      md += `- Total Changes: ${plan.summary.totalChanges}\n`;
      md += `- Breaking Changes: ${plan.summary.breakingChanges}\n`;
      md += `- Safe Changes: ${plan.summary.safeChanges}\n\n`;
      
      md += `## Changes\n\n`;
      for (const change of plan.changes) {
        md += `### ${change.description}\n`;
        md += `- **Type**: ${change.type}\n`;
        md += `- **Breaking**: ${change.breaking ? 'Yes' : 'No'}\n`;
        md += `- **Location**: Line ${change.location.line}\n`;
        md += `- **Suggestion**: ${change.suggestion}\n\n`;
      }
      
      return md;
    }
    
    return JSON.stringify(plan);
  }
}

module.exports = { RefactoringEngine };
