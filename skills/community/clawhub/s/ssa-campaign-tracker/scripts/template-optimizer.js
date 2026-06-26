#!/usr/bin/env node

/**
 * template-optimizer.js - 开发信模板优化器
 * 
 * 功能：
 * 1. 读取 analytics-report 生成的 JSON 报告（reports/ 目录）
 * 2. 读取 tracking-schema.json 的 ab_testing 配置
 * 3. 识别高效模板（回复率 top 30%）和低效模板（回复率 bottom 30%）
 * 4. 生成优化建议报告：
 *    - 高效模板分析：哪些特征导致高回复率（主题行长度/个性化程度/发送时间）
 *    - 低效模板改进建议：主题行优化/内容结构/CTA 调整
 *    - A/B 测试方案推荐（哪些变量值得测试）
 * 5. 更新 ab_testing 配置文件，添加新的测试组
 * 6. 输出格式：Markdown（存入 Obsidian）+ JSON
 * 7. 支持 dry-run 模式
 * 8. 记录优化建议日志
 * 
 * 用法：
 *   node template-optimizer.js [--dry-run] [--report-file REPORT]
 */

const fs = require('fs');
const path = require('path');

// ============ 配置 ============
const CONFIG = {
  baseDir: path.join(__dirname, '..'),
  configDir: path.join(__dirname, '..', 'config'),
  reportsDir: path.join(__dirname, '..', 'reports'),
  logsDir: path.join(__dirname, '..', 'logs', 'optimizer'),
  obsidianDir: process.env.OBSIDIAN_VAULT ? path.join(process.env.OBSIDIAN_VAULT, 'Farreach 知识库/业务分析/开发信效果') : '<path-to-obsidian-vault>/Farreach 知识库/业务分析/开发信效果',
  trackingSchemaPath: path.join(__dirname, '..', 'config', 'tracking-schema.json')
};

// ============ 工具函数 ============

/**
 * 日志记录
 */
