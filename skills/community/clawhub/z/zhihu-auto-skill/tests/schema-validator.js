/**
 * schema-validator.js — API 响应格式校验器
 *
 * 作为 zhihu-http.js 的验证模块，独立也可运行：
 *   node tests/schema-validator.js
 *
 * S9
 */

import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ENDPOINTS_PATH = resolve(__dirname, '..', 'config', 'api-endpoints.json');

// ──────────────────────────────────────────
// Schema 校验规则
// ──────────────────────────────────────────

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

function getValueByPath(obj, path) {
  const keys = path.replace(/\[(\d+)\]/g, '.$1').split('.');
  let current = obj;
  for (const key of keys) {
    if (current == null || current === undefined) return undefined;
    current = current[key];
  }
  return current;
}

function detectType(value) {
  if (Array.isArray(value)) return 'array';
  return typeof value;
}

/**
 * 校验 API 响应数据是否符合预期 Schema
 *
 * @param {string} endpointName - 端点名称
 * @param {object} data - API 响应数据
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
export function validateResponse(endpointName, data) {
  const rules = SCHEMA_RULES[endpointName];
  if (!rules) {
    return { valid: true, errors: [], warnings: [`未知端点: ${endpointName}`] };
  }

  const errors = [];
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

function main() {
  console.log('📋 API 响应 Schema 校验器');
  console.log('');

  if (!existsSync(ENDPOINTS_PATH)) {
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
      console.log(`   ⚠️  ${name}: Schema 与实际验证规则不一致`);
      allPass = false;
    } else {
      console.log(`   ✅  ${name}: Schema 定义完整`);
    }
  }

  console.log('');
  if (allPass) {
    console.log('✅ 所有端点 Schema 检查通过');
  } else {
    console.warn('⚠️  部分端点 Schema 需更新');
  }
}

// 独立运行时执行 CLI
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}

export default { validateResponse };
