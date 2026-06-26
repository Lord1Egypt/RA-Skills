/**
 * Code Refactor - 代码重构助手
 * 主入口文件
 */

const { CodeAnalyzer } = require('./analyzer');
const { RefactoringEngine } = require('./refactorer');
const { ChangeApplier } = require('./applier');
const { TestValidator } = require('./validator');
const fs = require('fs');
const path = require('path');

class CodeRefactor {
  constructor(options = {}) {
    this.analyzer = new CodeAnalyzer(options.analyzer);
    this.refactorer = new RefactoringEngine(options.refactorer);
    this.applier = new ChangeApplier(options.applier);
    this.validator = new TestValidator(options.validator);
    this.options = options;
  }

  /**
   * 分析代码
   * @param {string} filePath - 文件路径
   * @returns {Object} 分析结果
   */
  analyze(filePath) {
    if (!fs.existsSync(filePath)) {
      throw new Error(`File not found: ${filePath}`);
    }
    return this.analyzer.analyze(filePath);
  }

  /**
   * 生成重构方案
   * @param {string} filePath - 文件路径
   * @returns {Object} 重构方案
   */
  generatePlan(filePath) {
    const analysis = this.analyze(filePath);
    return this.refactorer.generateRefactoringPlan(analysis);
  }

  /**
   * 重构代码（干运行）
   * @param {string} filePath - 文件路径
   * @param {Object} options - 选项
   * @returns {Object} 重构结果
   */
  async refactor(filePath, options = {}) {
    const dryRun = options.dryRun !== false;
    
    // 1. 分析
    const analysis = this.analyze(filePath);
    
    if (analysis.issues.length === 0) {
      return {
        filePath,
        status: 'no-issues',
        message: 'No refactoring issues found',
        analysis
      };
    }

    // 2. 生成方案
    const plan = this.refactorer.generateRefactoringPlan(analysis);

    // 3. 应用变更
    this.applier.setDryRun(dryRun);
    const application = await this.applier.applyRefactoringPlan(plan, {
      filePath,
      ...options.context
    });

    // 4. 验证（如果不是干运行）
    let validation = null;
    if (!dryRun) {
      validation = await this.validator.validate(filePath, options.context);
    }

    return {
      filePath,
      status: dryRun ? 'dry-run' : 'refactored',
      dryRun,
      analysis,
      plan,
      application,
      validation,
      canApply: application.summary.failed === 0
    };
  }

  /**
   * 应用重构变更
   * @param {Array} changes - 变更列表
   * @param {Object} context - 上下文
   * @returns {Object} 应用结果
   */
  async applyChanges(changes, context = {}) {
    const results = [];
    
    for (const change of changes) {
      const result = await this.applier.applyChange(change, context);
      results.push(result);
    }

    return {
      results,
      summary: {
        total: results.length,
        successful: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length
      }
    };
  }

  /**
   * 验证重构
   * @param {string} filePath - 文件路径
   * @param {Object} context - 上下文
   * @returns {Object} 验证结果
   */
  async validate(filePath, context = {}) {
    return await this.validator.validate(filePath, context);
  }

  /**
   * 完整重构流程
   * @param {string} filePath - 文件路径
   * @param {Object} options - 选项
   * @returns {Object} 重构结果
   */
  async fullRefactor(filePath, options = {}) {
    // 1. 干运行
    const dryRunResult = await this.refactor(filePath, { dryRun: true });
    
    if (dryRunResult.status === 'no-issues') {
      return dryRunResult;
    }

    // 2. 实际重构
    const refactorResult = await this.refactor(filePath, { dryRun: false });

    // 3. 如果验证失败，回滚
    if (refactorResult.validation && !refactorResult.validation.valid) {
      if (options.autoRollback !== false) {
        this.applier.rollback(filePath);
        return {
          ...refactorResult,
          status: 'rolled-back',
          message: 'Refactoring failed validation and was rolled back'
        };
      }
    }

    return refactorResult;
  }

