export type StellaProvider = "gemini" | "fal" | "laozhang" | "openclaw";

export type StellaErrorCategory =
  | "user_fixable"
  | "transient"
  | "policy"
  | "auth"
  | "config"
  | "unknown";

export type StellaErrorCode =
  | "CONFIG_MISSING"
  | "INPUT_INVALID"
  | "AUTH_INVALID_KEY"
  | "PERMISSION_DENIED"
  | "RESOURCE_NOT_FOUND"
  | "RATE_LIMITED"
  | "UPSTREAM_UNAVAILABLE"
  | "TIMEOUT"
  | "SAFETY_BLOCKED"
  | "NO_OUTPUT"
  | "SEND_FAILED"
  | "UNKNOWN";

export interface StellaErrorDetails {
  provider: StellaProvider;
  code: StellaErrorCode;
  category: StellaErrorCategory;
  retryable: boolean;
  userMessage: string;
  actionHint: string;
  statusCode?: number;
  upstreamType?: string;
  rawMessage?: string;
}

export class StellaError extends Error {
  public readonly details: StellaErrorDetails;
  public readonly cause?: unknown;

  constructor(details: StellaErrorDetails, cause?: unknown) {
    super(`[${details.provider}:${details.code}] ${details.rawMessage || details.userMessage}`);
    this.name = "StellaError";
    this.details = details;
    this.cause = cause;
  }
}

interface NormalizationContext {
  message: string;
  status?: number;
  lower: string;
}

interface FalNormalizationContext extends NormalizationContext {
  errorType?: string;
  modelType?: string;
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object") return {};
  return value as Record<string, unknown>;
}

function asArray(value: unknown): unknown[] {
  if (Array.isArray(value)) return value;
  return [];
}

function readMessage(err: unknown): string {
  if (err instanceof Error && err.message) return err.message;
  const rec = asRecord(err);
  if (typeof rec.message === "string") return rec.message;
  if (typeof rec.detail === "string") return rec.detail;
  return String(err);
}

function readStatus(err: unknown): number | undefined {
  const rec = asRecord(err);
  if (typeof rec.status === "number") return rec.status;
  const nested = asRecord(rec.error);
  if (typeof nested.code === "number") return nested.code;
  return undefined;
}

function readFalErrorType(err: unknown): string | undefined {
  const rec = asRecord(err);
  if (typeof rec.error_type === "string") return rec.error_type;
  const body = asRecord(rec.body);
  if (typeof body.error_type === "string") return body.error_type;
  return undefined;
}

function readFalModelErrorType(err: unknown): string | undefined {
  const rec = asRecord(err);
  const detail = asArray(rec.detail);
  if (detail.length > 0) {
    const first = asRecord(detail[0]);
    if (typeof first.type === "string") return first.type;
  }
  const body = asRecord(rec.body);
  const bodyDetail = asArray(body.detail);
  if (bodyDetail.length > 0) {
    const first = asRecord(bodyDetail[0]);
    if (typeof first.type === "string") return first.type;
  }
  return undefined;
}

function isTruthyStringFlag(value: unknown): boolean {
  return typeof value === "string" && value.toLowerCase() === "true";
}

function defaultUnknown(provider: StellaProvider, err: unknown): StellaErrorDetails {
  return {
    provider,
    code: "UNKNOWN",
    category: "unknown",
    retryable: false,
    userMessage: "这次图片没生成成功。",
    actionHint: "请稍后重试；若持续失败，请检查 provider 配置和网络连通性。",
    statusCode: readStatus(err),
    rawMessage: readMessage(err),
  };
}

function makeDetails(
  provider: StellaProvider,
  ctx: NormalizationContext,
  partial: Omit<
    StellaErrorDetails,
    "provider" | "statusCode" | "rawMessage" | "upstreamType"
  > & Pick<StellaErrorDetails, "upstreamType">
): StellaErrorDetails {
  return {
    provider,
    code: partial.code,
    category: partial.category,
    retryable: partial.retryable,
    userMessage: partial.userMessage,
    actionHint: partial.actionHint,
    statusCode: ctx.status,
    upstreamType: partial.upstreamType,
    rawMessage: ctx.message,
  };
}

