/**
 * 共享参数校验模块
 *
 * 供给 Edge Functions 和 Cloud Functions 复用。
 * 每个校验函数返回 { valid: boolean, error?: string, sanitized?: any }
 *
 * 使用方式：
 *   import { validateEmail, validateOrderId } from '../sharing/validators.js';
 *
 *   const result = validateEmail(input);
 *   if (!result.valid) return errorResponse(400, result.error);
 */

// ===================== 通用工具 =====================

/** 安全整数值范围 */
const SAFE_INT_MAX = 2147483647;

/** 常见 SQL/NoSQL 注入特征 */
const INJECTION_PATTERNS = [
  /(\bUNION\b.*\bSELECT\b)/i,
  /(\bDROP\b\s+\bTABLE\b)/i,
  /(\bALTER\b\s+\bTABLE\b)/i,
  /(\bINSERT\b\s+\bINTO\b)/i,
  /(\bDELETE\b\s+\bFROM\b)/i,
  /(<\s*script\b)/i,
  /(\$\{.*\})/,       // 模板注入
  /(\bOR\b\s+1\s*=\s*1)/i,  // 布尔盲注
];

// ===================== 字符串校验 =====================

/**
 * 校验并清理字符串
 */
export function validateString(value, { min = 1, max = 255, required = true } = {}) {
  if (value === undefined || value === null) {
    if (required) return { valid: false, error: '此项为必填' };
    return { valid: true, sanitized: '' };
  }
  const str = String(value).trim();
  if (required && str.length === 0) {
    return { valid: false, error: '此项不能为空' };
  }
  if (str.length < min) {
    return { valid: false, error: `最少需要 ${min} 个字符` };
  }
  if (str.length > max) {
    return { valid: false, error: `最多允许 ${max} 个字符` };
  }
  return { valid: true, sanitized: str };
}

// ===================== Email =====================

const EMAIL_RE = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

export function validateEmail(email) {
  if (!email || typeof email !== 'string') {
    return { valid: false, error: '邮箱为必填项' };
  }
  const trimmed = email.trim().toLowerCase();
  if (trimmed.length > 254) {
    return { valid: false, error: '邮箱地址过长' };
  }
  if (!EMAIL_RE.test(trimmed)) {
    return { valid: false, error: '邮箱格式不正确' };
  }
  return { valid: true, sanitized: trimmed };
}

// ===================== 密码 =====================

export function validatePassword(password) {
  if (!password || typeof password !== 'string') {
    return { valid: false, error: '密码为必填项' };
  }
  if (password.length < 8) {
    return { valid: false, error: '密码最少需要 8 个字符' };
  }
  if (password.length > 128) {
    return { valid: false, error: '密码最多 128 个字符' };
  }
  // 强度检查：至少含字母+数字
  if (!/[a-zA-Z]/.test(password) || !/\d/.test(password)) {
    return { valid: false, error: '密码必须包含字母和数字' };
  }
  return { valid: true, sanitized: password };
}

// ===================== 订单ID =====================

const ORDER_ID_RE = /^[A-Z0-9]{8,64}$/;

export function validateOrderId(orderId) {
  if (!orderId || typeof orderId !== 'string') {
    return { valid: false, error: '订单ID为必填项' };
  }
  const trimmed = orderId.trim();
  if (!ORDER_ID_RE.test(trimmed)) {
    return { valid: false, error: '订单ID格式无效' };
  }
  return { valid: true, sanitized: trimmed };
}

// ===================== 金额 =====================

export function validateAmount(amount, { required = true, min = 0.01, max = 999999.99 } = {}) {
  if (amount === undefined || amount === null) {
    if (required) return { valid: false, error: '金额为必填项' };
    return { valid: true, sanitized: 0 };
  }
  const num = Number(amount);
  if (isNaN(num) || !isFinite(num)) {
    return { valid: false, error: '金额格式无效' };
  }
  if (num < min) {
    return { valid: false, error: `金额不能低于 ${min}` };
  }
  if (num > max) {
    return { valid: false, error: `金额不能超过 ${max}` };
  }
  // 保留两位小数
  return { valid: true, sanitized: Math.round(num * 100) / 100 };
}

// ===================== 数量 =====================

export function validateQuantity(qty, { required = true, min = 1, max = 999 } = {}) {
  if (qty === undefined || qty === null) {
    if (required) return { valid: false, error: '数量为必填项' };
    return { valid: true, sanitized: 1 };
  }
  const num = parseInt(qty, 10);
  if (isNaN(num) || num < min) {
    return { valid: false, error: `数量最少为 ${min}` };
  }
  if (num > max) {
    return { valid: false, error: `数量最多为 ${max}` };
  }
  return { valid: true, sanitized: num };
}

// ===================== 租户ID =====================

const TENANT_ID_RE = /^[a-z][a-z0-9_-]{1,31}$/;

export function validateTenantId(tenantId) {
  if (!tenantId || typeof tenantId !== 'string') {
    return { valid: false, error: '租户ID为必填项' };
  }
  const trimmed = tenantId.trim().toLowerCase();
  if (!TENANT_ID_RE.test(trimmed)) {
    return { valid: false, error: '租户ID格式无效（需以字母开头，2-32位）' };
  }
  return { valid: true, sanitized: trimmed };
}

// ===================== 商品 =====================

export function validateProductName(name) {
  if (!name || typeof name !== 'string') {
    return { valid: false, error: '商品名称为必填项' };
  }
  const trimmed = name.trim();
  if (trimmed.length < 1) return { valid: false, error: '商品名称不能为空' };
  if (trimmed.length > 200) return { valid: false, error: '商品名称最多 200 个字符' };
  return { valid: true, sanitized: trimmed };
}

// ===================== 注入检测 =====================

/**
 * 检测输入是否包含 SQL/脚本注入特征
 */
export function detectInjection(input) {
  if (!input || typeof input !== 'string') return false;
  return INJECTION_PATTERNS.some(pattern => pattern.test(input));
}

/**
 * 安全地校验输入，同时检测注入
 */
export function safeValidate(validatorFn, value, options) {
  // 如果是字符串，先检测注入
  if (typeof value === 'string' && detectInjection(value)) {
    return { valid: false, error: '输入包含非法字符' };
  }
  return validatorFn(value, options);
}

// ===================== 批量校验 =====================

/**
 * 批量参数校验
 *
 * @param {object} body - 请求体
 * @param {object} schema - { fieldName: validatorFn }
 * @returns {{ valid: boolean, errors?: object, sanitized?: object }}
 */
export function validateBody(body, schema) {
  const errors = {};
  const sanitized = {};

  for (const [field, validator] of Object.entries(schema)) {
    const result = validator(body[field]);
    if (!result.valid) {
      errors[field] = result.error;
    } else {
      sanitized[field] = result.sanitized !== undefined ? result.sanitized : body[field];
    }
  }

  if (Object.keys(errors).length > 0) {
    return { valid: false, errors, sanitized };
  }
  return { valid: true, sanitized };
}

// ===================== 安全类型转换 =====================

/** 安全转整数 */
export function safeParseInt(value, fallback = 0) {
  const num = parseInt(value, 10);
  if (isNaN(num) || !isFinite(num) || Math.abs(num) > SAFE_INT_MAX) {
    return fallback;
  }
  return num;
}

/** 安全分页参数 */
export function parsePagination(query) {
  const page = Math.max(1, safeParseInt(query?.page, 1));
  const pageSize = Math.min(100, Math.max(1, safeParseInt(query?.pageSize, 20)));
  const offset = (page - 1) * pageSize;
  return { page, pageSize, offset };
}
