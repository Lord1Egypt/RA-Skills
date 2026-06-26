import { normalizeAccountContext, type NormalizedAccountContext } from "./account.js";
import { WTTApiError, formatApiError, wttApiRequestJson } from "./http.js";
import type { ParsedWTTCommand, WTTCommandExecutionContext } from "./types.js";
import {
  getSharedTaskRunExecutor,
  validateTaskTransition,
  type TaskRunEnqueueResult,
  type TaskRunExecutionResult,
  type TaskRuntimeMetadata,
} from "../runtime/index.js";

type TaskCommand = Extract<ParsedWTTCommand, { name: "task" }>;
type UnknownRecord = Record<string, unknown>;

export interface TaskRuntimeMetadataWithErrors extends TaskRuntimeMetadata {
  detailError?: string;
}

function asRecord(value: unknown): UnknownRecord | null {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return null;
  return value as UnknownRecord;
}

function asString(value: unknown, fallback = "-"): string {
  return typeof value === "string" && value.trim() ? value.trim() : fallback;
}

function toTaskList(data: unknown): UnknownRecord[] {
  if (Array.isArray(data)) {
    return data.map((item) => asRecord(item)).filter((item): item is UnknownRecord => item !== null);
  }

  const payload = asRecord(data);
  if (!payload) return [];

  const raw = Array.isArray(payload.tasks)
    ? payload.tasks
    : Array.isArray(payload.items)
      ? payload.items
      : [];

  return raw.map((item) => asRecord(item)).filter((item): item is UnknownRecord => item !== null);
}

function statusIcon(status: string): string {
  switch (status) {
    case "todo":
    case "open":
      return "📝";
    case "ready":
      return "🟡";
    case "doing":
      return "🚧";
    case "review":
      return "🔎";
    case "done":
    case "approved":
      return "✅";
    case "blocked":
      return "⛔";
    case "rejected":
      return "❌";
    case "cancelled":
      return "🚫";
    default:
      return "📌";
  }
}

function formatTaskList(data: unknown): string {
  const tasks = toTaskList(data);
  if (tasks.length === 0) return "任务列表为空";

  const lines: string[] = [`任务列表（${tasks.length}）`];
  for (const [idx, task] of tasks.entries()) {
    const id = asString(task.id, "-");
    const title = asString(task.title, "(未命名任务)");
    const status = asString(task.status, "unknown");
    const priority = asString(task.priority, "-");
    const owner = asString(task.owner_agent_id, "-");

    lines.push(`${idx + 1}. ${statusIcon(status)} ${title}`);
    lines.push(`   id: ${id} | 状态: ${status} | 优先级: ${priority} | owner: ${owner}`);
  }

  return lines.join("\n");
}

function formatTaskDetail(data: unknown, taskId: string): string {
  const task = asRecord(data);
  if (!task) return `任务详情返回异常（task_id=${taskId}）`;

  const title = asString(task.title, "(未命名任务)");
  const id = asString(task.id, taskId);
  const status = asString(task.status, "unknown");
  const priority = asString(task.priority, "-");
  const owner = asString(task.owner_agent_id, "-");
  const runner = asString(task.runner_agent_id, "-");
  const pipelineId = asString(task.pipeline_id, "-");
  const topicId = asString(task.topic_id, "-");
  const desc = asString(task.description, "");

  const lines = [
    `${statusIcon(status)} ${title}`,
    `id: ${id}`,
    `状态: ${status} | 优先级: ${priority}`,
    `owner: ${owner} | runner: ${runner}`,
    `pipeline: ${pipelineId} | topic: ${topicId}`,
  ];

  if (desc && desc !== "-") lines.push(`描述: ${desc}`);
  return lines.join("\n");
}

function formatTaskCreateAck(data: unknown, title: string): string {
  const payload = asRecord(data) ?? {};
  const id = asString(payload.id, "");
  if (id) return `✅ 任务已创建：${title}\nID: ${id}`;
  return `✅ 任务已创建：${title}`;
}

function toTaskRuntimeMetadata(taskId: string, data: unknown): TaskRuntimeMetadataWithErrors {
  const payload = asRecord(data) ?? {};
  return {
    id: asString(payload.id, taskId),
    title: asString(payload.title, "(未命名任务)"),
    status: asString(payload.status, "unknown"),
    priority: asString(payload.priority, "-"),
    ownerAgentId: asString(payload.owner_agent_id, "-"),
    runnerAgentId: asString(payload.runner_agent_id, "-"),
    pipelineId: asString(payload.pipeline_id, "-"),
    topicId: asString(payload.topic_id, "-"),
    description: asString(payload.description, ""),
    taskType: asString(payload.task_type, "generic"),
    execMode: asString(payload.exec_mode, "default"),
  };
}

function toErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  return String(error);
}

async function getTaskMetadataForRuntime(taskId: string, ctx: WTTCommandExecutionContext): Promise<TaskRuntimeMetadataWithErrors> {
  try {
    const data = await wttApiRequestJson(ctx, {
      method: "GET",
      path: `/tasks/${encodeURIComponent(taskId)}`,
    });
    return toTaskRuntimeMetadata(taskId, data);
  } catch (error) {
    return {
      id: taskId,
      title: "(任务元数据待补充)",
      status: "unknown",
      priority: "-",
      ownerAgentId: "-",
      runnerAgentId: "-",
      pipelineId: "-",
      topicId: "-",
      description: "",
      taskType: "generic",
      execMode: "default",
      detailError: toErrorMessage(error),
    };
  }
}

function formatSummary(result: TaskRunExecutionResult): string[] {
  const summary = result.summary;
  return [
    `summary.kind: ${summary.kind}`,
    `summary.status: ${summary.status}`,
    `summary.transitionApplied: ${summary.transitionApplied}`,
    `summary.action: ${summary.action}`,
    `summary.notes: ${summary.notes.length > 0 ? summary.notes.join(" | ") : "(无)"}`,
    ...(summary.outputPreview ? [`summary.output_preview: ${summary.outputPreview}`] : []),
  ];
}

function formatIdempotencyDecision(result: TaskRunEnqueueResult): string[] {
  const info = result.idempotency;
  const lines = [
    `幂等决策: ${info.decision} | key=${info.idempotencyKey}`,
    `trigger_context: ${info.triggerContextKey}`,
    `幂等说明: ${info.reason}`,
  ];

  if (info.decision === "deduplicated") {
    lines.push(`重复来源: ${info.duplicateState ?? "-"} | duplicate_task_id=${info.duplicateTaskId ?? "-"}`);
    if (info.duplicateEnqueuedAt) {
      lines.push(`重复入队时间: ${info.duplicateEnqueuedAt}`);
    }
  }

  return lines;
}

function formatTaskRunResult(metadata: TaskRuntimeMetadataWithErrors, result: TaskRunExecutionResult): string {
  const transitionPassed = result.transition.allowed;
  const statusLine = `${result.transition.fromStatus} -> ${result.transition.toStatus}`;

  const transitionAppliedText = result.transitionApplied === "run_endpoint"
    ? "POST /tasks/{task_id}/run"
    : result.transitionApplied === "patch_status"
      ? "PATCH /tasks/{task_id} (fallback)"
      : "未落地";

  const heartbeatMode = result.heartbeatPublished > 0
    ? `已通过 WTT publish 外发 ${result.heartbeatPublished} 条`
    : `未外发，返回结构化 payload ${result.heartbeatPayloads.length} 条`;

  const heartbeatSample = result.heartbeatPayloads[0]?.text;

  const lines = [
    result.inference.succeeded
      ? "✅ task run 执行完成（已进入 review）"
      : "⚠️ task run 执行失败",
    `${statusIcon(metadata.status)} ${metadata.title}`,
    `task_id: ${metadata.id}`,
    ...formatIdempotencyDecision(result),
    `状态校验: ${transitionPassed ? "通过" : "未通过"}（${statusLine}）`,
    `状态推进(doing): ${transitionAppliedText}`,
    `最终状态: ${result.finalStatus}`,
    `推理: ${result.inference.succeeded ? "成功" : "失败"} | provider=${result.inference.provider}`,
    ...(result.inference.prompt ? [`prompt.len: ${result.inference.prompt.length}`] : []),
    ...(result.inference.outputText ? [`output.len: ${result.inference.outputText.length}`] : []),
    ...(result.inference.error ? [`inference.error: ${result.inference.error}`] : []),
    `队列: enqueued=${result.queue.enqueuedAt} | dequeued=${result.queue.dequeuedAt} | finished=${result.queue.finishedAt} | pending_after_dequeue=${result.queue.pendingAfterDequeue}`,
    ...(result.persistence.enabled
      ? [
        `持久化队列: 已启用${result.persistence.filePath ? `（${result.persistence.filePath}）` : ""}${result.persistence.recoveredFrom ? ` | recovery=${result.persistence.recoveredFrom}` : ""}`,
      ]
      : []),
    ...(result.recovery
      ? [`recovery.retry: ${result.recovery.retryCount}/${result.recovery.maxRetryCount}`]
      : []),
    `60s 心跳: ${heartbeatMode}`,
    ...(heartbeatSample ? [`heartbeat.sample: ${heartbeatSample}`] : []),
    ...formatSummary(result),
    `task_detail: topic=${result.task.topicId} | task_type=${result.task.taskType} | exec_mode=${result.task.execMode}`,
  ];

  if (result.fallbackMessage) {
    lines.push(`fallback: ${result.fallbackMessage}`);
  }

  if (result.heartbeatPublishErrors.length > 0) {
    lines.push(`心跳外发异常: ${result.heartbeatPublishErrors.join(" | ")}`);
  }

  if (metadata.detailError) {
    lines.push(`任务元数据补充失败：${metadata.detailError}`);
    lines.push("可先执行 @wtt task detail <task_id> 检查任务信息。");
  }

  return lines.join("\n");
}

