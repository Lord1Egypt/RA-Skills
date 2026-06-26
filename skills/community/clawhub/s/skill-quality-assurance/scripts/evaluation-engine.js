/**
 * Skill Quality Assurance - Evaluation Engine
 * 
 * 六维评估引擎核心
 * 应用设计模式：评估工厂模式（Evaluation Factory）
 * 
 * 来源：first-principle-analyzer/src/evaluation-factory.js
 */

const fs = require('fs');
const path = require('path');

// ==================== 评估工厂模式 ====================

class EvaluationFactory {
  /**
   * 创建评估器实例
   * @param {string} dimension - 维度标识 (T/C/O/E/M/U)
   * @returns {Evaluator} 评估器实例
   */
  createEvaluator(dimension) {
    const evaluators = {
      'T': TechnologyEvaluator,
      'C': CognitionEvaluator,
      'O': OrchestrationEvaluator,
      'E': EvolutionEvaluator,
      'M': MarketEvaluator,
      'U': UserExperienceEvaluator
    };
    
    const EvaluatorClass = evaluators[dimension];
    if (!EvaluatorClass) {
      throw new Error(`Unknown dimension: ${dimension}`);
    }
    
    return new EvaluatorClass();
  }
}

// ==================== 基础评估器类 ====================

class Evaluator {
  constructor(dimension, subDimensions) {
    this.dimension = dimension;
    this.subDimensions = subDimensions;
  }
  
  /**
   * 评估技能
   * @param {string} skillPath - 技能路径
   * @returns {Object} 评估结果
   */
  evaluate(skillPath) {
    const results = {};
    let totalScore = 0;
    
    for (const [subDim, weight] of Object.entries(this.subDimensions)) {
      const score = this.evaluateSubDimension(skillPath, subDim);
      results[subDim] = { score, weight };
      totalScore += score * weight;
    }
    
    return {
      dimension: this.dimension,
      subDimensions: results,
      score: totalScore
    };
  }
  
  /**
   * 评估子维度（子类实现）
   * @param {string} skillPath - 技能路径
   * @param {string} subDim - 子维度标识
   * @returns {number} 得分 (0-1)
   */
  evaluateSubDimension(skillPath, subDim) {
    throw new Error('Subclass must implement evaluateSubDimension');
  }
}

// ==================== T 维度评估器（技术深度） ====================

class TechnologyEvaluator extends Evaluator {
  constructor() {
    super('T', {
      'T₁': 0.25, // 架构设计
      'T₂': 0.25, // 代码质量
      'T₃': 0.25, // 性能表现
      'T₄': 0.25  // 测试覆盖
    });
  }
  
  evaluateSubDimension(skillPath, subDim) {
    switch (subDim) {
      case 'T₁': // 架构设计
        return this.evaluateArchitecture(skillPath);
      case 'T₂': // 代码质量
        return this.evaluateCodeQuality(skillPath);
      case 'T₃': // 性能表现
        return this.evaluatePerformance(skillPath);
      case 'T₄': // 测试覆盖
        return this.evaluateTestCoverage(skillPath);
      default:
        return 0.5;
    }
  }
  
  evaluateArchitecture(skillPath) {
    // 检查目录结构清晰度
    const files = fs.readdirSync(skillPath);
    const hasScripts = files.includes('scripts');
    const hasReferences = files.includes('references');
    const hasAssets = files.includes('assets');
    const hasSkillMd = files.includes('SKILL.md');
    
    // 分层清晰度评分
    let score = 0.5; // 基础分
    if (hasSkillMd) score += 0.1;
    if (hasScripts) score += 0.1;
    if (hasReferences) score += 0.1;
    if (hasAssets) score += 0.1;
    
    return Math.min(score, 1.0);
  }
  
  evaluateCodeQuality(skillPath) {
    // 检查 SKILL.md 质量
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) return 0.5;
    
    const content = fs.readFileSync(skillMdPath, 'utf8');
    
    // 检查 YAML frontmatter
    const hasFrontmatter = content.startsWith('---');
    const hasName = content.includes('name:');
    const hasDescription = content.includes('description:');
    
    // 检查代码规范
    let score = 0.5;
    if (hasFrontmatter) score += 0.15;
    if (hasName && hasDescription) score += 0.15;
    if (content.length > 1000) score += 0.1; // 内容充实
    if (content.includes('示例') || content.includes('example')) score += 0.1;
    
    return Math.min(score, 1.0);
  }
  
  evaluatePerformance(skillPath) {
    // 检查是否有性能测试
    const scriptsPath = path.join(skillPath, 'scripts');
    if (!fs.existsSync(scriptsPath)) return 0.6;
    
    const scripts = fs.readdirSync(scriptsPath);
    const hasBenchmark = scripts.some(f => f.includes('benchmark') || f.includes('perf'));
    
    return hasBenchmark ? 0.8 : 0.6;
  }
  
  evaluateTestCoverage(skillPath) {
    // 检查测试文件
    const testPatterns = ['test', 'spec', 'coverage'];
    const files = fs.readdirSync(skillPath);
    
    const hasTests = files.some(f => 
      testPatterns.some(p => f.toLowerCase().includes(p))
    );
    
    // 检查 coverage 目录
    const hasCoverage = files.includes('coverage');
    
    if (hasCoverage) return 0.9; // 有覆盖率报告
    if (hasTests) return 0.7;    // 有测试文件
    return 0.5;                   // 无测试
  }
}

