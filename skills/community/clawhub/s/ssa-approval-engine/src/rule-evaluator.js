/**
 * rule-evaluator.js
 * 
 * 规则评估器模块 - 评估触发条件和附加条件
 * 
 * 支持三种触发类型：
 * 1. threshold - 阈值比较 (>, <, >=, <=, ==, !=)
 * 2. status - 状态匹配 (in, not_in, ==, !=)
 * 3. event - 事件类型匹配
 * 
 * 从 config/approval-rules.json 加载规则配置
 */

const fs = require('fs');
const path = require('path');

// 配置文件路径
const CONFIG_FILE = path.join(__dirname, '..', 'config', 'approval-rules.json');

/**
 * 加载规则配置
 * @returns {object}
 */
function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    throw new Error(`Config file not found: ${CONFIG_FILE}`);
  }
  const content = fs.readFileSync(CONFIG_FILE, 'utf8');
  return JSON.parse(content);
}

/**
 * 获取嵌套字段值
 * 支持点号路径：如 "quotation.amount" 从 {quotation: {amount: 100}} 获取 100
 * @param {object} obj 
 * @param {string} fieldPath 
 * @returns {any}
 */
function getNestedValue(obj, fieldPath) {
  const parts = fieldPath.split('.');
  let current = obj;
  
  for (const part of parts) {
    if (current === null || current === undefined) {
      return undefined;
    }
    current = current[part];
  }
  
  return current;
}

/**
 * 获取阈值配置值
 * @param {string} reference - 如 "thresholds.quotation_amount_limit"
 * @param {object} config - 配置对象
 * @returns {any}
 */
function getThresholdValue(reference, config) {
  const parts = reference.split('.');
  if (parts[0] === 'thresholds' && config.thresholds) {
    return config.thresholds[parts[1]];
  }
  return undefined;
}

/**
 * 评估比较操作符
 * @param {any} actual - 实际值
 * @param {string} operator - 操作符 (>, <, >=, <=, ==, !=, in, not_in)
 * @param {any} expected - 期望值
 * @returns {boolean}
 */
function evaluateOperator(actual, operator, expected) {
  switch (operator) {
    case '>':
      return Number(actual) > Number(expected);
    case '<':
      return Number(actual) < Number(expected);
    case '>=':
      return Number(actual) >= Number(expected);
    case '<=':
      return Number(actual) <= Number(expected);
    case '==':
    case '===':
      return actual == expected;
    case '!=':
    case '!==':
      return actual != expected;
    case 'in':
      return Array.isArray(expected) ? expected.includes(actual) : false;
    case 'not_in':
      return Array.isArray(expected) ? !expected.includes(actual) : true;
    default:
      console.warn(`[RuleEvaluator] Unknown operator: ${operator}`);
      return false;
  }
}

/**
 * 评估阈值触发条件
 * @param {object} trigger - 触发配置 {type, field, operator, reference}
 * @param {object} context - 上下文数据
 * @param {object} config - 配置对象
 * @returns {boolean}
 */
function evaluateThresholdTrigger(trigger, context, config) {
  const actualValue = getNestedValue(context, trigger.field);
  const expectedValue = getThresholdValue(trigger.reference, config);
  
  if (actualValue === undefined || expectedValue === undefined) {
    console.log(`[RuleEvaluator] Threshold evaluation failed: field=${trigger.field}, reference=${trigger.reference}`);
    return false;
  }
  
  const result = evaluateOperator(actualValue, trigger.operator, expectedValue);
  console.log(`[RuleEvaluator] Threshold: ${trigger.field}(${actualValue}) ${trigger.operator} ${expectedValue} = ${result}`);
  return result;
}

/**
 * 评估状态触发条件
 * @param {object} trigger - 触发配置 {type, field, operator, value}
 * @param {object} context - 上下文数据
 * @returns {boolean}
 */
function evaluateStatusTrigger(trigger, context) {
  const actualValue = getNestedValue(context, trigger.field);
  
  if (actualValue === undefined) {
    console.log(`[RuleEvaluator] Status evaluation failed: field=${trigger.field}`);
    return false;
  }
  
  const result = evaluateOperator(actualValue, trigger.operator, trigger.value);
  console.log(`[RuleEvaluator] Status: ${trigger.field}(${actualValue}) ${trigger.operator} ${JSON.stringify(trigger.value)} = ${result}`);
  return result;
}

/**
 * 评估事件触发条件
 * @param {object} trigger - 触发配置 {type, event_type, source}
 * @param {object} context - 上下文数据
 * @returns {boolean}
 */
function evaluateEventTrigger(trigger, context) {
  const eventTypeMatch = context.event_type === trigger.event_type;
  const sourceMatch = !trigger.source || context.source === trigger.source;
  
  const result = eventTypeMatch && sourceMatch;
  console.log(`[RuleEvaluator] Event: ${context.event_type} from ${context.source} matches ${trigger.event_type} = ${result}`);
  return result;
}

/**
 * 评估触发条件
 * @param {object} trigger - 触发配置
 * @param {object} context - 上下文数据
 * @param {object} config - 配置对象
 * @returns {boolean}
 */
