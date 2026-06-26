import { describe, it, expect } from 'vitest';
import { ok, created, badRequest, unauthorized, forbidden, notFound, conflict, rateLimited, internalError, validationErrors } from '../../sharing/response.js';

describe('response.js — success responses', () => {
  it('ok returns 200 with data and meta', async () => {
    const res = ok({ id: 1, name: 'test' }, { extra: 'meta' });
    expect(res).toBeInstanceOf(Response);
    expect(res.status).toBe(200);
    expect(res.headers.get('Content-Type')).toBe('application/json');
    const body = await res.json();
    expect(body.success).toBe(true);
    expect(body.data).toEqual({ id: 1, name: 'test' });
    expect(body.extra).toBe('meta');
  });

  it('ok works without meta', async () => {
    const res = ok({ id: 1 });
    const body = await res.json();
    expect(body.success).toBe(true);
    expect(body.data).toEqual({ id: 1 });
  });

  it('created returns 201 with data', async () => {
    const res = created({ id: 42 });
    expect(res).toBeInstanceOf(Response);
    expect(res.status).toBe(201);
    expect(res.headers.get('Content-Type')).toBe('application/json');
    const body = await res.json();
    expect(body.success).toBe(true);
    expect(body.data).toEqual({ id: 42 });
  });
});

describe('response.js — client error responses', () => {
  it('badRequest returns 400 with VALIDATION_ERROR code', async () => {
    const res = badRequest('邮箱格式不正确');
    expect(res.status).toBe(400);
    expect(res.headers.get('Content-Type')).toBe('application/json');
    const body = await res.json();
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('VALIDATION_ERROR');
    expect(body.error.message).toBe('邮箱格式不正确');
  });

  it('badRequest supports custom error code', async () => {
    const res = badRequest('自定义错误', 'CUSTOM_CODE');
    const body = await res.json();
    expect(body.error.code).toBe('CUSTOM_CODE');
  });

  it('unauthorized returns 401', async () => {
    const res = unauthorized();
    expect(res.status).toBe(401);
    const body = await res.json();
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('UNAUTHORIZED');
    expect(body.error.message).toBe('Unauthorized');
  });

  it('unauthorized supports custom message', async () => {
    const res = unauthorized('请先登录');
    const body = await res.json();
    expect(body.error.message).toBe('请先登录');
  });

  it('forbidden returns 403', async () => {
    const res = forbidden();
    expect(res.status).toBe(403);
    const body = await res.json();
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('FORBIDDEN');
    expect(body.error.message).toBe('Forbidden');
  });

  it('forbidden supports custom message', async () => {
    const res = forbidden('无权限');
    const body = await res.json();
    expect(body.error.message).toBe('无权限');
  });

  it('notFound returns 404', async () => {
    const res = notFound();
    expect(res.status).toBe(404);
    const body = await res.json();
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('NOT_FOUND');
    expect(body.error.message).toBe('Not found');
  });

  it('notFound supports custom message', async () => {
    const res = notFound('订单不存在');
    const body = await res.json();
    expect(body.error.message).toBe('订单不存在');
  });

  it('conflict returns 409', async () => {
    const res = conflict();
    expect(res.status).toBe(409);
    const body = await res.json();
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('CONFLICT');
    expect(body.error.message).toBe('Conflict');
  });

  it('rateLimited returns 429 with Retry-After header', async () => {
    const res = rateLimited('请求过于频繁', 30);
    expect(res.status).toBe(429);
    expect(res.headers.get('Retry-After')).toBe('30');
    const body = await res.json();
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('RATE_LIMITED');
    expect(body.error.message).toBe('请求过于频繁');
  });

  it('rateLimited defaults retryAfter to 60', async () => {
    const res = rateLimited();
    expect(res.headers.get('Retry-After')).toBe('60');
  });
});

describe('response.js — server error responses', () => {
  it('internalError returns 500', async () => {
    const res = internalError();
    expect(res.status).toBe(500);
    const body = await res.json();
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('INTERNAL_ERROR');
    expect(body.error.message).toBe('Internal server error');
  });

  it('internalError supports custom message', async () => {
    const res = internalError('数据库连接失败');
    const body = await res.json();
    expect(body.error.message).toBe('数据库连接失败');
  });
});

describe('response.js — validationErrors', () => {
  it('validationErrors returns 400 with details array', async () => {
    const errors = [{ field: 'email', message: '邮箱格式不正确' }];
    const res = validationErrors(errors);
    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('VALIDATION_ERROR');
    expect(body.error.message).toBe('参数校验失败');
    expect(body.error.details).toEqual(errors);
  });
});
