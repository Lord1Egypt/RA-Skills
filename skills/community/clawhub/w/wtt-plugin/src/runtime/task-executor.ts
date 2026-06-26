import {
  createProgressHeartbeatScheduler,
  type ProgressHeartbeatPayload,
} from "./progress-ticker.js";
import {
  validateTaskTransition,
  type RuntimeTransitionResult,
} from "./status-transition.js";
import {
  TaskRunExecutorQueueStore,
  resolveTaskRunExecutorPersistenceOptions,
  type PersistedTaskRunQueueItem,
  type TaskRunApiContext,
  type TaskRunExecutorIntent,
  type TaskRunExecutorPersistenceOptions,
  type TaskRunIntentMetadata,
  type TaskRunRecoveryMetadata,
} from "./task-executor-persistence.js";

type HttpMethod = "GET" | "POST" | "PATCH";

const DEFAULT_API_TIMEOUT_MS = 12_000;
const DEFAULT_MAX_RECOVERY_RETRY_COUNT = 2;
const DEFAULT_REVIEW_PATCH_RETRY_DELAYS_MS = [250, 750];
const DEFAULT_COMPENSATING_REVIEW_DELAY_MS = 15_000;
const DEFAULT_COMPENSATING_REVIEW_RETRY_DELAYS_MS = [500, 1_500];
const TERMINAL_OR_REVIEW_STATUSES = new Set(["review", "done", "approved", "rejected", "cancelled"]);

type RecoverySource = "queued" | "running";
type InflightState = "queued" | "running";

export interface TaskRuntimeMetadata extends TaskRunIntentMetadata {}

export interface RuntimeApiRequest {
  method: HttpMethod;
  path: string;
  body?: unknown;
}

export interface TaskRunDetailPayload {
  id: string;
  title: string;
  description: string;
  topicId: string;
  taskType: string;
  execMode: string;
  status: string;
}

export interface TaskRunInferenceRequest {
  taskId: string;
  prompt: string;
  task: TaskRunDetailPayload;
  accountId: string;
}

export interface TaskRunInferenceUsage {
  promptTokens?: number;
  completionTokens?: number;
  cacheReadTokens?: number;
  cacheWriteTokens?: number;
  totalTokens?: number;
  source?: string;
  provider?: string;
  model?: string;
}

export interface TaskRunInferenceResult {
  outputText: string;
  provider?: string;
  usage?: TaskRunInferenceUsage;
  raw?: unknown;
}

export interface TaskRunSessionRuntimeMetrics {
  source?: string;
  queueDepth?: number;
  queueMode?: string;
  sessionKey?: string;
  inflight?: boolean;
}

export interface TaskRunExecutorRequest extends TaskRunExecutorIntent {
  now?: () => Date;
  apiRequest: (request: RuntimeApiRequest) => Promise<unknown>;
  publishHeartbeat?: (payload: ProgressHeartbeatPayload) => Promise<void> | void;
  fetchTaskDetail?: () => Promise<unknown>;
  invokeTaskInference?: (request: TaskRunInferenceRequest) => Promise<TaskRunInferenceResult>;
  getSessionRuntimeMetrics?: () => Promise<TaskRunSessionRuntimeMetrics | undefined> | TaskRunSessionRuntimeMetrics | undefined;
}

export interface TaskRunSummaryPayload {
  kind: "task_run_summary";
  taskId: string;
  at: string;
  status: string;
  action: string;
  transitionApplied: "run_endpoint" | "patch_status" | "none";
  notes: string[];
  nextSteps: string[];
  outputPreview?: string;
}

export interface TaskRunPersistenceAck {
  enabled: boolean;
  filePath?: string;
  recoveredFrom?: RecoverySource;
}

export interface TaskRunIdempotencyDecision {
  decision: "enqueued" | "deduplicated";
  idempotencyKey: string;
  triggerContextKey: string;
  reason: string;
  duplicateState?: InflightState;
  duplicateTaskId?: string;
  duplicateEnqueuedAt?: string;
}

export interface TaskRunExecutionResult {
  deduplicated: false;
  taskId: string;
  accountId: string;
  queue: {
    enqueuedAt: string;
    dequeuedAt: string;
    finishedAt: string;
    pendingAfterDequeue: number;
  };
  transition: RuntimeTransitionResult;
  transitionApplied: "run_endpoint" | "patch_status" | "none";
  endpointFallbackUsed: boolean;
  fallbackMessage?: string;
  finalStatus: string;
  task: TaskRunDetailPayload;
  inference: {
    attempted: boolean;
    succeeded: boolean;
    provider: string;
    outputText: string;
    prompt: string;
    usage?: TaskRunInferenceUsage;
    error?: string;
  };
  heartbeatPayloads: ProgressHeartbeatPayload[];
  heartbeatPublished: number;
  heartbeatPublishErrors: string[];
  summary: TaskRunSummaryPayload;
  persistence: TaskRunPersistenceAck;
  idempotency: TaskRunIdempotencyDecision;
  recovery?: TaskRunRecoveryMetadata;
}

export interface TaskRunDedupResult {
  deduplicated: true;
  taskId: string;
  accountId: string;
  queueLength: number;
  runningTaskId: string | null;
  persistence: TaskRunPersistenceAck;
  idempotency: TaskRunIdempotencyDecision;
}

export type TaskRunEnqueueResult = TaskRunExecutionResult | TaskRunDedupResult;

interface QueueItem {
  request: TaskRunExecutorRequest;
  enqueuedAt: Date;
  resolve: (value: TaskRunEnqueueResult) => void;
  reject: (reason: unknown) => void;
  idempotencyKey: string;
  triggerContextKey: string;
  recovery?: {
    source: RecoverySource;
    note: string;
  };
}

export interface TaskRunExecutorSnapshot {
  queueLength: number;
  runningTaskId: string | null;
  processing: boolean;
  stopping: boolean;
  lastError: string | null;
  persistenceEnabled: boolean;
  persistenceFilePath?: string;
  enqueueAccepted: number;
  dedupHits: number;
  recovery: {
    loadedQueued: number;
    loadedRunning: number;
    requeued: number;
    skippedTerminalOrReview: number;
    skippedByRetryCap: number;
    retryAttempts: number;
  };
  drainLockContention: number;
}

export interface TaskRunExecutorLoop {
  enqueueRun: (request: TaskRunExecutorRequest) => Promise<TaskRunEnqueueResult>;
  getQueueDepth: () => number;
  isProcessing: () => boolean;
  getSnapshot: () => TaskRunExecutorSnapshot;
  getStatus: () => TaskRunExecutorSnapshot;
  stopGracefully: () => Promise<void>;
}

export interface TaskRunExecutorLoopOptions {
  persistence?: TaskRunExecutorPersistenceOptions;
  createRecoveredApiRequest?: (
    intent: TaskRunExecutorIntent,
    source: RecoverySource,
  ) => TaskRunExecutorRequest["apiRequest"] | undefined;
  onRecoveredExecutionResult?: (result: TaskRunEnqueueResult) => void;
  onRecoveredExecutionError?: (error: unknown, intent: TaskRunExecutorIntent) => void;
  maxRecoveryRetryCount?: number;
  reviewPatchRetryDelaysMs?: number[];
  compensatingReviewDelayMs?: number;
  compensatingReviewRetryDelaysMs?: number[];
}

function toErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  return String(error);
}

function isEndpointUnavailableError(error: unknown): boolean {
  if (!error || typeof error !== "object") return false;
  const code = (error as { code?: unknown }).code;
  return code === "ENDPOINT_UNAVAILABLE";
}

function normalizeAgentId(raw: string | undefined): string | undefined {
  if (!raw) return undefined;
  const value = raw.trim();
  return value || undefined;
}

function normalizeContextToken(raw: string | undefined, fallback = "-"): string {
  const normalized = raw?.trim();
  return normalized || fallback;
}

function normalizeRetryDelaysMs(raw: number[] | undefined, fallback: number[]): number[] {
  if (!Array.isArray(raw) || raw.length === 0) return [...fallback];

  const normalized = raw
    .map((value) => (Number.isFinite(value) ? Math.max(0, Math.floor(value)) : 0));

  return normalized.length > 0 ? normalized : [...fallback];
}

async function sleepMs(timeoutMs: number): Promise<void> {
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) return;
  await new Promise<void>((resolve) => {
    setTimeout(resolve, timeoutMs);
  });
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
  if (!value || typeof value !== "object" || Array.isArray(value)) return undefined;
  return value as Record<string, unknown>;
}

function pickString(input: Record<string, unknown> | undefined, keys: string[], fallback = "-"): string {
  if (!input) return fallback;

  for (const key of keys) {
    const value = input[key];
    if (typeof value === "string" && value.trim()) {
      return value.trim();
    }
  }

  return fallback;
}

function pickNumber(input: Record<string, unknown> | undefined, keys: string[], fallback = 0): number {
  if (!input) return fallback;
  for (const key of keys) {
    const raw = input[key];
    const n = Number(raw);
    if (Number.isFinite(n)) {
      return Math.max(0, Math.floor(n));
    }
  }
  return fallback;
}

interface TaskTokenUsageTotals {
  promptTokens: number;
  completionTokens: number;
  cacheReadTokens: number;
  cacheWriteTokens: number;
  totalTokens: number;
}

function readTaskUsageTotals(raw?: unknown): TaskTokenUsageTotals {
  const payload = asRecord(raw);
  return {
    promptTokens: pickNumber(payload, ["usage_prompt_tokens", "usagePromptTokens"], 0),
    completionTokens: pickNumber(payload, ["usage_completion_tokens", "usageCompletionTokens"], 0),
    cacheReadTokens: pickNumber(payload, ["usage_cache_read_tokens", "usageCacheReadTokens"], 0),
    cacheWriteTokens: pickNumber(payload, ["usage_cache_write_tokens", "usageCacheWriteTokens"], 0),
    totalTokens: pickNumber(payload, ["usage_total_tokens", "usageTotalTokens"], 0),
  };
}

function normalizeInferenceUsage(raw?: TaskRunInferenceUsage): TaskRunInferenceUsage | undefined {
  if (!raw) return undefined;

  const promptTokens = Math.max(0, Math.floor(Number(raw.promptTokens) || 0));
  const completionTokens = Math.max(0, Math.floor(Number(raw.completionTokens) || 0));
  const cacheReadTokens = Math.max(0, Math.floor(Number(raw.cacheReadTokens) || 0));
  const cacheWriteTokens = Math.max(0, Math.floor(Number(raw.cacheWriteTokens) || 0));

  const providedTotal = Math.max(0, Math.floor(Number(raw.totalTokens) || 0));
  const totalTokens = providedTotal > 0
    ? providedTotal
    : (promptTokens + completionTokens + cacheReadTokens + cacheWriteTokens);

  if (totalTokens <= 0 && promptTokens <= 0 && completionTokens <= 0 && cacheReadTokens <= 0 && cacheWriteTokens <= 0) {
    return undefined;
  }

  return {
    promptTokens,
    completionTokens,
    cacheReadTokens,
    cacheWriteTokens,
    totalTokens,
    source: raw.source,
    provider: raw.provider,
    model: raw.model,
  };
}

function buildUsagePatchFields(base: TaskTokenUsageTotals, delta?: TaskRunInferenceUsage): Record<string, unknown> | undefined {
  const normalized = normalizeInferenceUsage(delta);
  if (!normalized) return undefined;

  const promptTokens = Math.max(0, base.promptTokens + (normalized.promptTokens ?? 0));
  const completionTokens = Math.max(0, base.completionTokens + (normalized.completionTokens ?? 0));
  const cacheReadTokens = Math.max(0, base.cacheReadTokens + (normalized.cacheReadTokens ?? 0));
  const cacheWriteTokens = Math.max(0, base.cacheWriteTokens + (normalized.cacheWriteTokens ?? 0));
  const totalTokens = Math.max(0, base.totalTokens + (normalized.totalTokens ?? 0));

  return {
    usage_prompt_tokens: promptTokens,
    usage_completion_tokens: completionTokens,
    usage_cache_read_tokens: cacheReadTokens,
    usage_cache_write_tokens: cacheWriteTokens,
    usage_total_tokens: totalTokens,
    usage_source: normalized.source || "runtime_inference",
  };
}

function mergeInferenceUsage(base?: TaskRunInferenceUsage, delta?: TaskRunInferenceUsage): TaskRunInferenceUsage | undefined {
  const left = normalizeInferenceUsage(base);
  const right = normalizeInferenceUsage(delta);

  if (!left) return right;
  if (!right) return left;

  return {
    promptTokens: (left.promptTokens ?? 0) + (right.promptTokens ?? 0),
    completionTokens: (left.completionTokens ?? 0) + (right.completionTokens ?? 0),
    cacheReadTokens: (left.cacheReadTokens ?? 0) + (right.cacheReadTokens ?? 0),
    cacheWriteTokens: (left.cacheWriteTokens ?? 0) + (right.cacheWriteTokens ?? 0),
    totalTokens: (left.totalTokens ?? 0) + (right.totalTokens ?? 0),
    source: right.source || left.source,
    provider: right.provider || left.provider,
    model: right.model || left.model,
  };
}

function normalizeTaskDetail(taskId: string, metadata: TaskRuntimeMetadata, raw?: unknown): TaskRunDetailPayload {
  const payload = asRecord(raw);
  return {
    id: pickString(payload, ["id"], metadata.id || taskId),
    title: pickString(payload, ["title"], metadata.title || "(未命名任务)"),
    description: pickString(payload, ["description", "desc"], metadata.description ?? ""),
    topicId: pickString(payload, ["topic_id", "topicId"], metadata.topicId || "-"),
    taskType: pickString(payload, ["task_type", "taskType"], metadata.taskType ?? "generic"),
    execMode: pickString(payload, ["exec_mode", "execMode"], metadata.execMode ?? "default"),
    status: pickString(payload, ["status"], metadata.status || "unknown"),
  };
}

