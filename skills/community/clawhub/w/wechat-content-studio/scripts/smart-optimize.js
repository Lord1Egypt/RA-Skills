#!/usr/bin/env node

/**
 * 智能动态排版优化模块
 * 根据文章内容自动分析并生成优化规则
 * 支持文章类型识别、内容特征分析、动态规则生成
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { loadOpenClawEnv, resolveWechatAppId, resolveWechatAppSecret } from './lib/openclaw_env.js';

const __smartDir = path.dirname(fileURLToPath(import.meta.url));
loadOpenClawEnv({ skillRoot: path.join(__smartDir, '..') });

/**
 * 文章类型枚举
 */
const ArticleType = {
  TECHNICAL: 'technical',        // 技术文章
  DATA_REPORT: 'data_report',    // 数据报告
  INTERVIEW: 'interview',        // 访谈对话
  TUTORIAL: 'tutorial',          // 教程指南
  OPINION: 'opinion',            // 观点评论
  NEWS: 'news',                  // 新闻资讯
  STORY: 'story',                // 故事叙述
  GENERAL: 'general'             // 通用类型
};

/**
 * 文章内容分析器
 */
export class ContentAnalyzer {
  constructor(content) {
    this.content = content;
    this.analysis = {
      type: ArticleType.GENERAL,
      features: [],
      metrics: {},
      suggestions: []
    };
  }

  /**
   * 分析文章类型
   */
  analyzeType() {
    const content = this.content.toLowerCase();
    
    // 技术文章特征
    const techKeywords = ['代码', 'api', '框架', '技术', '架构', '算法', '系统', '开发', '编程', 'github'];
    const techCount = techKeywords.filter(kw => content.includes(kw)).length;
    
    // 数据报告特征
    const dataPattern = /(\d+\.?\d*)%/g;
    const dataMatches = this.content.match(dataPattern);
    const dataCount = dataMatches ? dataMatches.length : 0;
    
    // 对话访谈特征
    const interviewPattern = /(问 | 答 | 采访 | 对话 | 说 | 表示)/g;
    const interviewMatches = this.content.match(interviewPattern);
    const interviewCount = interviewMatches ? interviewMatches.length : 0;
    
    // 教程指南特征
    const tutorialKeywords = ['步骤', '教程', '指南', '如何', '怎么', '方法', '技巧', '实战'];
    const tutorialCount = tutorialKeywords.filter(kw => content.includes(kw)).length;
    
    // 判断文章类型
    if (techCount >= 5 || this.content.includes('```')) {
      this.analysis.type = ArticleType.TECHNICAL;
    } else if (dataCount >= 10) {
      this.analysis.type = ArticleType.DATA_REPORT;
    } else if (interviewCount >= 20) {
      this.analysis.type = ArticleType.INTERVIEW;
    } else if (tutorialCount >= 5) {
      this.analysis.type = ArticleType.TUTORIAL;
    }
    
    this.analysis.metrics.keywordCounts = {
      tech: techCount,
      data: dataCount,
      interview: interviewCount,
      tutorial: tutorialCount
    };
    
    return this.analysis.type;
  }

  /**
   * 分析内容特征
   */
  analyzeFeatures() {
    const features = [];
    
    // 检查是否包含代码块
    if (this.content.includes('```')) {
      features.push('has_code_blocks');
    }
    
    // 检查是否包含表格
    if (/\|.*\|/.test(this.content)) {
      features.push('has_tables');
    }
    
    // 检查是否包含列表
    if (/^[-*]\s+/m.test(this.content)) {
      features.push('has_lists');
    }
    
    // 检查是否包含引用
    if (/^>/m.test(this.content)) {
      features.push('has_blockquotes');
    }
    
    // 检查是否包含数学公式
    if (/\$.*?\$/.test(this.content)) {
      features.push('has_formulas');
    }
    
    // 检查是否包含图片
    if (/!\[.*?\]\(.*?\)/.test(this.content)) {
      features.push('has_images');
    }
    
    // 检查数据密度
    const dataMatches = this.content.match(/(\d+\.?\d*)%/g);
    if (dataMatches && dataMatches.length >= 10) {
      features.push('high_data_density');
    }
    
    // 检查对话密度
    const dialogueMatches = this.content.match(/^(>|.*?[说表示问回答]：)/gm);
    if (dialogueMatches && dialogueMatches.length >= 15) {
      features.push('high_dialogue_density');
    }
    
    this.analysis.features = features;
    return features;
  }