function log(level, message, data = null) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level,
    message,
    data
  };
  
  console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`);
  if (data) {
    console.log(JSON.stringify(data, null, 2));
  }
  
  // 写入日志文件
  try {
    if (!fs.existsSync(CONFIG.logsDir)) {
      fs.mkdirSync(CONFIG.logsDir, { recursive: true });
    }
    const logFile = path.join(CONFIG.logsDir, `${new Date().toISOString().split('T')[0]}.log`);
    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
  } catch (err) {
    console.error('Failed to write log:', err.message);
  }
}

/**
 * 读取 JSON 文件
 */
function readJsonFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }
  
  const content = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(content);
}

/**
 * 读取目录下所有 JSON 报告文件
 */
function readAllReports(dirPath) {
  if (!fs.existsSync(dirPath)) {
    return [];
  }
  
  const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.json') && !f.includes('example'));
  const reports = [];
  
  for (const file of files) {
    const filePath = path.join(dirPath, file);
    try {
      const report = readJsonFile(filePath);
      if (report && report.breakdown && report.breakdown.by_template) {
        reports.push({ file, ...report });
      }
    } catch (err) {
      log('warn', `Failed to parse report ${file}: ${err.message}`);
    }
  }
  
  return reports;
}

/**
 * 计算百分位数阈值
 */
function calculatePercentileThresholds(templates) {
  if (templates.length === 0) {
    return { top30: null, bottom30: null };
  }
  
  const sorted = [...templates].sort((a, b) => b.reply_rate - a.reply_rate);
  const top30Index = Math.max(0, Math.floor(sorted.length * 0.3) - 1);
  const bottom30Index = Math.max(0, sorted.length - Math.floor(sorted.length * 0.3));
  
  return {
    top30: sorted[top30Index]?.reply_rate || 0,
    bottom30: sorted[bottom30Index]?.reply_rate || 0
  };
}

/**
 * 分析模板特征
 */
function analyzeTemplateFeatures(template, reports) {
  const features = {
    template_id: template.template_id,
    sent_count: template.sent_count,
    replied_count: template.replied_count,
    reply_rate: template.reply_rate,
    characteristics: []
  };
  
  // 主题行分析
  if (template.subject_line) {
    const subjectLength = template.subject_line.length;
    if (subjectLength <= 30) {
      features.characteristics.push('short_subject');
    } else if (subjectLength <= 50) {
      features.characteristics.push('medium_subject');
    } else {
      features.characteristics.push('long_subject');
    }
  }
  
  // 个性化程度分析（基于模板 ID 命名约定）
  if (template.template_id.includes('personalized') || template.template_id.includes('custom')) {
    features.characteristics.push('high_personalization');
  } else if (template.template_id.includes('generic') || template.template_id.includes('template')) {
    features.characteristics.push('low_personalization');
  }
  
  // 变体分析
  if (template.template_variant) {
    features.characteristics.push(`variant_${template.template_variant.toLowerCase()}`);
  }
  
  return features;
}

/**
 * 生成高效模板分析
 */
function analyzeHighPerformers(highPerformers, allTemplates) {
  const analysis = {
    count: highPerformers.length,
    avg_reply_rate: 0,
    common_characteristics: {},
    recommendations: []
  };
  
  if (highPerformers.length === 0) {
    return analysis;
  }
  
  const totalRate = highPerformers.reduce((sum, t) => sum + t.reply_rate, 0);
  analysis.avg_reply_rate = totalRate / highPerformers.length;
  
  // 统计共同特征
  const charCounts = {};
  highPerformers.forEach(t => {
    t.characteristics.forEach(c => {
      charCounts[c] = (charCounts[c] || 0) + 1;
    });
  });
  
  // 找出出现频率最高的特征
  Object.entries(charCounts).forEach(([char, count]) => {
    const percentage = (count / highPerformers.length) * 100;
    analysis.common_characteristics[char] = {
      count,
      percentage: percentage.toFixed(1) + '%'
    };
  });
  
  // 生成建议
  const topChars = Object.entries(charCounts).sort((a, b) => b[1] - a[1]).slice(0, 3);
  topChars.forEach(([char, count]) => {
    const percentage = ((count / highPerformers.length) * 100).toFixed(0);
    if (char.includes('subject')) {
      analysis.recommendations.push(`高效模板普遍采用${char.replace('_', ' ')}（${percentage}%），建议保持此风格`);
    } else if (char.includes('personalization')) {
      analysis.recommendations.push(`${percentage}% 的高效模板使用${char.replace('_', ' ')}，建议加强个性化元素`);
    } else if (char.includes('variant')) {
      analysis.recommendations.push(`变体${char.replace('variant_', '').toUpperCase()}表现优异，可作为对照组`);
    }
  });
  
  return analysis;
}

/**
 * 生成低效模板改进建议
 */
function generateImprovementSuggestions(lowPerformers) {
  const suggestions = [];
  
  lowPerformers.forEach(template => {
    const suggestion = {
      template_id: template.template_id,
      current_reply_rate: template.reply_rate,
      issues: [],
      improvements: []
    };
    
    // 主题行优化
    if (template.subject_line && template.subject_line.length > 60) {
      suggestion.issues.push('主题行过长（>60 字符）');
      suggestion.improvements.push('缩短主题行至 30-50 字符，突出核心价值');
    } else if (!template.subject_line) {
      suggestion.issues.push('缺少主题行数据');
      suggestion.improvements.push('添加明确的主题行，包含客户痛点或价值主张');
    }
    
    // 回复率过低
    if (template.reply_rate < 0.05) {
      suggestion.issues.push('回复率极低（<5%）');
      suggestion.improvements.push('重新设计开场白，增加个性化元素');
      suggestion.improvements.push('优化 CTA，使其更明确、更易执行');
      suggestion.improvements.push('考虑调整发送时间或目标受众');
    }
    
    // 样本量不足
    if (template.sent_count < 50) {
      suggestion.issues.push('样本量不足，数据可能不具代表性');
      suggestion.improvements.push('增加发送量至至少 50 封以获得可靠数据');
    }
    
    if (suggestion.improvements.length > 0) {
      suggestions.push(suggestion);
    }
  });
  
  return suggestions;
}

/**
 * 生成 A/B 测试推荐
 */
function generateABTestRecommendations(highPerformers, lowPerformers, allTemplates) {
  const recommendations = [];
  
  // 推荐 1: 高效模板特征测试
  if (highPerformers.length > 0) {
    const topPerformer = highPerformers[0];
    recommendations.push({
      test_name: `高效模板特征验证：${topPerformer.template_id}`,
      hypothesis: `${topPerformer.template_id} 的高回复率源于其${topPerformer.characteristics.join('/')}特征`,
      variant_a: {
        description: '对照组：当前低效模板',
        template_id: lowPerformers[0]?.template_id || 'current_template'
      },
      variant_b: {
        description: '实验组：高效模板特征',
        template_id: topPerformer.template_id
      },
      success_metric: 'reply_rate',
      min_sample_size: 100,
      priority: 'high'
    });
  }
  
  // 推荐 2: 主题行长度测试
  const shortSubjects = allTemplates.filter(t => t.subject_line && t.subject_line.length <= 30);
  const longSubjects = allTemplates.filter(t => t.subject_line && t.subject_line.length > 50);
  if (shortSubjects.length > 0 && longSubjects.length > 0) {
    const shortAvg = shortSubjects.reduce((sum, t) => sum + t.reply_rate, 0) / shortSubjects.length;
    const longAvg = longSubjects.reduce((sum, t) => sum + t.reply_rate, 0) / longSubjects.length;
    recommendations.push({
      test_name: '主题行长度优化测试',
      hypothesis: `短主题行（≤30 字符）回复率${(shortAvg * 100).toFixed(1)}% vs 长主题行（>50 字符）${(longAvg * 100).toFixed(1)}%`,
      variant_a: {
        description: '短主题行（≤30 字符）',
        subject_pattern: '简短直接'
      },
      variant_b: {
        description: '长主题行（>50 字符）',
        subject_pattern: '详细描述'
      },
      success_metric: 'reply_rate',
      min_sample_size: 100,
      priority: 'medium'
    });
  }
  
  // 推荐 3: 个性化程度测试
  const highPersonalization = allTemplates.filter(t => t.characteristics.includes('high_personalization'));
  const lowPersonalization = allTemplates.filter(t => t.characteristics.includes('low_personalization'));
  if (highPersonalization.length > 0 && lowPersonalization.length > 0) {
    const highAvg = highPersonalization.reduce((sum, t) => sum + t.reply_rate, 0) / highPersonalization.length;
    const lowAvg = lowPersonalization.reduce((sum, t) => sum + t.reply_rate, 0) / lowPersonalization.length;
    recommendations.push({
      test_name: '个性化程度测试',
      hypothesis: `高个性化模板回复率${(highAvg * 100).toFixed(1)}% vs 低个性化${(lowAvg * 100).toFixed(1)}%`,
      variant_a: {
        description: '低个性化（通用模板）',
        personalization_level: 'low'
      },
      variant_b: {
        description: '高个性化（客户定制）',
        personalization_level: 'high'
      },
      success_metric: 'reply_rate',
      min_sample_size: 100,
      priority: 'high'
    });
  }
  
  return recommendations;
}

/**
 * 生成 Markdown 报告
 */
function generateMarkdownReport(analysis, outputPath) {
  const date = new Date().toISOString().split('T')[0];
  const md = `---
