/**
 * zhihu-http.js — 知乎 HTTP 读通道
 *
 * 通过知乎内部 API 读取数据，无需启动浏览器。
 * 支持：热榜、搜索、文章、用户、问题、回答
 * 自动处理签名头、降级、重试、限流
 *
 * C3a | S6 | S9 | I20 (Plan B)
 */

import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { defaultSignatureManager } from './zhihu-signature.js';
import { httpRateLimiter } from './zhihu-ratelimiter.js';
import { withRetry, writeLog, preflightCookieCheck } from './zhihu-core.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ──────────────────────────────────────────
// 配置
// ──────────────────────────────────────────

const ENDPOINTS_PATH = resolve(__dirname, '..', 'config', 'api-endpoints.json');

/** @type {{ version: string, baseUrls: object, endpoints: object }} */
let endpointsConfig = null;

function loadEndpoints() {
  if (endpointsConfig) return endpointsConfig;
  endpointsConfig = JSON.parse(readFileSync(ENDPOINTS_PATH, 'utf-8'));
  return endpointsConfig;
}

const DEFAULT_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Referer': 'https://www.zhihu.com/',
  'Origin': 'https://www.zhihu.com',
};

// ──────────────────────────────────────────
// 端点 Schema 校验 (S9)
// ──────────────────────────────────────────

const SCHEMA_CHECKS = {
  hotList: (data) => {
    if (!Array.isArray(data?.data)) return '缺少 .data 数组';
    if (data.data.length === 0) return '热榜为空';
    const first = data.data[0];
    if (!first?.target?.title_area?.text && !first?.target?.title) return '热榜条目缺少标题';
    return null;
  },
  search: (data) => {
    if (!Array.isArray(data?.data)) return '缺少 .data 数组';
    if (data.data.length === 0) return '搜索结果为空';
    const first = data.data[0];
    if (!first?.object?.text && !first?.title) return '搜索结果缺少正文';
    return null;
  },
  article: (data) => {
    if (!data?.id) return '缺少 id';
    if (!data?.title) return '缺少 title';
    return null;
  },
  user: (data) => {
    if (!data?.id && !data?.url_token) return '缺少标识符';
    return null;
  },
  question: (data) => {
    if (!data?.id) return '缺少 id';
    if (!data?.title) return '缺少 title';
    return null;
  },
  answers: (data) => {
    if (!Array.isArray(data?.data)) return '缺少 .data 数组';
    return null;
  },
};

function validateSchema(endpointName, data) {
  const check = SCHEMA_CHECKS[endpointName];
  if (!check) return { valid: true }; // 无校验规则

  const error = check(data);
  if (error) {
    console.warn(`[zhihu-http] Schema 校验失败 [${endpointName}]: ${error}`);
    writeLog({
      level: 'WARN',
      module: 'zhihu-http',
      operation: endpointName,
      status: 'schema_failure',
      details: { schemaError: error, endpointName },
    });
    return { valid: false, error };
  }

  return { valid: true };
}

// ──────────────────────────────────────────
// HTTP 请求
// ──────────────────────────────────────────

/**
 * 构建完整的 API URL
 */
function buildUrl(baseUrl, endpointPath, params) {
  let url = `${baseUrl}${endpointPath}`;

  if (params) {
    // 替换路径参数 {id}
    for (const [key, value] of Object.entries(params)) {
      url = url.replace(`{${key}}`, encodeURIComponent(value));
    }
  }

  return url;
}

/**
 * 发送 HTTP 请求到知乎 API
 *
 * @param {string} endpointName - 端点名称（对应 api-endpoints.json）
 * @param {object} [pathParams] - 路径参数（如 { id: '123' }）
 * @param {object} [queryParams] - 查询参数（如 { q: '关键词' }）
 * @returns {Promise<object>} API 响应数据
 */