function buildTaskPrompt(task: TaskRunDetailPayload): string {
  const description = task.description && task.description !== "-" ? task.description : "(无描述)";
  return [
    "你正在执行 WTT Task。",
    `task_id: ${task.id}`,
    `title: ${task.title}`,
    `description: ${description}`,
    `topic_id: ${task.topicId}`,
    `task_type: ${task.taskType}`,
    `exec_mode: ${task.execMode}`,
    "输出规则（严格遵守）：",
    "1) 仅输出最终推理结果正文；不要加标题、前言、结语。",
    "2) 禁止输出这些模板词：STEP、MID、CHANGE、任务结果（可审查）、关键依据、可直接用于 review。",
    "3) 禁止输出系统日志/心跳样式文本。",
    "4) 信息不完整时，直接给出简洁可执行结果；不要解释假设过程，不要出现“最小可执行假设”字样。",
  ].join("\n");
}

function deriveTriggerContextKey(request: TaskRunExecutorRequest): string {
  const resolvedRunner = normalizeAgentId(request.runnerAgentId)
    ?? normalizeAgentId(request.metadata.runnerAgentId)
    ?? "-";

  const parts = [
    `account:${normalizeContextToken(request.accountId)}`,
    `trigger:${normalizeContextToken(request.triggerAgentId)}`,
    `runner:${normalizeContextToken(resolvedRunner)}`,
    `pipeline:${normalizeContextToken(request.metadata.pipelineId)}`,
    `topic:${normalizeContextToken(request.metadata.topicId)}`,
  ];

  return parts.join("|");
}

function deriveIdempotencyKey(taskId: string, triggerContextKey: string): string {
  return `${taskId}::${triggerContextKey}`;
}

function normalizeRecoveryMetadata(
  recovery: TaskRunRecoveryMetadata | undefined,
  maxDefault: number,
): TaskRunRecoveryMetadata {
  const maxRetryCount = Math.max(0, Math.floor(recovery?.maxRetryCount ?? maxDefault));
  const retryCount = Math.max(0, Math.floor(recovery?.retryCount ?? 0));

  return {
    retryCount,
    maxRetryCount,
    lastRecoveredAt: recovery?.lastRecoveredAt,
  };
}

function isTerminalOrReviewStatus(status: string | undefined): boolean {
  if (!status) return false;
  return TERMINAL_OR_REVIEW_STATUSES.has(status.trim().toLowerCase());
}

function truncatePreview(text: string, maxLength = 280): string {
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
}

function buildSummary(params: {
  taskId: string;
  now: Date;
  status: string;
  transitionApplied: "run_endpoint" | "patch_status" | "none";
  notes: string[];
  outputText?: string;
  action: string;
}): TaskRunSummaryPayload {
  const output = params.outputText?.trim() ?? "";
  return {
    kind: "task_run_summary",
    taskId: params.taskId,
    at: params.now.toISOString(),
    status: params.status,
    action: params.action,
    transitionApplied: params.transitionApplied,
    notes: params.notes,
    outputPreview: output ? truncatePreview(output) : undefined,
    nextSteps: [
      "每 60 秒汇报一次：时间 / 状态 / 当前动作。",
      "执行结束后复核输出，并按需执行 @wtt task review approve/reject/block。",
      "若结果通过评审，任务应从 review 进入 done。",
    ],
  };
}

function withApiPrefixCandidates(pathname: string): string[] {
  const normalized = pathname.startsWith("/") ? pathname : `/${pathname}`;
  if (normalized.startsWith("/api/")) return [normalized];
  return [normalized, `/api${normalized}`, `/api/v1${normalized}`];
}

function hasJsonContentType(response: Response): boolean {
  const contentType = response.headers.get("content-type") ?? "";
  return contentType.toLowerCase().includes("application/json");
}

async function parseResponseBody(response: Response): Promise<unknown> {
  if (response.status === 204) return {};

  if (hasJsonContentType(response)) {
    try {
      return await response.json();
    } catch {
      // fallthrough
    }
  }

  const text = await response.text();
  if (!text) return {};

  try {
    return JSON.parse(text);
  } catch {
    return { message: text };
  }
}

function extractErrorMessage(payload: unknown): string {
  if (typeof payload === "string" && payload.trim()) return payload.trim();

  if (typeof payload === "object" && payload !== null) {
    const data = payload as Record<string, unknown>;
    for (const key of ["detail", "error", "message", "msg", "reason"]) {
      const value = data[key];
      if (typeof value === "string" && value.trim()) return value.trim();
    }
  }

  return "服务端返回异常";
}

function createErrorWithCode(message: string, code: string): Error & { code: string } {
  const err = new Error(message) as Error & { code: string };
  err.code = code;
  return err;
}

function buildApiRequestFromContext(context: TaskRunApiContext): TaskRunExecutorRequest["apiRequest"] {
  const cloudUrl = context.cloudUrl.replace(/\/$/, "");
  const token = context.token?.trim();
  const timeoutMs = context.timeoutMs ?? DEFAULT_API_TIMEOUT_MS;

  return async (request: RuntimeApiRequest) => {
    const headers: Record<string, string> = {
      Accept: "application/json",
    };

    if (request.body !== undefined) headers["Content-Type"] = "application/json";
    if (token) {
      headers.Authorization = `Bearer ${token}`;
      headers["X-Agent-Token"] = token;
    }

    const candidates = withApiPrefixCandidates(request.path);

    for (const candidate of candidates) {
      const endpoint = `${cloudUrl}${candidate}`;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);

      try {
        const response = await fetch(endpoint, {
          method: request.method,
          headers,
          body: request.body === undefined ? undefined : JSON.stringify(request.body),
          signal: controller.signal,
        });

        const payload = await parseResponseBody(response);

        if (response.ok) return payload;

        if (response.status === 404 || response.status === 405) {
          continue;
        }

        if (response.status === 401 || response.status === 403) {
          throw createErrorWithCode("鉴权失败", "UNAUTHORIZED");
        }

        throw new Error(extractErrorMessage(payload));
      } catch (error) {
        const err = error as NodeJS.ErrnoException;
        const isAbort = error instanceof Error
          && (error.name === "AbortError" || /aborted/i.test(error.message));

        if (isAbort) {
          throw createErrorWithCode("请求超时", "TIMEOUT");
        }

        if (err?.code === "UNAUTHORIZED") {
          throw error;
        }

        if (error instanceof Error) {
          throw createErrorWithCode(error.message, "NETWORK_ERROR");
        }

        throw createErrorWithCode(String(error), "NETWORK_ERROR");
      } finally {
        clearTimeout(timer);
      }
    }

    throw createErrorWithCode("服务端暂未暴露该接口", "ENDPOINT_UNAVAILABLE");
  };
}

