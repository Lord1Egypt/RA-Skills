---
name: wiro-nextjs
description: Build Next.js App Router features on Wiro AI, the API for 1,000+ image, video, speech, music and LLM models. Keeps the API key in route handlers and server actions, finds models in the Wiro catalog and shows the price before a run, starts tasks on the server and follows them by polling or a webhook, uploads input files, and streams chat from the Wiro LLM gateway with the AI SDK. Use when adding Wiro AI to a Next.js app, or when working in the wiroai/Wiro-Next-Starter repository.
---

# Wiro AI in Next.js

Wiro AI runs 1,000+ models through one API. A run is a task: start it with `POST /Run/{owner}/{model}`, follow it with `POST /Task/Detail`, and read the files from the finished task. Chat models also answer through the OpenAI-compatible LLM gateway at `https://llm.wiro.ai/v1`. Only successful runs are billed, from the prepaid wallet of the project that owns the key.

This skill is the Next.js App Router layer. For every Run API detail (all statuses, error codes, workflows, the MCP server), use the `wiro-ai` skill from wiroai/Wiro-Plugin. For the gateway in depth, use the `wiro-llm` skill from wiroai/Wiro-LLM.

Each code block below is a file in `examples/` next to this file, at the path in its first line. The CI of wiroai/Wiro-Next-Starter type-checks every one of them against the starter's own code.

## Rules

- **The key stays on the server.** Read `WIRO_API_KEY`, plus `WIRO_API_SECRET` for a Signature project, from server environment variables. Never prefix them with `NEXT_PUBLIC_`, never import them into a client component, and never log them or send them in a response. Call Wiro from route handlers and server actions, and start server helper modules with `import 'server-only'`.
- If the variables are missing, ask the user to create a project at https://wiro.ai/panel/project/new and set them in `.env.local` and on their host. Do not ask them to paste a key into the chat.
- **The server decides.** It picks the model and checks every input; the browser sends only what the user typed. The browser gets the task token (`socketaccesstoken`) to follow its own run, never the key and never other task ids.
- **Show the price before the run**, from the model's price list (section 2), and the billed amount (`totalcost`) after it.
- **A run is a paid job.** After a timeout or a dropped connection, read the task before you start anything again: a second Run is a second charge.
- **Public apps need a ceiling.** Use a key from a separate Wiro team with a team spend limit, refuse runs above a price, and add a password if strangers should not use the app. Wiro-Next-Starter does this with `MAX_RUN_PRICE` and `BASIC_AUTH_PASSWORD`.

## 1. A server helper

```ts
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
```

- Every project sends `x-api-key`. A Signature project also sends `x-nonce` and `x-signature`, made fresh for each request.
- Check `result` in the body, not only the HTTP status. Error code `96` means too many tasks are running: nothing was started or charged, so retry after a few seconds. Code `97` means the balance is too low, and the user adds funds at https://wiro.ai/panel/billing.

## 2. Find a model and show its price

```ts
// lib/models.ts
import 'server-only';

/** One row of a model's price list. `inputs` is empty when one price fits every setting. */
export type PriceRow = { price: number; priceMethod: string; inputs?: Record<string, unknown> };

export type ModelSummary = { id: string; title: string; prices: PriceRow[] };

type ToolItem = { cleanslugowner?: string; cleanslugproject?: string; title?: string; dynamicprice?: unknown };

const PER: Record<string, string> = {
  cpr: 'per run',
  cpo: 'per output',
  cps: 'per second of run time',
  cpt: 'per token',
  'cp-pixel': 'per 1024x1024 tile',
  'cp-promptlength': 'per prompt character',
  'cp-audiosecondslength': 'per second of input audio',
  'cp-outputVideoLength': 'per second of video',
};

/** Tool/List and Tool/Detail are public: they need no key. */
async function catalog<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const response = await fetch(`https://api.wiro.ai/v1${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return (await response.json()) as T;
}

/** `dynamicprice` is an array in Tool/Detail and JSON text in Tool/List. */
function parsePrices(value: unknown): PriceRow[] {
  const rows: unknown = typeof value === 'string' ? JSON.parse(value || '[]') : value;
  return Array.isArray(rows) ? (rows as PriceRow[]) : [];
}

