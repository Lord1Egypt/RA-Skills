import type { Signal, WorldLoopsBriefResponse } from './types';

const DEFAULT_API_BASE_URL = 'https://api.worldloops.ai';

function getApiBaseUrl(): string {
  const baseUrl = process.env.WORLDLOOPS_API_BASE_URL ?? DEFAULT_API_BASE_URL;

  return baseUrl.replace(/\/$/, '');
}

export async function callWorldLoopsBrief(input: {
  signals: Signal[];
  mode?: 'demo' | 'connected' | 'reconciliation';
}): Promise<WorldLoopsBriefResponse> {
  const apiKey = process.env.WORLDLOOPS_API_KEY;
  const baseUrl = getApiBaseUrl();

  const response = await fetch(`${baseUrl}/api/v1/openclaw/brief`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
    },
    body: JSON.stringify({
      signals: input.signals,
      mode: input.mode ?? (apiKey ? 'connected' : 'demo'),
    }),
  });

  const json = (await response.json()) as WorldLoopsBriefResponse;

  if (!response.ok) {
    return {
      ok: false,
      error: {
        code: `HTTP_${response.status}`,
        message: json.error?.message ?? response.statusText,
      },
      safety: {
        externalWrite: false,
      },
    };
  }

  return {
    ...json,
    safety: {
      ...(json.safety ?? {}),
      externalWrite: false,
    },
  };
}
