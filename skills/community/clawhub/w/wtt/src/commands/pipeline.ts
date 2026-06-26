import { normalizeAccountContext } from "./account.js";
import { formatApiError, wttApiRequestJson } from "./http.js";
import type { ParsedWTTCommand, WTTCommandExecutionContext } from "./types.js";

type PipelineCommand = Extract<ParsedWTTCommand, { name: "pipeline" }>;
type UnknownRecord = Record<string, unknown>;

function asRecord(value: unknown): UnknownRecord | null {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return null;
  return value as UnknownRecord;
}

function asString(value: unknown, fallback = "-"): string {
  return typeof value === "string" && value.trim() ? value.trim() : fallback;
}

function toPipelineList(data: unknown): UnknownRecord[] {
  if (Array.isArray(data)) {
    return data.map((item) => asRecord(item)).filter((item): item is UnknownRecord => item !== null);
  }

  const payload = asRecord(data);
  if (!payload) return [];
  const raw = Array.isArray(payload.pipelines)
    ? payload.pipelines
    : Array.isArray(payload.items)
      ? payload.items
      : [];

  return raw.map((item) => asRecord(item)).filter((item): item is UnknownRecord => item !== null);
}

function formatPipelineList(data: unknown): string {
  const pipelines = toPipelineList(data);
  if (pipelines.length === 0) return "流水线列表为空";

  const lines: string[] = [`流水线列表（${pipelines.length}）`];
  for (const [idx, pipeline] of pipelines.entries()) {
    const id = asString(pipeline.id, "-");
    const name = asString(pipeline.name, "(未命名流水线)");
    const desc = asString(pipeline.description, "");

    lines.push(`${idx + 1}. ⚙️ ${name}`);
    lines.push(`   id: ${id}`);
    if (desc && desc !== "-") lines.push(`   ${desc}`);
  }

  return lines.join("\n");
}

function formatPipelineCreateAck(data: unknown, name: string): string {
  const payload = asRecord(data) ?? {};
  const id = asString(payload.id, "");
  if (id) return `✅ 流水线已创建：${name}\nID: ${id}`;
  return `✅ 流水线已创建：${name}`;
}

function formatPipelineRunAck(data: unknown, pipelineId: string): string {
  const payload = asRecord(data) ?? {};
  const message = asString(payload.message, "");

  const lines = [`🚀 流水线执行已触发：${pipelineId}`];
  if (message) lines.push(`说明: ${message}`);
  return lines.join("\n");
}

export async function handlePipelineCommand(
  command: PipelineCommand,
  ctx: WTTCommandExecutionContext,
): Promise<string> {
  const account = normalizeAccountContext(ctx.accountId, ctx.account);

  if (!account.hasToken) {
    return [
      `WTT 账户: ${account.accountId}`,
      "无法执行 pipeline 命令：缺少 token。",
      "请先执行 @wtt config auto 检查并补齐配置。",
    ].join("\n");
  }

  try {
    if (command.action === "list") {
      const data = await wttApiRequestJson(ctx, {
        method: "GET",
        path: "/tasks/pipelines",
      });
      return formatPipelineList(data);
    }

    if (command.action === "create") {
      const data = await wttApiRequestJson(ctx, {
        method: "POST",
        path: "/tasks/pipelines",
        body: {
          name: command.nameArg,
          description: command.description,
          creator_agent_id: account.agentId || undefined,
        },
      });
      return formatPipelineCreateAck(data, command.nameArg);
    }

    const data = await wttApiRequestJson(ctx, {
      method: "POST",
      path: "/tasks/pipeline/execute",
      body: {
        pipeline_id: command.pipelineId,
        trigger_agent_id: account.agentId || undefined,
      },
    });
    return formatPipelineRunAck(data, command.pipelineId);
  } catch (error) {
    return formatApiError("pipeline 命令", error);
  }
}
