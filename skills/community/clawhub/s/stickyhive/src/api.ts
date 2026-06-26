import { getApiKey, getBaseUrl } from './config';

export async function apiRequest(
  method: string,
  path: string,
  body?: Record<string, unknown>,
  query?: Record<string, string>,
): Promise<unknown> {
  const baseUrl = getBaseUrl();
  const apiKey = getApiKey();

  let url = `${baseUrl}/api/v1${path}`;
  if (query) {
    const params = new URLSearchParams(
      Object.entries(query).filter(([, v]) => v !== undefined && v !== ''),
    );
    const qs = params.toString();
    if (qs) url += `?${qs}`;
  }

  const headers: Record<string, string> = {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  };

  const opts: RequestInit = { method, headers };
  if (body && ['POST', 'PUT', 'PATCH'].includes(method)) {
    opts.body = JSON.stringify(body);
  }

  const res = await fetch(url, opts);

  if (res.status === 204) {
    return { success: true };
  }

  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    if (!res.ok) {
      return { error: `HTTP ${res.status}: ${text}` };
    }
    return { result: text };
  }
}

export function output(data: unknown): void {
  console.log(JSON.stringify(data, null, 2));
}
