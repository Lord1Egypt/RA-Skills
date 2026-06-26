import {
  CliError,
  ExitCode,
  getApiHost,
  getApiKey,
  isRecord,
} from "./config.ts";
import { getJsonWithRetry, type HttpGetRequest } from "./http.ts";
import type { CommandName } from "./validators.ts";

export interface ExecuteCommandDependencies {
  requestJson?: (request: HttpGetRequest) => Promise<unknown>;
  apiKey?: string;
  apiHost?: string;
  timeoutMs?: number;
  retries?: number;
}

interface RuntimeContext {
  requestJson: (request: HttpGetRequest) => Promise<unknown>;
  apiKey: string;
  apiHost: string;
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
    url: `${context.apiHost}${path}`,
    params: { ...params, key: context.apiKey },
    timeoutMs: context.timeoutMs,
    retries: context.retries,
  });

  if (!isRecord(payload)) {
    throw new CliError(
      "Unexpected API response format",
      ExitCode.API_BUSINESS,
      { rawResponse: payload },
    );
  }

  if (payload.code !== "200") {
    throw new CliError(
      `QWeather API error (code ${payload.code})`,
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
    apiKey: dependencies.apiKey ?? getApiKey(),
    apiHost: dependencies.apiHost ?? getApiHost(),
    timeoutMs: dependencies.timeoutMs,
    retries: dependencies.retries,
  };

  switch (command) {
    case "lookup": {
      const location = getRequiredString(flags, "location");
      const adm = getOptionalString(flags, "adm");
      const range = getOptionalString(flags, "range");

      return runQuery("/geo/v2/city/lookup", {
        location,
        adm,
        range,
      }, context);
    }
    case "now": {
      const location = getRequiredString(flags, "location");
      const lang = getRequiredString(flags, "lang");
      const unit = getRequiredString(flags, "unit");

      return runQuery( "/v7/weather/now", {
        location,
        lang,
        unit,
      }, context);
    }
    case "forecast": {
      const location = getRequiredString(flags, "location");
      const days = getRequiredString(flags, "days");
      const lang = getRequiredString(flags, "lang");
      const unit = getRequiredString(flags, "unit");

      return runQuery( `/v7/weather/${days}d`, {
        location,
        lang,
        unit,
      }, context);
    }
    case "indices": {
      const location = getRequiredString(flags, "location");
      const type = getRequiredString(flags, "type");

      return runQuery( "/v7/indices/1d", {
        location,
        type,
      }, context);
    }
    default: {
      const unhandled: never = command;
      throw new CliError(`Unsupported command: ${unhandled}`, ExitCode.INTERNAL);
    }
  }
}
