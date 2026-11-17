// lib/wiro.ts
import 'server-only';

import { createHmac } from 'node:crypto';

const RUN_API = 'https://api.wiro.ai/v1';

/** One task, as Task/Detail and the webhook send it. Only the fields most apps read. */
export type WiroTask = {
  id?: string;
  socketaccesstoken?: string;
  status?: string;
  /** "0" when the run succeeded. Only successful runs are billed. */
  pexit?: string;
  /** The text of an LLM. Models that make files write progress logs here. */
  debugoutput?: string;
  /** The billed amount in USD, as text. */
  totalcost?: string;
  outputs?: { name?: string; contenttype?: string; url?: string }[];
};

/** Only these two statuses end a task. `task_error` does not. */
export const isFinal = (task: WiroTask) => task.status === 'task_postprocess_end' || task.status === 'task_cancel';

export const succeeded = (task: WiroTask) => task.status === 'task_postprocess_end' && task.pexit === '0';

let lastNonce = 0;

function authHeaders(): Record<string, string> {
  const apiKey = process.env.WIRO_API_KEY;
  if (!apiKey) throw new Error('Set WIRO_API_KEY in the server environment.');
  const apiSecret = process.env.WIRO_API_SECRET;
  if (!apiSecret) return { 'x-api-key': apiKey };
  // Signature project: a fresh nonce and the hex HMAC-SHA256 of secret + nonce, keyed with the API key.
  lastNonce = Math.max(Date.now(), lastNonce + 1);
  const nonce = String(lastNonce);
  const signature = createHmac('sha256', apiKey)
    .update(apiSecret + nonce)
    .digest('hex');
  return { 'x-api-key': apiKey, 'x-nonce': nonce, 'x-signature': signature };
}

type WiroError = string | { code?: number; message?: string };

/** One POST to the Run API. Wiro answers HTTP 200 with `result: false` when it refuses, so read the body. */
export async function wiro<T>(path: string, body: Record<string, unknown> | FormData): Promise<T> {
  const isForm = body instanceof FormData;
  const response = await fetch(`${RUN_API}${path}`, {
    method: 'POST',
    headers: isForm ? authHeaders() : { ...authHeaders(), 'Content-Type': 'application/json' },
    body: isForm ? body : JSON.stringify(body),
    cache: 'no-store',
  });
  const data = (await response.json()) as T & { result?: boolean; errors?: WiroError[] };
  if (data.result !== true) {
    const error = data.errors?.[0];
    const message = typeof error === 'string' ? error : (error?.message ?? `HTTP ${response.status}`);
    const code = typeof error === 'object' ? error.code : undefined;
    // Code 96: too many tasks at once, retry later. Code 97: the balance is too low.
    throw new Error(`Wiro AI refused the request${code === undefined ? '' : ` (code ${code})`}: ${message}`);
  }
  return data;
}

/** Starts a run of `owner/model` and returns its task token. */
export async function runModel(model: string, params: Record<string, unknown>): Promise<string> {
  const { socketaccesstoken } = await wiro<{ socketaccesstoken: string }>(`/Run/${model}`, params);
  return socketaccesstoken;
}

/** Reads a task by its token or its id. */
export async function getTask(ref: { tasktoken: string } | { taskid: string }): Promise<WiroTask | undefined> {
  const { tasklist } = await wiro<{ tasklist?: WiroTask[] }>('/Task/Detail', ref);
  return tasklist?.[0];
}

/** Stores a file with Wiro AI (up to 100 MB) and returns a URL that file inputs take. */
export async function uploadFile(file: File): Promise<string> {
  const form = new FormData();
  form.append('file', file, file.name);
  const { list } = await wiro<{ list: { url: string }[] }>('/File/Upload', form);
  return list[0].url;
}