/** Searches the catalog, optionally within categories such as "text-to-image" or "text-to-speech". */
export async function findModels(search: string, categories: string[] = []): Promise<ModelSummary[]> {
  const { tool = [] } = await catalog<{ tool?: ToolItem[] }>('/Tool/List', {
    search,
    categories,
    start: '0',
    limit: '20',
    summary: true,
    hideworkflows: true,
  });
  return tool.map((item) => ({
    id: `${item.cleanslugowner}/${item.cleanslugproject}`,
    title: item.title ?? '',
    prices: parsePrices(item.dynamicprice),
  }));
}

/** One model's price list, from Tool/Detail, which also lists its inputs in `parameters[].items[]`. */
export async function getPrices(model: string): Promise<PriceRow[]> {
  const [slugowner, slugproject] = model.split('/');
  const { tool } = await catalog<{ tool?: ToolItem[] }>('/Tool/Detail', { slugowner, slugproject });
  return parsePrices(tool?.[0]?.dynamicprice);
}

/** The row for the settings you will send: one whose inputs all match, or else the row without inputs. */
export function priceFor(prices: PriceRow[], params: Record<string, unknown>): PriceRow | undefined {
  const matches = (row: PriceRow) =>
    Object.entries(row.inputs ?? {}).every(([key, value]) => String(params[key]) === String(value));
  return (
    prices.find((row) => Object.keys(row.inputs ?? {}).length > 0 && matches(row)) ??
    prices.find((row) => Object.keys(row.inputs ?? {}).length === 0)
  );
}

/** "$0.005 per run", "$0.00008 per prompt character". */
export const priceLabel = (row: PriceRow) => `$${row.price} ${PER[row.priceMethod] ?? row.priceMethod}`;
```

- `Tool/List` takes `search`, `categories` (such as `text-to-image`, `image-to-video`, `text-to-speech` or `speech-to-text`), `start` and `limit`. Run a model by `cleanslugowner/cleanslugproject`. People browse the same catalog at https://wiro.ai/models.
- `Tool/Detail` lists the inputs in `tool[0].parameters[].items[]`: `id` (the field to send), `type`, `required`, `options` and the default `value`. Send every required input. Wiro fills in the optional inputs you leave out, except file and prompt fields.
- `priceMethod` says what one `price` buys: `cpr` per run, `cpo` per output file, `cps` per second of run time, `cpt` per token, `cp-pixel` per 1024x1024 tile, `cp-promptlength` per prompt character, `cp-audiosecondslength` per second of input audio, `cp-outputVideoLength` per second of output video. A model without `dynamicprice` bills per second of run time.
- Rows with a `QUANTITY` input price each output. `lib/catalog/pricing.ts` in Wiro-Next-Starter covers every method, prompt length and audio length included.
- The catalog changes slowly, so cache it for a few minutes.

## 3. Start a run and follow it

```ts
// app/api/image/route.ts
import { connection } from 'next/server';
import { getPrices, priceFor, priceLabel } from '../../../lib/models';
import { runModel } from '../../../lib/wiro';

// The server picks the model and its settings. The browser sends only the prompt.
const MODEL = 'pruna/p-image';
const SETTINGS = { aspectRatio: '1:1' };

/** The price the page shows before the run, such as "$0.005 per run". */
export async function GET() {
  await connection(); // answer per request, not once at build time
  const row = priceFor(await getPrices(MODEL), SETTINGS);
  return Response.json({ price: row ? priceLabel(row) : null });
}

export async function POST(request: Request) {
  const { prompt } = (await request.json().catch(() => ({}))) as { prompt?: unknown };
  if (typeof prompt !== 'string' || !prompt.trim() || prompt.length > 2000) {
    return Response.json({ error: 'Send a prompt of up to 2,000 characters.' }, { status: 400 });
  }
  try {
    const token = await runModel(MODEL, { prompt, ...SETTINGS });
    return Response.json({ token }); // the task token goes to the browser, the key never does
  } catch (error) {
    console.error(error);
    return Response.json({ error: 'Could not start the run.' }, { status: 502 });
  }
}
```

```ts
// app/api/tasks/[token]/route.ts
import { getTask, isFinal, succeeded } from '../../../../lib/wiro';

