#!/usr/bin/env node
/**
 * HIIC日报配置加载器
 * 用于加载和合并产业配置、数据源配置
 */

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * 加载配置文件
 * @param {string} configPath - 配置文件路径
 * @returns {object|null} 配置对象或null
 */
function loadConfigFile(configPath) {
  if (!existsSync(configPath)) {
    return null;
  }
  
  try {
    const content = readFileSync(configPath, 'utf-8');
    return JSON.parse(content);
  } catch (err) {
    console.error(`❌ 加载配置文件失败: ${configPath}`);
    console.error(`   错误: ${err.message}`);
    return null;
  }
}

/**
 * 加载所有配置
 * @param {string} customConfigDir - 自定义配置目录（可选）
 * @returns {object} 合并后的配置
 */
export function loadConfig(customConfigDir = null) {
  const skillDir = join(__dirname, '..');
  const defaultConfigDir = join(skillDir, 'config', 'defaults');
  
  // 1. 加载默认配置
  const defaultIndustries = loadConfigFile(join(defaultConfigDir, 'industries.json'));
  const defaultSources = loadConfigFile(join(defaultConfigDir, 'sources.json'));
  const defaultTopics = loadConfigFile(join(defaultConfigDir, 'topics.json'));
  
  // 2. 加载自定义配置（如果存在）
  let customIndustries = null;
  let customSources = null;
  let customTopics = null;
  
  if (customConfigDir) {
    customIndustries = loadConfigFile(join(customConfigDir, 'industries.json'));
    customSources = loadConfigFile(join(customConfigDir, 'sources.json'));
    customTopics = loadConfigFile(join(customConfigDir, 'topics.json'));
  }
  
  // 3. 合并配置
  const config = {
    industries: [],
    sources: [],
    topics: []
  };
  
  // 合并产业配置
  if (defaultIndustries?.industries) {
    config.industries = defaultIndustries.industries;
  }
  if (customIndustries?.industries) {
    // 自定义产业会覆盖同名产业
    const customIds = new Set(customIndustries.industries.map(i => i.id));
    config.industries = config.industries.filter(i => !customIds.has(i.id));
    config.industries.push(...customIndustries.industries);
  }
  
  // 合并数据源配置
  if (defaultSources?.sources) {
    config.sources = defaultSources.sources;
  }
  if (customSources?.sources) {
    // 自定义数据源追加到默认数据源
    const customIds = new Set(customSources.sources.map(s => s.id));
    config.sources = config.sources.filter(s => !customIds.has(s.id));
    config.sources.push(...customSources.sources);
  }
  
  // 合并主题配置
  if (defaultTopics?.topics) {
    config.topics = defaultTopics.topics;
  }
  if (customTopics?.topics) {
    const customIds = new Set(customTopics.topics.map(t => t.id));
    config.topics = config.topics.filter(t => !customIds.has(t.id));
    config.topics.push(...customTopics.topics);
  }
  
  return config;
}

/**
 * 根据产业名称查找产业配置
 * @param {string} industryName - 产业名称
 * @param {object} config - 配置对象
 * @returns {object|null} 产业配置或null
 */
export function findIndustry(industryName, config) {
  return config.industries.find(industry => 
    industry.name === industryName || 
    industry.id === industryName ||
    industry.keywords.some(kw => industryName.includes(kw))
  );
}

/**
 * 获取启用的产业列表
 * @param {object} config - 配置对象
 * @returns {array} 启用的产业列表
 */
export function getEnabledIndustries(config) {
  return config.industries.filter(industry => industry.enabled);
}

/**
 * 获取启用的数据源列表
 * @param {object} config - 配置对象
 * @returns {array} 启用的数据源列表
 */
export function getEnabledSources(config) {
  return config.sources.filter(source => source.enabled);
}

// CLI 入口
if (process.argv[1] === __filename) {
  const args = process.argv.slice(2);
  const customConfigDir = args[0] || null;
  
  const config = loadConfig(customConfigDir);
  
  console.log(JSON.stringify(config, null, 2));
}