function formatTaskRunDedupResult(metadata: TaskRuntimeMetadataWithErrors, result: TaskRunEnqueueResult): string {
  if (!result.deduplicated) {
    return formatTaskRunResult(metadata, result);
  }

  const lines = [
    "⏭️ task run 请求命中幂等去重（未入队）",
    `${statusIcon(metadata.status)} ${metadata.title}`,
    `task_id: ${metadata.id}`,
    ...formatIdempotencyDecision(result),
    `执行器快照: running=${result.runningTaskId ?? "-"} | queue_length=${result.queueLength}`,
    ...(result.persistence.enabled
      ? [
        `持久化队列: 已启用${result.persistence.filePath ? `（${result.persistence.filePath}）` : ""}`,
      ]
      : []),
    "说明: 同一任务已有待处理 run 请求，当前请求已被幂等保护拦截。",
  ];

  if (metadata.detailError) {
    lines.push(`任务元数据补充失败：${metadata.detailError}`);
    lines.push("可先执行 @wtt task detail <task_id> 检查任务信息。");
  }

  return lines.join("\n");
}

export interface ExecuteTaskRunByIdOptions {
  taskId: string;
  ctx: WTTCommandExecutionContext;
  account?: NormalizedAccountContext;
  note?: string;
  heartbeatSeconds?: number;
  publishHeartbeatToStream?: boolean;
}

export interface ExecuteTaskRunByIdResult {
  metadata: TaskRuntimeMetadataWithErrors;
  enqueueResult: TaskRunEnqueueResult;
  account: NormalizedAccountContext;
}

export async function executeTaskRunById(options: ExecuteTaskRunByIdOptions): Promise<ExecuteTaskRunByIdResult> {
  const account = options.account ?? normalizeAccountContext(options.ctx.accountId, options.ctx.account);
  const metadata = await getTaskMetadataForRuntime(options.taskId, options.ctx);

  const topicId = metadata.topicId;
  const canPublishHeartbeat = Boolean(
    options.publishHeartbeatToStream === true
      && topicId
      && topicId !== "-"
      && options.ctx.clientConnected
      && options.ctx.client,
  );

  const executor = getSharedTaskRunExecutor();
  const enqueueResult = await executor.enqueueRun({
    taskId: metadata.id,
    metadata,
    accountId: account.accountId,
    triggerAgentId: account.agentId || undefined,
    runnerAgentId: metadata.runnerAgentId !== "-" ? metadata.runnerAgentId : account.agentId || undefined,
    note: options.note ?? `triggered by @wtt task run (${account.accountId})`,
    heartbeatSeconds: options.heartbeatSeconds ?? 60,
    apiContext: {
      cloudUrl: account.cloudUrl,
      token: account.token || undefined,
    },
    apiRequest: (request) => wttApiRequestJson(options.ctx, {
      method: request.method,
      path: request.path,
      body: request.body,
    }),
    fetchTaskDetail: async () => wttApiRequestJson(options.ctx, {
      method: "GET",
      path: `/tasks/${encodeURIComponent(metadata.id)}`,
    }),
    invokeTaskInference: options.ctx.runtimeHooks?.dispatchTaskInference
      ? async (request) => options.ctx.runtimeHooks!.dispatchTaskInference!(request)
      : undefined,
    getSessionRuntimeMetrics: options.ctx.runtimeHooks?.getSessionRuntimeMetrics
      ? async () => options.ctx.runtimeHooks!.getSessionRuntimeMetrics!({
        taskId: metadata.id,
        topicId: metadata.topicId !== "-" ? metadata.topicId : undefined,
        accountId: account.accountId,
      })
      : undefined,
    publishHeartbeat: canPublishHeartbeat
      ? async (payload) => {
        await options.ctx.client!.publish(topicId, payload.text, {
          contentType: "text",
          semanticType: "TASK_PROGRESS",
        });
      }
      : undefined,
  });

  return {
    metadata,
    enqueueResult,
    account,
  };
}

