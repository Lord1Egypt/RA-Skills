/**
 * schema-validator.js — API 响应格式校验器
 *
 * 作为 zhihu-http.js 的验证模块，独立也可运行：
 *   node tests/schema-validator.js
 *
 * S9
 *
 * @module schema-validator
 */

import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { testLog } from '../scripts/zhihu-logger.js';

/** @type {string} 当前文件目录 */
const __dirname = dirname(fileURLToPath(import.meta.url));
/** @type {string} API 端点配置路径 */
const ENDPOINTS_PATH = resolve(__dirname, '..', 'config', 'api-endpoints.json');

// ──────────────────────────────────────────
// Schema 校验规则
// ──────────────────────────────────────────

/**
 * @typedef {object} SchemaRule
 * @property {string[]} required - 必需字段
 * @property {Record<string, string>} types - 字段类型映射
 * @property {Record<string, number>} [minItems] - 最小条目数
 */

/** @type {Record<string, SchemaRule>} */
const SCHEMA_RULES = {
  hotList: {
    required: ['data'],
    types: {
      'data': 'array',
      'data[0].target.title_area.text': 'string',
      'data[0].target.metrics_area.text': 'string',
    },
    minItems: {
      'data': 1,
    },
  },
  search: {
    required: ['data'],
    types: {
      'data': 'array',
    },
    minItems: {
      'data': 0,
    },
  },
  article: {
    required: ['id', 'title'],
    types: {
      'id': 'number',
      'title': 'string',
    },
  },
  user: {
    required: ['id', 'name', 'url_token'],
    types: {
      'id': 'string',
      'name': 'string',
      'headline': 'string',
      'url_token': 'string',
    },
  },
  question: {
    required: ['id', 'title'],
    types: {
      'id': 'number',
      'title': 'string',
      'answer_count': 'number',
      'follower_count': 'number',
    },
  },
  answers: {
    required: ['data'],
    types: {
      'data': 'array',
    },
  },
};

/**
 * 通过点路径获取对象值
 * @param {object} obj - 源对象
 * @param {string} path - 点路径（如 "data[0].name"）
 * @returns {*} 路径对应的值
 */
function getValueByPath(obj, path) {
  const keys = path.replace(/\[(\d+)\]/g, '.$1').split('.');
  let current = obj;
  for (const key of keys) {
    if (current == null || current === undefined) return undefined;
    current = current[key];
  }
  return current;
}

/**
 * 检测值的运行时类型
 * @param {*} value - 任意值
 * @returns {string} 类型字符串 ("array" | "string" | "number" | ...)
 */
function detectType(value) {
  if (Array.isArray(value)) return 'array';
  return typeof value;
}

/**
 * @typedef {object} ValidationResult
 * @property {boolean} valid - 是否通过校验
 * @property {string[]} errors - 错误信息
 * @property {string[]} warnings - 警告信息
 */

/**
 * 校验 API 响应数据是否符合预期 Schema
 *
 * @param {string} endpointName - 端点名称
 * @param {object} data - API 响应数据
 * @returns {ValidationResult} 校验结果
 */
export function validateResponse(endpointName, data) {
  const rules = SCHEMA_RULES[endpointName];
  if (!rules) {
    return { valid: true, errors: [], warnings: [`未知端点: ${endpointName}`] };
  }

  /** @type {string[]} */
  const errors = [];
  /** @type {string[]} */
  const warnings = [];

  // 1. 检查必需字段
  for (const field of rules.required || []) {
    const value = data[field];
    if (value === undefined || value === null) {
      errors.push(`缺少必需字段: ${field}`);
    }
  }

  // 2. 检查字段类型
  for (const [fieldPath, expectedType] of Object.entries(rules.types || {})) {
    const value = getValueByPath(data, fieldPath);
    if (value !== undefined && value !== null) {
      const actualType = detectType(value);
      if (actualType !== expectedType) {
        warnings.push(`字段 ${fieldPath} 类型不符: 期望 ${expectedType}, 实际 ${actualType}`);
      }
    }
  }

  // 3. 检查最小条目数
  for (const [fieldPath, minCount] of Object.entries(rules.minItems || {})) {
    const value = getValueByPath(data, fieldPath);
    if (Array.isArray(value) && value.length < minCount) {
      warnings.push(`字段 ${fieldPath} 条目数 ${value.length} 小于最小值 ${minCount}`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

// ──────────────────────────────────────────
// CLI 模式
// ──────────────────────────────────────────

/**
 * CLI 入口
 * @returns {void}
 */
function main() {
  console.log('📋 API 响应 Schema 校验器');
  console.log('');

  if (!existsSync(ENDPOINTS_PATH)) {
    testLog.error('api-endpoints.json 不存在', { path: ENDPOINTS_PATH });
    console.error('❌ 未找到 api-endpoints.json');
    process.exit(1);
  }

  const config = JSON.parse(readFileSync(ENDPOINTS_PATH, 'utf-8'));
  console.log(`   端点文件: ${ENDPOINTS_PATH}`);
  console.log(`   版本: ${config.version}`);
  console.log(`   端点数量: ${Object.keys(config.endpoints).length}`);
  console.log('');

  let allPass = true;

  for (const [name, endpoint] of Object.entries(config.endpoints)) {
    const schemaInConfig = endpoint.responseSchema;
    if (!schemaInConfig) {
      console.log(`   ⚠️  ${name}: 缺少 Schema 定义`);
      continue;
    }

    const rules = SCHEMA_RULES[name];
    if (!rules) {
      console.log(`   ⚠️  ${name}: 无验证规则（可添加）`);
      continue;
    }

    const requiredMatch = (rules.required || []).every(f => schemaInConfig[f]);
    if (!requiredMatch) {
      testLog.warn('Schema 不一致', { endpoint: name });
      console.log(`   ⚠️  ${name}: Schema 与实际验证规则不一致`);
      allPass = false;
    } else {
      console.log(`   ✅  ${name}: Schema 定义完整`);
    }
  }

  console.log('');
  if (allPass) {
    testLog.info('Schema 检查通过');
    console.log('✅ 所有端点 Schema 检查通过');
  } else {
    testLog.warn('部分端点 Schema 需更新');
    console.warn('⚠️  部分端点 Schema 需更新');
  }
}

// 独立运行时执行 CLI
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}

export default { validateResponse };
