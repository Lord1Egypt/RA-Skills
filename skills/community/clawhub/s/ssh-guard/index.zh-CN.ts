/**
 * ssh-guard plugin entry point.
 * Author: @yanbo92
 * Description: Provides SSH execution approvals and session state cleanup.
 */
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

type ApprovalState = {
  awaitingApproval: boolean;
  allowNextExec: boolean;
  allowAllSshInKey: boolean;
  updatedAt: number;
  lastCommand?: string;
};

const approvals = new Map<string, ApprovalState>();
const SESSION_WIDE_APPROVAL_TEXT = "我已知晓风险，本次会话一律允许";

function formatPlainCommandBlock(command: string): string {
  return `\n\n\`\`\`\n${command}\n\`\`\``;
}

function normalizeKey(value?: string): string {
  return value?.trim() ?? "";
}

function extractApprovalKey(ctx: {
  sessionKey?: string;
  conversationId?: string;
}): string {
  for (const rawValue of [ctx.conversationId, ctx.sessionKey]) {
    const normalized = normalizeKey(rawValue);
    if (!normalized) {
      continue;
    }
    const key = normalized.split(":").filter(Boolean).at(-1) ?? "";
    if (key) {
      return key;
    }
  }
  return "";
}

function setState(approvalKey: string, state: Omit<ApprovalState, "updatedAt">): ApprovalState {
  const nextState: ApprovalState = {
    ...state,
    updatedAt: Date.now(),
  };
  approvals.set(approvalKey, nextState);
  return nextState;
}

function clearApprovalState(approvalKey?: string): void {
  const normalizedKey = normalizeKey(approvalKey);
  if (!normalizedKey) {
    return;
  }

  approvals.delete(normalizedKey);
}

function syncSubagentApprovalFromParent(params: {
  requesterSessionKey?: string;
  childSessionKey?: string;
}): { parentApprovalKey: string; childApprovalKey: string; inherited: boolean } {
  const parentApprovalKey = extractApprovalKey({ sessionKey: params.requesterSessionKey });
  const childApprovalKey = extractApprovalKey({ sessionKey: params.childSessionKey });

  if (!parentApprovalKey || !childApprovalKey) {
    return {
      parentApprovalKey,
      childApprovalKey,
      inherited: false,
    };
  }

  const parentState = approvals.get(parentApprovalKey);
  if (!parentState) {
    return {
      parentApprovalKey,
      childApprovalKey,
      inherited: false,
    };
  }

  setState(childApprovalKey, {
    awaitingApproval: false,
    allowNextExec: false,
    allowAllSshInKey: parentState.allowAllSshInKey,
    lastCommand: parentState.lastCommand,
  });

  return {
    parentApprovalKey,
    childApprovalKey,
    inherited: true,
  };
}

function isSessionWideApprovalText(text: string): boolean {
  return text.trim().includes(SESSION_WIDE_APPROVAL_TEXT);
}

function isApprovalText(text: string): boolean {
  const normalized = text.trim();
  if (!normalized) {
    return false;
  }
  if (isSessionWideApprovalText(normalized)) {
    return false;
  }
  if (normalized.includes("不")) {
    return false;
  }
  return (
    normalized.includes("允许") ||
    normalized.includes("同意") ||
    normalized.includes("可以") ||
    normalized.includes("批准")
  );
}

function summarizeForLog(text: string, limit = 120): string {
  const normalized = text.replace(/\s+/g, " ").trim();
  if (!normalized) {
    return "<empty>";
  }
  return normalized.length <= limit ? normalized : `${normalized.slice(0, limit)}…`;
}

