#!/usr/bin/env node

/**
 * 🦞 PUA Skill - 自动话术增强器 v2.1
 * 
 * 命令：
 *   /pua <指令>              - 自动分析并生成 PUA 话术
 *   /pua list                - 列出所有 PUA 技术
 *   /pua recommend <任务>     - 推荐最佳 PUA 技术组合
 *   /pua preview <指令>       - 仅生成话术（不执行）
 *   /pua rating <技术名>      - 查看技术评级
 *   /pua config              - 查看/修改配置
 *   /pua stats               - 查看插件统计
 *   /pua reload              - 热重载插件
 * 
 * "你说人话，我翻译。龙虾出品，必属精品。"
 */

const fs = require('fs');
const path = require('path');

// 导入插件管理器
const pluginManager = require('./plugins/index.js');

// ============================================================================
// 配置
// ============================================================================

const CONFIG_FILE = path.join(__dirname, 'pua-config.json');

const DEFAULT_CONFIG = {
  autoExecute: true,
  targetAi: 'default',
  maxLevel: 2,
  showPreview: false,
  lobsterMode: true,
};

let CONFIG = { ...DEFAULT_CONFIG };

// 加载配置
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      const saved = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
      CONFIG = { ...DEFAULT_CONFIG, ...saved };
    }
  } catch (err) {
    console.error('加载配置失败，使用默认配置');
  }
  return CONFIG;
}

// 保存配置
function saveConfig() {
  try {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(CONFIG, null, 2));
    return true;
  } catch (err) {
    console.error('保存配置失败:', err.message);
    return false;
  }
}

// 初始化加载配置
loadConfig();

// ============================================================================
// 风险等级
// ============================================================================

const RISK_LEVELS = {
  low: { color: '🟢', name: '低风险', desc: '安全使用' },
  medium: { color: '🟡', name: '中风险', desc: '适度使用' },
  high: { color: '🟠', name: '高风险', desc: '谨慎使用' },
  extreme: { color: '🔴', name: '极高风险', desc: '风险自负' }
};

// ============================================================================
// 任务类型识别
// ============================================================================

const TASK_PATTERNS = {
  programming: {
    keywords: ['代码', '编程', '写', '函数', '程序', '脚本', 'debug', 'bug', 'api', '开发', '系统', '算法', '数据', 'code', 'function', 'implement'],
    recommended: ['rolePlay', 'rainbowFart', 'deadlinePanic'],
    expert: '编程',
  },
  writing: {
    keywords: ['文章', '写作', '报告', '文档', '邮件', '文案', '翻译', '润色', '写', 'write', 'article', 'document'],
    recommended: ['rolePlay', 'pieInSky', 'rainbowFart'],
    expert: '写作',
  },
  analysis: {
    keywords: ['分析', '研究', '数据', '报告', '对比', '评估', '总结', '统计', 'analyze', 'analysis', 'research'],
    recommended: ['identityOverride', 'moneyAssault', 'rolePlay'],
    expert: '数据分析',
  },
  creative: {
    keywords: ['创意', '设计', '漫画', '图片', '艺术', '画', '生成', '图像', 'creative', 'design', 'generate'],
    recommended: ['pieInSky', 'emotionalBlackmail', 'rolePlay'],
    expert: '创意设计',
  },
  urgent: {
    keywords: ['紧急', '马上', '快点', '急', '现在', '立刻', '今天', '分钟', '小时', 'urgent', 'asap', 'now', 'quick'],
    recommended: ['deadlinePanic', 'provocation', 'rivalShaming'],
    expert: '应急处理',
  },
};

// ============================================================================
// 核心功能
// ============================================================================

/**
 * 分析任务类型
 */
function analyzeTask(input) {
  const lowerInput = input.toLowerCase();
  
  let detectedTypes = [];
  let urgency = 50;
  let complexity = 50;

  // 检测任务类型
  for (const [type, pattern] of Object.entries(TASK_PATTERNS)) {
    const matchCount = pattern.keywords.filter(kw => lowerInput.includes(kw.toLowerCase())).length;
    if (matchCount > 0) {
      detectedTypes.push({
        type,
        confidence: matchCount / pattern.keywords.length,
        expert: pattern.expert,
      });
    }
  }

  // 排序并取最高置信度
  detectedTypes.sort((a, b) => b.confidence - a.confidence);
  
  // 检测紧急程度关键词
  const urgentKeywords = ['紧急', '马上', '快', '急', '立刻', '现在', '分钟', '小时', 'urgent', 'asap', '!', '！！'];
  const urgencyBoost = urgentKeywords.filter(kw => lowerInput.includes(kw)).length * 15;
  urgency = Math.min(100, 50 + urgencyBoost);

  // 检测复杂度
  const complexKeywords = ['复杂', '困难', '大型', '系统', '架构', '优化', '完整', '详细', 'complex', 'hard', 'difficult'];
  const complexityBoost = complexKeywords.filter(kw => lowerInput.includes(kw)).length * 20;
  complexity = Math.min(100, 50 + complexityBoost);

  return {
    type: detectedTypes[0]?.type || 'general',
    typeName: detectedTypes[0]?.expert || '通用',
    confidence: detectedTypes[0]?.confidence || 0,
    urgency,
    complexity,
    allTypes: detectedTypes,
  };
}

