import type { WsTaskStatus } from "../types.js";

const DEFAULT_EVENT_DEDUP_WINDOW_MS = 20_000;

const STATUS_ALIASES: Record<string, string> = {
  open: "todo",
  ready: "todo",
  in_progress: "doing",
  inprogress: "doing",
};

// Accept todo+doing; final execution decision can be refined by live task detail checks.
const RUNNABLE_STATUSES = new Set(["todo", "doing"]);

function normalizeStatus(raw: string | undefined): string {
  const value = (raw ?? "").trim().toLowerCase();
  if (!value) return "unknown";
  return STATUS_ALIASES[value] ?? value;
}

function normalizeTaskId(raw: string | undefined): string {
  return (raw ?? "").trim();
}

export interface TaskStatusRunDispatchResult {
  deduplicated?: boolean;
  detail?: string;
}

export interface TaskStatusRunDispatchRequest {
  event: WsTaskStatus;
  taskId: string;
  status: string;
}

export interface TaskStatusConsumeResult {
  decision: "accepted" | "dedup" | "skipped";
  reason: string;
  taskId: string;
  status: string;
  dedupSource?: "event" | "executor";
  dispatch?: TaskStatusRunDispatchResult;
}

export interface TaskStatusEventHandler {
  handle: (event: WsTaskStatus) => Promise<TaskStatusConsumeResult>;
}

export interface TaskStatusEventHandlerOptions {
  runTask: (request: TaskStatusRunDispatchRequest) => Promise<TaskStatusRunDispatchResult>;
  dedupWindowMs?: number;
  nowMs?: () => number;
}

export function createTaskStatusEventHandler(options: TaskStatusEventHandlerOptions): TaskStatusEventHandler {
  const dedupWindowMs = Math.max(1000, Math.floor(options.dedupWindowMs ?? DEFAULT_EVENT_DEDUP_WINDOW_MS));
  const nowMs = options.nowMs ?? (() => Date.now());
  const seenEventAt = new Map<string, number>();

  const prune = (now: number): void => {
    const cutoff = now - dedupWindowMs;
    for (const [key, seenAt] of seenEventAt) {
      if (seenAt < cutoff) {
        seenEventAt.delete(key);
      }
    }
  };

  return {
    async handle(event: WsTaskStatus): Promise<TaskStatusConsumeResult> {
      const taskId = normalizeTaskId(event.task_id);
      const status = normalizeStatus(event.status);

      if (!taskId) {
        return {
          decision: "skipped",
          reason: "missing_task_id",
          taskId,
          status,
        };
      }

      if (!RUNNABLE_STATUSES.has(status)) {
        return {
          decision: "skipped",
          reason: `status_not_runnable:${status}`,
          taskId,
          status,
        };
      }

      const now = nowMs();
      const dedupKey = `${taskId}`;
      prune(now);

      const seenAt = seenEventAt.get(dedupKey);
      if (typeof seenAt === "number" && now - seenAt <= dedupWindowMs) {
        return {
          decision: "dedup",
          reason: `event_window_task_dedup:${dedupWindowMs}ms`,
          taskId,
          status,
          dedupSource: "event",
        };
      }

      seenEventAt.set(dedupKey, now);

      try {
        const dispatch = await options.runTask({
          event,
          taskId,
          status,
        });

        if (dispatch.deduplicated) {
          return {
            decision: "dedup",
            reason: "executor_idempotency_dedup",
            taskId,
            status,
            dedupSource: "executor",
            dispatch,
          };
        }

        return {
          decision: "accepted",
          reason: "task_run_dispatched",
          taskId,
          status,
          dispatch,
        };
      } catch (error) {
        seenEventAt.delete(dedupKey);
        const errMsg = error instanceof Error ? error.message : String(error);

        return {
          decision: "skipped",
          reason: `dispatch_failed:${errMsg}`,
          taskId,
          status,
        };
      }
    },
  };
}