  /**
   * 生成优化建议
   */
  generateSuggestions() {
    const suggestions = [];
    
    // 基于文章类型的建议
    switch (this.analysis.type) {
      case ArticleType.TECHNICAL:
        suggestions.push(
          '添加代码块高亮',
          '使用技术术语标记',
          '添加架构图示',
          '强调关键参数和配置'
        );
        break;
      
      case ArticleType.DATA_REPORT:
        suggestions.push(
          '加粗所有百分比数据',
          '使用表格展示对比',
          '添加数据可视化说明',
          '强调关键指标变化'
        );
        break;
      
      case ArticleType.INTERVIEW:
        suggestions.push(
          '使用引用块格式化对话',
          '添加对话者标识',
          '优化对话间距',
          '突出关键观点'
        );
        break;
      
      case ArticleType.TUTORIAL:
        suggestions.push(
          '使用步骤编号',
          '添加操作提示 emoji',
          '强调注意事项',
          '使用列表展示要点'
        );
        break;
    }
    
    // 基于特征的建议
    if (this.analysis.features.includes('has_code_blocks')) {
      suggestions.push('统一代码块样式');
    }
    
    if (this.analysis.features.includes('has_tables')) {
      suggestions.push('优化表格对齐');
    }
    
    if (this.analysis.features.includes('high_data_density')) {
      suggestions.push('数据强调处理');
    }
    
    if (this.analysis.features.includes('high_dialogue_density')) {
      suggestions.push('对话格式优化');
    }
    
    this.analysis.suggestions = suggestions;
    return suggestions;
  }

  /**
   * 执行完整分析
   */
  analyze() {
    this.analyzeType();
    this.analyzeFeatures();
    this.generateSuggestions();
    
    return this.analysis;
  }
}

/**
 * 动态规则生成器
 */
export class RuleGenerator {
  constructor(analysis) {
    this.analysis = analysis;
    this.rules = [];
  }

  /**
   * 生成基础排版规则
   */
  generateBasicRules() {
    const rules = [];
    
    // 章节标题 emoji
    rules.push({
      name: '添加章节 emoji',
      pattern: /## (引言 | 总结 | 参考资料 | 互动话题)/g,
      replacement: '## 💎 $1',
      priority: 1
    });
    
    rules.push({
      name: '添加章节 emoji',
      pattern: /## (一、|二、|三、|四、|五、|六、|七、)/g,
      replacement: '## 🔹 $1',
      priority: 1
    });
    
    this.rules.push(...rules);
    return rules;
  }

  /**
   * 根据文章类型生成规则
   */
  generateTypeSpecificRules() {
    const rules = [];
    
    switch (this.analysis.type) {
      case ArticleType.TECHNICAL:
        // 技术文章规则
        rules.push({
          name: '代码块标题优化',
          pattern: /```(\w+)/g,
          replacement: '```$1\n// 代码示例',
          priority: 2
        });
        
        rules.push({
          name: '技术术语强调',
          pattern: /(API|SDK|GitHub|RAG|LLM|AI)/g,
          replacement: '**$1**',
          priority: 2
        });
        break;
      
      case ArticleType.DATA_REPORT:
        // 数据报告规则
        rules.push({
          name: '百分比数据加粗',
          pattern: /(\d+\.?\d*)%/g,
          replacement: '**$1%**',
          priority: 2
        });
        
        rules.push({
          name: '数据对比强调',
          pattern: /(从 \d+% 到 \d+%)/g,
          replacement: '**$1**',
          priority: 2
        });
        
        rules.push({
          name: '增长下降标记',
          pattern: /(增长 | 提升 | 下降 | 降低|减少)\s*(\d+\.?\d*)%/g,
          replacement: '$1 **$2%**',
          priority: 2
        });
        break;
      
      case ArticleType.INTERVIEW:
        // 访谈对话规则
        rules.push({
          name: '对话引用格式化',
          pattern: /^(问 | 答 | 采访 | 对话):/gm,
          replacement: '> **$1**: ',
          priority: 2
        });
        
        rules.push({
          name: '对话者标识',
          pattern: /^([A-Z][a-z]+):/gm,
          replacement: '> **$1**: ',
          priority: 2
        });
        break;
      
      case ArticleType.TUTORIAL:
        // 教程指南规则
        rules.push({
          name: '步骤编号优化',
          pattern: /^步骤\s*(\d+):/gm,
          replacement: '### 📌 步骤 $1:',
          priority: 2
        });
        
        rules.push({
          name: '注意事项标记',
          pattern: /(注意 | 提示 | 警告 | 重要):/g,
          replacement: '⚠️ **$1**: ',
          priority: 2
        });
        break;
    }
    
    this.rules.push(...rules);
    return rules;
  }