function isGeminiNetworkTransient(lower: string): boolean {
  return (
    lower.includes("econnreset") ||
    lower.includes("etimedout") ||
    lower.includes("fetch failed") ||
    lower.includes("network") ||
    lower.includes("socket hang up") ||
    lower.includes("eai_again") ||
    lower.includes("enotfound")
  );
}

export function normalizeGeminiError(err: unknown): StellaErrorDetails {
  const ctx: NormalizationContext = {
    message: readMessage(err),
    status: readStatus(err),
    lower: readMessage(err).toLowerCase(),
  };

  if (ctx.message.includes("GEMINI_API_KEY is not set")) {
    return makeDetails("gemini", ctx, {
      code: "CONFIG_MISSING",
      category: "config",
      retryable: false,
      userMessage: "这次图片没生成成功：缺少 Gemini API Key。",
      actionHint: "请在 skills.entries.stella-selfie.env 中配置 GEMINI_API_KEY 后重试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.lower.includes("safety") ||
    ctx.lower.includes("block_reason") ||
    ctx.lower.includes("blockedreason")
  ) {
    return makeDetails("gemini", ctx, {
      code: "SAFETY_BLOCKED",
      category: "policy",
      retryable: false,
      userMessage: "这次图片没生成成功：请求触发了内容安全限制。",
      actionHint: "请改用更中性、非敏感的描述后再试。",
      upstreamType: undefined,
    });
  }

  if (ctx.status === 400) {
    return makeDetails("gemini", ctx, {
      code: "INPUT_INVALID",
      category: "user_fixable",
      retryable: false,
      userMessage: "这次图片没生成成功：请求参数不合法。",
      actionHint: "请简化提示词或调整参数后重试。",
      upstreamType: undefined,
    });
  }

  if (ctx.status === 403 || ctx.lower.includes("permission_denied")) {
    return makeDetails("gemini", ctx, {
      code: "PERMISSION_DENIED",
      category: "auth",
      retryable: false,
      userMessage: "这次图片没生成成功：Gemini 鉴权失败或权限不足。",
      actionHint: "请检查 API Key 是否正确、可用并具备对应模型权限。",
      upstreamType: undefined,
    });
  }

  if (ctx.status === 404 || ctx.lower.includes("not_found")) {
    return makeDetails("gemini", ctx, {
      code: "RESOURCE_NOT_FOUND",
      category: "user_fixable",
      retryable: false,
      userMessage: "这次图片没生成成功：请求引用的资源不存在。",
      actionHint: "请检查输入资源路径或链接后重试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.status === 429 ||
    ctx.lower.includes("resource_exhausted") ||
    ctx.lower.includes("rate limit")
  ) {
    return makeDetails("gemini", ctx, {
      code: "RATE_LIMITED",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：请求过于频繁。",
      actionHint: "请等待 1-2 分钟后重试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.status === 504 ||
    ctx.lower.includes("deadline_exceeded") ||
    ctx.lower.includes("timeout")
  ) {
    return makeDetails("gemini", ctx, {
      code: "TIMEOUT",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：Gemini 处理超时。",
      actionHint: "请稍后重试，或简化提示词后再试。",
      upstreamType: undefined,
    });
  }

  if (isGeminiNetworkTransient(ctx.lower)) {
    return makeDetails("gemini", ctx, {
      code: "UPSTREAM_UNAVAILABLE",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：网络或上游服务暂时不可用。",
      actionHint: "请稍后重试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.status === 500 ||
    ctx.status === 503 ||
    ctx.lower.includes("unavailable") ||
    ctx.lower.includes("internal")
  ) {
    return makeDetails("gemini", ctx, {
      code: "UPSTREAM_UNAVAILABLE",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：Gemini 服务暂时不可用。",
      actionHint: "请稍后重试，必要时切换 Provider=fal。",
      upstreamType: undefined,
    });
  }

  if (ctx.lower.includes("no image data") || ctx.lower.includes("no content parts")) {
    return makeDetails("gemini", ctx, {
      code: "NO_OUTPUT",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：模型未返回有效图片。",
      actionHint: "请直接重试一次，或稍微改写提示词后再试。",
      upstreamType: undefined,
    });
  }

  return defaultUnknown("gemini", err);
}

export function normalizeFalError(err: unknown): StellaErrorDetails {
  const message = readMessage(err);
  const status = readStatus(err);
  const lower = message.toLowerCase();
  const errorType = readFalErrorType(err);
  const modelType = readFalModelErrorType(err);
  const rec = asRecord(err);
  const retryableHeader = isTruthyStringFlag(rec["x-fal-retryable"]);
  const retryableField = isTruthyStringFlag(rec.retryable);
  const retryable = retryableHeader || retryableField;
  const ctx: FalNormalizationContext = {
    message,
    status,
    lower,
    errorType,
    modelType,
  };

  if (ctx.message.includes("FAL_KEY is not set")) {
    return makeDetails("fal", ctx, {
      code: "CONFIG_MISSING",
      category: "config",
      retryable: false,
      userMessage: "这次图片没生成成功：缺少 fal API Key。",
      actionHint: "请在 skills.entries.stella-selfie.env 中配置 FAL_KEY 后重试。",
      upstreamType: undefined,
    });
  }

  if (ctx.status === 401 || ctx.status === 403) {
    return makeDetails("fal", ctx, {
      code: "AUTH_INVALID_KEY",
      category: "auth",
      retryable: false,
      userMessage: "这次图片没生成成功：fal 鉴权失败。",
      actionHint: "请检查 FAL_KEY 是否有效且有权限访问该模型。",
      upstreamType: undefined,
    });
  }

  if (ctx.status === 429) {
    return makeDetails("fal", ctx, {
      code: "RATE_LIMITED",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：fal 当前请求较拥堵。",
      actionHint: "请稍后重试。",
      upstreamType: ctx.errorType,
    });
  }

  if (
    ctx.modelType === "content_policy_violation" ||
    ctx.lower.includes("content policy") ||
    ctx.lower.includes("safety")
  ) {
    return makeDetails("fal", ctx, {
      code: "SAFETY_BLOCKED",
      category: "policy",
      retryable: false,
      userMessage: "这次图片没生成成功：请求触发了内容安全限制。",
      actionHint: "请改用更中性、非敏感的描述后再试。",
      upstreamType: ctx.modelType || ctx.errorType,
    });
  }

  if (ctx.modelType === "file_download_error" || ctx.modelType === "image_load_error") {
    return makeDetails("fal", ctx, {
      code: "INPUT_INVALID",
      category: "user_fixable",
      retryable: false,
      userMessage: "这次图片没生成成功：参考图地址不可访问或无法读取。",
      actionHint: "请确认 AvatarsURLs 为公开可下载的 http/https 图片地址。",
      upstreamType: ctx.modelType,
    });
  }

  if (
    ctx.modelType === "unsupported_image_format" ||
    ctx.modelType === "image_too_small" ||
    ctx.modelType === "image_too_large" ||
    ctx.modelType === "feature_not_supported"
  ) {
    return makeDetails("fal", ctx, {
      code: "INPUT_INVALID",
      category: "user_fixable",
      retryable: false,
      userMessage: "这次图片没生成成功：输入图片规格不符合要求。",
      actionHint: "请更换为支持格式并确保尺寸满足模型要求后重试。",
      upstreamType: ctx.modelType,
    });
  }

  if (ctx.modelType === "no_media_generated" || ctx.lower.includes("no images")) {
    return makeDetails("fal", ctx, {
      code: "NO_OUTPUT",
      category: "user_fixable",
      retryable: false,
      userMessage: "这次图片没生成成功：模型未生成有效图片。",
      actionHint: "请简化提示词或调整描述后重试。",
      upstreamType: ctx.modelType,
    });
  }

  const timeoutErrorTypes = new Set(["request_timeout", "startup_timeout", "generation_timeout"]);
  if (
    ctx.status === 504 ||
    (ctx.errorType && timeoutErrorTypes.has(ctx.errorType)) ||
    (ctx.modelType && timeoutErrorTypes.has(ctx.modelType))
  ) {
    return makeDetails("fal", ctx, {
      code: "TIMEOUT",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：fal 处理超时。",
      actionHint: "请稍后重试。",
      upstreamType: ctx.errorType || ctx.modelType,
    });
  }

  if (
    ctx.status === 500 ||
    ctx.status === 502 ||
    ctx.status === 503 ||
    (ctx.errorType && (ctx.errorType.startsWith("runner_") || ctx.errorType === "internal_error"))
  ) {
    return makeDetails("fal", ctx, {
      code: "UPSTREAM_UNAVAILABLE",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：fal 服务暂时不可用。",
      actionHint: "请稍后重试。",
      upstreamType: ctx.errorType,
    });
  }

  if (ctx.status === 400 || ctx.status === 422 || ctx.errorType === "bad_request") {
    return makeDetails("fal", ctx, {
      code: "INPUT_INVALID",
      category: "user_fixable",
      retryable: false,
      userMessage: "这次图片没生成成功：请求参数不符合 fal 接口要求。",
      actionHint: "请检查提示词和参考图参数后重试。",
      upstreamType: ctx.modelType || ctx.errorType,
    });
  }

  return defaultUnknown("fal", err);
}

export function normalizeLaozhangError(err: unknown): StellaErrorDetails {
  const ctx: NormalizationContext = {
    message: readMessage(err),
    status: readStatus(err),
    lower: readMessage(err).toLowerCase(),
  };

  if (ctx.message.includes("LAOZHANG_API_KEY is not set")) {
    return makeDetails("laozhang", ctx, {
      code: "CONFIG_MISSING",
      category: "config",
      retryable: false,
      userMessage: "这次图片没生成成功：缺少 laozhang.ai API Key。",
      actionHint: "请在 skills.entries.stella-selfie.env 中配置 LAOZHANG_API_KEY 后重试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.lower.includes("safety") ||
    ctx.lower.includes("block_reason") ||
    ctx.lower.includes("blockedreason")
  ) {
    return makeDetails("laozhang", ctx, {
      code: "SAFETY_BLOCKED",
      category: "policy",
      retryable: false,
      userMessage: "这次图片没生成成功：请求触发了内容安全限制。",
      actionHint: "请改用更中性、非敏感的描述后再试。",
      upstreamType: undefined,
    });
  }

  if (ctx.status === 400) {
    return makeDetails("laozhang", ctx, {
      code: "INPUT_INVALID",
      category: "user_fixable",
      retryable: false,
      userMessage: "这次图片没生成成功：请求参数不合法。",
      actionHint: "请简化提示词或调整参数后重试。",
      upstreamType: undefined,
    });
  }

  if (ctx.status === 401 || ctx.status === 403 || ctx.lower.includes("permission_denied")) {
    return makeDetails("laozhang", ctx, {
      code: "AUTH_INVALID_KEY",
      category: "auth",
      retryable: false,
      userMessage: "这次图片没生成成功：laozhang.ai 鉴权失败或权限不足。",
      actionHint: "请检查 LAOZHANG_API_KEY 是否正确、可用，并已在令牌设置中配置计费模式。",
      upstreamType: undefined,
    });
  }

  if (ctx.status === 404 || ctx.lower.includes("not_found")) {
    return makeDetails("laozhang", ctx, {
      code: "RESOURCE_NOT_FOUND",
      category: "user_fixable",
      retryable: false,
      userMessage: "这次图片没生成成功：请求引用的资源不存在。",
      actionHint: "请检查输入资源路径或链接后重试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.status === 429 ||
    ctx.lower.includes("resource_exhausted") ||
    ctx.lower.includes("rate limit")
  ) {
    return makeDetails("laozhang", ctx, {
      code: "RATE_LIMITED",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：请求过于频繁。",
      actionHint: "请等待 1-2 分钟后重试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.status === 504 ||
    ctx.lower.includes("deadline_exceeded") ||
    ctx.lower.includes("timeout")
  ) {
    return makeDetails("laozhang", ctx, {
      code: "TIMEOUT",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：laozhang.ai 处理超时。",
      actionHint: "请稍后重试，或简化提示词后再试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.lower.includes("econnreset") ||
    ctx.lower.includes("etimedout") ||
    ctx.lower.includes("fetch failed") ||
    ctx.lower.includes("network") ||
    ctx.lower.includes("socket hang up") ||
    ctx.lower.includes("eai_again") ||
    ctx.lower.includes("enotfound")
  ) {
    return makeDetails("laozhang", ctx, {
      code: "UPSTREAM_UNAVAILABLE",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：网络或上游服务暂时不可用。",
      actionHint: "请稍后重试。",
      upstreamType: undefined,
    });
  }

  if (
    ctx.status === 500 ||
    ctx.status === 503 ||
    ctx.lower.includes("unavailable") ||
    ctx.lower.includes("internal")
  ) {
    return makeDetails("laozhang", ctx, {
      code: "UPSTREAM_UNAVAILABLE",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：laozhang.ai 服务暂时不可用。",
      actionHint: "请稍后重试，必要时切换其他 Provider。",
      upstreamType: undefined,
    });
  }

  if (ctx.lower.includes("no image data") || ctx.lower.includes("no content parts")) {
    return makeDetails("laozhang", ctx, {
      code: "NO_OUTPUT",
      category: "transient",
      retryable: true,
      userMessage: "这次图片没生成成功：模型未返回有效图片。",
      actionHint: "请直接重试一次，或稍微改写提示词后再试。",
      upstreamType: undefined,
    });
  }

  return defaultUnknown("laozhang", err);
}

export function normalizeOpenClawSendError(err: unknown): StellaErrorDetails {
  const message = readMessage(err);
  return {
    provider: "openclaw",
    code: "SEND_FAILED",
    category: "transient",
    retryable: true,
    userMessage: "消息发送失败。",
    actionHint: "请检查 OpenClaw CLI 与 Gateway 连通性后重试。",
    rawMessage: message,
  };
}

export function toStellaError(details: StellaErrorDetails, cause?: unknown): StellaError {
  return new StellaError(details, cause);
}

export function isStellaError(err: unknown): err is StellaError {
  return err instanceof StellaError;
}

export function asStellaError(provider: StellaProvider, err: unknown): StellaError {
  if (isStellaError(err)) return err;
  if (provider === "gemini") return toStellaError(normalizeGeminiError(err), err);
  if (provider === "fal") return toStellaError(normalizeFalError(err), err);
  if (provider === "laozhang") return toStellaError(normalizeLaozhangError(err), err);
  return toStellaError(normalizeOpenClawSendError(err), err);
}

export function shouldRetryGemini(err: unknown): boolean {
  return normalizeGeminiError(err).retryable;
}

export function shouldRetryFal(err: unknown): boolean {
  return normalizeFalError(err).retryable;
}

export function shouldRetryLaozhang(err: unknown): boolean {
  return normalizeLaozhangError(err).retryable;
}

export function formatFailureMessage(details: StellaErrorDetails): string {
  return `${details.userMessage} ${details.actionHint}`;
}
