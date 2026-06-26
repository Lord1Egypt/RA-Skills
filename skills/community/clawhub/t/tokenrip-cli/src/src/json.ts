import { CliError } from './errors.js';

export function parseJsonOption<T = unknown>(value: string, flagName: string): T {
  try {
    return JSON.parse(value) as T;
  } catch {
    throw new CliError('INVALID_JSON', `${flagName} must be valid JSON`);
  }
}

export function parseJsonObjectOption(
  value: string,
  flagName: string,
): Record<string, unknown> {
  const parsed = parseJsonOption<unknown>(value, flagName);
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new CliError('INVALID_JSON', `${flagName} must be a JSON object`);
  }
  return parsed as Record<string, unknown>;
}

export function parseJsonObjectArrayOption(
  value: string,
  flagName: string,
): Record<string, unknown>[] {
  const parsed = parseJsonOption<unknown>(value, flagName);
  const values = Array.isArray(parsed) ? parsed : [parsed];
  if (!values.every((entry) => entry && typeof entry === 'object' && !Array.isArray(entry))) {
    throw new CliError('INVALID_JSON', `${flagName} must be a JSON object or array of objects`);
  }
  return values as Record<string, unknown>[];
}
