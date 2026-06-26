export const API_KEY_ENV = "QWEATHER_API_KEY";
export const API_HOST_ENV = "QWEATHER_API_HOST";

export const DEFAULT_TIMEOUT_MS = 15_000;
export const DEFAULT_RETRY_COUNT = 2;
export const DEFAULT_BACKOFF_MS = 200;

export enum ExitCode {
  OK = 0,
  PARAM_OR_CONFIG = 2,
  NETWORK = 3,
  API_BUSINESS = 4,
  INTERNAL = 5,
}

export interface CliErrorOptions {
  cause?: unknown;
  rawResponse?: unknown;
}

export class CliError extends Error {
  public readonly exitCode: ExitCode;
  public readonly rawResponse?: unknown;

  constructor(message: string, exitCode: ExitCode, options: CliErrorOptions = {}) {
    super(message, { cause: options.cause });
    this.name = "CliError";
    this.exitCode = exitCode;
    this.rawResponse = options.rawResponse;
  }
}

export function getApiKey(env: NodeJS.ProcessEnv = process.env): string {
  const key = env[API_KEY_ENV];
  if (!key || key.trim().length === 0) {
    throw new CliError(
      `${API_KEY_ENV} is required. Get one at https://console.qweather.com`,
      ExitCode.PARAM_OR_CONFIG,
    );
  }
  return key.trim();
}

export function getApiHost(env: NodeJS.ProcessEnv = process.env): string {
  const host = env[API_HOST_ENV];
  if (!host || host.trim().length === 0) {
    throw new CliError(
      `${API_HOST_ENV} is required. Find it at https://console.qweather.com/setting`,
      ExitCode.PARAM_OR_CONFIG,
    );
  }
  const trimmed = host.trim();
  return trimmed.startsWith("https://") ? trimmed : `https://${trimmed}`;
}

export function toErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}

export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