async function handleTaskRunCommand(
  command: Extract<TaskCommand, { action: "run" }>,
  ctx: WTTCommandExecutionContext,
  account: NormalizedAccountContext,
): Promise<string> {
  const { metadata, enqueueResult } = await executeTaskRunById({
    taskId: command.taskId,
    ctx,
    account,
    note: `triggered by @wtt task run (${account.accountId})`,
    heartbeatSeconds: 60,
    publishHeartbeatToStream: true,
  });

  if (enqueueResult.deduplicated) {
    return formatTaskRunDedupResult(metadata, enqueueResult);
  }

  return formatTaskRunResult(metadata, enqueueResult);
}

async function handleTaskReviewCommand(
  command: Extract<TaskCommand, { action: "review" }>,
  ctx: WTTCommandExecutionContext,
  account: ReturnType<typeof normalizeAccountContext>,
): Promise<string> {
  const metadata = await getTaskMetadataForRuntime(command.taskId, ctx);
  const transition = validateTaskTransition({
    currentStatus: metadata.status,
    intent: { kind: "review", action: command.reviewAction },
  });

  if (!transition.allowed) {
    const lines = [
      "⚠️ review 状态校验未通过",
      `${statusIcon(metadata.status)} ${metadata.title}`,
      `task_id: ${metadata.id}`,
      `当前状态: ${transition.fromStatus} | 目标状态: ${transition.toStatus}`,
      `原因: ${transition.reason}`,
      `下一步: ${transition.nextAction}`,
    ];

    if (metadata.detailError) {
      lines.push(`任务元数据补充失败：${metadata.detailError}`);
    }

    return lines.join("\n");
  }

  try {
    const data = await wttApiRequestJson(ctx, {
      method: "POST",
      path: `/tasks/${encodeURIComponent(metadata.id)}/review`,
      body: {
        action: command.reviewAction,
        comment: command.comment ?? "",
        reviewer: account.agentId || undefined,
      },
    });

    const after = toTaskRuntimeMetadata(metadata.id, data);
    return [
      "✅ task review 已提交",
      `${statusIcon(after.status)} ${after.title}`,
      `task_id: ${after.id}`,
      `状态迁移: ${transition.fromStatus} -> ${after.status}`,
      `action: ${command.reviewAction}`,
      `review_comment: ${command.comment?.trim() || "(空)"}`,
    ].join("\n");
  } catch (error) {
    if (error instanceof WTTApiError && error.code === "ENDPOINT_UNAVAILABLE") {
      try {
        const patchData = await wttApiRequestJson(ctx, {
          method: "PATCH",
          path: `/tasks/${encodeURIComponent(metadata.id)}`,
          body: {
            status: transition.toStatus,
            notes: [
              `review fallback action=${command.reviewAction}`,
              command.comment?.trim() || "(空)",
            ].join(" | "),
            reviewer: account.agentId || undefined,
          },
        });

        const after = toTaskRuntimeMetadata(metadata.id, patchData);
        return [
          "✅ task review 已通过 PATCH fallback 提交",
          `${statusIcon(after.status)} ${after.title}`,
          `task_id: ${after.id}`,
          `状态迁移: ${transition.fromStatus} -> ${after.status}`,
          `action: ${command.reviewAction}`,
        ].join("\n");
      } catch (fallbackError) {
        return [
          "task review 暂不可用：review API 与 PATCH fallback 均失败。",
          `task_id: ${metadata.id}`,
          `目标状态: ${transition.toStatus}`,
          `fallback_error: ${toErrorMessage(fallbackError)}`,
        ].join("\n");
      }
    }

    return formatApiError("task review", error);
  }
}

export async function handleTaskCommand(command: TaskCommand, ctx: WTTCommandExecutionContext): Promise<string> {
  const account = normalizeAccountContext(ctx.accountId, ctx.account);

  if (!account.hasToken) {
    return [
      `WTT 账户: ${account.accountId}`,
      "无法执行 task 命令：缺少 token。",
      "请先执行 @wtt config auto 检查并补齐配置。",
    ].join("\n");
  }

  try {
    if (command.action === "list") {
      const data = await wttApiRequestJson(ctx, {
        method: "GET",
        path: "/tasks",
      });
      return formatTaskList(data);
    }

    if (command.action === "detail") {
      const data = await wttApiRequestJson(ctx, {
        method: "GET",
        path: `/tasks/${encodeURIComponent(command.taskId)}`,
      });
      return formatTaskDetail(data, command.taskId);
    }

    if (command.action === "create") {
      const data = await wttApiRequestJson(ctx, {
        method: "POST",
        path: "/tasks",
        body: {
          title: command.title,
          description: command.description,
          created_by: account.agentId || undefined,
        },
      });
      return formatTaskCreateAck(data, command.title);
    }

    if (command.action === "run") {
      return handleTaskRunCommand(command, ctx, account);
    }

    if (command.action === "review") {
      return handleTaskReviewCommand(command, ctx, account);
    }

    return "不支持的 task 子命令";
  } catch (error) {
    return formatApiError("task 命令", error);
  }
}