/** The browser polls this with the task token every few seconds. */
export async function GET(_request: Request, { params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  if (!/^[\w-]{8,200}$/.test(token)) return Response.json({ error: 'Not a task token.' }, { status: 400 });
  try {
    const task = await getTask({ tasktoken: token });
    if (!task) return Response.json({ error: 'There is no such task.' }, { status: 404 });
    const files = (task.outputs ?? []).flatMap((output) => (output.url ? [output.url] : []));
    return Response.json(
      {
        status: task.status,
        done: isFinal(task),
        ok: succeeded(task),
        files,
        // An LLM answers in debugoutput. For models that make files it only holds logs.
        text: files.length === 0 && task.debugoutput ? task.debugoutput : null,
        cost: isFinal(task) ? Number(task.totalcost ?? 0) : null,
      },
      { headers: { 'Cache-Control': 'no-store' } },
    );
  } catch (error) {
    console.error(error);
    return Response.json({ error: 'Could not read the task.' }, { status: 502 });
  }
}
```

```ts
// components/use-task.ts
'use client';

import { useEffect, useState } from 'react';

export type TaskState = {
  status?: string;
  done?: boolean;
  ok?: boolean;
  files?: string[];
  text?: string | null;
  cost?: number | null;
  error?: string;
};

/** Polls /api/tasks/[token] every 3 seconds until the task ends. */
export function useTask(token: string | null): TaskState | null {
  const [state, setState] = useState<TaskState | null>(null);

  useEffect(() => {
    if (!token) return;
    let stopped = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const poll = async () => {
      try {
        const response = await fetch(`/api/tasks/${token}`, { cache: 'no-store' });
        const next = (await response.json()) as TaskState;
        if (stopped) return;
        setState(next);
        if (!next.done && !next.error) timer = setTimeout(poll, 3000);
      } catch {
        if (!stopped) timer = setTimeout(poll, 5000);
      }
    };
    void poll();
    return () => {
      stopped = true;
      clearTimeout(timer);
    };
  }, [token]);

  return state;
}
```

- Only `task_postprocess_end` and `task_cancel` end a task. `task_error` is not final, and `task_end` comes before the outputs are saved.
- A failed run also ends with `task_postprocess_end`, so check `pexit`: `"0"` is success. Failed runs are not billed.
- Files are in `outputs[].url`, with `name` and `contenttype`. The text of an LLM is in `debugoutput`. The charge is `totalcost`, in USD.
- Poll every 3 seconds or so, less often for video.

## 4. Files, video and a webhook

```ts
// app/api/video/route.ts
import { runModel, uploadFile } from '../../../lib/wiro';

export const maxDuration = 60;

/**
 * Image to video with Seedance 1 Pro Fast: $0.05 for 5 seconds at 480p.
 * Send every required input; Wiro fills in only the optional ones you leave out.
 */
export async function POST(request: Request) {
  const form = await request.formData().catch(() => null);
  const prompt = form?.get('prompt');
  const image = form?.get('image');
  if (typeof prompt !== 'string' || !prompt.trim() || !(image instanceof File) || !image.type.startsWith('image/')) {
    return Response.json({ error: 'Send a prompt and an image.' }, { status: 400 });
  }
  try {
    const imageUrl = await uploadFile(image); // any public https URL works too
    const webhook = process.env.APP_URL ? new URL('/api/wiro-webhook', process.env.APP_URL).toString() : undefined;
    const token = await runModel('bytedance/seedance-v1-pro-fast', {
      prompt,
      inputImage: [imageUrl], // a combinefileinput takes its URLs in the field itself
      resolution: '480p',
      ratio: 'adaptive',
      duration: '5',
      ...(webhook ? { callbackUrl: webhook } : {}), // public URLs only; on localhost, poll
    });
    return Response.json({ token });
  } catch (error) {
    console.error(error);
    return Response.json({ error: 'Could not start the video.' }, { status: 502 });
  }
}
```

```ts
// app/api/wiro-webhook/route.ts
import { after } from 'next/server';
import { getTask, succeeded } from '../../../lib/wiro';

/**
 * Wiro POSTs the task here when a run started with `callbackUrl` ends, whether
 * it succeeded or failed. The request is not signed, so treat the body as a
 * hint: match the task id with your own records and read the task again.
 */
export async function POST(request: Request) {
  const body = (await request.json().catch(() => null)) as { id?: unknown } | null;
  const taskid = typeof body?.id === 'string' || typeof body?.id === 'number' ? String(body.id) : null;
  if (taskid && /^\d{1,20}$/.test(taskid)) {
    after(async () => {
      const task = await getTask({ taskid });
      if (task && succeeded(task)) {
        // Find the run you saved for this task id, then store task.outputs and task.totalcost.
      }
    });
  }
  // Answer with a 2xx at once. Anything else makes Wiro try again, up to 3 tries, 2 seconds apart.
  return new Response(null, { status: 204 });
}
```

- File inputs take public URLs. A `fileinput` reads its URL from `{id}Url` (`inputImageUrl`), a `multifileinput` reads comma-separated URLs from the field with `Url` before `Multiple` (`inputDocumentUrlMultiple`), and a `combinefileinput` takes them in the field itself, as an array.
- Upload files from the server with `POST /File/Upload`. Vercel functions take request bodies up to 4.5 MB, so on Vercel take a public link for larger files instead of the file.
- A `callbackUrl` must be a public http(s) address. On localhost no webhook arrives, so poll. Wiro sends the task as JSON when it ends, success or failure, tries up to 3 times when the answer is not a 2xx, and follows no redirects. The request has no signature, so read the task again before you act on it.

## 5. Speech from a server action

```ts
// app/actions.ts
'use server';

import { runModel } from '../lib/wiro';

/** Text to speech with Eleven v4, $0.00008 per character. A server action keeps the key on the server too. */
export async function speak(text: string): Promise<{ token?: string; error?: string }> {
  if (typeof text !== 'string' || !text.trim() || text.length > 1000) {
    return { error: 'Send between 1 and 1,000 characters.' };
  }
  try {
    const token = await runModel('elevenlabs/eleven-v4', {
      prompt: text,
      voice: 'alice',
      outputFormat: 'mp3_44100_128',
    });
    return { token };
  } catch {
    return { error: 'Could not start the speech.' };
  }
}
```

Server actions are public endpoints: check every argument as you would in a route handler. The client gets the token and follows it with `useTask`.

## 6. Chat through the LLM gateway

```ts
// app/api/chat/route.ts
import { createWiro } from '@wiro-ai/wiro-llm';
import { convertToModelMessages, streamText, type UIMessage } from 'ai';

export const maxDuration = 60;

export async function POST(request: Request) {
  const { messages } = (await request.json()) as { messages: UIMessage[] };
  const { WIRO_API_KEY, WIRO_API_SECRET } = process.env;
  // The gateway takes the key, or KEY:SECRET for a Signature project. No nonce or signature here.
  const wiro = createWiro({ apiKey: WIRO_API_SECRET ? `${WIRO_API_KEY}:${WIRO_API_SECRET}` : WIRO_API_KEY });

  const result = streamText({
    model: wiro('openai/gpt-5-4-nano'), // any chat model id from GET https://llm.wiro.ai/v1/models
    messages: await convertToModelMessages(messages.slice(-20)),
    maxOutputTokens: 1024, // reasoning tokens count too, so keep this at 512 or more
    abortSignal: request.signal,
  });

  return result.toUIMessageStreamResponse({
    // Every step reports what it cost, in USD.
    messageMetadata: ({ part }) =>
      part.type === 'finish-step' ? { cost: Number(part.providerMetadata?.wiro?.cost ?? 0) } : undefined,
  });
}
```

```tsx
// components/chat.tsx
'use client';

import { useChat } from '@ai-sdk/react';
import { useState } from 'react';

/** A minimal chat: useChat posts to /api/chat and streams the reply in. */
export function Chat() {
  const { messages, sendMessage, status } = useChat();
  const [input, setInput] = useState('');

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        if (!input.trim()) return;
        void sendMessage({ text: input });
        setInput('');
      }}
    >
      {messages.map((message) => (
        <p key={message.id}>
          <strong>{message.role === 'user' ? 'You' : 'Model'}:</strong>{' '}
          {message.parts.map((part) => (part.type === 'text' ? part.text : '')).join('')}
        </p>
      ))}
      <input value={input} onChange={(event) => setInput(event.target.value)} disabled={status !== 'ready'} />
    </form>
  );
}
```

- `@wiro-ai/wiro-llm` is the Wiro AI provider for the AI SDK (`npm i @wiro-ai/wiro-llm ai @ai-sdk/react`). The gateway also works with the OpenAI SDK and `baseURL: 'https://llm.wiro.ai/v1'`.
- Pick ids from `GET https://llm.wiro.ai/v1/models`, which needs no key. Check `capabilities.endpoints` and `supported_parameters` before you rely on a feature such as tools or reasoning settings.
- The billed amount of each step is in `providerMetadata.wiro.cost`.