async function fetchFromAPI(endpointName, pathParams = {}, queryParams = {}) {
  const config = loadEndpoints();
  const endpoint = config.endpoints[endpointName];

  if (!endpoint) {
    throw new Error(`未知端点: ${endpointName}`);
  }

  // 速率限制
  await httpRateLimiter.wait();

  // 构建 URL
  let path = endpoint.url;
  for (const [key, value] of Object.entries(pathParams)) {
    path = path.replace(`{${key}}`, encodeURIComponent(String(value)));
  }

  // 处理查询参数
  let finalPath = path;
  const queryKeys = Object.keys(queryParams);
  if (queryKeys.length > 0) {
    // 替换路径中的 {query} 占位符
    if (finalPath.includes('{query}')) {
      finalPath = finalPath.replace('{query}', encodeURIComponent(queryParams.q || queryParams.query || ''));
    } else {
      const qs = queryKeys
        .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(queryParams[k])}`)
        .join('&');
      finalPath = finalPath.includes('?') ? `${finalPath}&${qs}` : `${finalPath}?${qs}`;
    }
  }

  const baseUrl = config.baseUrls.zhihu;
  const fullUrl = `${baseUrl}${finalPath}`;

  // 构建请求头
  const headers = { ...DEFAULT_HEADERS };

  // 签名头（如果需要）
  if (endpoint.requiresSignature) {
    const sigHeaders = await defaultSignatureManager.getHeaders(finalPath, 'GET');
    Object.assign(headers, sigHeaders);
  }

  // 使用 withRetry 自动重试
  const data = await withRetry(
    async () => {
      const response = await fetch(fullUrl, { headers, method: 'GET' });

      // 处理 429 限流
      if (response.status === 429) {
        httpRateLimiter.triggerBackoff();
        throw new Error(`HTTP 429 限流 [${endpointName}]`);
      }

      // 处理 403（签名失效或风控）
      if (response.status === 403) {
        const healthOk = await defaultSignatureManager.healthCheck();
        if (!healthOk) {
          throw new Error(`签名失效 [${endpointName}]: 准备降级到 Plan B`);
        }
        throw new Error(`HTTP 403 被拒绝 [${endpointName}]`);
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status} [${endpointName}]`);
      }

      return response.json();
    },
    {
      maxRetries: 3,
      baseDelay: 1000,
      retryOn: (err) => {
        // 只对 429 和网络错误重试
        return err.message.includes('429') ||
               err.message.includes('ETIMEDOUT') ||
               err.message.includes('ECONNRESET') ||
               err.message.includes('fetch failed');
      },
      context: endpointName,
    }
  );

  httpRateLimiter.resetBackoff();

  // Schema 校验
  const schemaResult = validateSchema(endpointName, data);
  if (!schemaResult.valid && endpoint.planBFallback !== 'none') {
    console.log(`[zhihu-http] ${endpointName} 数据格式异常，标记为降级候选`);
    writeLog({
      level: 'WARN',
      module: 'zhihu-http',
      operation: endpointName,
      status: 'schema_failure_will_degrade',
      details: { endpointName, error: schemaResult.error },
    });
  }

  return data;
}

// ──────────────────────────────────────────
// 各端点专用函数
// ──────────────────────────────────────────

/**
 * 获取全站热榜
 * @param {number} [limit=20] - 返回条数
 * @returns {Promise<Array>} 热榜条目
 */
async function getHotList(limit = 20) {
  const data = await fetchFromAPI('hotList');
  const items = (data?.data || []).slice(0, limit);

  return items.map((item, index) => {
    const target = item.target || item;
    return {
      rank: index + 1,
      title: target.title_area?.text || target.title || '',
      excerpt: target.excerpt || target.desc || '',
      heat: target.metrics_area?.text || target.debate_count || '',
      url: target.url || `https://www.zhihu.com/question/${target.id}`,
      answerCount: target.answer_count || 0,
      followCount: target.follower_count || 0,
    };
  });
}

/**
 * 搜索内容
 * @param {string} query - 搜索关键词
 * @param {number} [limit=10] - 返回条数
 * @returns {Promise<Array>} 搜索结果
 */
async function search(query, limit = 10) {
  const data = await fetchFromAPI('search', {}, { q: query });
  const items = (data?.data || []).slice(0, limit);

  return items.map(item => {
    const obj = item.object || item;
    return {
      type: obj.type || 'unknown',
      title: obj.title || obj.question?.name || '',
      excerpt: obj.excerpt || obj.content || '',
      url: obj.url || `https://www.zhihu.com/question/${obj.question?.id}`,
      answerCount: obj.answer_count || 0,
      voteCount: obj.voteup_count || 0,
    };
  });
}

/**
 * 获取文章详情
 * @param {number|string} articleId - 文章 ID
 * @returns {Promise<object>} 文章数据
 */