  /**
   * 批量重构
   * @param {Array<string>} filePaths - 文件路径列表
   * @param {Object} options - 选项
   * @returns {Array<Object>} 重构结果列表
   */
  async refactorBatch(filePaths, options = {}) {
    const results = [];
    
    for (const filePath of filePaths) {
      try {
        const result = await this.refactor(filePath, options);
        results.push(result);
      } catch (error) {
        results.push({
          filePath,
          status: 'error',
          message: error.message
        });
      }
    }

    return results;
  }

  /**
   * 导出报告
   * @param {Object} result - 重构结果
   * @param {string} format - 格式
   * @returns {string} 报告内容
   */
  exportReport(result, format = 'markdown') {
    if (format === 'json') {
      return JSON.stringify(result, null, 2);
    }

    let report = `# Code Refactoring Report\n\n`;
    report += `**File**: ${result.filePath}\n`;
    report += `**Status**: ${result.status}\n`;
    report += `**Dry Run**: ${result.dryRun ? 'Yes' : 'No'}\n\n`;

    if (result.analysis) {
      report += `## Analysis Summary\n`;
      report += `- Total Lines: ${result.analysis.metrics.totalLines}\n`;
      report += `- Code Lines: ${result.analysis.metrics.codeLines}\n`;
      report += `- Functions: ${result.analysis.metrics.functions.length}\n`;
      report += `- Total Issues: ${result.analysis.summary.totalIssues}\n`;
      report += `  - Errors: ${result.analysis.summary.errors}\n`;
      report += `  - Warnings: ${result.analysis.summary.warnings}\n`;
      report += `  - Info: ${result.analysis.summary.info}\n\n`;

      if (result.analysis.issues.length > 0) {
        report += `## Issues Found\n\n`;
        for (const issue of result.analysis.issues) {
          report += `### ${issue.type}\n`;
          report += `- **Severity**: ${issue.severity}\n`;
          report += `- **Message**: ${issue.message}\n`;
          report += `- **Location**: Line ${issue.location.line}\n`;
          report += `- **Suggestion**: ${issue.suggestion}\n\n`;
        }
      }
    }

    if (result.plan) {
      report += `## Refactoring Plan\n`;
      report += `- Total Changes: ${result.plan.summary.totalChanges}\n`;
      report += `- Breaking Changes: ${result.plan.summary.breakingChanges}\n`;
      report += `- Safe Changes: ${result.plan.summary.safeChanges}\n\n`;
    }

    if (result.application) {
      report += `## Application Results\n`;
      report += `- Total: ${result.application.summary.total}\n`;
      report += `- Successful: ${result.application.summary.successful}\n`;
      report += `- Failed: ${result.application.summary.failed}\n\n`;
    }

    if (result.validation) {
      report += `## Validation Results\n`;
      report += `- Valid: ${result.validation.valid ? 'Yes' : 'No'}\n`;
      report += `- Tests Passed: ${result.validation.testsPassed ? 'Yes' : 'No'}\n`;
      if (result.validation.coverage) {
        report += `- Coverage: ${result.validation.coverage.lines}%\n`;
      }
      report += `\n`;
    }

    return report;
  }
}

// CLI support
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const filePath = args[1];

  const refactor = new CodeRefactor();

  if (command === 'analyze' && filePath) {
    const analysis = refactor.analyze(filePath);
    console.log(JSON.stringify(analysis, null, 2));
  } else if (command === 'refactor' && filePath) {
    const dryRun = !args.includes('--apply');
    refactor.refactor(filePath, { dryRun }).then(result => {
      console.log(refactor.exportReport(result, 'markdown'));
    });
  } else {
    console.log(`
Usage:
  node index.js analyze <file>     Analyze code for issues
  node index.js refactor <file>    Preview refactoring (dry-run)
  node index.js refactor <file> --apply    Apply refactoring
    `);
  }
}

module.exports = {
  CodeRefactor,
  CodeAnalyzer,
  RefactoringEngine,
  ChangeApplier,
  TestValidator
};