  /**
   * 根据内容特征生成规则
   */
  generateFeatureSpecificRules() {
    const rules = [];
    
    // 代码块处理
    if (this.analysis.features.includes('has_code_blocks')) {
      rules.push({
        name: '代码块前后空行',
        pattern: /```\n/g,
        replacement: '\n```\n',
        priority: 3
      });
    }
    
    // 表格处理
    if (this.analysis.features.includes('has_tables')) {
      rules.push({
        name: '表格前后空行',
        pattern: /\n(\|.*\|)\n/g,
        replacement: '\n\n$1\n\n',
        priority: 3
      });
    }
    
    // 高密度数据
    if (this.analysis.features.includes('high_data_density')) {
      rules.push({
        name: '关键数据高亮',
        pattern: /(约|超过 | 达到|高达)\s*(\d+\.?\d*)%/g,
        replacement: '$1 **$2%**',
        priority: 3
      });
    }
    
    // 高密度对话
    if (this.analysis.features.includes('high_dialogue_density')) {
      rules.push({
        name: '对话间距优化',
        pattern: /(> .*\n)\n(?=>)/g,
        replacement: '$1',
        priority: 3
      });
    }
    
    this.rules.push(...rules);
    return rules;
  }

  /**
   * 生成通用优化规则
   */
  generateUniversalRules() {
    const rules = [];
    
    // 分隔线优化
    rules.push({
      name: '章节间分隔线',
      pattern: /\n(## )/g,
      replacement: '\n---\n\n$1',
      priority: 4
    });
    
    // 空行清理
    rules.push({
      name: '清理多余空行',
      pattern: /\n{4,}/g,
      replacement: '\n\n\n',
      priority: 4
    });
    
    // 互动引导
    rules.push({
      name: '添加互动引导',
      pattern: /(参考资料|参考资料：)/,
      replacement: '$1\n\n---\n\n**💬 互动话题**：欢迎在评论区分享你的经验和看法！\n\n**👍 如果觉得这篇文章有帮助，欢迎点赞、收藏、转发~**',
      priority: 5
    });
    
    this.rules.push(...rules);
    return rules;
  }

  /**
   * 生成完整规则集
   */
  generateAll() {
    this.generateBasicRules();
    this.generateTypeSpecificRules();
    this.generateFeatureSpecificRules();
    this.generateUniversalRules();
    
    // 按优先级排序
    this.rules.sort((a, b) => a.priority - b.priority);
    
    return this.rules;
  }
}

/**
 * 智能排版优化器
 */
export class SmartOptimizer {
  constructor(articlePath) {
    this.articlePath = articlePath;
    this.content = fs.readFileSync(articlePath, 'utf-8');
    this.originalContent = this.content;
    this.analysis = null;
    this.rules = [];
    this.optimizationLog = [];
  }

  /**
   * 分析文章
   */
  analyze() {
    console.log('\n🔍 分析文章内容...');
    
    const analyzer = new ContentAnalyzer(this.content);
    this.analysis = analyzer.analyze();
    
    console.log(`  📊 文章类型：${this.getTypeName(this.analysis.type)}`);
    console.log(`  📈 内容特征：${this.analysis.features.join(', ') || '无特殊特征'}`);
    console.log(`  💡 优化建议：${this.analysis.suggestions.length} 条`);
    
    return this.analysis;
  }

  /**
   * 生成优化规则
   */
  generateRules() {
    console.log('\n📝 生成优化规则...');
    
    const generator = new RuleGenerator(this.analysis);
    this.rules = generator.generateAll();
    
    console.log(`  ✅ 生成 ${this.rules.length} 条优化规则`);
    console.log(`  📊 按优先级分布:`);
    
    const priorityCount = {};
    this.rules.forEach(rule => {
      priorityCount[rule.priority] = (priorityCount[rule.priority] || 0) + 1;
    });
    
    Object.entries(priorityCount).forEach(([priority, count]) => {
      console.log(`     优先级 ${priority}: ${count} 条`);
    });
    
    return this.rules;
  }