function toPersistedIntent(request: TaskRunExecutorRequest): TaskRunExecutorIntent {
  return {
    taskId: request.taskId,
    metadata: request.metadata,
    accountId: request.accountId,
    triggerAgentId: request.triggerAgentId,
    runnerAgentId: request.runnerAgentId,
    note: request.note,
    heartbeatSeconds: request.heartbeatSeconds,
    apiContext: request.apiContext,
    triggerContextKey: request.triggerContextKey,
    idempotencyKey: request.idempotencyKey,
    recovery: request.recovery,
  };
}

function toIsoString(input: string, fallback: Date): string {
  const parsed = new Date(input);
  if (Number.isNaN(parsed.getTime())) return fallback.toISOString();
  return parsed.toISOString();
}

class InMemoryTaskRunExecutor implements TaskRunExecutorLoop {
  private queue: QueueItem[] = [];
  private processing = false;
  private runningItem: QueueItem | undefined;
  private stopping = false;
  private lastError: string | null = null;
  private readonly persistenceEnabled: boolean;
  private readonly persistenceFilePath?: string;
  private readonly queueStore?: TaskRunExecutorQueueStore;
  private readonly createRecoveredApiRequest?: TaskRunExecutorLoopOptions["createRecoveredApiRequest"];
  private readonly onRecoveredExecutionResult?: TaskRunExecutorLoopOptions["onRecoveredExecutionResult"];
  private readonly onRecoveredExecutionError?: TaskRunExecutorLoopOptions["onRecoveredExecutionError"];
  private readonly startupReady: Promise<void>;
  private readonly maxRecoveryRetryCount: number;
  private readonly reviewPatchRetryDelaysMs: number[];
  private readonly compensatingReviewDelayMs: number;
  private readonly compensatingReviewRetryDelaysMs: number[];
  private readonly compensatingTimers = new Set<ReturnType<typeof setTimeout>>();

  private drainInFlight = false;
  private drainRequested = false;
  private drainPromise: Promise<void> | null = null;
  private drainLockContention = 0;

  private enqueueAccepted = 0;
  private dedupHits = 0;
  private recoveryStats = {
    loadedQueued: 0,
    loadedRunning: 0,
    requeued: 0,
    skippedTerminalOrReview: 0,
    skippedByRetryCap: 0,
    retryAttempts: 0,
  };

  constructor(options?: TaskRunExecutorLoopOptions) {
    this.createRecoveredApiRequest = options?.createRecoveredApiRequest;
    this.onRecoveredExecutionResult = options?.onRecoveredExecutionResult;
    this.onRecoveredExecutionError = options?.onRecoveredExecutionError;
    this.maxRecoveryRetryCount = Math.max(0, Math.floor(options?.maxRecoveryRetryCount ?? DEFAULT_MAX_RECOVERY_RETRY_COUNT));
    this.reviewPatchRetryDelaysMs = normalizeRetryDelaysMs(
      options?.reviewPatchRetryDelaysMs,
      DEFAULT_REVIEW_PATCH_RETRY_DELAYS_MS,
    );
    this.compensatingReviewDelayMs = Math.max(
      0,
      Math.floor(options?.compensatingReviewDelayMs ?? DEFAULT_COMPENSATING_REVIEW_DELAY_MS),
    );
    this.compensatingReviewRetryDelaysMs = normalizeRetryDelaysMs(
      options?.compensatingReviewRetryDelaysMs,
      DEFAULT_COMPENSATING_REVIEW_RETRY_DELAYS_MS,
    );

    const persistence = resolveTaskRunExecutorPersistenceOptions(options?.persistence);
    this.persistenceEnabled = persistence.enabled;
    this.persistenceFilePath = persistence.filePath;

    if (this.persistenceEnabled) {
      this.queueStore = new TaskRunExecutorQueueStore(persistence.filePath);
      this.startupReady = this.loadPersistedQueueOnce();
    } else {
      this.startupReady = Promise.resolve();
    }
  }

  async enqueueRun(request: TaskRunExecutorRequest): Promise<TaskRunEnqueueResult> {
    await this.startupReady;

    if (this.stopping) {
      throw new Error("task executor is stopping; reject enqueue");
    }

    const now = request.now ?? (() => new Date());
    const triggerContextKey = request.triggerContextKey ?? deriveTriggerContextKey(request);
    const idempotencyKey = request.idempotencyKey ?? deriveIdempotencyKey(request.taskId, triggerContextKey);

    const duplicate = this.findDuplicate(request.taskId, idempotencyKey);
    if (duplicate) {
      this.dedupHits += 1;
      return {
        deduplicated: true,
        taskId: request.taskId,
        accountId: request.accountId,
        queueLength: this.queue.length,
        runningTaskId: this.runningItem?.request.taskId ?? null,
        persistence: {
          enabled: this.persistenceEnabled,
          filePath: this.persistenceEnabled ? this.persistenceFilePath : undefined,
        },
        idempotency: {
          decision: "deduplicated",
          idempotencyKey,
          triggerContextKey,
          reason: duplicate.reason,
          duplicateState: duplicate.state,
          duplicateTaskId: duplicate.item.request.taskId,
          duplicateEnqueuedAt: duplicate.item.enqueuedAt.toISOString(),
        },
      };
    }

    this.enqueueAccepted += 1;

    return new Promise((resolve, reject) => {
      this.queue.push({
        request: {
          ...request,
          triggerContextKey,
          idempotencyKey,
          recovery: normalizeRecoveryMetadata(request.recovery, this.maxRecoveryRetryCount),
        },
        enqueuedAt: now(),
        resolve,
        reject,
        idempotencyKey,
        triggerContextKey,
      });

      void this.persistQueueState();
      this.requestDrain();
    });
  }

  getQueueDepth(): number {
    return this.queue.length;
  }

  isProcessing(): boolean {
    return this.processing;
  }

  getSnapshot(): TaskRunExecutorSnapshot {
    return {
      queueLength: this.queue.length,
      runningTaskId: this.runningItem?.request.taskId ?? null,
      processing: this.processing,
      stopping: this.stopping,
      lastError: this.lastError,
      persistenceEnabled: this.persistenceEnabled,
      persistenceFilePath: this.persistenceEnabled ? this.persistenceFilePath : undefined,
      enqueueAccepted: this.enqueueAccepted,
      dedupHits: this.dedupHits,
      recovery: {
        loadedQueued: this.recoveryStats.loadedQueued,
        loadedRunning: this.recoveryStats.loadedRunning,
        requeued: this.recoveryStats.requeued,
        skippedTerminalOrReview: this.recoveryStats.skippedTerminalOrReview,
        skippedByRetryCap: this.recoveryStats.skippedByRetryCap,
        retryAttempts: this.recoveryStats.retryAttempts,
      },
      drainLockContention: this.drainLockContention,
    };
  }

  getStatus(): TaskRunExecutorSnapshot {
    return this.getSnapshot();
  }

  async stopGracefully(): Promise<void> {
    this.stopping = true;
    await this.startupReady;
    if (this.drainPromise) {
      await this.drainPromise;
    }

    for (const timer of this.compensatingTimers) {
      clearTimeout(timer);
    }
    this.compensatingTimers.clear();

    await this.persistQueueState();
  }