## 7. In Wiro-Next-Starter

When the project is wiroai/Wiro-Next-Starter, use its helpers instead of the ones above:

```ts
// starter/price-then-run.ts
import 'server-only';

import { quote } from '@/lib/catalog/pricing';
import { buildParams, promptParam, withDefaults, type FormValues } from '@/lib/catalog/schema';
import { getModel } from '@/lib/wiro/catalog';
import { runModel } from '@/lib/wiro/client';

/** In Wiro-Next-Starter: check the inputs, price the run the way Wiro bills it, then start it under a limit. */
export async function priceThenRun(modelId: string, values: FormValues, limitUsd: number) {
  const model = await getModel(modelId); // Tool/Detail, kept for 10 minutes
  if (!model) throw new Error(`Wiro AI has no listed model ${modelId}.`);

  const built = buildParams(model.params, values); // drops unknown inputs, checks choices, ranges and file URLs
  if (built.errors.length > 0 || built.missing.length > 0) throw new Error([...built.errors, ...built.missing][0]);

  const prompt = promptParam(model.params);
  const promptText = prompt ? built.params[prompt.id] : undefined;
  const price = quote(model.pricing, withDefaults(model.params, built.params), {
    promptChars: typeof promptText === 'string' ? promptText.length : undefined,
  });
  if (price.amount === undefined || price.amount > limitUsd) throw new Error(`This run costs ${price.label}.`);

  const { token } = await runModel(model.id, built.params);
  return { token, price: price.label };
}
```

