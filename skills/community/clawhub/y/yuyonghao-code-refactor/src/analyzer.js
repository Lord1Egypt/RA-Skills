/**
 * Code Analyzer - 代码分析器
 * 检测代码异味、计算复杂度指标
 */

const fs = require('fs');

class CodeAnalyzer {
  constructor(options = {}) {
    this.options = {
      maxFunctionLength: options.maxFunctionLength || 50,
      maxParameters: options.maxParameters || 4,
      maxNestingDepth: options.maxNestingDepth || 3,
      minDuplicateLines: options.minDuplicateLines || 5,
      complexityThreshold: options.complexityThreshold || 10,
      ...options
    };
  }

  analyze(filePath) {
    const code = fs.readFileSync(filePath, 'utf-8');
    const lines = code.split('\n');
    
    const issues = [];
    const metrics = {
      totalLines: lines.length,
      codeLines: lines.filter(l => l.trim() && !l.trim().startsWith('//')).length,
      commentLines: lines.filter(l => l.trim().startsWith('//')).length,
      functions: [],
      complexity: 0
    };

    const functionMatches = this.extractFunctions(code, lines);
    for (const func of functionMatches) {
      const funcMetrics = this.analyzeFunction(func, code);
      metrics.functions.push(funcMetrics);
      metrics.complexity += funcMetrics.cyclomaticComplexity;

      if (funcMetrics.lineCount > this.options.maxFunctionLength) {
        issues.push({
          type: 'long-function',
          severity: 'warning',
          message: `Function "${func.name}" too long (${funcMetrics.lineCount} lines)`,
          location: { line: func.startLine, column: 1 },
          suggestion: 'Consider splitting into smaller functions'
        });
      }

      if (funcMetrics.parameterCount > this.options.maxParameters) {
        issues.push({
          type: 'too-many-parameters',
          severity: 'warning',
          message: `Function "${func.name}" has too many parameters (${funcMetrics.parameterCount})`,
          location: { line: func.startLine, column: 1 },
          suggestion: 'Consider using an object for parameters'
        });
      }

      if (funcMetrics.maxNestingDepth > this.options.maxNestingDepth) {
        issues.push({
          type: 'deep-nesting',
          severity: 'warning',
          message: `Function "${func.name}" has deep nesting (${funcMetrics.maxNestingDepth} levels)`,
          location: { line: func.startLine, column: 1 },
          suggestion: 'Consider early returns or extracting nested logic'
        });
      }

      if (funcMetrics.cyclomaticComplexity > this.options.complexityThreshold) {
        issues.push({
          type: 'high-complexity',
          severity: 'error',
          message: `Function "${func.name}" has high complexity (${funcMetrics.cyclomaticComplexity})`,
          location: { line: func.startLine, column: 1 },
          suggestion: 'Consider simplifying conditional logic'
        });
      }
    }

    const magicNumbers = this.detectMagicNumbers(code, lines);
    for (const num of magicNumbers) {
      issues.push({
        type: 'magic-number',
        severity: 'info',
        message: `Magic number detected: ${num.value}`,
        location: { line: num.line, column: num.column },
        suggestion: 'Consider defining as a constant'
      });
    }

    return {
      filePath,
      metrics,
      issues,
      summary: {
        totalIssues: issues.length,
        errors: issues.filter(i => i.severity === 'error').length,
        warnings: issues.filter(i => i.severity === 'warning').length,
        info: issues.filter(i => i.severity === 'info').length
      }
    };
  }

  extractFunctions(code, lines) {
    const functions = [];
    const pattern = /function\s+(\w+)\s*\(([^)]*)\)/g;
    
    for (let i = 0; i < lines.length; i++) {
      const match = pattern.exec(lines[i]);
      if (match) {
        functions.push({
          name: match[1],
          parameters: match[2] ? match[2].split(',').map(p => p.trim()).filter(Boolean) : [],
          startLine: i + 1
        });
      }
      pattern.lastIndex = 0;
    }

    return functions;
  }

  analyzeFunction(func, code) {
    const lines = code.split('\n');
    const funcLines = lines.slice(func.startLine - 1);
    let braceCount = 0;
    let endLine = func.startLine;
    
    for (let i = 0; i < funcLines.length; i++) {
      for (const char of funcLines[i]) {
        if (char === '{') braceCount++;
        if (char === '}') braceCount--;
      }
      if (braceCount === 0 && i > 0) {
        endLine = func.startLine + i;
        break;
      }
    }

    const lineCount = endLine - func.startLine + 1;
    
    // Calculate cyclomatic complexity
    const funcCode = funcLines.slice(0, lineCount).join('\n');
    const complexityPatterns = [/\bif\b/g, /\bwhile\b/g, /\bfor\b/g, /\bcase\b/g, /\bcatch\b/g];
    let cyclomaticComplexity = 1;
    for (const pattern of complexityPatterns) {
      const matches = funcCode.match(pattern);
      if (matches) cyclomaticComplexity += matches.length;
    }

    // Calculate nesting depth
    let maxNestingDepth = 0;
    let currentDepth = 0;
    for (const line of funcLines.slice(0, lineCount)) {
      const trimmed = line.trim();
      if (/^(if|while|for)\b/.test(trimmed)) {
        currentDepth++;
        maxNestingDepth = Math.max(maxNestingDepth, currentDepth);
      }
      if (trimmed.startsWith('}')) currentDepth = Math.max(0, currentDepth - 1);
    }

    return {
      name: func.name,
      lineCount,
      parameterCount: func.parameters.length,
      cyclomaticComplexity,
      maxNestingDepth,
      startLine: func.startLine,
      endLine
    };
  }

  detectMagicNumbers(code, lines) {
    const magicNumbers = [];
    const pattern = /[^\w](\d{2,})/g;
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      let match;
      while ((match = pattern.exec(line)) !== null) {
        const value = match[1];
        if (!['10', '100', '1000'].includes(value)) {
          magicNumbers.push({
            value,
            line: i + 1,
            column: match.index + 1
          });
        }
      }
    }
    
    return magicNumbers;
  }
}

module.exports = { CodeAnalyzer };