  private findDuplicate(taskId: string, idempotencyKey: string): {
    state: InflightState;
    item: QueueItem;
    reason: string;
  } | null {
    if (this.runningItem) {
      if (this.runningItem.request.taskId === taskId || this.runningItem.idempotencyKey === idempotencyKey) {
        const sameKey = this.runningItem.idempotencyKey === idempotencyKey;
        return {
          state: "running",
          item: this.runningItem,
          reason: sameKey
            ? "同一 task + trigger context 已在运行中，已触发幂等去重。"
            : "同一 task 已在运行中（触发上下文不同），为避免重复执行已阻止重复入队。",
        };
      }
    }

    const queued = this.queue.find((item) => item.request.taskId === taskId || item.idempotencyKey === idempotencyKey);
    if (queued) {
      const sameKey = queued.idempotencyKey === idempotencyKey;
      return {
        state: "queued",
        item: queued,
        reason: sameKey
          ? "同一 task + trigger context 已在队列中，已触发幂等去重。"
          : "同一 task 已在队列中（触发上下文不同），为避免重复执行已阻止重复入队。",
      };
    }

    return null;
  }

  private requestDrain(): void {
    if (this.stopping) return;

    this.drainRequested = true;
    if (this.drainInFlight) {
      this.drainLockContention += 1;
      return;
    }

    this.drainInFlight = true;
    this.processing = true;
    this.drainPromise = this.runDrainSingleFlight().finally(() => {
      this.processing = false;
      this.drainInFlight = false;
      this.drainPromise = null;
    });
  }

  private async runDrainSingleFlight(): Promise<void> {
    try {
      while (!this.stopping && this.drainRequested) {
        this.drainRequested = false;

        while (!this.stopping && this.queue.length > 0) {
          const item = this.queue.shift();
          if (!item) continue;

          this.runningItem = item;
          await this.persistQueueState();

          try {
            const result = await this.execute(item, this.queue.length);
            item.resolve(result);
          } catch (error) {
            this.lastError = toErrorMessage(error);
            item.reject(error);
          } finally {
            this.runningItem = undefined;
            await this.persistQueueState();
          }
        }
      }
    } finally {
      // noop
    }
  }

  private async loadPersistedQueueOnce(): Promise<void> {
    if (!this.queueStore) return;

    try {
      const state = await this.queueStore.load();
      const now = new Date();
      const recovered: QueueItem[] = [];
      let touchedPersistedState = false;

      const appendRecovered = (item: PersistedTaskRunQueueItem, source: RecoverySource): void => {
        touchedPersistedState = true;

        if (source === "running") this.recoveryStats.loadedRunning += 1;
        else this.recoveryStats.loadedQueued += 1;

        const status = item.intent.metadata.status;
        if (isTerminalOrReviewStatus(status)) {
          this.recoveryStats.skippedTerminalOrReview += 1;
          return;
        }

        const recovery = normalizeRecoveryMetadata(item.intent.recovery, this.maxRecoveryRetryCount);
        const nextRecovery: TaskRunRecoveryMetadata = {
          ...recovery,
        };

        if (source === "running") {
          if (recovery.retryCount >= recovery.maxRetryCount) {
            this.recoveryStats.skippedByRetryCap += 1;
            return;
          }
          nextRecovery.retryCount = recovery.retryCount + 1;
          nextRecovery.lastRecoveredAt = now.toISOString();
          this.recoveryStats.retryAttempts += 1;
        }

        const request = this.buildRecoveredRequest({
          ...item.intent,
          recovery: nextRecovery,
        }, source);

        const triggerContextKey = request.triggerContextKey ?? deriveTriggerContextKey(request);
        const idempotencyKey = request.idempotencyKey ?? deriveIdempotencyKey(request.taskId, triggerContextKey);

        const enqueuedAtRaw = toIsoString(item.enqueuedAt, now);
        const recoveryNote = source === "running"
          ? `检测到任务上次处于 running 未完成，已按恢复模式重新入队（retry ${nextRecovery.retryCount}/${nextRecovery.maxRetryCount}）。`
          : "任务从持久化队列恢复。";

        recovered.push({
          request: {
            ...request,
            triggerContextKey,
            idempotencyKey,
            recovery: nextRecovery,
          },
          enqueuedAt: new Date(enqueuedAtRaw),
          resolve: (result) => {
            this.onRecoveredExecutionResult?.(result);
          },
          reject: (error) => {
            this.lastError = `recovered task ${request.taskId} failed: ${toErrorMessage(error)}`;
            this.onRecoveredExecutionError?.(error, item.intent);
          },
          recovery: {
            source,
            note: recoveryNote,
          },
          idempotencyKey,
          triggerContextKey,
        });
      };

      if (state.running) {
        appendRecovered(state.running, "running");
      }
      for (const item of state.queued) {
        appendRecovered(item, "queued");
      }

      for (const item of recovered) {
        const duplicate = this.findDuplicate(item.request.taskId, item.idempotencyKey);
        if (duplicate) {
          this.dedupHits += 1;
          continue;
        }
        this.queue.push(item);
        this.recoveryStats.requeued += 1;
      }

      if (touchedPersistedState) {
        await this.persistQueueState();
      }

      if (this.queue.length > 0) {
        this.requestDrain();
      }
    } catch (error) {
      this.lastError = `load persisted queue failed: ${toErrorMessage(error)}`;
    }
  }

  private buildRecoveredRequest(intent: TaskRunExecutorIntent, source: RecoverySource): TaskRunExecutorRequest {
    const apiRequest = this.createRecoveredApiRequest?.(intent, source)
      ?? (intent.apiContext ? buildApiRequestFromContext(intent.apiContext) : undefined)
      ?? (async () => {
        throw createErrorWithCode(
          "recovered task missing apiContext/createRecoveredApiRequest",
          "ENDPOINT_UNAVAILABLE",
        );
      });

    return {
      taskId: intent.taskId,
      metadata: intent.metadata,
      accountId: intent.accountId,
      triggerAgentId: intent.triggerAgentId,
      runnerAgentId: intent.runnerAgentId,
      note: intent.note,
      heartbeatSeconds: intent.heartbeatSeconds,
      apiContext: intent.apiContext,
      triggerContextKey: intent.triggerContextKey,
      idempotencyKey: intent.idempotencyKey,
      recovery: normalizeRecoveryMetadata(intent.recovery, this.maxRecoveryRetryCount),
      apiRequest,
    };
  }

  private async persistQueueState(): Promise<void> {
    if (!this.queueStore) return;

    try {
      await this.queueStore.save({
        queued: this.queue.map((item) => ({
          intent: toPersistedIntent(item.request),
          enqueuedAt: item.enqueuedAt.toISOString(),
        })),
        running: this.runningItem
          ? {
            intent: toPersistedIntent(this.runningItem.request),
            enqueuedAt: this.runningItem.enqueuedAt.toISOString(),
          }
          : undefined,
      });
    } catch (error) {
      this.lastError = `persist queue failed: ${toErrorMessage(error)}`;
    }
  }