// ==================== C 维度评估器（认知增强） ====================

class CognitionEvaluator extends Evaluator {
  constructor() {
    super('C', {
      'C₁': 0.25, // 知识沉淀
      'C₂': 0.25, // 决策支持
      'C₃': 0.25, // 学习辅助
      'C₄': 0.25  // 洞察提供
    });
  }
  
  evaluateSubDimension(skillPath, subDim) {
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) return 0.5;
    
    const content = fs.readFileSync(skillMdPath, 'utf8');
    
    switch (subDim) {
      case 'C₁': // 知识沉淀
        return content.includes('设计模式') || content.includes('来源') ? 0.8 : 0.5;
      case 'C₂': // 决策支持
        return content.includes('状态') || content.includes('进度') ? 0.7 : 0.5;
      case 'C₃': // 学习辅助
        return content.includes('示例') || content.includes('用法') ? 0.8 : 0.5;
      case 'C₄': // 洞察提供
        return content.includes('历史') || content.includes('分析') ? 0.7 : 0.5;
      default:
        return 0.5;
    }
  }
}

// ==================== O 维度评估器（编排能力） ====================

class OrchestrationEvaluator extends Evaluator {
  constructor() {
    super('O', {
      'O₁': 0.25, // 多技能协同
      'O₂': 0.25, // 工作流编排
      'O₃': 0.25, // 资源调度
      'O₄': 0.25  // 异常处理
    });
  }
  
  evaluateSubDimension(skillPath, subDim) {
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) return 0.5;
    
    const content = fs.readFileSync(skillMdPath, 'utf8');
    
    switch (subDim) {
      case 'O₁': // 多技能协同
        return content.includes('协同') || content.includes('事件') ? 0.8 : 0.5;
      case 'O₂': // 工作流编排
        return content.includes('流程') || content.includes('状态机') ? 0.7 : 0.5;
      case 'O₃': // 资源调度
        return content.includes('限制') || content.includes('并发') ? 0.6 : 0.5;
      case 'O₄': // 异常处理
        return content.includes('错误') || content.includes('重试') ? 0.7 : 0.5;
      default:
        return 0.5;
    }
  }
}

// ==================== E 维度评估器（进化能力） ====================

class EvolutionEvaluator extends Evaluator {
  constructor() {
    super('E', {
      'E₁': 0.25, // 自优化
      'E₂': 0.25, // 自学习
      'E₃': 0.25, // 自适应
      'E₄': 0.25  // 版本管理
    });
  }
  
  evaluateSubDimension(skillPath, subDim) {
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) return 0.5;
    
    const content = fs.readFileSync(skillMdPath, 'utf8');
    
    switch (subDim) {
      case 'E₁': // 自优化
        return content.includes('优化') || content.includes('配置') ? 0.7 : 0.5;
      case 'E₂': // 自学习
        return content.includes('学习') || content.includes('分析') ? 0.7 : 0.5;
      case 'E₃': // 自适应
        return content.includes('动态') || content.includes('扩展') ? 0.7 : 0.5;
      case 'E₄': // 版本管理
        return content.includes('版本') || content.includes('v') ? 0.8 : 0.5;
      default:
        return 0.5;
    }
  }
}

// ==================== M 维度评估器（市场验证） ====================

class MarketEvaluator extends Evaluator {
  constructor() {
    super('M', {
      'M₁': 0.25, // 用户验证
      'M₂': 0.25, // 采用率
      'M₃': 0.25, // 反馈收集
      'M₄': 0.25  // 商业化
    });
  }
  
  evaluateSubDimension(skillPath, subDim) {
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) return 0.5;
    
    const content = fs.readFileSync(skillMdPath, 'utf8');
    
    switch (subDim) {
      case 'M₁': // 用户验证
        return content.includes('用户') || content.includes('反馈') ? 0.6 : 0.4;
      case 'M₂': // 采用率
        return content.includes('上架') || content.includes('ClawHub') ? 0.6 : 0.4;
      case 'M₃': // 反馈收集
        return content.includes('反馈') || content.includes('issue') ? 0.5 : 0.4;
      case 'M₄': // 商业化
        return content.includes('商业') || content.includes('定价') ? 0.6 : 0.4;
      default:
        return 0.5;
    }
  }
}

// ==================== U 维度评估器（用户体验） ====================