date: ${date}
tags: [开发信，模板优化，A/B 测试]
---

# 开发信模板优化分析报告

**生成时间：** ${new Date().toISOString()}

---

## 📊 执行摘要

- **分析模板总数：** ${analysis.total_templates}
- **高效模板（Top 30%）：** ${analysis.high_performers.count} 个，平均回复率 ${(analysis.high_performers.avg_reply_rate * 100).toFixed(1)}%
- **低效模板（Bottom 30%）：** ${analysis.low_performers.count} 个
- **A/B 测试推荐：** ${analysis.ab_tests.length} 个

---

## 🏆 高效模板分析

${analysis.high_performers.count > 0 ? `
**平均回复率：** ${(analysis.high_performers.avg_reply_rate * 100).toFixed(1)}%

**共同特征：**
${Object.entries(analysis.high_performers.common_characteristics).map(([char, data]) => `- ${char}: ${data.percentage} (${data.count}个模板)`).join('\n')}

**成功建议：**
${analysis.high_performers.recommendations.map(r => `- ${r}`).join('\n')}
` : '数据不足，无法分析高效模板特征。'}

---

## ⚠️ 低效模板改进建议

${analysis.improvement_suggestions.length > 0 ? analysis.improvement_suggestions.map(s => `
### ${s.template_id}
**当前回复率：** ${(s.current_reply_rate * 100).toFixed(1)}%

**问题：**
${s.issues.map(i => `- ${i}`).join('\n')}

**改进建议：**
${s.improvements.map(i => `- ${i}`).join('\n')}
`).join('\n\n') : '无需改进的低效模板。'}

---

