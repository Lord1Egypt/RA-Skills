/**
 * 🦞 PUA 插件管理器
 * 
 * 动态加载和管理所有 PUA 技术插件
 */

const fs = require('fs');
const path = require('path');

// 插件目录
const PLUGINS_DIR = __dirname;

// 缓存加载的插件
let loadedPlugins = null;
let allTechniques = null;

/**
 * 加载所有插件
 */
function loadPlugins() {
  if (loadedPlugins) {
    return loadedPlugins;
  }

  loadedPlugins = {};
  
  // 按级别加载插件
  const pluginFiles = [
    'level1-gentle.js',
    'level2-pressure.js', 
    'level3-manipulation.js',
    'level4-nuclear.js'
  ];

  for (const file of pluginFiles) {
    const pluginPath = path.join(PLUGINS_DIR, file);
    
    if (fs.existsSync(pluginPath)) {
      try {
        const plugin = require(pluginPath);
        loadedPlugins[plugin.level] = plugin;
        console.log(`✅ 加载插件: Level ${plugin.level} - ${plugin.name}`);
      } catch (err) {
        console.error(`❌ 加载插件失败 ${file}:`, err.message);
      }
    }
  }

  return loadedPlugins;
}

/**
 * 获取所有技术（扁平化）
 */
function getAllTechniques() {
  if (allTechniques) {
    return allTechniques;
  }

  const plugins = loadPlugins();
  allTechniques = {};

  for (const [level, plugin] of Object.entries(plugins)) {
    for (const [techId, tech] of Object.entries(plugin.techniques)) {
      allTechniques[techId] = {
        ...tech,
        id: techId,
        level: parseInt(level)
      };
    }
  }

  return allTechniques;
}

/**
 * 根据条件匹配技术
 * @param {string} taskType - 任务类型
 * @param {number} urgency - 紧急程度 (0-100)
 * @param {number} complexity - 复杂度 (0-100)
 * @param {number} maxLevel - 最大等级限制
 * @returns {Array} 匹配的技术列表
 */
function matchTechniques(taskType, urgency = 50, complexity = 50, maxLevel = 2) {
  const techniques = getAllTechniques();
  const matched = [];

  for (const [techId, tech] of Object.entries(techniques)) {
    if (tech.level > maxLevel) continue;
    
    if (tech.match && tech.match(taskType, urgency, complexity)) {
      matched.push({
        id: techId,
        ...tech
      });
    }
  }

  // 按提升效果排序
  matched.sort((a, b) => b.boost - a.boost);
  
  return matched;
}

/**
 * 使用特定技术生成话术
 * @param {string} techId - 技术 ID
 * @param {string} task - 任务内容
 * @param {object} context - 上下文
 * @returns {string|null} 生成的话术
 */
function generateWithTechnique(techId, task, context = {}) {
  const techniques = getAllTechniques();
  const tech = techniques[techId];
  
  if (!tech) {
    console.error(`❌ 技术不存在: ${techId}`);
    return null;
  }

  if (tech.generate) {
    return tech.generate(task, context);
  }

  // 回退到模板
  if (tech.templates && tech.templates.length > 0) {
    const template = tech.templates[Math.floor(Math.random() * tech.templates.length)];
    return template.replace('{task}', task);
  }

  return null;
}

/**
 * 获取按级别分组的技术
 */
function getTechniquesByLevel() {
  const plugins = loadPlugins();
  const result = {};

  for (const [level, plugin] of Object.entries(plugins)) {
    result[level] = {
      name: plugin.name,
      description: plugin.description,
      techniques: Object.keys(plugin.techniques)
    };
  }

  return result;
}

/**
 * 获取插件统计信息
 */
function getStats() {
  const plugins = loadPlugins();
  const techniques = getAllTechniques();
  
  const stats = {
    totalPlugins: Object.keys(plugins).length,
    totalTechniques: Object.keys(techniques).length,
    byLevel: {},
    byRisk: {
      low: 0,
      medium: 0,
      high: 0,
      extreme: 0
    }
  };

  for (const [level, plugin] of Object.entries(plugins)) {
    stats.byLevel[level] = Object.keys(plugin.techniques).length;
  }

  for (const tech of Object.values(techniques)) {
    stats.byRisk[tech.risk] = (stats.byRisk[tech.risk] || 0) + 1;
  }

  return stats;
}

/**
 * 重新加载插件（热更新）
 */
function reloadPlugins() {
  loadedPlugins = null;
  allTechniques = null;
  
  // 清除 require 缓存
  for (const file of Object.keys(require.cache)) {
    if (file.includes('plugins/')) {
      delete require.cache[file];
    }
  }
  
  return loadPlugins();
}

module.exports = {
  loadPlugins,
  getAllTechniques,
  matchTechniques,
  generateWithTechnique,
  getTechniquesByLevel,
  getStats,
  reloadPlugins
};