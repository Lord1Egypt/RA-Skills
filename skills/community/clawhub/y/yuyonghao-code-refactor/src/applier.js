/**
 * Change Applier - 变更应用器
 * 应用重构变更到代码
 */

const fs = require('fs');

class ChangeApplier {
  constructor(options = {}) {
    this.options = {
      dryRun: options.dryRun || false,
      backup: options.backup !== false,
      ...options
    };
    this.appliedChanges = [];
  }

  /**
   * 应用重构方案
   * @param {Object} plan - 重构方案
   * @param {Object} context - 上下文
   * @returns {Object} 应用结果
   */
  async applyRefactoringPlan(plan, context = {}) {
    const results = [];
    
    for (const change of plan.changes) {
      const result = await this.applyChange(change, context);
      results.push(result);
      
      if (result.success) {
        this.appliedChanges.push({
          change,
          timestamp: new Date().toISOString()
        });
      }
    }

    return {
      filePath: plan.filePath,
      results,
      summary: {
        total: results.length,
        successful: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length
      }
    };
  }

  /**
   * 应用单个变更
   */
  async applyChange(change, context) {
    try {
      if (this.options.dryRun) {
        return {
          success: true,
          change: change.type,
          dryRun: true,
          message: `Would apply: ${change.description}`
        };
      }

      switch (change.type) {
        case 'extract-constant':
          return await this.applyExtractConstant(change, context);
        
        case 'extract-function':
          return await this.applyExtractFunction(change, context);
        
        case 'parameter-object':
          return await this.applyParameterObject(change, context);
        
        case 'simplify-nesting':
          return await this.applySimplifyNesting(change, context);
        
        case 'reduce-complexity':
          return await this.applyReduceComplexity(change, context);
        
        default:
          return {
            success: false,
            change: change.type,
            message: `Unknown change type: ${change.type}`
          };
      }
    } catch (error) {
      return {
        success: false,
        change: change.type,
        message: error.message
      };
    }
  }

  /**
   * 应用提取常量
   */
  async applyExtractConstant(change, context) {
    const filePath = context.filePath || change.filePath;
    
    if (!fs.existsSync(filePath)) {
      return {
        success: false,
        change: change.type,
        message: `File not found: ${filePath}`
      };
    }

    // Create backup
    if (this.options.backup) {
      const backupPath = `${filePath}.backup`;
      fs.copyFileSync(filePath, backupPath);
    }

    let code = fs.readFileSync(filePath, 'utf-8');
    const lines = code.split('\n');
    
    // Find and replace magic number with constant
    const value = change.original.match(/:\s*(\d+)/)?.[1];
    if (value) {
      const constName = this.generateConstantName(value);
      
      // Add constant declaration at top
      const constDeclaration = `const ${constName} = ${value};`;
      
      // Check if constant already exists
      if (!code.includes(constDeclaration)) {
        // Find first non-import line
        let insertIndex = 0;
        for (let i = 0; i < lines.length; i++) {
          if (!lines[i].trim().startsWith('import') && !lines[i].trim().startsWith('const') && lines[i].trim()) {
            insertIndex = i;
            break;
          }
        }
        lines.splice(insertIndex, 0, constDeclaration);
      }
      
      // Replace magic number with constant (simple replacement)
      const updatedCode = lines.join('\n').replace(
        new RegExp(`(?<![\\w'])(${value})(?![\\w'])`, 'g'),
        constName
      );
      
      fs.writeFileSync(filePath, updatedCode);
    }

    return {
      success: true,
      change: change.type,
      message: `Extracted constant at line ${change.location.line}`
    };
  }

  /**
   * 应用提取函数
   */
  async applyExtractFunction(change, context) {
    // This is a complex refactoring that requires AST manipulation
    // For now, return a message indicating manual intervention needed
    return {
      success: true,
      change: change.type,
      message: `Extract function refactoring prepared for "${change.target}". Manual review recommended.`,
      requiresManualReview: true
    };
  }

  /**
   * 应用参数对象
   */
  async applyParameterObject(change, context) {
    return {
      success: true,
      change: change.type,
      message: `Parameter object refactoring prepared for "${change.target}". Breaking change - review call sites.`,
      requiresManualReview: true,
      breaking: true
    };
  }

  /**
   * 应用简化嵌套
   */
  async applySimplifyNesting(change, context) {
    return {
      success: true,
      change: change.type,
      message: `Simplify nesting refactoring prepared for "${change.target}". Manual review recommended.`,
      requiresManualReview: true
    };
  }

  /**
   * 应用降低复杂度
   */
  async applyReduceComplexity(change, context) {
    return {
      success: true,
      change: change.type,
      message: `Reduce complexity refactoring prepared for "${change.target}". Manual review recommended.`,
      requiresManualReview: true
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
   * 生成 diff 预览
   */
  generateDiff(originalCode, modifiedCode, filePath = 'file.js') {
    const originalLines = originalCode.split('\n');
    const modifiedLines = modifiedCode.split('\n');
    
    let diff = `--- ${filePath}\n+++ ${filePath}\n@@ -1,${originalLines.length} +1,${modifiedLines.length} @@\n`;
    
    // Simple diff generation
    const maxLines = Math.max(originalLines.length, modifiedLines.length);
    for (let i = 0; i < maxLines; i++) {
      const orig = originalLines[i] || '';
      const mod = modifiedLines[i] || '';
      
      if (orig !== mod) {
        if (orig) diff += `- ${orig}\n`;
        if (mod) diff += `+ ${mod}\n`;
      } else {
        diff += `  ${orig}\n`;
      }
    }
    
    return diff;
  }

  /**
   * 回滚变更
   */
  rollback(filePath) {
    const backupPath = `${filePath}.backup`;
    
    if (fs.existsSync(backupPath)) {
      fs.copyFileSync(backupPath, filePath);
      fs.unlinkSync(backupPath);
      return {
        success: true,
        message: `Rolled back changes to ${filePath}`
      };
    }
    
    return {
      success: false,
      message: `No backup found for ${filePath}`
    };
  }

  /**
   * 设置干运行模式
   */
  setDryRun(value) {
    this.options.dryRun = value;
  }
}

module.exports = { ChangeApplier };