| File                             | What it does                                                                                  |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| `lib/wiro/client.ts`             | Run API client: headers and signature, `runModel`, `getTask`, `uploadFile`, `describeError`   |
| `lib/wiro/catalog.ts`            | Tool/List and Tool/Detail, kept for 10 minutes: `getModel`, `listModels`, `searchModels`      |
| `lib/wiro/gateway.ts`            | Chat models from the gateway's `GET /v1/models`                                               |
| `lib/wiro/limits.ts`             | `MAX_RUN_PRICE` and `MAX_UPLOAD_MB`                                                           |
| `lib/catalog/schema.ts`          | Model inputs as form fields, and `buildParams`, which checks values and fills file URL fields |
| `lib/catalog/pricing.ts`         | `quote`: the price of a run before it starts, the way Wiro bills it                           |
| `lib/catalog/tools.ts`           | The Image, Video and Audio tools and their default models. Add a tool here                    |
| `lib/catalog/filters.ts`         | Models the app never lists                                                                    |
| `lib/tasks.ts`                   | Task statuses folded into stages, and the view the browser polls                              |
| `lib/use-task-run.ts`            | Client hook that starts a run and polls it                                                    |
| `app/api/runs/route.ts`          | Starts a run: checks the inputs, prices the run, applies `MAX_RUN_PRICE`                      |
| `app/api/tasks/[token]/route.ts` | Reads a task by its token                                                                     |
| `app/api/uploads/route.ts`       | Stores a file from the browser with Wiro AI                                                   |
| `app/api/chat/route.ts`          | Streams chat from the gateway with the AI SDK                                                 |
| `proxy.ts`                       | Optional password for the whole app (`BASIC_AUTH_PASSWORD`)                                   |
| `tests/`                         | Vitest tests with a mocked fetch                                                              |

Run `npm run check` (format, lint, type check and tests) before you commit.

## Before you ship

- No `WIRO_` variable is readable in the browser, and none is logged.
- Every Run comes from server code that picked the model and checked the inputs.
- The page shows the price before the run and the billed amount after it.
- Polling stops at `task_postprocess_end` or `task_cancel`, and success means `pexit: "0"`.
- A timeout never starts a second Run before the first task has been read.
- A public deployment has a team spend limit and a price cap per run.

## Links

- Run a model: https://wiro.ai/docs/run-a-model
- Tasks: https://wiro.ai/docs/tasks
- Model parameters and webhooks: https://wiro.ai/docs/model-parameters
- Authentication: https://wiro.ai/docs/authentication
- LLM gateway: https://wiro.ai/docs/completions-api
- Models: https://wiro.ai/models
- Starter: https://github.com/wiroai/Wiro-Next-Starter
