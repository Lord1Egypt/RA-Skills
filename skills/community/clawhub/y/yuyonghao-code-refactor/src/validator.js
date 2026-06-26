/**
 * Test Validator - 测试验证器
 * 验证重构后代码的正确性
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class TestValidator {
  constructor(options = {}) {
    this.options = {
      testCommand: options.testCommand || 'npm test',
      coverageThreshold: options.coverageThreshold || 80,
      timeout: options.timeout || 60000,
      ...options
    };
  }

  /**
   * 验证重构
   * @param {string} filePath - 文件路径
   * @param {Object} context - 上下文
   * @returns {Object} 验证结果
   */
  async validate(filePath, context = {}) {
    const results = {
      filePath,
      testsPassed: false,
      coverage: null,
      errors: [],
      warnings: []
    };

    try {
      // 1. 语法检查
      const syntaxResult = await this.checkSyntax(filePath);
      if (!syntaxResult.valid) {
        results.errors.push({
          type: 'syntax-error',
          message: syntaxResult.message
        });
        return results;
      }

      // 2. 运行测试
      const testResult = await this.runTests(context);
      results.testsPassed = testResult.passed;
      if (!testResult.passed) {
        results.errors.push({
          type: 'test-failure',
          message: testResult.message,
          details: testResult.details
        });
      }

      // 3. 检查覆盖率
      if (testResult.coverage) {
        results.coverage = testResult.coverage;
        if (testResult.coverage.lines < this.options.coverageThreshold) {
          results.warnings.push({
            type: 'low-coverage',
            message: `Line coverage ${testResult.coverage.lines}% is below threshold ${this.options.coverageThreshold}%`
          });
        }
      }

      // 4. 静态分析
      const lintResult = await this.runLinting(filePath);
      if (lintResult.issues.length > 0) {
        results.warnings.push(...lintResult.issues.map(issue => ({
          type: 'lint-issue',
          message: issue.message,
          line: issue.line
        })));
      }

      results.valid = results.errors.length === 0;
      return results;

    } catch (error) {
      results.errors.push({
        type: 'validation-error',
        message: error.message
      });
      results.valid = false;
      return results;
    }
  }

  /**
   * 检查语法
   */
  async checkSyntax(filePath) {
    try {
      const code = fs.readFileSync(filePath, 'utf-8');
      
      // Try to parse as JavaScript
      new Function(code);
      
      return {
        valid: true,
        message: 'Syntax is valid'
      };
    } catch (error) {
      return {
        valid: false,
        message: `Syntax error: ${error.message}`
      };
    }
  }

  /**
   * 运行测试
   */
  async runTests(context = {}) {
    try {
      const cwd = context.cwd || process.cwd();
      
      // Check if package.json exists
      const packageJsonPath = path.join(cwd, 'package.json');
      if (!fs.existsSync(packageJsonPath)) {
        return {
          passed: true,
          message: 'No package.json found, skipping tests',
          coverage: null
        };
      }

      // Run tests
      const output = execSync(this.options.testCommand, {
        cwd,
        encoding: 'utf-8',
        timeout: this.options.timeout,
        stdio: ['pipe', 'pipe', 'pipe']
      });

      // Parse test results
      const passed = !output.includes('FAIL') && !output.includes('failed');
      
      // Try to extract coverage
      const coverageMatch = output.match(/Lines\s*:\s*(\d+\.?\d*)%/);
      const coverage = coverageMatch ? {
        lines: parseFloat(coverageMatch[1])
      } : null;

      return {
        passed,
        message: passed ? 'All tests passed' : 'Some tests failed',
        coverage,
        details: output
      };

    } catch (error) {
      return {
        passed: false,
        message: `Test execution failed: ${error.message}`,
        coverage: null,
        details: error.stderr || error.stdout || error.message
      };
    }
  }

  /**
   * 运行代码检查
   */
  async runLinting(filePath) {
    const issues = [];
    
    try {
      // Check for common issues
      const code = fs.readFileSync(filePath, 'utf-8');
      const lines = code.split('\n');

      // Check for console.log statements
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('console.log') && !lines[i].includes('//')) {
          issues.push({
            type: 'console-log',
            message: `console.log found at line ${i + 1}`,
            line: i + 1
          });
        }
      }

      // Check for TODO comments
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('TODO') || lines[i].includes('FIXME')) {
          issues.push({
            type: 'todo',
            message: `TODO/FIXME found at line ${i + 1}`,
            line: i + 1
          });
        }
      }

      return { issues };

    } catch (error) {
      return {
        issues: [{
          type: 'lint-error',
          message: `Linting failed: ${error.message}`,
          line: 0
        }]
      };
    }
  }

  /**
   * 生成验证报告
   */
  generateReport(results) {
    let report = `# Validation Report for ${results.filePath}\n\n`;
    
    report += `## Summary\n`;
    report += `- **Valid**: ${results.valid ? 'Yes' : 'No'}\n`;
    report += `- **Tests Passed**: ${results.testsPassed ? 'Yes' : 'No'}\n`;
    if (results.coverage) {
      report += `- **Coverage**: ${results.coverage.lines}%\n`;
    }
    report += `\n`;

    if (results.errors.length > 0) {
      report += `## Errors\n`;
      for (const error of results.errors) {
        report += `- **${error.type}**: ${error.message}\n`;
      }
      report += `\n`;
    }

    if (results.warnings.length > 0) {
      report += `## Warnings\n`;
      for (const warning of results.warnings) {
        report += `- **${warning.type}**: ${warning.message}\n`;
      }
      report += `\n`;
    }

    return report;
  }
}

module.exports = { TestValidator };
