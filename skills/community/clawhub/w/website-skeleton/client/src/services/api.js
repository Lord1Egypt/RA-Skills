/**
 * api — 统一 HTTP 客户端
 *
 * 功能：
 * - 鉴权通过 HttpOnly Cookie 自动携带（防 XSS）
 * - 401 → 跳转登录页
 * - JSON 自动序列化/反序列化
 * - 统一错误处理
 *
 * 用法：
 *   import { api } from './api.js';
 *   const products = await api.get('/products', { page: 1 });
 *   const created = await api.post('/products', { name: '...' });
 */

import { navigate } from '../utils/router.js';

const BASE = '/api';

/**
 * 统一请求函数
 */
async function request(method, path, options = {}) {
  const { body, params, headers: extraHeaders, raw } = options;

  // 拼 URL
  let url = `${BASE}${path}`;
  if (params) {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') qs.set(k, v);
    });
    const qstr = qs.toString();
    if (qstr) url += `?${qstr}`;
  }

  // 构造请求头
  const headers = {
    'Content-Type': 'application/json',
    ...extraHeaders,
  };
  // 注意：鉴权通过 HttpOnly Cookie 自动携带，不在客户端存储 token
  // 如需要手动携带（开发环境），可通过 extraHeaders 传入 Authorization

  // 发起请求
  let res;
  try {
    res = await fetch(url, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (err) {
    throw new NetworkError('网络连接失败，请检查网络', err);
  }

  // 401 — Cookie 过期或无效，跳转登录
  if (res.status === 401) {
    navigate('/login');
    throw new AuthError('登录已过期，请重新登录');
  }

  // 解析响应
  if (raw) return res;

  const contentType = res.headers.get('content-type') || '';
  const data = contentType.includes('application/json')
    ? await res.json()
    : await res.text();

  if (!res.ok) {
    const msg = data?.message || data?.error || `请求失败 (${res.status})`;
    throw new ApiError(msg, res.status, data);
  }

  return data;
}

// ===================== 导出 =====================
// ===================== 导出 API 对象 =====================

export const api = {
  get(path, params) {
    return request('GET', path, { params });
  },

  post(path, body) {
    return request('POST', path, { body });
  },

  put(path, body) {
    return request('PUT', path, { body });
  },

  del(path, params) {
    return request('DELETE', path, { params });
  },

  /**
   * 上传文件（multipart/form-data）
   * 注意：鉴权通过 HttpOnly Cookie 自动携带
   */
  upload(path, formData) {
    return request('POST', path, { body: formData, raw: true });
  },
};

// ===================== 错误类 =====================

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

export class NetworkError extends Error {
  constructor(message, original) {
    super(message);
    this.name = 'NetworkError';
    this.original = original;
  }
}

export class AuthError extends Error {
  constructor(message) {
    super(message);
    this.name = 'AuthError';
  }
}
