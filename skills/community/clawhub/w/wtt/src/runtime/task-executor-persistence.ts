import { mkdir, readFile, rename, unlink, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

export interface TaskRunIntentMetadata {
  id: string;
  title: string;
  status: string;
  priority: string;
  ownerAgentId: string;
  runnerAgentId: string;
  pipelineId: string;
  topicId: string;
  description?: string;
  taskType?: string;
  execMode?: string;
}

export interface TaskRunApiContext {
  cloudUrl: string;
  token?: string;
  timeoutMs?: number;
}

export interface TaskRunRecoveryMetadata {
  retryCount: number;
  maxRetryCount: number;
  lastRecoveredAt?: string;
}

export interface TaskRunExecutorIntent {
  taskId: string;
  metadata: TaskRunIntentMetadata;
  accountId: string;
  triggerAgentId?: string;
  runnerAgentId?: string;
  note?: string;
  heartbeatSeconds?: number;
  apiContext?: TaskRunApiContext;
  triggerContextKey?: string;
  idempotencyKey?: string;
  recovery?: TaskRunRecoveryMetadata;
}

export interface PersistedTaskRunQueueItem {
  intent: TaskRunExecutorIntent;
  enqueuedAt: string;
}

export interface PersistedTaskRunQueueState {
  queued: PersistedTaskRunQueueItem[];
  running?: PersistedTaskRunQueueItem;
}

interface PersistedTaskRunQueueFile extends PersistedTaskRunQueueState {
  version: 1;
  updatedAt: string;
}

export interface TaskRunExecutorPersistenceOptions {
  enabled?: boolean;
  dataDir?: string;
  filePath?: string;
}

export interface ResolvedTaskRunExecutorPersistenceOptions {
  enabled: boolean;
  dataDir: string;
  filePath: string;
}

const DEFAULT_RUNTIME_DATA_DIR = fileURLToPath(new URL("../../runtime-data", import.meta.url));
const DEFAULT_QUEUE_FILE_NAME = "task-executor-queue.json";

function asRecord(value: unknown): Record<string, unknown> | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  return value as Record<string, unknown>;
}

function asString(value: unknown): string | undefined {
  if (typeof value !== "string") return undefined;
  const trimmed = value.trim();
  return trimmed || undefined;
}

function asNumber(value: unknown): number | undefined {
  if (typeof value !== "number" || !Number.isFinite(value)) return undefined;
  return value;
}

function asInt(value: unknown): number | undefined {
  const raw = asNumber(value);
  if (raw === undefined) return undefined;
  const normalized = Math.floor(raw);
  if (!Number.isFinite(normalized) || normalized < 0) return undefined;
  return normalized;
}

function parseMetadata(value: unknown): TaskRunIntentMetadata | null {
  const raw = asRecord(value);
  if (!raw) return null;

  const id = asString(raw.id);
  const title = asString(raw.title);
  const status = asString(raw.status);
  const priority = asString(raw.priority);
  const ownerAgentId = asString(raw.ownerAgentId);
  const runnerAgentId = asString(raw.runnerAgentId);
  const pipelineId = asString(raw.pipelineId);
  const topicId = asString(raw.topicId);
  const description = asString(raw.description);
  const taskType = asString(raw.taskType);
  const execMode = asString(raw.execMode);

  if (!id || !title || !status || !priority || !ownerAgentId || !runnerAgentId || !pipelineId || !topicId) {
    return null;
  }

  return {
    id,
    title,
    status,
    priority,
    ownerAgentId,
    runnerAgentId,
    pipelineId,
    topicId,
    description,
    taskType,
    execMode,
  };
}

function parseApiContext(value: unknown): TaskRunApiContext | undefined {
  const raw = asRecord(value);
  if (!raw) return undefined;

  const cloudUrl = asString(raw.cloudUrl);
  if (!cloudUrl) return undefined;

  const token = asString(raw.token);
  const timeoutMs = asNumber(raw.timeoutMs);

  return {
    cloudUrl,
    token,
    timeoutMs,
  };
}