## 🧪 A/B 测试推荐

${analysis.ab_tests.length > 0 ? analysis.ab_tests.map((test, i) => `
### 测试 ${i + 1}: ${test.test_name}

**假设：** ${test.hypothesis}

**对照组（A）：** ${test.variant_a.description}
${test.variant_a.template_id ? `- 模板 ID: ${test.variant_a.template_id}` : ''}
${test.variant_a.subject_pattern ? `- 主题模式：${test.variant_a.subject_pattern}` : ''}
${test.variant_a.personalization_level ? `- 个性化程度：${test.variant_a.personalization_level}` : ''}

**实验组（B）：** ${test.variant_b.description}
${test.variant_b.template_id ? `- 模板 ID: ${test.variant_b.template_id}` : ''}
${test.variant_b.subject_pattern ? `- 主题模式：${test.variant_b.subject_pattern}` : ''}
${test.variant_b.personalization_level ? `- 个性化程度：${test.variant_b.personalization_level}` : ''}

**成功指标：** ${test.success_metric}
**最小样本量：** ${test.min_sample_size}
**优先级：** ${test.priority}
`).join('\n\n') : '暂无 A/B 测试推荐。'}

---

## 📋 下一步行动

1. **立即执行：** 根据高效模板特征，优化低效模板
2. **本周内：** 启动优先级为 high 的 A/B 测试
3. **持续追踪：** 每周生成分析报告，监控模板性能变化

---