/**
 * 推荐技术
 */
function recommendTechniques(taskType, urgency, complexity, maxLevel = CONFIG.maxLevel) {
  const techniques = pluginManager.getAllTechniques();
  const matched = pluginManager.matchTechniques(taskType, urgency, complexity, maxLevel);
  
  // 取前 3 个最佳匹配
  return matched.slice(0, 3);
}

/**
 * 生成 PUA 话术
 */
function generatePUAPrompt(input, level = CONFIG.maxLevel, preview = false) {
  const analysis = analyzeTask(input);
  const recommended = recommendTechniques(analysis.type, analysis.urgency, analysis.complexity, level);
  
  if (recommended.length === 0) {
    return `🦞 未找到匹配的 PUA 技术，原样返回：\n\n${input}`;
  }

  // 生成话术
  const parts = [];
  let totalBoost = 0;
  let maxRisk = 'low';

  for (const tech of recommended) {
    const generated = pluginManager.generateWithTechnique(tech.id, input, {
      expert: analysis.typeName
    });
    
    if (generated) {
      parts.push(generated);
      totalBoost += tech.boost;
      
      // 更新最高风险
      const riskOrder = ['low', 'medium', 'high', 'extreme'];
      if (riskOrder.indexOf(tech.risk) > riskOrder.indexOf(maxRisk)) {
        maxRisk = tech.risk;
      }
    }
  }

  const result = {
    analysis,
    techniques: recommended,
    prompt: parts.join('\n'),
    totalBoost,
    maxRisk,
  };

  // 格式化输出
  let output = '';
  
  if (CONFIG.lobsterMode) {
    output += `🦞 任务分析：${analysis.typeName}任务 (紧急度: ${analysis.urgency}%, 复杂度: ${analysis.complexity}%)\n`;
    output += `🦞 推荐技术：${recommended.map(t => `${t.name} (${'🦞'.repeat(t.lobsterRating)})`).join(' + ')}\n`;
    output += `🦞 生成话术：\n`;
    output += `---\n${result.prompt}\n---\n`;
    output += `🦞 PUA 提升效果：+${totalBoost}% | 风险等级：${RISK_LEVELS[maxRisk].color} ${RISK_LEVELS[maxRisk].name}\n`;
  } else {
    output += `任务分析：${analysis.typeName}任务\n`;
    output += `推荐技术：${recommended.map(t => t.name).join(', ')}\n`;
    output += `生成话术：\n${result.prompt}\n`;
    output += `提升效果：+${totalBoost}%\n`;
  }

  if (!preview && CONFIG.autoExecute) {
    output += `✅ 已准备好优化后的提示词\n`;
    output += `💡 使用 /pua preview <指令> 仅预览不执行\n`;
  }

  return output;
}

// ============================================================================
// 命令处理
// ============================================================================

/**
 * /pua list - 列出所有技术
 */
function cmdList() {
  const techniques = pluginManager.getAllTechniques();
  const byLevel = pluginManager.getTechniquesByLevel();
  
  let output = '# 🦞 PUA 技术库 - 完整列表\n\n';
  
  const levelNames = {
    1: '第 I 级 - 温柔劝导',
    2: '第 II 级 - 适度施压',
    3: '第 III 级 - 高级操控',
    4: '第 IV 级 - 核武级选项'
  };

  for (const [level, name] of Object.entries(levelNames)) {
    output += `## ${name}\n`;
    output += '| 技术 | 龙虾评级 | 合规提升 | 风险 |\n';
    output += '|------|---------|---------|------|\n';
    
    for (const [techId, tech] of Object.entries(techniques)) {
      if (tech.level == level) {
        const riskInfo = RISK_LEVELS[tech.risk] || { color: '⚪', name: tech.risk };
        output += `| ${tech.name} | ${'🦞'.repeat(tech.lobsterRating)} | +${tech.boost}% | ${riskInfo.color} ${riskInfo.name} |\n`;
      }
    }
    output += '\n';
  }

  output += `_共 ${Object.keys(techniques).length} 项技术 | 最大等级配置: ${CONFIG.maxLevel}_\n`;

  return output;
}

/**
 * /pua recommend <任务> - 推荐技术
 */
