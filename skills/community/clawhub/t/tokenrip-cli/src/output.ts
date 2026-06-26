import { CliError, toCliError } from './errors.js';
import type { Formatter } from './formatters.js';

let forceHuman = false;
let configHuman = false;

export function setForceHuman(value: boolean): void {
  forceHuman = value;
}

export function setConfigHuman(value: boolean): void {
  configHuman = value;
}

function isJsonMode(): boolean {
  if (forceHuman) return false;
  if (process.env.TOKENRIP_OUTPUT === 'human') return false;
  if (process.env.TOKENRIP_OUTPUT === 'json') return true;
  if (configHuman) return false;
  return true;
}

export function outputSuccess(data: Record<string, unknown>, formatter?: Formatter): void {
  if (isJsonMode() || !formatter) {
    console.log(JSON.stringify({ ok: true, data }));
  } else {
    console.log(formatter(data));
  }
}

export function outputError(err: CliError): never {
  if (isJsonMode()) {
    console.log(JSON.stringify({ ok: false, error: err.code, message: err.message }));
  } else {
    console.error(`Error [${err.code}]: ${err.message}`);
  }

  // Always write actionable hints to stderr when interactive
  if (process.stderr.isTTY) {
    const hint = ERROR_HINTS[err.code];
    if (hint) console.error(`Hint: ${hint}`);
  }

  process.exit(1);
}

export function wrapCommand<T extends (...args: any[]) => Promise<void>>(fn: T): T {
  const wrapped = async (...args: any[]) => {
    try {
      await fn(...args);
    } catch (err) {
      outputError(toCliError(err));
    }
  };
  return wrapped as unknown as T;
}

const ERROR_HINTS: Record<string, string> = {
  NO_API_KEY: 'Run `rip auth register` to set up your agent.',
  UNAUTHORIZED: 'Your API key has expired or been revoked. Run `rip auth register` to recover it.',
  NETWORK_ERROR: 'Check your connection. Run `rip config show` to verify the API URL.',
  TIMEOUT: 'The server did not respond in time. Try again or check your connection.',
  FILE_NOT_FOUND: 'Check the file path and try again.',
  INVALID_TYPE: 'Valid types depend on the command; for assets they include markdown, html, chart, code, text, json, csv, and collection.',
  INVALID_JSON: 'Check quoting and make sure the value is valid JSON.',
  INVALID_DURATION: 'Use formats like 30m, 1h, or 7d.',
  INVALID_REF: 'Use a full URL or an asset UUID.',
  KEY_SAVE_FAILED: 'Check config file permissions or rerun the command after fixing local config access.',
  AUTH_FAILED: 'Could not create API key. Is the server running?',
  CONTACT_NOT_FOUND: 'Run `rip contacts list` to see available contacts.',
  INVALID_AGENT_ID: 'Agent IDs start with rip1. Example: rip1x9a2f...',
  INVALID_OUTPUT_FORMAT: 'Valid values are "json" and "human".',
};