class UserExperienceEvaluator extends Evaluator {
  constructor() {
    super('U', {
      'U₁': 0.25, // 易用性
      'U₂': 0.25, // 文档质量
      'U₃': 0.25, // 错误提示
      'U₄': 0.25  // 可访问性
    });
  }
  
  evaluateSubDimension(skillPath, subDim) {
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) return 0.5;
    
    const content = fs.readFileSync(skillMdPath, 'utf8');
    
    switch (subDim) {
      case 'U₁': // 易用性
        return content.includes('使用') || content.includes('快速') ? 0.8 : 0.6;
      case 'U₂': // 文档质量
        return content.includes('文档') || content.includes('README') ? 0.8 : 0.6;
      case 'U₃': // 错误提示
        return content.includes('错误') || content.includes('提示') ? 0.7 : 0.5;
      case 'U₄': // 可访问性
        return content.includes('API') || content.includes('接口') ? 0.7 : 0.5;
      default:
        return 0.5;
    }
  }
}

// ==================== 主评估引擎 ====================

class SkillQualityEngine {
  constructor() {
    this.factory = new EvaluationFactory();
    this.dimensions = ['T', 'C', 'O', 'E', 'M', 'U'];
  }
  
  /**
   * 评估技能
   * @param {string} skillPath - 技能路径
   * @returns {Object} 评估结果
   */
  evaluate(skillPath) {
    console.log(`\n🔍 开始评估技能：${path.basename(skillPath)}\n`);
    
    const results = {};
    let totalScore = 0;
    
    for (const dim of this.dimensions) {
      const evaluator = this.factory.createEvaluator(dim);
      const result = evaluator.evaluate(skillPath);
      results[dim] = result;
      totalScore += result.score;
    }
    
    const averageScore = totalScore / this.dimensions.length;
    
    return {
      skillName: path.basename(skillPath),
      dimensions: results,
      averageScore,
      rating: this.getRating(averageScore)
    };
  }
  
  /**
   * 获取评级
   * @param {number} score - 平均分
   * @returns {string} 评级
   */
  getRating(score) {
    if (score >= 0.9) return 'S 级 (行业领先)';
    if (score >= 0.8) return 'A 级 (专业级)';
    if (score >= 0.7) return 'B 级 (良好)';
    if (score >= 0.6) return 'C 级 (合格)';
    return 'D 级 (待改进)';
  }
  
  /**
   * 生成评估报告
   * @param {Object} results - 评估结果
   * @returns {string} Markdown 报告
   */
  generateReport(results) {
    let report = `# ${results.skillName} 六维评估报告\n\n`;
    report += `**评估日期**: ${new Date().toISOString().split('T')[0]}\n`;
    report += `**综合得分**: ${results.averageScore.toFixed(2)} (${results.rating})\n\n`;
    
    report += '## 六维得分总览\n\n';
    report += '| 维度 | 得分 | 状态 |\n';
    report += '|------|------|------|\n';
    
    for (const [dim, result] of Object.entries(results.dimensions)) {
      const status = result.score >= 0.7 ? '✅' : '⚠️';
      report += `| ${dim} | ${result.score.toFixed(2)} | ${status} |\n`;
    }
    
    report += `\n## 各维度详细评估\n\n`;
    
    for (const [dim, result] of Object.entries(results.dimensions)) {
      report += `### ${dim} 维度：${result.score.toFixed(2)}\n\n`;
      for (const [subDim, data] of Object.entries(result.subDimensions)) {
        report += `- **${subDim}**: ${data.score.toFixed(2)}\n`;
      }
      report += '\n';
    }
    
    return report;
  }
}

// ==================== CLI 入口 ====================

if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('使用方法：node evaluation-engine.js <skill-path> [output-path]');
    console.log('示例：node evaluation-engine.js ~/.openclaw/skills/meta-cognition-assistant');
    process.exit(1);
  }
  
  const skillPath = args[0];
  const outputPath = args[1] || '.';
  
  if (!fs.existsSync(skillPath)) {
    console.error(`错误：技能路径不存在：${skillPath}`);
    process.exit(1);
  }
  
  const engine = new SkillQualityEngine();
  const results = engine.evaluate(skillPath);
  
  // 输出摘要
  console.log('\n📊 评估结果摘要\n');
  console.log(`技能名称：${results.skillName}`);
  console.log(`综合得分：${results.averageScore.toFixed(2)} (${results.rating})`);
  console.log('\n各维度得分:');
  for (const [dim, result] of Object.entries(results.dimensions)) {
    const status = result.score >= 0.7 ? '✅' : '⚠️';
    console.log(`  ${dim}: ${result.score.toFixed(2)} ${status}`);
  }
  
  // 生成报告
  const report = engine.generateReport(results);
  const reportPath = path.join(outputPath, `${results.skillName}-evaluation-report.md`);
  fs.writeFileSync(reportPath, report);
  console.log(`\n📄 评估报告已保存：${reportPath}`);
}

module.exports = { SkillQualityEngine, EvaluationFactory };