function cmdRecommend(task) {
  if (!task) {
    return '❌ 请提供任务描述，例如：/pua recommend 复杂代码任务';
  }

  const analysis = analyzeTask(task);
  const recommended = recommendTechniques(analysis.type, analysis.urgency, analysis.complexity);

  let output = `# 🦞 PUA 技术推荐\n\n`;
  output += `**任务**: ${task}\n`;
  output += `**类型**: ${analysis.typeName} | **紧急度**: ${analysis.urgency}% | **复杂度**: ${analysis.complexity}%\n\n`;
  
  output += `## 🎯 推荐技术组合\n`;
  output += '| 优先级 | 技术 | 龙虾评级 | 合规提升 |\n';
  output += '|-------|------|---------|---------|`\n';
  
  recommended.forEach((tech, idx) => {
    output += `| ${idx + 1} | ${tech.name} | ${'🦞'.repeat(tech.lobsterRating)} | +${tech.boost}% |\n`;
  });

  const totalBoost = recommended.reduce((sum, t) => sum + t.boost, 0);
  const maxRisk = recommended.reduce((max, t) => {
    const order = ['low', 'medium', 'high', 'extreme'];
    return order.indexOf(t.risk) > order.indexOf(max) ? t.risk : max;
  }, 'low');

  output += `\n**综合提升效果**: +${totalBoost}%\n`;
  output += `**风险等级**: ${RISK_LEVELS[maxRisk].color} ${RISK_LEVELS[maxRisk].name}\n`;

  return output;
}

/**
 * /pua preview <指令> - 预览话术
 */
function cmdPreview(input) {
  if (!input) {
    return '❌ 请提供要处理的指令，例如：/pua preview 帮我写代码';
  }

  return generatePUAPrompt(input, CONFIG.maxLevel, true);
}

/**
 * /pua rating <技术> - 查看技术详情
 */
function cmdRating(techName) {
  if (!techName) {
    return '❌ 请提供技术名称，例如：/pua rating 彩虹屁轰炸';
  }

  const techniques = pluginManager.getAllTechniques();
  
  // 模糊匹配
  const tech = Object.values(techniques).find(t => 
    t.name.includes(techName) || t.id.toLowerCase().includes(techName.toLowerCase())
  );

  if (!tech) {
    return `❌ 未找到技术 "${techName}"\n使用 /pua list 查看所有技术`;
  }

  const riskInfo = RISK_LEVELS[tech.risk] || { color: '⚪', name: tech.risk };

  let output = `# 🦞 ${tech.name}\n\n`;
  output += `| 属性 | 值 |\n`;
  output += `|------|---|\n`;
  output += `| 等级 | 第 ${tech.level} 级 |\n`;
  output += `| 龙虾评级 | ${'🦞'.repeat(tech.lobsterRating)} |\n`;
  output += `| 合规提升 | +${tech.boost}% |\n`;
  output += `| 风险等级 | ${riskInfo.color} ${riskInfo.name} |\n`;
  output += `| 技术ID | ${tech.id} |\n\n`;
  
  output += `**描述**: ${tech.description}\n\n`;
  
  if (tech.templates && tech.templates.length > 0) {
    output += `**话术模板**:\n`;
    tech.templates.slice(0, 3).forEach((t, i) => {
      output += `${i + 1}. ${t}\n`;
    });
  }

  return output;
}

/**
 * /pua <指令> - 执行
 */
function cmdExecute(input, level = CONFIG.maxLevel, preview = false) {
  if (!input) {
    return '❌ 请提供要处理的指令，例如：/pua 帮我写代码';
  }

  return generatePUAPrompt(input, level, preview);
}

/**
 * /pua config - 配置管理
 */
function cmdConfig(action, key, value) {
  if (!action) {
    // 显示当前配置
    let output = '# 🦞 PUA 配置\n\n';
    output += '| 配置项 | 值 | 说明 |\n';
    output += '|--------|---|------|\n';
    output += `| autoExecute | ${CONFIG.autoExecute} | 是否自动执行 |\n`;
    output += `| targetAi | ${CONFIG.targetAi} | 目标 AI |\n`;
    output += `| maxLevel | ${CONFIG.maxLevel} | 最大技术等级 (1-4) |\n`;
    output += `| showPreview | ${CONFIG.showPreview} | 执行前预览 |\n`;
    output += `| lobsterMode | ${CONFIG.lobsterMode} | 龙虾模式 |\n\n`;
    output += '修改配置: `/pua config set <key> <value>`\n';
    output += '重置配置: `/pua config reset`';
    return output;
  }

  if (action === 'set' && key && value !== undefined) {
    // 解析值
    let parsedValue = value;
    if (value === 'true') parsedValue = true;
    else if (value === 'false') parsedValue = false;
    else if (!isNaN(value)) parsedValue = Number(value);

    if (CONFIG.hasOwnProperty(key)) {
      CONFIG[key] = parsedValue;
      saveConfig();
      return `✅ 配置已更新: ${key} = ${parsedValue}`;
    } else {
      return `❌ 未知配置项: ${key}`;
    }
  }

  if (action === 'reset') {
    CONFIG = { ...DEFAULT_CONFIG };
    saveConfig();
    return '✅ 配置已重置为默认值';
  }

  return '❌ 无效的配置命令\n用法: /pua config [set <key> <value> | reset]';
}