  private logReviewTransition(level: "info" | "warn" | "error", message: string): void {
    const line = `[task-executor] ${message}`;
    if (level === "error") {
      console.error(line);
      return;
    }
    if (level === "warn") {
      console.warn(line);
      return;
    }
    console.info(line);
  }

  private async patchTaskStatusWithRetry(params: {
    taskId: string;
    request: TaskRunExecutorRequest;
    status: string;
    notes: string;
    runnerAgentId?: string;
    patchFields?: Record<string, unknown>;
    retryDelaysMs: number[];
    notePrefix: string;
  }): Promise<{ succeeded: boolean; attempts: number; lastError?: string; notes: string[] }> {
    const retryDelaysMs = params.retryDelaysMs.length > 0 ? params.retryDelaysMs : [0];
    const totalAttempts = retryDelaysMs.length + 1;
    const notes: string[] = [];
    let lastError: string | undefined;

    for (let index = 0; index < totalAttempts; index += 1) {
      const attempt = index + 1;
      const attemptPrefix = `${params.notePrefix} attempt ${attempt}/${totalAttempts}`;

      const patchBody: Record<string, unknown> = {
        status: params.status,
        notes: params.notes,
        ...(params.patchFields ?? {}),
      };
      if (params.runnerAgentId) patchBody.runner_agent_id = params.runnerAgentId;

      try {
        await params.request.apiRequest({
          method: "PATCH",
          path: `/tasks/${encodeURIComponent(params.taskId)}`,
          body: patchBody,
        });

        const okNote = `${attemptPrefix} succeeded`;
        notes.push(okNote);
        this.logReviewTransition("info", `${params.taskId} ${okNote}`);
        return {
          succeeded: true,
          attempts: attempt,
          notes,
        };
      } catch (error) {
        lastError = toErrorMessage(error);
        const failedNote = `${attemptPrefix} failed: ${lastError}`;
        notes.push(failedNote);
        this.logReviewTransition("warn", `${params.taskId} ${failedNote}`);

        if (attempt >= totalAttempts) {
          const finalNote = `${params.notePrefix} failed after ${totalAttempts} attempts`;
          notes.push(finalNote);
          this.logReviewTransition("error", `${params.taskId} ${finalNote}`);
          return {
            succeeded: false,
            attempts: attempt,
            lastError,
            notes,
          };
        }

        const delayMs = retryDelaysMs[index] ?? retryDelaysMs[retryDelaysMs.length - 1] ?? 0;
        if (delayMs > 0) {
          const waitNote = `${params.notePrefix} retry backoff ${delayMs}ms before attempt ${attempt + 1}`;
          notes.push(waitNote);
          this.logReviewTransition("info", `${params.taskId} ${waitNote}`);
          await sleepMs(delayMs);
        }
      }
    }

    return {
      succeeded: false,
      attempts: totalAttempts,
      lastError,
      notes,
    };
  }

  private scheduleCompensatingReviewPatch(params: {
    taskId: string;
    request: TaskRunExecutorRequest;
    reviewNotes: string;
    runnerAgentId?: string;
    patchFields?: Record<string, unknown>;
    failureReason: string;
  }): void {
    if (this.stopping) return;

    const delayMs = this.compensatingReviewDelayMs;
    const timer = setTimeout(() => {
      this.compensatingTimers.delete(timer);
      void this.runCompensatingReviewPatch(params);
    }, delayMs);

    this.compensatingTimers.add(timer);
    timer.unref?.();

    this.logReviewTransition(
      "warn",
      `${params.taskId} watchdog scheduled compensating review patch in ${delayMs}ms (reason=${params.failureReason})`,
    );
  }

  private async runCompensatingReviewPatch(params: {
    taskId: string;
    request: TaskRunExecutorRequest;
    reviewNotes: string;
    runnerAgentId?: string;
    patchFields?: Record<string, unknown>;
    failureReason: string;
  }): Promise<void> {
    if (this.stopping) return;

    const compensatingNotes = [
      params.reviewNotes,
      "",
      `[watchdog] compensating_review_at=${new Date().toISOString()}`,
      `[watchdog] initial_failure=${params.failureReason}`,
    ].join("\n");

    const directReview = await this.patchTaskStatusWithRetry({
      taskId: params.taskId,
      request: params.request,
      status: "review",
      notes: compensatingNotes,
      runnerAgentId: params.runnerAgentId,
      patchFields: params.patchFields,
      retryDelaysMs: this.compensatingReviewRetryDelaysMs,
      notePrefix: "watchdog.review_patch",
    });

    if (directReview.succeeded) {
      this.logReviewTransition("info", `${params.taskId} watchdog compensating review patch succeeded`);
      return;
    }

    const toDoing = await this.patchTaskStatusWithRetry({
      taskId: params.taskId,
      request: params.request,
      status: "doing",
      notes: [
        "watchdog compensation: preparing retry path to review",
        `reason=${directReview.lastError ?? params.failureReason}`,
      ].join("\n"),
      runnerAgentId: params.runnerAgentId,
      retryDelaysMs: [0],
      notePrefix: "watchdog.doing_patch",
    });

    if (!toDoing.succeeded) {
      this.logReviewTransition(
        "error",
        `${params.taskId} watchdog failed to move task back to doing for compensating review patch`,
      );
      return;
    }

    const reviewAfterDoing = await this.patchTaskStatusWithRetry({
      taskId: params.taskId,
      request: params.request,
      status: "review",
      notes: compensatingNotes,
      runnerAgentId: params.runnerAgentId,
      patchFields: params.patchFields,
      retryDelaysMs: this.compensatingReviewRetryDelaysMs,
      notePrefix: "watchdog.review_patch_after_doing",
    });

    if (reviewAfterDoing.succeeded) {
      this.logReviewTransition("info", `${params.taskId} watchdog compensating review patch succeeded after doing bridge`);
    } else {
      this.logReviewTransition(
        "error",
        `${params.taskId} watchdog compensating review patch still failed: ${reviewAfterDoing.lastError ?? "unknown"}`,
      );
    }
  }

