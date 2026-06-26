/**
 * Knowledge Graph Configuration - External entity types loader
 * 
 * Loads entity types from config file instead of hardcoding.
 * Supports custom entity types per domain.
 * 
 * @module graph/entity_config
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const HOME = process.env.HOME || '/root';
const CONFIG_DIR = join(HOME, '.openclaw', 'workspace', 'memory', 'config');
const ENTITY_CONFIG_FILE = join(CONFIG_DIR, 'entity_types.json');

/**
 * Default entity type definitions
 * Can be overridden by entity_types.json config
 */
export const DEFAULT_ENTITY_TYPES = {
  person: {
    label: '人物',
    labelEn: 'Person',
    color: '#667eea',
    patterns: ['@([^\s@,，、。！？!?,.\n]+)'],
    keywords: ['用户', '刘总', '我', '你', '他', '她', '老板', '同事'],
    priority: 10,
  },
  organization: {
    label: '组织',
    labelEn: 'Organization',
    color: '#10b981',
    patterns: ['([^\s]{2,20})(?:有限公司|股份有限公司|Ltd|Inc|Corp|实验室|研究院|团队|部门|公司)'],
    keywords: [],
    priority: 8,
  },
  project: {
    label: '项目',
    labelEn: 'Project',
    color: '#f59e0b',
    patterns: ['#([^\s#,，、。！？!?,.\n]+)'],
    keywords: ['项目', '龙宫', '官网', '重构', '开发', '迭代', '版本'],
    priority: 9,
  },
  topic: {
    label: '主题',
    labelEn: 'Topic',
    color: '#8b5cf6',
    patterns: ['##([^\s#,，、。！？!?,.\n]+)'],
    keywords: ['话题', '主题', '讨论', '问题', '方案'],
    priority: 6,
  },
  tool: {
    label: '工具',
    labelEn: 'Tool',
    color: '#06b6d4',
    patterns: [],
    keywords: [
      '飞书', '钉钉', 'Slack', '微信', 'QQ', '企业微信', 'Teams', 'Telegram',
      'VSCode', 'Vim', 'Neovim', 'Emacs', 'JetBrains',
      'GitHub', 'GitLab', 'Gitee', 'Jira', 'Notion', 'Figma',
      'Docker', 'Kubernetes', 'k8s', 'Nginx', 'Redis', 'MongoDB', 'MySQL', 'PostgreSQL',
      'Python', 'JavaScript', 'TypeScript', 'Go', 'Rust', 'Java', 'C++', 'Ruby',
      'Ollama', 'OpenAI', 'Claude', 'DeepSeek', 'Qwen', 'Kimi', 'ChatGPT', 'Cursor',
      'OpenClaw', 'MetaGPT', 'Unified Memory',
    ],
    priority: 7,
  },
  location: {
    label: '地点',
    labelEn: 'Location',
    color: '#ef4444',
    patterns: [],
    keywords: ['北京', '上海', '深圳', '杭州', '广州', '成都', '办公室', '公司', '家里'],
    priority: 5,
  },
  date: {
    label: '日期',
    labelEn: 'Date',
    color: '#ec4899',
    patterns: [
      '(\d{4}年\d{1,2}月\d{1,2}日)',
      '(\d{4}-\d{2}-\d{2})',
      '(\d{1,2}/\d{1,2}/\d{4})',
      '(\d{1,2}月\d{1,2}日)',
    ],
    temporalKeywords: ['今天', '明天', '昨天', '后天', '前天', '周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    priority: 4,
  },
  event: {
    label: '事件',
    labelEn: 'Event',
    color: '#84cc16',
    patterns: [],
    keywords: [
      '会议', 'meeting', '讨论', '评审', '面试', '发布会', '发布', '上线', '版本发布',
      'debug', '重构', '迁移', '部署', '培训', '周会', '例会', '头脑风暴',
      '出差', '旅行', '度假', '生日', '节日',
    ],
    priority: 6,
  },
};

/**
 * Load entity config from file
 * Falls back to defaults if file doesn't exist
 */
export function loadEntityConfig() {
  if (!existsSync(ENTITY_CONFIG_FILE)) {
    // Create default config
    saveEntityConfig(DEFAULT_ENTITY_TYPES);
    return DEFAULT_ENTITY_TYPES;
  }
  
  try {
    const content = readFileSync(ENTITY_CONFIG_FILE, 'utf-8');
    const config = JSON.parse(content);
    // Merge with defaults to ensure all fields exist
    return mergeWithDefaults(config);
  } catch (err) {
    console.warn(`[EntityConfig] Failed to load config: ${err.message}, using defaults`);
    return DEFAULT_ENTITY_TYPES;
  }
}

/**
 * Save entity config to file
 */
export function saveEntityConfig(config) {
  if (!existsSync(CONFIG_DIR)) {
    mkdirSync(CONFIG_DIR, { recursive: true });
  }
  writeFileSync(ENTITY_CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
}

/**
 * Merge loaded config with defaults
 */
function mergeWithDefaults(config) {
  const merged = { ...DEFAULT_ENTITY_TYPES };
  
  for (const [type, loadedDef] of Object.entries(config)) {
    if (merged[type]) {
      merged[type] = { ...merged[type], ...loadedDef };
    } else {
      // New custom type
      merged[type] = { ...loadedDef, priority: loadedDef.priority || 5 };
    }
  }
  
  return merged;
}

/**
 * Add a custom entity type at runtime
 */
export function addEntityType(typeName, definition) {
  const config = loadEntityConfig();
  config[typeName] = {
    ...definition,
    priority: definition.priority || 5,
  };
  saveEntityConfig(config);
  return config;
}

/**
 * Remove an entity type at runtime
 */
export function removeEntityType(typeName) {
  const config = loadEntityConfig();
  if (DEFAULT_ENTITY_TYPES[typeName]) {
    // Don't remove built-in types, just clear keywords
    config[typeName].keywords = [];
    config[typeName].patterns = [];
  } else {
    delete config[typeName];
  }
  saveEntityConfig(config);
  return config;
}

/**
 * Get entity types sorted by priority
 */
export function getEntityTypesByPriority() {
  const config = loadEntityConfig();
  return Object.entries(config)
    .sort(([, a], [, b]) => (b.priority || 5) - (a.priority || 5))
    .map(([name, def]) => ({ name, ...def }));
}

/**
 * Reload config (for hot-reload support)
 */
export function reloadEntityConfig() {
  return loadEntityConfig();
}

export default {
  loadEntityConfig,
  saveEntityConfig,
  addEntityType,
  removeEntityType,
  getEntityTypesByPriority,
  reloadEntityConfig,
  DEFAULT_ENTITY_TYPES,
};
