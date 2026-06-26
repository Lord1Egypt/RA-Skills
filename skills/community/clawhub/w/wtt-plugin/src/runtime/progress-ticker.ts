const DEFAULT_HEARTBEAT_SECONDS = 60;

export interface ProgressHeartbeatPayload {
  kind: "task_progress_heartbeat";
  taskId: string;
  heartbeatSeconds: number;
  at: string;
  status: string;
  action: string;
  elapsedSeconds?: number;
  queueDepth?: number;
  queueMode?: string;
  source?: string;
  sessionKey?: string;
  inflight?: boolean;
  text: string;
}

export interface ProgressHeartbeatScheduler {
  start: () => void;
  stop: () => void;
  emitNow: (overrides?: { status?: string; action?: string; now?: Date }) => Promise<ProgressHeartbeatPayload>;
  getGeneratedPayloads: () => ProgressHeartbeatPayload[];
  getHeartbeatSeconds: () => number;
}

function normalizeHeartbeatSeconds(raw: number | undefined): number {
  return Number.isFinite(raw)
    ? Math.max(1, Math.floor(raw as number))
    : DEFAULT_HEARTBEAT_SECONDS;
}

function normalizeText(raw: string, fallback: string): string {
  const value = raw.trim();
  return value || fallback;
}

export function buildProgressHeartbeat(params: {
  taskId: string;
  status: string;
  action: string;
  heartbeatSeconds?: number;
  now?: Date;
  elapsedSeconds?: number;
  queueDepth?: number;
  queueMode?: string;
  source?: string;
  sessionKey?: string;
  inflight?: boolean;
}): ProgressHeartbeatPayload {
  const heartbeatSeconds = normalizeHeartbeatSeconds(params.heartbeatSeconds);

  const at = (params.now ?? new Date()).toISOString();
  const status = normalizeText(params.status, "unknown");
  const action = normalizeText(params.action, "(未提供动作描述)");

  const elapsedSeconds = Number.isFinite(params.elapsedSeconds)
    ? Math.max(0, Math.floor(params.elapsedSeconds as number))
    : undefined;
  const queueDepth = Number.isFinite(params.queueDepth)
    ? Math.max(0, Math.floor(params.queueDepth as number))
    : undefined;
  const queueMode = typeof params.queueMode === "string" ? params.queueMode.trim() : "";
  const source = typeof params.source === "string" ? params.source.trim() : "";
  const sessionKey = typeof params.sessionKey === "string" ? params.sessionKey.trim() : "";
  const inflight = typeof params.inflight === "boolean" ? params.inflight : undefined;

  const parts = [`[${at}]`, `状态=${status}`, `动作=${action}`];
  if (typeof elapsedSeconds === "number") parts.push(`elapsed=${elapsedSeconds}s`);
  if (typeof queueDepth === "number") parts.push(`queue_depth=${queueDepth}`);
  if (queueMode) parts.push(`queue_mode=${queueMode}`);
  if (source) parts.push(`source=${source}`);
  if (sessionKey) parts.push(`session=${sessionKey}`);
  if (typeof inflight === "boolean") parts.push(`inflight=${inflight ? 1 : 0}`);
  parts.push(`心跳=${heartbeatSeconds}s`);
  const text = parts.join(" | ");

  return {
    kind: "task_progress_heartbeat",
    taskId: params.taskId,
    heartbeatSeconds,
    at,
    status,
    action,
    elapsedSeconds,
    queueDepth,
    queueMode: queueMode || undefined,
    source: source || undefined,
    sessionKey: sessionKey || undefined,
    inflight,
    text,
  };
}

export function createProgressHeartbeatScheduler(params: {
  taskId: string;
  status: string;
  action: string;
  heartbeatSeconds?: number;
  now?: () => Date;
  getMetrics?: () => (
    { elapsedSeconds?: number; queueDepth?: number; queueMode?: string; source?: string; sessionKey?: string; inflight?: boolean }
    | Promise<{ elapsedSeconds?: number; queueDepth?: number; queueMode?: string; source?: string; sessionKey?: string; inflight?: boolean }>
  );
  publish?: (payload: ProgressHeartbeatPayload) => void | Promise<void>;
  setIntervalFn?: (handler: () => void, timeoutMs: number) => ReturnType<typeof setInterval>;
  clearIntervalFn?: (id: ReturnType<typeof setInterval>) => void;
}): ProgressHeartbeatScheduler {
  const heartbeatSeconds = normalizeHeartbeatSeconds(params.heartbeatSeconds);
  const nowFn = params.now ?? (() => new Date());
  const setIntervalFn = params.setIntervalFn ?? setInterval;
  const clearIntervalFn = params.clearIntervalFn ?? clearInterval;

  let latestStatus = normalizeText(params.status, "unknown");
  let latestAction = normalizeText(params.action, "(未提供动作描述)");
  let timer: ReturnType<typeof setInterval> | null = null;
  const generated: ProgressHeartbeatPayload[] = [];

  const emitNow: ProgressHeartbeatScheduler["emitNow"] = async (overrides) => {
    if (typeof overrides?.status === "string") {
      latestStatus = normalizeText(overrides.status, latestStatus);
    }
    if (typeof overrides?.action === "string") {
      latestAction = normalizeText(overrides.action, latestAction);
    }

    const metrics = params.getMetrics ? await params.getMetrics() : undefined;

    const payload = buildProgressHeartbeat({
      taskId: params.taskId,
      status: latestStatus,
      action: latestAction,
      heartbeatSeconds,
      now: overrides?.now ?? nowFn(),
      elapsedSeconds: metrics?.elapsedSeconds,
      queueDepth: metrics?.queueDepth,
      queueMode: metrics?.queueMode,
      source: metrics?.source,
      sessionKey: metrics?.sessionKey,
      inflight: metrics?.inflight,
    });

    generated.push(payload);
    if (params.publish) {
      await params.publish(payload);
    }

    return payload;
  };

  const start = () => {
    if (timer) return;
    timer = setIntervalFn(() => {
      void emitNow().catch(() => {
        // 由调用方（执行器）记录 publish 错误；定时触发不应中断执行队列
      });
    }, heartbeatSeconds * 1000);
  };

  const stop = () => {
    if (!timer) return;
    clearIntervalFn(timer);
    timer = null;
  };

  return {
    start,
    stop,
    emitNow,
    getGeneratedPayloads: () => [...generated],
    getHeartbeatSeconds: () => heartbeatSeconds,
  };
}