function evaluateTrigger(trigger, context, config) {
  switch (trigger.type) {
    case 'threshold':
      return evaluateThresholdTrigger(trigger, context, config);
    case 'status':
      return evaluateStatusTrigger(trigger, context);
    case 'event':
      return evaluateEventTrigger(trigger, context);
    default:
      console.warn(`[RuleEvaluator] Unknown trigger type: ${trigger.type}`);
      return false;
  }
}

/**
 * 评估附加条件
 * @param {Array} conditions - 条件数组 [{field, operator, value}]
 * @param {object} context - 上下文数据
 * @returns {boolean} 所有条件都满足返回 true
 */
function evaluateConditions(conditions, context) {
  if (!conditions || conditions.length === 0) {
    return true; // 无条件则默认满足
  }
  
  for (const condition of conditions) {
    const actualValue = getNestedValue(context, condition.field);
    const result = evaluateOperator(actualValue, condition.operator, condition.value);
    
    if (!result) {
      console.log(`[RuleEvaluator] Condition failed: ${condition.field} ${condition.operator} ${condition.value}`);
      return false;
    }
  }
  
  return true;
}

/**
 * 评估审批人级别的触发条件（用于多级审批）
 * @param {string} triggerCondition - 条件表达式字符串，如 "amount > thresholds.quotation_amount_limit * 2"
 * @param {object} context - 上下文数据
 * @param {object} config - 配置对象
 * @returns {boolean}
 */
function evaluateApproverTriggerCondition(triggerCondition, context, config) {
  if (!triggerCondition) {
    return false; // 无条件则不触发此级别
  }
  
  // 简单表达式解析（支持 >, <, >=, <=, ==, !=, &&, ||）
  // 替换 thresholds 引用
  let expr = triggerCondition;
  if (config.thresholds) {
    for (const [key, value] of Object.entries(config.thresholds)) {
      expr = expr.replace(new RegExp(`thresholds\\.${key}`, 'g'), value);
    }
  }
  
  // 替换 context 字段引用
  for (const [key, value] of Object.entries(context)) {
    if (typeof value === 'object') {
      for (const [subKey, subValue] of Object.entries(value)) {
        expr = expr.replace(new RegExp(`${key}\\.${subKey}`, 'g'), 
          typeof subValue === 'string' ? `'${subValue}'` : subValue);
      }
    } else {
      expr = expr.replace(new RegExp(`${key}`, 'g'), 
        typeof value === 'string' ? `'${value}'` : value);
    }
  }
  
  try {
    // 安全评估（仅允许基本运算和比较）
    const result = eval(expr); // eslint-disable-line no-eval
    console.log(`[RuleEvaluator] Approver condition: ${triggerCondition} => ${expr} = ${result}`);
    return Boolean(result);
  } catch (error) {
    console.warn(`[RuleEvaluator] Failed to evaluate condition: ${triggerCondition}`, error.message);
    return false;
  }
}

/**
 * 匹配规则 - 找到所有触发的规则
 * @param {object} context - 上下文数据
 * @returns {Array} 匹配的规则列表
 */
function matchRules(context) {
  const config = loadConfig();
  const matchedRules = [];
  
  for (const rule of config.rules) {
    if (!rule.enabled) {
      continue;
    }
    
    const triggerMatched = evaluateTrigger(rule.trigger, context, config);
    const conditionsMatched = evaluateConditions(rule.conditions, context);
    
    if (triggerMatched && conditionsMatched) {
      console.log(`[RuleEvaluator] Rule matched: ${rule.id} - ${rule.name}`);
      matchedRules.push(rule);
    }
  }
  
  return matchedRules;
}

/**
 * 获取规则详情
 * @param {string} ruleId - 规则 ID
 * @returns {object|null}
 */
function getRule(ruleId) {
  const config = loadConfig();
  return config.rules.find(r => r.id === ruleId) || null;
}

/**
 * 获取阈值配置
 * @returns {object}
 */
function getThresholds() {
  const config = loadConfig();
  return config.thresholds || {};
}

/**
 * 获取 escalation 规则
 * @returns {Array}
 */
function getEscalationRules() {
  const config = loadConfig();
  return config.escalation_rules || [];
}

/**
 * 获取自动恢复策略
 * @returns {object}
 */
function getAutoRecovery() {
  const config = loadConfig();
  return config.auto_recovery || {};
}

/**
 * 获取通知模板
 * @param {string} channel - 通知渠道 (discord/email)
 * @param {string} templateName - 模板名称
 * @returns {object|null}
 */
function getNotificationTemplate(channel, templateName) {
  const config = loadConfig();
  return config.templates?.[channel]?.[templateName] || null;
}

// 导出 API
module.exports = {
  // 核心评估
  evaluateTrigger,
  evaluateConditions,
  evaluateApproverTriggerCondition,
  matchRules,
  
  // 配置读取
  loadConfig,
  getRule,
  getThresholds,
  getEscalationRules,
  getAutoRecovery,
  getNotificationTemplate,
  
  // 工具
  getNestedValue,
  evaluateOperator
};
