import { API_BASE_URL, CliError, ExitCode, isRecord } from "./config.ts";
import { getJsonWithRetry, type HttpGetRequest } from "./http.ts";
import type { CommandName } from "./validators.ts";

export interface ExecuteCommandDependencies {
  requestJson?: (request: HttpGetRequest) => Promise<unknown>;
  timeoutMs?: number;
  retries?: number;
}

interface RuntimeContext {
  requestJson: (request: HttpGetRequest) => Promise<unknown>;
  timeoutMs: number | undefined;
  retries: number | undefined;
}

function getRequiredString(flags: Record<string, unknown>, key: string): string {
  const value = flags[key];
  if (typeof value === "string" && value.length > 0) {
    return value;
  }
  throw new CliError(`Missing required argument: --${key}`, ExitCode.INTERNAL);
}

function getOptionalString(flags: Record<string, unknown>, key: string): string | undefined {
  const value = flags[key];
  if (typeof value === "string") {
    return value;
  }
  return undefined;
}

async function runQuery(
  path: string,
  params: Record<string, string | undefined>,
  context: RuntimeContext,
): Promise<unknown> {
  const payload = await context.requestJson({
    url: `${API_BASE_URL}${path}`,
    params,
    timeoutMs: context.timeoutMs,
    retries: context.retries,
  });

  if (!isRecord(payload)) {
    throw new CliError(
      `Unexpected API response format`,
      ExitCode.API_BUSINESS,
      { rawResponse: payload },
    );
  }

  if (typeof payload.message === "string") {
    throw new CliError(
      `API error: ${payload.message}`,
      ExitCode.API_BUSINESS,
      { rawResponse: payload },
    );
  }

  return payload;
}

export async function executeCommand(
  command: CommandName,
  flags: Record<string, unknown>,
  dependencies: ExecuteCommandDependencies = {},
): Promise<unknown> {
  const context: RuntimeContext = {
    requestJson: dependencies.requestJson ?? getJsonWithRetry,
    timeoutMs: dependencies.timeoutMs,
    retries: dependencies.retries,
  };

  switch (command) {
    case "convert": {
      const from = getRequiredString(flags, "from");
      const to = getRequiredString(flags, "to");
      const amount = getOptionalString(flags, "amount") ?? "1";
      const date = getOptionalString(flags, "date");
      const path = date ? `/${date}` : "/latest";

      return runQuery(path, { from, to, amount }, context);
    }
    case "latest": {
      const from = getRequiredString(flags, "from");
      const to = getOptionalString(flags, "to");

      return runQuery("/latest", { from, to }, context);
    }
    case "history": {
      const from = getRequiredString(flags, "from");
      const date = getRequiredString(flags, "date");
      const to = getOptionalString(flags, "to");

      return runQuery(`/${date}`, { from, to }, context);
    }
    case "series": {
      const from = getRequiredString(flags, "from");
      const start = getRequiredString(flags, "start");
      const end = getRequiredString(flags, "end");
      const to = getOptionalString(flags, "to");

      return runQuery(`/${start}..${end}`, { from, to }, context);
    }
    case "currencies": {
      return runQuery("/currencies", {}, context);
    }
    default: {
      const unhandled: never = command;
      throw new CliError(`Unsupported command: ${unhandled}`, ExitCode.INTERNAL);
    }
  }
}