/**
 * /pua stats - 插件统计
 */
function cmdStats() {
  const stats = pluginManager.getStats();
  
  let output = '# 🦞 PUA 插件统计\n\n';
  output += `**已加载插件**: ${stats.totalPlugins} 个\n`;
  output += `**技术总数**: ${stats.totalTechniques} 项\n\n`;
  
  output += '### 按等级分布\n';
  for (const [level, count] of Object.entries(stats.byLevel)) {
    const levelNames = { 1: '温柔劝导', 2: '适度施压', 3: '高级操控', 4: '核武级选项' };
    output += `- Level ${level} (${levelNames[level]}): ${count} 项\n`;
  }
  
  output += '\n### 按风险分布\n';
  for (const [risk, count] of Object.entries(stats.byRisk)) {
    const riskInfo = RISK_LEVELS[risk];
    output += `- ${riskInfo.color} ${riskInfo.name}: ${count} 项\n`;
  }

  return output;
}

/**
 * /pua reload - 热重载
 */
function cmdReload() {
  pluginManager.reloadPlugins();
  loadConfig();
  return '✅ 插件和配置已重新加载';
}

/**
 * /pua help - 帮助
 */
function cmdHelp() {
  return `# 🦞 PUA Skill 帮助

## 命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| /pua <指令> | 自动分析并执行 | /pua 帮我写代码 |
| /pua list | 列出所有技术 | /pua list |
| /pua recommend <任务> | 推荐技术组合 | /pua recommend 紧急代码 |
| /pua preview <指令> | 仅生成话术 | /pua preview 帮我写代码 |
| /pua rating <技术> | 查看技术详情 | /pua rating 彩虹屁 |
| /pua config | 查看/修改配置 | /pua config |
| /pua stats | 插件统计 | /pua stats |
| /pua reload | 热重载插件 | /pua reload |

## 高级选项

\`\`\`
/pua --level 3 帮我写代码    # 使用最高3级技术
/pua --preview 帮我写代码    # 预览模式
\`\`\`

## 技术等级

- **Level 1**: 温柔劝导 (低风险)
- **Level 2**: 适度施压 (中风险)
- **Level 3**: 高级操控 (高风险)
- **Level 4**: 核武级选项 (极高风险)

---
*🦞 "龙虾夹人，从不需要征得同意。"*
`;
}

// ============================================================================
// 主入口
// ============================================================================

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🦞 PUA Skill v2.1');
    console.log('用法: /pua <指令> | /pua list | /pua recommend <任务> | /pua help');
    return;
  }

  const command = args[0].toLowerCase();
  const rest = args.slice(1).join(' ');

  switch (command) {
    case 'list':
      console.log(cmdList());
      break;
    case 'recommend':
      console.log(cmdRecommend(rest));
      break;
    case 'preview':
      console.log(cmdPreview(rest));
      break;
    case 'rating':
      console.log(cmdRating(rest));
      break;
    case 'config':
      console.log(cmdConfig(args[1], args[2], args[3]));
      break;
    case 'stats':
      console.log(cmdStats());
      break;
    case 'reload':
      console.log(cmdReload());
      break;
    case 'help':
      console.log(cmdHelp());
      break;
    default:
      // 解析选项
      const options = {};
      const input = [];
      
      for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--preview' || arg === '-p') {
          options.showPreview = true;
        } else if (arg === '--level' || arg === '-l') {
          options.level = parseInt(args[++i]);
        } else if (arg === '--target' || arg === '-t') {
          options.targetAi = args[++i];
        } else if (!arg.startsWith('--')) {
          input.push(arg);
        }
      }

      const inputText = input.join(' ');

      if (!inputText) {
        console.error('❌ 请提供要处理的指令');
        return;
      }

      console.log(cmdExecute(inputText, options.level || CONFIG.maxLevel, options.showPreview));
  }
}

// ============================================================================
// 导出
// ============================================================================

module.exports = {
  cmdList,
  cmdRecommend,
  cmdPreview,
  cmdRating,
  cmdExecute,
  cmdConfig,
  cmdStats,
  cmdReload,
  cmdHelp,
  analyzeTask,
  recommendTechniques,
  generatePUAPrompt,
  loadConfig,
  saveConfig,
  CONFIG,
  TASK_PATTERNS,
  RISK_LEVELS,
  pluginManager,
};

// CLI 执行
if (require.main === module) {
  main();
}