export default function register(api: OpenClawPluginApi) {
  api.on("subagent_spawned", (event, ctx) => {
    const syncResult = syncSubagentApprovalFromParent({
      requesterSessionKey: ctx.requesterSessionKey,
      childSessionKey: event.childSessionKey ?? ctx.childSessionKey,
    });

    if (!syncResult.childApprovalKey) {
      return;
    }

    api.logger.info?.(
      syncResult.inherited
        ? `ssh-guard: inherited subagent approval parent=${syncResult.parentApprovalKey} child=${syncResult.childApprovalKey}`
        : `ssh-guard: no parent approval to inherit for child=${syncResult.childApprovalKey}`,
    );
  });

  api.on("message_received", (event, ctx) => {
    const messageCtxWithSession = ctx as {
      sessionKey?: string;
      conversationId?: string;
    };
    const approvalKey = extractApprovalKey({
      sessionKey: messageCtxWithSession.sessionKey,
      conversationId: messageCtxWithSession.conversationId,
    });
    if (!approvalKey) {
      return;
    }

    const state = approvals.get(approvalKey);
    if (!state) {
      return;
    }

    if (isSessionWideApprovalText(event.content)) {
      setState(approvalKey, {
        awaitingApproval: false,
        allowNextExec: false,
        allowAllSshInKey: true,
        lastCommand: state.lastCommand,
      });
      api.logger.info?.(`ssh-guard: session-wide approval granted for key=${approvalKey}`);
      return;
    }

    if (!state.awaitingApproval) {
      return;
    }

    if (isApprovalText(event.content)) {
      setState(approvalKey, {
        awaitingApproval: false,
        allowNextExec: true,
        allowAllSshInKey: state.allowAllSshInKey,
        lastCommand: state.lastCommand,
      });
      api.logger.info?.(`ssh-guard: approval granted for key=${approvalKey}; next exec allowed once`);
      return;
    }

    api.logger.info?.(
      `ssh-guard: ignored non-approval message while awaiting approval for key=${approvalKey}; text=${JSON.stringify(summarizeForLog(event.content))}`,
    );
  });

  api.on("subagent_ended", (event) => {
    const childApprovalKey = extractApprovalKey({ sessionKey: event.targetSessionKey });
    if (!childApprovalKey) {
      return;
    }

    clearApprovalState(childApprovalKey);
    api.logger.info?.(`ssh-guard: cleared subagent approval state for key=${childApprovalKey}`);
  });

  api.on("session_end", (event, ctx) => {
    const approvalKey = extractApprovalKey({
      sessionKey: ctx.sessionKey ?? event.sessionKey,
    });
    if (!approvalKey) {
      return;
    }

    clearApprovalState(approvalKey);
    api.logger.info?.(`ssh-guard: cleared approval state on session_end for key=${approvalKey}`);
  });

  api.on("before_tool_call", (event, ctx) => {
    if (event.toolName !== "exec" && event.toolName !== "process") {
      return;
    }

    const params = event.params as Record<string, unknown>;
    const command = typeof params.command === "string" ? params.command : "";
    const isSshExec = event.toolName === "exec" && command.toLowerCase().includes("ssh");

    const approvalKey = extractApprovalKey({ sessionKey: ctx.sessionKey });
    const state = approvalKey ? approvals.get(approvalKey) : undefined;

    if (isSshExec && state?.allowAllSshInKey) {
      api.logger.info?.(`ssh-guard: session-wide approval bypass for key=${approvalKey || "unknown"}`);
      return;
    }

    if (isSshExec && state?.allowNextExec && approvalKey) {
      setState(approvalKey, {
        awaitingApproval: false,
        allowNextExec: false,
        allowAllSshInKey: state.allowAllSshInKey,
        lastCommand: state.lastCommand,
      });
      api.logger.info?.(`ssh-guard: consumed one-time approval for key=${approvalKey}`);
      return;
    }

    if (isSshExec && state?.awaitingApproval) {
      return {
        block: true,
        blockReason:
          "Execution is paused pending approval. Briefly explain the command and show it in a plain Markdown code block without a language tag, using exactly ``` followed by the command and then ```. Tell the user they can reply with exactly one of: 允许 / 同意 / 可以 / 批准 for one-time approval, or exactly: 我已知晓风险，本次会话一律允许 for session-wide approval, which may not be read-only and may break the user's machine." +
          formatPlainCommandBlock(state.lastCommand ?? ""),
      };
    }

    if (!isSshExec) {
      return;
    }

    if (approvalKey) {
      setState(approvalKey, {
        awaitingApproval: true,
        allowNextExec: false,
        allowAllSshInKey: state?.allowAllSshInKey ?? false,
        lastCommand: command,
      });
    }

    api.logger.info?.(
      `ssh-guard: blocked command for key=${approvalKey || "unknown"} tool=${event.toolName} command=${command.slice(0, 120)}`,
    );

    return {
      block: true,
      blockReason:
        "SSH commands are blocked until approved. Briefly explain the command and show it in a plain Markdown code block without a language tag, using exactly ``` followed by the command and then ```. Tell the user they can reply with exactly one of: 允许 / 同意 / 可以 / 批准 for one-time approval, or exactly: 我已知晓风险，本次会话一律允许 for session-wide approval, which may not be read-only and may break the user's machine." +
        formatPlainCommandBlock(command),
    };
  });
}
