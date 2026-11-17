/**
 * Jev 判定服务客户端边界。
 *
 * 与 mi-client.js 同级隔离：这是第二个（也是除小米客户端外唯一）允许
 * 发起网络请求的模块，只接收已解析好的配置对象，不读取 `process.env`。
 * 入口脚本因此不同时具备“读取环境变量”和“网络发送”两种能力。
 *
 * 接口约定（https://tokenrhythm.studio/docs/api-integration）：
 * - POST {baseUrl}/v1/decision，Bearer 鉴权，非流式 JSON；
 * - state：背景与待判断内容；questions：调用方自定义键，这里用两道 noul 题；
 * - 响应为 { model, answers, ... } 结构化 JSON，answers.<qid>.noul 为 0-1 概率。
 */

import { JevError } from "./errors.js";
import {
  JEV_QUESTION_FORWARD,
  JEV_QUESTION_NATIVE,
  buildJevQuestions,
  buildJevState,
  decideForward,
  extractNoul,
} from "./jev-policy.js";

/** 判定结果缓存：同文本短时间重复出现不重复调用 API。 */
export const JEV_CACHE_MAX_ENTRIES = 200;
export const JEV_CACHE_TTL_MS = 10 * 60 * 1000;

const DECISION_PATH = "/v1/decision";

/**
 * 创建 Jev 判定客户端。
 *
 * @param {{ apiKey: string, baseUrl: string, model: string, level: "loose" | "balanced" | "strict", decisionThreshold?: number, timeoutMs: number }} config
 * @param {{ fetchImpl?: typeof fetch, now?: () => number }} [options] fetchImpl/now 供测试注入
 */
export function createJevClient(config, options = {}) {
  const fetchImpl = options.fetchImpl ?? fetch;
  const now = options.now ?? (() => Date.now());
  // Map 按插入序淘汰：命中时先删后插，即可实现 LRU。
  const cache = new Map();

  /**
   * 调用 /v1/decision 并返回解析后的 JSON。
   * 网络层错误一律抛 JevError（category 见 errors.js）。
   */
  async function callDecision(state, questions) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), config.timeoutMs);
    let response;
    try {
      response = await fetchImpl(`${config.baseUrl}${DECISION_PATH}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${config.apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ model: config.model, state, questions }),
        signal: controller.signal,
      });
    } catch (error) {
      if (error?.name === "AbortError") {
        throw new JevError(`Jev 请求超时（${config.timeoutMs}ms）`, { category: "timeout" });
      }
      throw new JevError(`Jev 请求失败：${error?.message ?? error}`, { category: "network" });
    } finally {
      clearTimeout(timer);
    }

    let payload = null;
    try {
      payload = await response.json();
    } catch {
      // 非 JSON 响应：保持 payload 为 null，走统一的错误分支。
    }

    if (!response.ok) {
      const detail = typeof payload?.message === "string" ? payload.message : "";
      const traceId = typeof payload?.traceId === "string" ? payload.traceId : undefined;
      const category =
        response.status === 401 || response.status === 403
          ? "auth"
          : response.status === 429
            ? "rate_limit"
            : response.status >= 500
              ? "server"
              : "request";
      throw new JevError(`Jev 服务返回 ${response.status}${detail ? `：${detail}` : ""}`, {
        category,
        status: response.status,
        traceId,
      });
    }

    if (payload === null || typeof payload !== "object") {
      throw new JevError("Jev 响应不是合法的 JSON 对象", { category: "protocol" });
    }
    return payload;
  }

  /**
   * 对一条语音转写做转发判定（带缓存）。
   *
   * @param {string} query 转写原文（已 trim）
   * @param {{ prefix?: string, prefixMatched?: boolean }} [context]
   */
  async function decide(query, context = {}) {
    const key = String(query ?? "").trim();
    const cached = cache.get(key);
    if (cached) {
      if (cached.expiresAt > now()) {
        // 刷新插入序，实现 LRU。
        cache.delete(key);
        cache.set(key, cached);
        return cached.decision;
      }
      cache.delete(key);
    }

    const payload = await callDecision(
      buildJevState({
        query: key,
        prefix: context.prefix ?? "",
        prefixMatched: context.prefixMatched === true,
      }),
      buildJevQuestions(config.level),
    );

    const decision = decideForward(
      {
        shouldForward: extractNoul(payload.answers?.[JEV_QUESTION_FORWARD], JEV_QUESTION_FORWARD),
        isNativeCapability: extractNoul(payload.answers?.[JEV_QUESTION_NATIVE], JEV_QUESTION_NATIVE),
      },
      config.level,
      { decisionThreshold: config.decisionThreshold },
    );
    if (typeof payload.traceId === "string") {
      decision.traceId = payload.traceId;
    }
    if (typeof payload.model === "string") {
      decision.model = payload.model;
    }

    cache.set(key, { expiresAt: now() + JEV_CACHE_TTL_MS, decision });
    while (cache.size > JEV_CACHE_MAX_ENTRIES) {
      const oldest = cache.keys().next().value;
      cache.delete(oldest);
    }
    return decision;
  }

  /**
   * 连通性检查（test 命令）：一次最小 noul 调用，返回延迟与模型标识。
   */
  async function ping() {
    const startedAt = now();
    const payload = await callDecision(
      "连通性测试：这是一条来自 xiaoai-bridge 的探活请求，内容本身无需判断。",
      { ping: { type: "noul", instructions: "这是一次连通性测试，请返回任意 0-1 概率。" } },
    );
    return {
      latencyMs: now() - startedAt,
      model: typeof payload.model === "string" ? payload.model : undefined,
    };
  }

  return { decide, ping, level: config.level };
}