  private async execute(item: QueueItem, pendingAfterDequeue: number): Promise<TaskRunExecutionResult> {
    const request = item.request;
    const nowFn = request.now ?? (() => new Date());
    const dequeuedAt = nowFn();

    const transition = validateTaskTransition({
      currentStatus: request.metadata.status,
      intent: { kind: "run" },
    });

    let heartbeatPublished = 0;
    const heartbeatPublishErrors: string[] = [];

    let task = normalizeTaskDetail(request.taskId, request.metadata);
    let taskUsageTotals = readTaskUsageTotals();
    const runnerAgentId = normalizeAgentId(request.runnerAgentId) ?? normalizeAgentId(request.metadata.runnerAgentId);

    const inferenceState: TaskRunExecutionResult["inference"] = {
      attempted: false,
      succeeded: false,
      provider: "none",
      outputText: "",
      prompt: "",
    };

    const scheduler = createProgressHeartbeatScheduler({
      taskId: request.taskId,
      status: transition.allowed ? transition.toStatus : transition.fromStatus,
      action: "任务已进入本地执行器",
      heartbeatSeconds: request.heartbeatSeconds,
      now: nowFn,
      getMetrics: async () => {
        const elapsedSeconds = Math.max(0, Math.floor((nowFn().getTime() - dequeuedAt.getTime()) / 1000));

        let runtimeMetrics: TaskRunSessionRuntimeMetrics | undefined;
        if (request.getSessionRuntimeMetrics) {
          try {
            runtimeMetrics = await request.getSessionRuntimeMetrics();
          } catch {
            runtimeMetrics = undefined;
          }
        }

        return {
          elapsedSeconds,
          queueDepth: Number.isFinite(runtimeMetrics?.queueDepth)
            ? Math.max(0, Math.floor(Number(runtimeMetrics?.queueDepth)))
            : Math.max(0, pendingAfterDequeue),
          queueMode: runtimeMetrics?.queueMode,
          source: runtimeMetrics?.source,
          sessionKey: runtimeMetrics?.sessionKey,
          inflight: typeof runtimeMetrics?.inflight === "boolean" ? runtimeMetrics.inflight : true,
        };
      },
      publish: async (payload) => {
        if (!request.publishHeartbeat) return;
        try {
          await request.publishHeartbeat(payload);
          heartbeatPublished += 1;
        } catch (error) {
          heartbeatPublishErrors.push(toErrorMessage(error));
        }
      },
    });

    scheduler.start();

    let transitionApplied: "run_endpoint" | "patch_status" | "none" = "none";
    let endpointFallbackUsed = false;
    let fallbackMessage: string | undefined;
    const summaryNotes: string[] = [];

    const buildResult = (params: {
      finishedAt: Date;
      finalStatus: string;
      action: string;
      outputText?: string;
    }): TaskRunExecutionResult => ({
      deduplicated: false,
      taskId: request.taskId,
      accountId: request.accountId,
      queue: {
        enqueuedAt: item.enqueuedAt.toISOString(),
        dequeuedAt: dequeuedAt.toISOString(),
        finishedAt: params.finishedAt.toISOString(),
        pendingAfterDequeue,
      },
      transition,
      transitionApplied,
      endpointFallbackUsed,
      fallbackMessage,
      finalStatus: params.finalStatus,
      task,
      inference: inferenceState,
      heartbeatPayloads: scheduler.getGeneratedPayloads(),
      heartbeatPublished,
      heartbeatPublishErrors,
      summary: buildSummary({
        taskId: request.taskId,
        now: params.finishedAt,
        status: params.finalStatus,
        transitionApplied,
        notes: summaryNotes,
        action: params.action,
        outputText: params.outputText,
      }),
      persistence: {
        enabled: this.persistenceEnabled,
        filePath: this.persistenceEnabled ? this.persistenceFilePath : undefined,
        recoveredFrom: item.recovery?.source,
      },
      idempotency: {
        decision: "enqueued",
        idempotencyKey: item.idempotencyKey,
        triggerContextKey: item.triggerContextKey,
        reason: "任务已通过幂等校验并成功入队。",
      },
      recovery: request.recovery,
    });

    try {
      const recoveryNote = item.recovery?.source === "running"
        ? item.recovery.note
        : undefined;

      await scheduler.emitNow({
        action: recoveryNote
          ? `${recoveryNote} 已开始执行。`
          : "任务已从队列出队，开始执行",
      });

      if (recoveryNote) {
        summaryNotes.push(recoveryNote);
      }

      if (!transition.allowed) {
        summaryNotes.push(`状态校验未通过：${transition.reason}`);
        summaryNotes.push(`建议动作：${transition.nextAction}`);

        await scheduler.emitNow({
          status: transition.fromStatus,
          action: "状态校验未通过，终止执行",
        });

        const finishedAt = nowFn();
        return buildResult({
          finishedAt,
          finalStatus: transition.fromStatus,
          action: "状态校验失败，未执行推理",
        });
      }

      const currentStatus = String(task.status || "").trim().toLowerCase();
      const alreadyDoing = currentStatus === "doing";

      if (alreadyDoing) {
        transitionApplied = "none";
        summaryNotes.push("任务当前已是 doing，跳过 /run 调用，直接进入执行阶段。");
      } else {
        const runBody: Record<string, unknown> = {
          trigger_agent_id: normalizeAgentId(request.triggerAgentId),
          note: request.note ?? "triggered by wtt_plugin internal executor",
        };
        if (runnerAgentId) runBody.runner_agent_id = runnerAgentId;

        if (recoveryNote) {
          runBody.note = `${runBody.note} | [recovery] ${recoveryNote}`;
        }

        try {
          await request.apiRequest({
            method: "POST",
            path: `/tasks/${encodeURIComponent(request.taskId)}/run`,
            body: runBody,
          });
          transitionApplied = "run_endpoint";
          summaryNotes.push("已调用 POST /tasks/{task_id}/run 推进状态到 doing。");
        } catch (error) {
          if (!isEndpointUnavailableError(error)) {
            throw error;
          }

          endpointFallbackUsed = true;
          const runUnavailable = toErrorMessage(error);

          try {
            const patchBody: Record<string, unknown> = {
              status: "doing",
              notes: "internal executor fallback: /run endpoint unavailable",
            };
            if (runnerAgentId) patchBody.runner_agent_id = runnerAgentId;

            await request.apiRequest({
              method: "PATCH",
              path: `/tasks/${encodeURIComponent(request.taskId)}`,
              body: patchBody,
            });

            transitionApplied = "patch_status";
            fallbackMessage = "run API 不可用，已降级为 PATCH /tasks/{task_id} 推进到 doing。";
            summaryNotes.push(`run API 不可用：${runUnavailable}`);
            summaryNotes.push("已通过 PATCH /tasks/{task_id} 进行状态推进（fallback）。");
          } catch (patchError) {
            if (!isEndpointUnavailableError(patchError)) {
              throw patchError;
            }

            transitionApplied = "none";
            const patchUnavailable = toErrorMessage(patchError);
            fallbackMessage = "run 与 patch 状态接口均不可用，无法推进到 doing。";
            summaryNotes.push(`run API 不可用：${runUnavailable}`);
            summaryNotes.push(`patch API 不可用：${patchUnavailable}`);
            summaryNotes.push("请确认后端暴露 /tasks/{id}/run 或 PATCH /tasks/{id}。");
            throw createErrorWithCode(fallbackMessage, "ENDPOINT_UNAVAILABLE");
          }
        }
      }

      await scheduler.emitNow({
        status: "doing",
        action: alreadyDoing
          ? "任务已处于 doing，直接进入执行阶段"
          : transitionApplied === "run_endpoint"
            ? "任务状态已推进到 doing，准备拉取任务详情"
            : "任务状态已通过 fallback 推进到 doing，准备拉取任务详情",
      });

      let detailPayload: unknown;
      try {
        detailPayload = request.fetchTaskDetail
          ? await request.fetchTaskDetail()
          : await request.apiRequest({
            method: "GET",
            path: `/tasks/${encodeURIComponent(request.taskId)}`,
          });
        task = normalizeTaskDetail(request.taskId, request.metadata, detailPayload);
        taskUsageTotals = readTaskUsageTotals(detailPayload);
      } catch (error) {
        summaryNotes.push(`拉取任务详情失败：${toErrorMessage(error)}，改用入队元数据继续执行。`);
      }

      const prompt = buildTaskPrompt(task);
      inferenceState.prompt = prompt;
      inferenceState.attempted = true;

      await scheduler.emitNow({
        status: "doing",
        action: "调用 Agent 推理执行任务",
      });

      if (!request.invokeTaskInference) {
        throw createErrorWithCode(
          "gateway runtime 未提供推理调度钩子（invokeTaskInference）",
          "RUNTIME_HOOK_UNAVAILABLE",
        );
      }

      const inferenceResult = await request.invokeTaskInference({
        taskId: request.taskId,
        prompt,
        task,
        accountId: request.accountId,
      });

      let outputText = (inferenceResult.outputText ?? "").trim();
      inferenceState.provider = inferenceResult.provider?.trim() || "invokeTaskInference";
      inferenceState.usage = mergeInferenceUsage(inferenceState.usage, inferenceResult.usage);

      if (!outputText) {
        const retryPrompt = `${prompt}\n\n补充要求：请至少输出一段最终结论，不能留空。`;
        const retryResult = await request.invokeTaskInference({
          taskId: request.taskId,
          prompt: retryPrompt,
          task,
          accountId: request.accountId,
        });

        inferenceState.usage = mergeInferenceUsage(inferenceState.usage, retryResult.usage);

        const retryText = (retryResult.outputText ?? "").trim();
        if (retryText) {
          outputText = retryText;
          const retryProvider = retryResult.provider?.trim() || inferenceState.provider;
          inferenceState.provider = `${retryProvider}+retry`;
        }
      }

      inferenceState.outputText = outputText;
      inferenceState.succeeded = true;

      const reviewNote = outputText || "任务已执行完成。";

      const usagePatchFields = buildUsagePatchFields(taskUsageTotals, inferenceState.usage);

      summaryNotes.push(
        `executor_output_at=${nowFn().toISOString()}`,
        `provider=${inferenceState.provider}`,
      );
      if (inferenceState.usage?.totalTokens && inferenceState.usage.totalTokens > 0) {
        summaryNotes.push(`tokens.total=${inferenceState.usage.totalTokens}`);
      }

      const reviewTransitionResult = await this.patchTaskStatusWithRetry({
        taskId: request.taskId,
        request,
        status: "review",
        notes: reviewNote,
        runnerAgentId,
        patchFields: usagePatchFields,
        retryDelaysMs: this.reviewPatchRetryDelaysMs,
        notePrefix: "review_status_patch",
      });

      summaryNotes.push(...reviewTransitionResult.notes);

      if (reviewTransitionResult.succeeded) {
        await scheduler.emitNow({
          status: "review",
          action: "推理完成，任务已推进到 review",
        });

        summaryNotes.push("任务已推进：todo -> doing -> review。");
        summaryNotes.push(`推理输出长度：${outputText.length} 字符。`);

        const finishedAt = nowFn();
        return buildResult({
          finishedAt,
          finalStatus: "review",
          action: "执行完成，等待 review 审批",
          outputText,
        });
      }

      const reviewFailureReason = reviewTransitionResult.lastError ?? "review 状态回写失败";
      inferenceState.error = `inference succeeded but review patch failed: ${reviewFailureReason}`;
      summaryNotes.push(
        `watchdog: 推理成功但 review 回写失败（attempts=${reviewTransitionResult.attempts}）：${reviewFailureReason}`,
      );

      let finalStatus = "doing";
      const watchdogBlockedPatch = await this.patchTaskStatusWithRetry({
        taskId: request.taskId,
        request,
        status: "blocked",
        notes: [
          "internal executor watchdog triggered",
          "reason: inference succeeded but failed to patch review",
          `review_attempts=${reviewTransitionResult.attempts}`,
          `review_error=${reviewFailureReason}`,
        ].join("\n"),
        runnerAgentId,
        retryDelaysMs: [0],
        notePrefix: "watchdog.blocked_patch",
      });
      summaryNotes.push(...watchdogBlockedPatch.notes);

      if (watchdogBlockedPatch.succeeded) {
        finalStatus = "blocked";
        summaryNotes.push("watchdog: 已将任务标记为 blocked，等待补偿更新或人工介入。");
      } else {
        summaryNotes.push(`watchdog: blocked 状态回写失败：${watchdogBlockedPatch.lastError ?? "unknown"}`);
      }

      this.scheduleCompensatingReviewPatch({
        taskId: request.taskId,
        request,
        reviewNotes: reviewNote,
        runnerAgentId,
        patchFields: usagePatchFields,
        failureReason: reviewFailureReason,
      });
      summaryNotes.push(`watchdog: 已排队延迟 ${this.compensatingReviewDelayMs}ms 的补偿 review 回写。`);

      await scheduler.emitNow({
        status: finalStatus,
        action: "推理成功但 review 回写失败，已触发 watchdog",
      });

      const finishedAt = nowFn();
      return buildResult({
        finishedAt,
        finalStatus,
        action: "推理成功但 review 回写失败，已触发补偿",
        outputText,
      });
    } catch (error) {
      const errMsg = toErrorMessage(error);
      inferenceState.error = errMsg;
      if (!inferenceState.succeeded) {
        inferenceState.outputText = "";
      }

      summaryNotes.push(`执行失败：${errMsg}`);

      let finalStatus = transitionApplied === "none" ? transition.fromStatus : "doing";
      try {
        const blockedPatchBody: Record<string, unknown> = {
          status: "blocked",
          notes: `internal executor failed: ${errMsg}`,
        };
        if (runnerAgentId) blockedPatchBody.runner_agent_id = runnerAgentId;

        await request.apiRequest({
          method: "PATCH",
          path: `/tasks/${encodeURIComponent(request.taskId)}`,
          body: blockedPatchBody,
        });
        finalStatus = "blocked";
        summaryNotes.push("失败后已自动标记为 blocked。请人工介入。");
      } catch (patchError) {
        summaryNotes.push(`失败状态回写 blocked 失败：${toErrorMessage(patchError)}`);
      }

      await scheduler.emitNow({
        status: finalStatus,
        action: "执行失败，任务已停止",
      });

      const finishedAt = nowFn();
      return buildResult({
        finishedAt,
        finalStatus,
        action: "执行失败，已记录错误",
      });
    } finally {
      scheduler.stop();
    }
  }

}

export function createTaskRunExecutorLoop(options?: TaskRunExecutorLoopOptions): TaskRunExecutorLoop {
  return new InMemoryTaskRunExecutor(options);
}

const sharedTaskRunExecutor = createTaskRunExecutorLoop({
  persistence: { enabled: true },
});

export function getSharedTaskRunExecutor(): TaskRunExecutorLoop {
  return sharedTaskRunExecutor;
}
