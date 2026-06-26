import { executeWTTCommand } from "./handlers.js";
import { isWTTCommandText, normalizeWTTCommandText, parseWTTCommandText } from "./parser.js";
import type {
  WTTCommandAccountContext,
  WTTCommandClient,
  WTTCommandProcessResult,
  WTTCommandRuntimeHooks,
  WTTFetchLike,
} from "./types.js";

export interface WTTCommandRouterOptions {
  getClient: (accountId: string) => WTTCommandClient | undefined;
  getAccount?: (accountId: string) => WTTCommandAccountContext | undefined;
  defaultAccountId?: string;
}

export interface WTTCommandRouter {
  processText: (
    text: string,
    opts?: {
      accountId?: string;
      account?: WTTCommandAccountContext;
      fetchImpl?: WTTFetchLike;
      runtimeHooks?: WTTCommandRuntimeHooks;
    },
  ) => Promise<WTTCommandProcessResult>;
}

const DEFAULT_ACCOUNT_ID = "default";

function noClientRequired(commandName: string): boolean {
  return (
    commandName === "help"
    || commandName === "invalid"
    || commandName === "config"
    || commandName === "bind"
    || commandName === "setup"
    || commandName === "update"
    || commandName === "version"
    || commandName === "task"
    || commandName === "pipeline"
    || commandName === "delegate"
  );
}

export function createWTTCommandRouter(options: WTTCommandRouterOptions): WTTCommandRouter {
  const defaultAccountId = options.defaultAccountId ?? DEFAULT_ACCOUNT_ID;

  return {
    async processText(
      text: string,
      opts?: {
        accountId?: string;
        account?: WTTCommandAccountContext;
        fetchImpl?: WTTFetchLike;
        runtimeHooks?: WTTCommandRuntimeHooks;
      },
    ): Promise<WTTCommandProcessResult> {
      const normalized = normalizeWTTCommandText(text);
      if (!normalized || !isWTTCommandText(normalized)) return { handled: false };

      const accountId = opts?.accountId ?? defaultAccountId;
      const command = parseWTTCommandText(normalized);
      if (!command) return { handled: false };

      const client = options.getClient(accountId);
      const account = opts?.account ?? options.getAccount?.(accountId);

      if (!noClientRequired(command.name)) {
        if (!client) {
          return {
            handled: true,
            accountId,
            command: command.name,
            response: `WTT 账户未初始化：${accountId}`,
          };
        }

        if (!client.connected) {
          return {
            handled: true,
            accountId,
            command: command.name,
            response: `WTT 账户未连接：${accountId}`,
          };
        }
      }

      try {
        const response = await executeWTTCommand(command, client, {
          accountId,
          account,
          clientConnected: client?.connected ?? false,
          client,
          fetchImpl: opts?.fetchImpl,
          runtimeHooks: opts?.runtimeHooks,
        });
        return {
          handled: true,
          accountId,
          command: command.name,
          response,
        };
      } catch (error) {
        const msg = error instanceof Error ? error.message : String(error);
        return {
          handled: true,
          accountId,
          command: command.name,
          response: `执行失败：${msg}`,
        };
      }
    },
  };
}

export { normalizeWTTCommandText, parseWTTCommandText } from "./parser.js";
export type { ParsedWTTCommand, WTTCommandProcessResult } from "./types.js";
