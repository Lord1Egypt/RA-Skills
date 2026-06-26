/**
 * 统一 API 响应格式
 *
 * 所有 API 端点使用此模块构建标准错误/成功响应。
 *
 * 错误码体系：
 *   VALIDATION_ERROR — 参数校验失败 (400)
 *   UNAUTHORIZED      — 未认证 (401)
 *   FORBIDDEN         — 权限不足 (403)
 *   NOT_FOUND         — 资源不存在 (404)
 *   CONFLICT          — 并发冲突 (409)
 *   RATE_LIMITED      — 限流 (429)
 *   INTERNAL_ERROR    — 服务端错误 (500)
 *
 * 使用方式：
 *   import { badRequest, notFound, ok } from '../sharing/response.js';
 *
 *   if (!result.valid) return badRequest(result.error);
 *   return ok({ order });
 */

// ===================== 成功响应 =====================

export function ok(data, meta = {}) {
  return new Response(JSON.stringify({ success: true, data, ...meta }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}

export function created(data) {
  return new Response(JSON.stringify({ success: true, data }), {
    status: 201,
    headers: { 'Content-Type': 'application/json' },
  });
}

// ===================== 客户端错误 =====================

export function badRequest(message, code = 'VALIDATION_ERROR') {
  return new Response(JSON.stringify({
    success: false,
    error: { code, message },
  }), {
    status: 400,
    headers: { 'Content-Type': 'application/json' },
  });
}

export function unauthorized(message = 'Unauthorized') {
  return new Response(JSON.stringify({
    success: false,
    error: { code: 'UNAUTHORIZED', message },
  }), {
    status: 401,
    headers: { 'Content-Type': 'application/json' },
  });
}

export function forbidden(message = 'Forbidden') {
  return new Response(JSON.stringify({
    success: false,
    error: { code: 'FORBIDDEN', message },
  }), {
    status: 403,
    headers: { 'Content-Type': 'application/json' },
  });
}

export function notFound(message = 'Not found') {
  return new Response(JSON.stringify({
    success: false,
    error: { code: 'NOT_FOUND', message },
  }), {
    status: 404,
    headers: { 'Content-Type': 'application/json' },
  });
}

export function conflict(message = 'Conflict') {
  return new Response(JSON.stringify({
    success: false,
    error: { code: 'CONFLICT', message },
  }), {
    status: 409,
    headers: { 'Content-Type': 'application/json' },
  });
}

export function rateLimited(message = 'Too many requests', retryAfter = 60) {
  return new Response(JSON.stringify({
    success: false,
    error: { code: 'RATE_LIMITED', message },
  }), {
    status: 429,
    headers: {
      'Content-Type': 'application/json',
      'Retry-After': String(retryAfter),
    },
  });
}

// ===================== 服务端错误 =====================

export function internalError(message = 'Internal server error') {
  return new Response(JSON.stringify({
    success: false,
    error: { code: 'INTERNAL_ERROR', message },
  }), {
    status: 500,
    headers: { 'Content-Type': 'application/json' },
  });
}

// ===================== 校验错误（批量） =====================

export function validationErrors(errors) {
  return new Response(JSON.stringify({
    success: false,
    error: {
      code: 'VALIDATION_ERROR',
      message: '参数校验失败',
      details: errors,
    },
  }), {
    status: 400,
    headers: { 'Content-Type': 'application/json' },
  });
}