async function getArticle(articleId) {
  const data = await fetchFromAPI('article', { id: articleId });
  return {
    id: data.id,
    title: data.title,
    content: data.content,
    excerpt: data.excerpt || '',
    author: data.author?.name || '',
    voteCount: data.voteup_count || 0,
    commentCount: data.comment_count || 0,
    created: data.created,
    updated: data.updated,
    url: `https://zhuanlan.zhihu.com/p/${data.id}`,
  };
}

/**
 * 获取用户信息
 * @param {string} userId - 用户 ID 或 url_token
 * @returns {Promise<object>} 用户数据
 */
async function getUser(userId) {
  const data = await fetchFromAPI('user', { id: userId });
  return {
    id: data.id,
    name: data.name,
    headline: data.headline || '',
    description: data.description || '',
    avatarUrl: data.avatar_url || '',
    urlToken: data.url_token,
    followerCount: data.follower_count || 0,
    answerCount: data.answer_count || 0,
    articleCount: data.article_count || 0,
    voteupCount: data.voteup_count || 0,
  };
}

/**
 * 获取问题详情
 * @param {number|string} questionId - 问题 ID
 * @returns {Promise<object>} 问题数据
 */
async function getQuestion(questionId) {
  const data = await fetchFromAPI('question', { id: questionId });
  return {
    id: data.id,
    title: data.title,
    detail: data.detail || '',
    answerCount: data.answer_count || 0,
    followCount: data.follower_count || 0,
    commentCount: data.comment_count || 0,
    created: data.created,
    url: `https://www.zhihu.com/question/${data.id}`,
  };
}

/**
 * 获取问题回答列表
 * @param {number|string} questionId - 问题 ID
 * @param {number} [limit=10] - 返回条数
 * @returns {Promise<Array>} 回答列表
 */
async function getAnswers(questionId, limit = 10) {
  const data = await fetchFromAPI('answers', { id: questionId }, { limit });
  const items = (data?.data || []).slice(0, limit);

  return items.map(item => {
    return {
      id: item.id,
      author: item.author?.name || '',
      content: item.content || '',
      voteCount: item.voteup_count || 0,
      commentCount: item.comment_count || 0,
      created: item.created_time || item.created,
      updated: item.updated_time || item.updated,
      url: `https://www.zhihu.com/question/${questionId}/answer/${item.id}`,
    };
  });
}

// ──────────────────────────────────────────
// 入口：智能读取（HTTP 优先 → 自动降级标记）
// ──────────────────────────────────────────

/**
 * 智能数据提取
 * HTTP 通道优先，标记是否适合降级到浏览器
 *
 * @param {string} type - 数据类型 (hotList|search|article|user|question|answers)
 * @param {object} params - 参数
 * @param {boolean} [useBrowser=false] - 是否强制使用浏览器
 * @returns {Promise<{ data: any, source: string, degraded: boolean }>}
 */
async function extract(type, params = {}, useBrowser = false) {
  const httpOnlyTypes = ['user', 'question', 'answers'];
  const needsSignature = !httpOnlyTypes.includes(type);

  if (useBrowser || (defaultSignatureManager.isPlanBActive() && needsSignature)) {
    // 标记为需要浏览器降级，但这里只返回标记，由调用方处理
    return { data: null, source: 'should_fallback_to_browser', degraded: true };
  }

  const timeStart = Date.now();
  let data;

  switch (type) {
    case 'hotList':
      data = await getHotList(params.limit);
      break;
    case 'search':
      data = await search(params.query, params.limit);
      break;
    case 'article':
      data = await getArticle(params.id);
      break;
    case 'user':
      data = await getUser(params.id);
      break;
    case 'question':
      data = await getQuestion(params.id);
      break;
    case 'answers':
      data = await getAnswers(params.id, params.limit);
      break;
    default:
      throw new Error(`未知数据类型: ${type}`);
  }

  writeLog({
    level: 'INFO',
    module: 'zhihu-http',
    operation: `extract_${type}`,
    status: 'success',
    duration_ms: Date.now() - timeStart,
    details: { type, params, planB: defaultSignatureManager.isPlanBActive() },
  });

  return { data, source: 'http', degraded: false };
}

// ──────────────────────────────────────────
// 导出
// ──────────────────────────────────────────

export {
  fetchFromAPI,
  getHotList,
  search,
  getArticle,
  getUser,
  getQuestion,
  getAnswers,
  extract,
  validateSchema,
};