*本报告由 template-optimizer.js 自动生成*
`;

  // 确保 Obsidian 目录存在
  try {
    if (!fs.existsSync(CONFIG.obsidianDir)) {
      fs.mkdirSync(CONFIG.obsidianDir, { recursive: true });
    }
  } catch (err) {
    log('warn', `Failed to create Obsidian directory: ${err.message}`);
  }

  // 写入文件
  const filePath = outputPath || path.join(CONFIG.obsidianDir, `模板优化报告-${date}.md`);
  fs.writeFileSync(filePath, md);
  log('info', `Markdown report written to ${filePath}`);
  
  return filePath;
}

/**
 * 更新 ab_testing 配置
 */
function updateABTestingConfig(abTests, configPath, dryRun = false) {
  const config = readJsonFile(configPath);
  if (!config) {
    log('error', 'Failed to read tracking-schema.json');
    return null;
  }
  
  if (!config.ab_testing) {
    config.ab_testing = { test_groups: [] };
  }
  
  if (!config.ab_testing.test_groups) {
    config.ab_testing.test_groups = [];
  }
  
  // 添加新的测试组
  const newTests = abTests.map((test, index) => ({
    test_id: `test-${new Date().toISOString().split('T')[0]}-${String(index + 1).padStart(2, '0')}`,
    name: test.test_name,
    hypothesis: test.hypothesis,
    variant_a: test.variant_a,
    variant_b: test.variant_b,
    success_metric: test.success_metric,
    sample_size: test.min_sample_size,
    split_ratio: { variant_a: 0.5, variant_b: 0.5 },
    statistical_significance: 0.95,
    status: 'recommended',
    priority: test.priority,
    created_at: new Date().toISOString()
  }));
  
  config.ab_testing.test_groups.push(...newTests);
  
  if (dryRun) {
    log('info', '[DRY-RUN] Would update ab_testing config with:', newTests);
    return config;
  }
  
  // 备份原配置
  const backupPath = configPath + `.bak.${Date.now()}`;
  fs.copyFileSync(configPath, backupPath);
  log('info', `Backup created: ${backupPath}`);
  
  // 写入新配置
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  log('info', `ab_testing config updated: ${configPath}`);
  
  return config;
}

// ============ 主函数 ============

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const reportFileArg = args.find((arg, i) => arg === '--report-file' && args[i + 1]);
  const reportFile = reportFileArg ? args[args.indexOf(reportFileArg) + 1] : null;
  
  log('info', 'Template Optimizer started', { dryRun, reportFile });
  
  // 1. 读取报告
  let reports;
  if (reportFile) {
    const reportPath = path.join(CONFIG.reportsDir, reportFile);
    const report = readJsonFile(reportPath);
    reports = report ? [{ file: reportFile, ...report }] : [];
  } else {
    reports = readAllReports(CONFIG.reportsDir);
  }
  
  if (reports.length === 0) {
    log('warn', 'No reports found to analyze');
    console.log('No analytics reports found in reports/ directory.');
    return;
  }
  
  log('info', `Loaded ${reports.length} report(s)`);
  
  // 2. 聚合模板数据
  const templateMap = new Map();
  reports.forEach(report => {
    if (report.breakdown && report.breakdown.by_template) {
      report.breakdown.by_template.forEach(t => {
        const existing = templateMap.get(t.template_id) || { sent_count: 0, replied_count: 0 };
        templateMap.set(t.template_id, {
          ...t,
          sent_count: existing.sent_count + t.sent_count,
          replied_count: existing.replied_count + (t.replied_count || 0)
        });
      });
    }
  });
  
  const allTemplates = Array.from(templateMap.values()).map(t => ({
    ...t,
    reply_rate: t.sent_count > 0 ? t.replied_count / t.sent_count : 0,
    characteristics: []
  }));
  
  // 分析每个模板的特征
  allTemplates.forEach(t => {
    Object.assign(t, analyzeTemplateFeatures(t, reports));
  });
  
  log('info', `Analyzed ${allTemplates.length} unique templates`);
  
  // 3. 计算百分位数阈值
  const thresholds = calculatePercentileThresholds(allTemplates);
  log('info', 'Percentile thresholds', thresholds);
  
  // 4. 识别高效和低效模板
  const highPerformers = allTemplates.filter(t => t.reply_rate >= thresholds.top30).sort((a, b) => b.reply_rate - a.reply_rate);
  const lowPerformers = allTemplates.filter(t => t.reply_rate <= thresholds.bottom30).sort((a, b) => a.reply_rate - b.reply_rate);
  
  log('info', `High performers: ${highPerformers.length}, Low performers: ${lowPerformers.length}`);
  
  // 5. 生成分析
  const analysis = {
    generated_at: new Date().toISOString(),
    total_templates: allTemplates.length,
    thresholds,
    high_performers: analyzeHighPerformers(highPerformers, allTemplates),
    low_performers: {
      count: lowPerformers.length,
      templates: lowPerformers
    },
    improvement_suggestions: generateImprovementSuggestions(lowPerformers),
    ab_tests: generateABTestRecommendations(highPerformers, lowPerformers, allTemplates)
  };
  
  // 6. 生成 Markdown 报告
  const date = new Date().toISOString().split('T')[0];
  const mdPath = path.join(CONFIG.obsidianDir, `模板优化报告-${date}.md`);
  
  if (dryRun) {
    log('info', '[DRY-RUN] Would generate Markdown report at:', mdPath);
    console.log('\n=== DRY-RUN MODE ===');
    console.log('Would generate report at:', mdPath);
  } else {
    generateMarkdownReport(analysis, mdPath);
  }
  
  // 7. 生成 JSON 报告
  const jsonPath = path.join(CONFIG.reportsDir, `optimizer-report-${date}.json`);
  if (dryRun) {
    log('info', '[DRY-RUN] Would write JSON report to:', jsonPath);
  } else {
    fs.writeFileSync(jsonPath, JSON.stringify(analysis, null, 2));
    log('info', `JSON report written to ${jsonPath}`);
  }
  
  // 8. 更新 ab_testing 配置
  if (analysis.ab_tests.length > 0) {
    if (dryRun) {
      log('info', '[DRY-RUN] Would update ab_testing config with', analysis.ab_tests.length, 'new tests');
    } else {
      updateABTestingConfig(analysis.ab_tests, CONFIG.trackingSchemaPath);
    }
  }
  
  // 9. 输出摘要
  console.log('\n=== 模板优化分析完成 ===');
  console.log(`分析模板总数：${allTemplates.length}`);
  console.log(`高效模板（Top 30%）：${highPerformers.length} 个`);
  console.log(`低效模板（Bottom 30%）：${lowPerformers.length} 个`);
  console.log(`A/B 测试推荐：${analysis.ab_tests.length} 个`);
  console.log(`改进建议：${analysis.improvement_suggestions.length} 个模板`);
  
  if (dryRun) {
    console.log('\n[DRY-RUN] 未实际写入文件');
  } else {
    console.log(`\n报告已生成：${mdPath}`);
    console.log(`JSON 报告：${jsonPath}`);
  }
  
  log('info', 'Template Optimizer completed');
}

// 运行
if (require.main === module) {
  main();
}

module.exports = { main, analyzeTemplateFeatures, generateABTestRecommendations };
