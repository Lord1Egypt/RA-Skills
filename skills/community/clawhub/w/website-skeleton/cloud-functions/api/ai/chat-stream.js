/**
 * AI 对话流式响应 API — SSE (text/event-stream)
 *
 * POST /api/ai/chat-stream
 * Body: { message, sessionId }
 *
 * - authenticate
 * - 读取 KV 历史 → 构建 context
 * - 调用 AI API (mock: 返回简单回复)
 * - 异步写回 KV 保存历史
 * - 处理限流
 * - 返回 SSE 流
 */

import { authenticate } from '../_helpers.js';
import { unauthorized, badRequest } from '../../../sharing/response.js';
import { aiSessionKey, rateLimitKey } from '../../../sharing/kv-keys.js';

const AI_HISTORY_TTL = 86400;        // 24h
const RATE_LIMIT_WINDOW = 60;        // 60秒
const RATE_LIMIT_MAX = 30;           // 每分钟最多30条消息
const MAX_HISTORY_LENGTH = 20;        // 最多保留20条历史消息

/**
 * 模拟 AI 回复生成器
 * 生产环境应替换为真实的 AI API 调用
 */
async function* mockAIResponse(message, history) {
  const contextLength = history.length;
  const replies = [
    `感谢您的提问。关于「${message}」这个话题，我理解您的关注点。`,
    `这是一个很好的问题！让我从几个方面来分析：\n\n1. 首先，我们需要理解核心需求\n2. 其次，考虑可行的实施方案\n3. 最后，评估预期效果\n\n希望这些对您有帮助！`,
    `收到您的消息：「${message}」\n\n根据之前的对话上下文（共 ${contextLength} 条历史记录），我建议您可以进一步明确具体需求，这样我能提供更精准的回答。`,
    `您好！关于您提到的内容，我有以下思考：\n\n> ${message}\n\n在实际应用中，我们需要结合具体场景来分析。您能提供更多背景信息吗？`,
    `我理解了您的问题。这是一个需要深入探讨的话题。我的建议是：\n\n✅ 先梳理关键点\n✅ 然后制定计划\n✅ 最后逐步实施\n\n有任何具体问题随时问我！`,
  ];

  const reply = replies[Math.floor(Math.random() * replies.length)];
  const words = reply.split('');

  // 逐字模拟 SSE 流式输出
  for (let i = 0; i < words.length; i++) {
    yield words[i];
    // 模拟 20-50ms 的间隔
    await new Promise((resolve) => setTimeout(resolve, 20 + Math.random() * 30));
  }
}

/**
 * 检查并应用限流
 */
async function checkRateLimit(env, tenant, userId) {
  const windowKey = Math.floor(Date.now() / (RATE_LIMIT_WINDOW * 1000)).toString();
  const rlKey = rateLimitKey(tenant, `chat:${userId}`, windowKey);

  try {
    const current = parseInt((await env.KV?.get?.(rlKey)) || '0', 10);
    if (current >= RATE_LIMIT_MAX) {
      return { limited: true, remaining: 0 };
    }
    await env.KV?.put?.(rlKey, String(current + 1), {
      expirationTtl: RATE_LIMIT_WINDOW,
    });
    return { limited: false, remaining: RATE_LIMIT_MAX - current - 1 };
  } catch {
    // KV 不可用时放行（安全降级）
    return { limited: false, remaining: -1 };
  }
}

/**
 * 从 KV 读取会话历史
 */
async function loadHistory(env, tenant, userId, sessionId) {
  const key = aiSessionKey(tenant, userId, sessionId);
  try {
    const raw = await env.KV?.get?.(key);
    if (raw) {
      return JSON.parse(raw);
    }
  } catch {
    // 解析失败返回空历史
  }
  return [];
}

/**
 * 保存会话历史到 KV（异步非阻塞）
 */
async function saveHistory(env, tenant, userId, sessionId, history) {
  const key = aiSessionKey(tenant, userId, sessionId);
  // 截断历史
  const trimmed = history.slice(-MAX_HISTORY_LENGTH);
  try {
    await env.KV?.put?.(key, JSON.stringify(trimmed), {
      expirationTtl: AI_HISTORY_TTL,
    });
  } catch (err) {
    console.warn('[ChatStream] Failed to save history:', err.message);
  }
}

export async function onRequest(request, env) {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // === 认证 ===
  const user = await authenticate(request, env);
  if (!user) {
    return unauthorized();
  }
  const { tenant, sub: userId } = user;

  // === 限流检查 ===
  const rateCheck = await checkRateLimit(env, tenant, userId);
  if (rateCheck.limited) {
    return new Response(JSON.stringify({
      error: { code: 'RATE_LIMITED', message: '消息频率过高，请稍后再试' },
    }), {
      status: 429,
      headers: {
        'Content-Type': 'application/json',
        'Retry-After': String(RATE_LIMIT_WINDOW),
      },
    });
  }

  // === 解析请求 ===
  let body;
  try {
    body = await request.json();
  } catch {
    return badRequest('Invalid JSON body');
  }

  const { message, sessionId } = body;

  if (!message || message.trim().length === 0) {
    return badRequest('消息内容不能为空');
  }
  if (!sessionId) {
    return badRequest('sessionId 为必填项');
  }

  // 消息长度限制
  if (message.length > 2000) {
    return badRequest('消息长度不能超过 2000 字符');
  }

  // === 加载历史 ===
  const history = await loadHistory(env, tenant, userId, sessionId);

  // === 构建 SSE 流 ===
  const stream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder();
      const sendEvent = (event, data) => {
        controller.enqueue(
          encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`)
        );
      };

      try {
        // 发送开始事件
        sendEvent('start', {
          sessionId,
          historyLength: history.length,
          remaining: rateCheck.remaining,
        });

        // 追加用户消息到历史
        const updatedHistory = [
          ...history,
          { role: 'user', content: message, timestamp: new Date().toISOString() },
        ];

        // 流式生成回复
        let fullResponse = '';
        const generator = mockAIResponse(message, history);

        for await (const chunk of generator) {
          fullResponse += chunk;
          sendEvent('message', { content: chunk });
        }

        // 追加 AI 回复到历史
        updatedHistory.push({
          role: 'assistant',
          content: fullResponse,
          timestamp: new Date().toISOString(),
        });

        // 异步保存历史
        saveHistory(env, tenant, userId, sessionId, updatedHistory).catch((err) => {
          console.warn('[ChatStream] Async history save failed:', err.message);
        });

        // 发送完成事件
        sendEvent('done', {
          fullResponse,
          totalTokens: fullResponse.length,
        });
      } catch (err) {
        console.error('[ChatStream] Stream error:', err);
        sendEvent('error', { message: 'AI 回复生成失败，请重试' });
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    },
  });
}