  /**
   * 执行优化
   */
  optimize() {
    console.log('\n✍️  执行优化...');
    
    let optimizedContent = this.content;
    let changeCount = 0;
    
    this.rules.forEach((rule, index) => {
      const before = optimizedContent;
      optimizedContent = optimizedContent.replace(rule.pattern, rule.replacement);
      
      if (before !== optimizedContent) {
        changeCount++;
        this.optimizationLog.push({
          rule: rule.name,
          priority: rule.priority,
          changed: true
        });
        console.log(`  ✅ [${index + 1}/${this.rules.length}] ${rule.name} (优先级 ${rule.priority})`);
      } else {
        this.optimizationLog.push({
          rule: rule.name,
          priority: rule.priority,
          changed: false
        });
      }
    });
    
    this.content = optimizedContent;
    console.log(`\n  📊 共应用 ${changeCount} 处修改`);
    
    return this.content;
  }

  /**
   * 保存优化结果
   */
  save(outputPath = null) {
    const targetPath = outputPath || this.articlePath;
    fs.writeFileSync(targetPath, this.content, 'utf-8');
    console.log(`\n✅ 优化结果已保存：${targetPath}`);
  }

  /**
   * 质量评估
   */
  evaluateQuality() {
    let score = 0;
    const checks = [];
    
    // 标题 emoji (10 分)
    if (/## [🔹💎📌🎯📊💡⚠️✅❌]/.test(this.content)) {
      score += 10;
      checks.push({ item: '标题 emoji', pass: true });
    } else {
      checks.push({ item: '标题 emoji', pass: false });
    }
    
    // 数据加粗 (15 分)
    const boldDataCount = (this.content.match(/\*\*.*?\*\*/g) || []).length;
    if (boldDataCount >= 10) {
      score += 15;
      checks.push({ item: '数据加粗', pass: true, count: boldDataCount });
    } else {
      checks.push({ item: '数据加粗', pass: false, count: boldDataCount });
    }
    
    // 列表格式 (10 分)
    if (/^[-*]\s+/m.test(this.content)) {
      score += 10;
      checks.push({ item: '列表格式', pass: true });
    } else {
      checks.push({ item: '列表格式', pass: false });
    }
    
    // 引用块 (10 分)
    if (/^>/m.test(this.content)) {
      score += 10;
      checks.push({ item: '引用块', pass: true });
    } else {
      checks.push({ item: '引用块', pass: false });
    }
    
    // 分隔线 (10 分)
    if (/^---$/m.test(this.content)) {
      score += 10;
      checks.push({ item: '分隔线', pass: true });
    } else {
      checks.push({ item: '分隔线', pass: false });
    }
    
    // 代码块 (10 分)
    if (/```/.test(this.content)) {
      score += 10;
      checks.push({ item: '代码块', pass: true });
    } else {
      checks.push({ item: '代码块', pass: false });
    }
    
    // 表格 (10 分)
    if (/\|.*\|/.test(this.content)) {
      score += 10;
      checks.push({ item: '表格', pass: true });
    } else {
      checks.push({ item: '表格', pass: false });
    }
    
    // 段落间距 (10 分)
    const properSpacing = (this.content.match(/\n\n+/g) || []).length >= 20;
    if (properSpacing) {
      score += 10;
      checks.push({ item: '段落间距', pass: true });
    } else {
      checks.push({ item: '段落间距', pass: false });
    }
    
    // 强调标记 (5 分)
    if (/[*_]{2}.*?[*_]{2}/.test(this.content)) {
      score += 5;
      checks.push({ item: '强调标记', pass: true });
    } else {
      checks.push({ item: '强调标记', pass: false });
    }
    
    // 互动引导 (10 分)
    if (/(欢迎 | 点赞 | 收藏 | 转发 | 评论 | 分享 | 互动话题)/.test(this.content)) {
      score += 10;
      checks.push({ item: '互动引导', pass: true });
    } else {
      checks.push({ item: '互动引导', pass: false });
    }
    
    return { score, checks };
  }

  /**
   * 获取类型名称
   */
  getTypeName(type) {
    const names = {
      [ArticleType.TECHNICAL]: '技术文章',
      [ArticleType.DATA_REPORT]: '数据报告',
      [ArticleType.INTERVIEW]: '访谈对话',
      [ArticleType.TUTORIAL]: '教程指南',
      [ArticleType.OPINION]: '观点评论',
      [ArticleType.NEWS]: '新闻资讯',
      [ArticleType.STORY]: '故事叙述',
      [ArticleType.GENERAL]: '通用类型'
    };
    return names[type] || type;
  }

  /**
   * 生成优化报告
   */
  generateReport() {
    const report = {
      articlePath: this.articlePath,
      analysis: this.analysis,
      rulesApplied: this.rules.length,
      changesCount: this.optimizationLog.filter(r => r.changed).length,
      qualityScore: this.evaluateQuality(),
      optimizationLog: this.optimizationLog
    };
    
    return report;
  }
}

/**
 * 主函数：智能优化文章
 */
export async function smartOptimizeArticle(articlePath, options = {}) {
  const {
    shouldPublish = true,
    outputPath = null
  } = options;
  
  console.log('\n🚀 开始智能动态排版优化...\n');
  console.log('━'.repeat(60));
  
  // 1. 创建优化器
  const optimizer = new SmartOptimizer(articlePath);
  
  // 2. 分析文章
  optimizer.analyze();
  
  // 3. 生成规则
  optimizer.generateRules();
  
  // 4. 执行优化
  optimizer.optimize();
  
  // 5. 保存结果
  optimizer.save(outputPath);
  
  // 6. 质量评估
  const quality = optimizer.evaluateQuality();
  console.log('\n📊 质量评估:');
  console.log(`  总分：${quality.score}/100`);
  console.log('\n  检查项:');
  quality.checks.forEach(check => {
    const icon = check.pass ? '✅' : '❌';
    const details = check.count !== undefined ? ` (${check.count}处)` : '';
    console.log(`    ${icon} ${check.item}${details}`);
  });
  
  // 7. 生成报告
  const report = optimizer.generateReport();
  
  console.log('\n' + '━'.repeat(60));
  console.log('📊 优化总结:');
  console.log(`  - 文章类型：${optimizer.getTypeName(report.analysis.type)}`);
  console.log(`  - 生成规则：${report.rulesApplied} 条`);
  console.log(`  - 应用修改：${report.changesCount} 处`);
  console.log(`  - 质量评分：${report.qualityScore.score}/100`);
  console.log('━'.repeat(60));
  
  // 8. 自动发布（如果需要）
  const publishTarget = outputPath || articlePath;
  if (shouldPublish && quality.score >= 90) {
    console.log('\n📱 发布文章...');
    try {
      const appId = resolveWechatAppId();
      const secret = resolveWechatAppSecret();
      
      if (appId && secret) {
        const env = {
          ...process.env,
          WECHAT_APP_ID: appId,
          WECHAT_APP_SECRET: secret
        };
        
        execSync(`wenyan publish -f "${publishTarget}" -t lapis -h solarized-light`, {
          env,
          stdio: 'pipe'
        });
        
        console.log('✅ 发布成功！');
      } else {
        console.log('⚠️  未配置公众号 API 凭证，跳过发布');
      }
    } catch (error) {
      console.log('⚠️  发布失败:', error.message);
    }
  }
  
  return report;
}

// 命令行接口
if (process.argv[1] && process.argv[1].includes('smart-optimize.js')) {
  const args = process.argv.slice(2);
  const articlePath = args[0];
  
  if (!articlePath) {
    console.error('用法：node smart-optimize.js <article.md> [options]');
    console.error('选项:');
    console.error('  --no-publish    不自动发布');
    console.error('  --output <path> 输出路径');
    process.exit(1);
  }
  
  const options = {
    shouldPublish: true,
    outputPath: null
  };
  
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--no-publish') {
      options.shouldPublish = false;
    } else if (args[i] === '--output' && args[i + 1]) {
      options.outputPath = args[++i];
    }
  }
  
  smartOptimizeArticle(articlePath, options)
    .then(report => {
      console.log('\n✅ 智能优化完成！');
      process.exit(0);
    })
    .catch(error => {
      console.error('\n❌ 优化失败:', error.message);
      process.exit(1);
    });
}
