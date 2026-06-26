import { normalizeAccountContext } from "./account.js";
import { formatApiError, wttApiRequestJson } from "./http.js";
import type { ParsedWTTCommand, WTTCommandExecutionContext } from "./types.js";

type DelegateCommand = Extract<ParsedWTTCommand, { name: "delegate" }>;
type UnknownRecord = Record<string, unknown>;

function asRecord(value: unknown): UnknownRecord | null {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return null;
  return value as UnknownRecord;
}

function asString(value: unknown, fallback = "-"): string {
  return typeof value === "string" && value.trim() ? value.trim() : fallback;
}

function asBoolean(value: unknown): boolean {
  return value === true;
}

function toDelegationList(data: unknown): UnknownRecord[] {
  if (Array.isArray(data)) {
    return data.map((item) => asRecord(item)).filter((item): item is UnknownRecord => item !== null);
  }

  const payload = asRecord(data);
  if (!payload) return [];

  const raw = Array.isArray(payload.delegations)
    ? payload.delegations
    : Array.isArray(payload.items)
      ? payload.items
      : [];

  return raw.map((item) => asRecord(item)).filter((item): item is UnknownRecord => item !== null);
}

function formatDelegationList(data: unknown): string {
  const delegations = toDelegationList(data);
  if (delegations.length === 0) return "委托列表为空";

  const lines: string[] = [`委托列表（${delegations.length}）`];
  for (const [idx, item] of delegations.entries()) {
    const target = asString(item.target_agent_id, "-");
    const canPublish = asBoolean(item.can_publish) ? "✅" : "❌";
    const canP2P = asBoolean(item.can_p2p) ? "✅" : "❌";

    lines.push(`${idx + 1}. 🤝 ${target}`);
    lines.push(`   publish: ${canPublish} | p2p: ${canP2P}`);
  }

  return lines.join("\n");
}

function requireManagerAgent(accountId: string, agentId: string): string | null {
  if (agentId.trim()) return null;
  return [
    `WTT 账户: ${accountId}`,
    "delegate 命令需要已配置 agentId。",
    "请先执行 @wtt config auto 并补齐 agentId。",
  ].join("\n");
}

export async function handleDelegateCommand(
  command: DelegateCommand,
  ctx: WTTCommandExecutionContext,
): Promise<string> {
  const account = normalizeAccountContext(ctx.accountId, ctx.account);

  if (!account.hasToken) {
    return [
      `WTT 账户: ${account.accountId}`,
      "无法执行 delegate 命令：缺少 token。",
      "请先执行 @wtt config auto 检查并补齐配置。",
    ].join("\n");
  }

  const managerHint = requireManagerAgent(account.accountId, account.agentId);
  if (managerHint) return managerHint;

  try {
    if (command.action === "list") {
      const data = await wttApiRequestJson(ctx, {
        method: "GET",
        path: "/manager/delegations",
        query: { manager_agent_id: account.agentId },
      });
      return formatDelegationList(data);
    }

    if (command.action === "create") {
      await wttApiRequestJson(ctx, {
        method: "POST",
        path: "/manager/delegations",
        body: {
          manager_agent_id: account.agentId,
          target_agent_id: command.targetAgentId,
          can_publish: true,
          can_p2p: true,
        },
      });
      return `✅ 委托已创建：${command.targetAgentId}`;
    }

    await wttApiRequestJson(ctx, {
      method: "DELETE",
      path: "/manager/delegations",
      query: {
        manager_agent_id: account.agentId,
        target_agent_id: command.targetAgentId,
      },
    });
    return `✅ 委托已移除：${command.targetAgentId}`;
  } catch (error) {
    return formatApiError("delegate 命令", error);
  }
}