function parseRecovery(value: unknown): TaskRunRecoveryMetadata | undefined {
  const raw = asRecord(value);
  if (!raw) return undefined;

  const retryCount = asInt(raw.retryCount);
  const maxRetryCount = asInt(raw.maxRetryCount);

  if (retryCount === undefined || maxRetryCount === undefined) return undefined;

  return {
    retryCount,
    maxRetryCount,
    lastRecoveredAt: asString(raw.lastRecoveredAt),
  };
}

function parseIntent(value: unknown): TaskRunExecutorIntent | null {
  const raw = asRecord(value);
  if (!raw) return null;

  const taskId = asString(raw.taskId);
  const accountId = asString(raw.accountId);
  const metadata = parseMetadata(raw.metadata);

  if (!taskId || !accountId || !metadata) return null;

  return {
    taskId,
    metadata,
    accountId,
    triggerAgentId: asString(raw.triggerAgentId),
    runnerAgentId: asString(raw.runnerAgentId),
    note: asString(raw.note),
    heartbeatSeconds: asNumber(raw.heartbeatSeconds),
    apiContext: parseApiContext(raw.apiContext),
    triggerContextKey: asString(raw.triggerContextKey),
    idempotencyKey: asString(raw.idempotencyKey),
    recovery: parseRecovery(raw.recovery),
  };
}

function parseQueueItem(value: unknown): PersistedTaskRunQueueItem | null {
  const raw = asRecord(value);
  if (!raw) return null;

  const intent = parseIntent(raw.intent);
  const enqueuedAt = asString(raw.enqueuedAt);

  if (!intent || !enqueuedAt) return null;
  return { intent, enqueuedAt };
}

export function resolveTaskRunExecutorPersistenceOptions(
  options?: TaskRunExecutorPersistenceOptions,
): ResolvedTaskRunExecutorPersistenceOptions {
  const enabled = options?.enabled === true;
  const dataDir = options?.dataDir
    ? path.resolve(options.dataDir)
    : DEFAULT_RUNTIME_DATA_DIR;
  const filePath = options?.filePath
    ? path.resolve(options.filePath)
    : path.join(dataDir, DEFAULT_QUEUE_FILE_NAME);

  return { enabled, dataDir, filePath };
}

export class TaskRunExecutorQueueStore {
  private readonly filePath: string;
  private writeChain: Promise<void> = Promise.resolve();

  constructor(filePath: string) {
    this.filePath = filePath;
  }

  async load(): Promise<PersistedTaskRunQueueState> {
    let rawText = "";
    try {
      rawText = await readFile(this.filePath, "utf8");
    } catch (error) {
      const err = error as NodeJS.ErrnoException;
      if (err?.code === "ENOENT") {
        return { queued: [] };
      }
      throw error;
    }

    if (!rawText.trim()) return { queued: [] };

    const parsed = JSON.parse(rawText) as unknown;
    const payload = asRecord(parsed);
    if (!payload) return { queued: [] };

    const queuedRaw = Array.isArray(payload.queued) ? payload.queued : [];
    const queued: PersistedTaskRunQueueItem[] = [];
    for (const item of queuedRaw) {
      const parsedItem = parseQueueItem(item);
      if (parsedItem) queued.push(parsedItem);
    }

    const running = parseQueueItem(payload.running);

    return {
      queued,
      running: running ?? undefined,
    };
  }

  async save(state: PersistedTaskRunQueueState): Promise<void> {
    this.writeChain = this.writeChain.then(async () => {
      const payload: PersistedTaskRunQueueFile = {
        version: 1,
        updatedAt: new Date().toISOString(),
        queued: state.queued,
        running: state.running,
      };

      const dir = path.dirname(this.filePath);
      await mkdir(dir, { recursive: true });

      const tmpPath = `${this.filePath}.tmp-${process.pid}-${Date.now()}`;
      const content = `${JSON.stringify(payload, null, 2)}\n`;

      try {
        await writeFile(tmpPath, content, "utf8");
        await rename(tmpPath, this.filePath);
      } catch (error) {
        try {
          await unlink(tmpPath);
        } catch {
          // ignore cleanup failure
        }
        throw error;
      }
    });

    return this.writeChain;
  }
}
