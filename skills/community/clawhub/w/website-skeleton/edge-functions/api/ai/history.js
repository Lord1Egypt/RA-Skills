/**
 * AI Chat History API — Edge Function
 *
 * GET /api/ai/history
 * 读 KV `ai:{tenant}:{userId}:history`，返回最近 N 条消息
 *
 * Phase 4A P0-6 实现
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';
import { aiSessionKey, getTenant } from '../../sharing/kv-keys.js';
import { ok, badRequest, unauthorized, internalError } from '../../sharing/response.js';

async function authenticate(request, env) {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) return null;
  const token = auth.slice(7);
  try {
    return await verifyJWT(token, env);
  } catch {
    return null;
  }
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'GET') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    const payload = await authenticate(request, env);
    if (!payload) {
      return unauthorized('请先登录');
    }

    const tenant = getTenant(payload);
    const userId = String(payload.sub);
    const url = new URL(request.url);

    // 可选的 sessionId 参数，不传则获取所有 session 的概要
    const sessionId = url.searchParams.get('sessionId');
    const limit = Math.min(100, Math.max(1, parseInt(url.searchParams.get('limit') || '50')));

    if (sessionId) {
      // 获取特定 session 的历史
      const historyKey = aiSessionKey(tenant, userId, sessionId);
      const historyData = await env.KV.get(historyKey);

      if (!historyData) {
        return ok({ messages: [], sessionId });
      }

      const messages = JSON.parse(historyData);
      // 只返回最近 N 条
      const recentMessages = messages.slice(-limit);

      return ok({ messages: recentMessages, sessionId });
    }

    // 如果没有 sessionId，列出该用户的所有 AI session keys
    // 注意：KV 不支持通配符列出，这里用约定前缀扫描
    // 由于 EdgeOne KV 通常不支持 list 操作，我们存储一个用户级的 session 索引
    const userSessionIndexKey = `${tenant}:ai:${userId}:sessions`;
    const indexData = await env.KV.get(userSessionIndexKey);

    if (!indexData) {
      return ok({ sessions: [] });
    }

    const sessions = JSON.parse(indexData);
    // 返回最近的 session 列表（不含详细消息）
    const recentSessions = sessions.slice(-limit).map(s => ({
      sessionId: s.sessionId,
      lastMessage: s.lastMessage,
      messageCount: s.messageCount,
      updatedAt: s.updatedAt,
    }));

    return ok({ sessions: recentSessions });
  } catch (err) {
    console.error('[AI History] Error:', err.message, err.stack);
    return internalError('获取聊天历史失败');
  }
}
