import { maskToken, missingRequiredFields, normalizeAccountContext } from "./account.js";
import type { WTTCommandExecutionContext } from "./types.js";

function configPathHint(accountId: string): string {
  return accountId === "default"
    ? "channels.wtt.accounts.default（或兼容配置 channels.wtt）"
    : `channels.wtt.accounts.${accountId}`;
}

function renderConfiguredSummary(ctx: WTTCommandExecutionContext, autoMode: boolean): string {
  const account = normalizeAccountContext(ctx.accountId, ctx.account);
  const lines = [
    `WTT 账户: ${account.accountId}`,
    `来源: ${account.source}`,
    `cloudUrl: ${account.cloudUrl}`,
    `agentId: ${account.agentId || "未配置"}`,
    `token: ${maskToken(account.token)}`,
  ];

  if (autoMode) {
    const missing = missingRequiredFields(account);
    if (missing.length > 0) {
      lines.push(`缺少关键配置: ${missing.join(" / ")}`);
      lines.push(`请在 openclaw.json 补齐 ${configPathHint(account.accountId)}。`);
      return lines.join("\n");
    }

    lines.push(`连接状态: ${ctx.clientConnected ? "已连接" : "未连接"}`);
    lines.push("配置已就绪，可执行 @wtt bind 生成绑定码。");
  }

  return lines.join("\n");
}

export function handleConfigCommand(
  mode: "show" | "auto",
  ctx: WTTCommandExecutionContext,
): string {
  if (!ctx.account) {
    return [
      `WTT 账户: ${ctx.accountId}`,
      "未检测到 channels.wtt 账户配置。",
      `请在 openclaw.json 配置 ${configPathHint(ctx.accountId)} 的 agentId/token/cloudUrl。`,
    ].join("\n");
  }

  return renderConfiguredSummary(ctx, mode === "auto");
}
