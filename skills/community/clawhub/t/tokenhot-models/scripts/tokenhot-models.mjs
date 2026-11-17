#!/usr/bin/env node

import { randomUUID } from 'node:crypto';
import { link, lstat, mkdir, readFile, unlink, writeFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';
import { downloadImage } from './image-download.mjs';

const endpoint = 'https://api.tokenhot.ai/v1/images/generations';
const supportedModel = {
  id: 'gpt-image-2',
  sizes: [
    '1024x1024', '1536x864', '864x1536', '1360x1024', '1024x1360',
    '1440x1440', '2048x1152', '1152x2048', '1664x1248', '1248x1664',
    '2880x2880', '3840x2160', '2160x3840', '3264x2448', '2448x3264',
  ],
  docs: 'https://docs.tokenhot.ai/main/gpt-image-2',
  pricing: 'https://tokenhot.ai/models/gpt-image-2',
};
const catalog = 'https://tokenhot.ai/models';
const receiptLimit = 1024 * 1024;

class WorkflowError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.details = details;
  }
}

function modelPlan(model = supportedModel.id, size = supportedModel.sizes[0]) {
  if (model !== supportedModel.id) throw new WorkflowError('Unsupported model. Run models for the supported route.');
  if (!supportedModel.sizes.includes(size)) throw new WorkflowError('Unsupported size. Run models for the documented dimensions.');
  return { model, size, n: 1, pricing_url: supportedModel.pricing };
}

function requestPayload(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)
    || Object.keys(input).some(key => !['prompt', 'model', 'size'].includes(key))) {
    throw new WorkflowError('Use a JSON object with prompt and optional model and size.');
  }
  if (typeof input.prompt !== 'string' || !input.prompt.trim()) throw new WorkflowError('Provide a nonempty text prompt.');
  const { model, size, n } = modelPlan(input.model, input.size);
  return { model, size, n, prompt: input.prompt };
}

async function readJson(file) {
  try {
    return JSON.parse(await readFile(file, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') return undefined;
    throw new WorkflowError('Could not read the local JSON record.');
  }
}

async function saveNew(file, data) {
  const temporary = `${file}.${randomUUID()}.tmp`;
  try {
    await writeFile(temporary, data, { flag: 'wx', mode: 0o600 });
    await link(temporary, file);
  } finally {
    await unlink(temporary).catch(() => {});
  }
}

async function record(file, data) {
  await saveNew(file, `${JSON.stringify(data, null, 2)}\n`);
}

async function boundedJson(response) {
  if (!response.body) throw new WorkflowError('TokenHot returned an empty response.');
  const chunks = [];
  let count = 0;
  for await (const chunk of response.body) {
    count += chunk.byteLength;
    if (count > receiptLimit) throw new WorkflowError('TokenHot response exceeded the supported receipt size.');
    chunks.push(Buffer.from(chunk));
  }
  return JSON.parse(Buffer.concat(chunks, count).toString('utf8'));
}

function usageCounts(usage) {
  return Object.fromEntries(['total_tokens', 'input_tokens', 'output_tokens']
    .filter(key => Number.isSafeInteger(usage?.[key]) && usage[key] >= 0)
    .map(key => [key, usage[key]]));
}

function responseId(headers) {
  const id = headers.get('x-request-id') || headers.get('x-new-api-request-id');
  return /^[a-zA-Z0-9_.-]{1,120}$/.test(id ?? '') ? id : undefined;
}

function resultUrl(raw) {
  if (typeof raw !== 'string') throw new WorkflowError('TokenHot returned no image URL.');
  const url = new URL(raw);
  if (url.protocol !== 'https:' || url.username || url.password) throw new WorkflowError('TokenHot returned an unsupported image URL.');
  return url.href;
}

async function savedImage(job, completed) {
  if (!/^image\.(png|jpg|gif|webp|avif)$/.test(completed?.file ?? '')) return undefined;
  const file = join(job, completed.file);
  try {
    const details = await lstat(file);
    return details.isFile() && details.size > 0 ? file : undefined;
  } catch (error) {
    if (error.code === 'ENOENT') return undefined;
    throw error;
  }
}

// Transport substitution is restricted to the test module, outside the CLI.
export function createWorkflow({ fetchImpl = fetch, download = downloadImage } = {}) {
  async function status(job) {
    const request = await readJson(join(job, 'request.json'));
    if (!request) throw new WorkflowError('No TokenHot job was found at this directory.');
    const receipt = await readJson(join(job, 'receipt.json'));
    const completed = await readJson(join(job, 'completed.json'));
    const response = await readJson(join(job, 'response.json'));
    const imagePath = await savedImage(job, completed);
    return {
      job, model: request.model, size: request.size,
      state: imagePath ? 'saved' : receipt ? 'download_pending' : 'submission_unknown',
      image_path: imagePath,
      http_status: response?.http_status,
      request_id: receipt?.request_id ?? response?.request_id,
      usage: receipt?.usage,
    };
  }

  async function resume(job) {
    const current = await status(job);
    if (current.state === 'saved') return current;
    if (current.state !== 'download_pending') {
      throw new WorkflowError('There is no saved result to download. Check the original request in TokenHot logs.', current);
    }
    const receipt = await readJson(join(job, 'receipt.json'));
    try {
      const { bytes, extension } = await download(receipt.url);
      const file = `image${extension}`;
      const completed = await readJson(join(job, 'completed.json'));
      if (completed && completed.file !== file) throw new Error('The recorded image type changed');
      const output = join(job, file);
      try {
        await saveNew(output, bytes);
      } catch (error) {
        // A prior download may have saved the file just before interruption.
        if (error.code !== 'EEXIST' || !(await readFile(output)).equals(bytes)) throw error;
      }
      try {
        await record(join(job, 'completed.json'), { file });
      } catch (error) {
        if (error.code !== 'EEXIST') throw error;
      }
      return await status(job);
    } catch {
      throw new WorkflowError('The result is recorded. Use resume to retry only its download.', current);
    }
  }

  async function generate(input, job, key) {
    const payload = requestPayload(input);
    if (!key?.trim()) throw new WorkflowError('Set TOKENHOT_API_KEY locally before generating.');
    try {
      await mkdir(job, { mode: 0o700 });
    } catch (error) {
      if (error.code === 'EEXIST') throw new WorkflowError('Job directory already exists. Use status or resume for the existing job.', { job });
      throw new WorkflowError('Cannot create the job directory. Make sure its parent exists and is writable.', { job });
    }
    await record(join(job, 'request.json'), { model: payload.model, size: payload.size, created_at: new Date().toISOString() });

    let requestId;
    let httpStatus;
    try {
      const response = await fetchImpl(endpoint, {
        method: 'POST', redirect: 'error', signal: AbortSignal.timeout(180_000),
        headers: { Authorization: `Bearer ${key.trim()}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      httpStatus = response.status;
      requestId = responseId(response.headers);
      await record(join(job, 'response.json'), { http_status: httpStatus, request_id: requestId });
      if (!response.ok) {
        await response.body?.cancel();
        throw new Error('Request rejected');
      }
      const result = await boundedJson(response);
      const url = resultUrl(result?.data?.[0]?.url);
      await record(join(job, 'receipt.json'), { url, request_id: requestId, usage: usageCounts(result.usage) });
    } catch {
      throw new WorkflowError('No usable generation receipt was saved. Check the job and TokenHot logs before submitting again.', {
        job, state: 'submission_unknown', http_status: httpStatus, request_id: requestId,
      });
    }
    return resume(job);
  }

  return { generate, status, resume };
}

async function cli() {
  const [command, ...args] = process.argv.slice(2);
  const options = {
    models: {}, plan: { model: { type: 'string' }, size: { type: 'string' } },
    generate: { request: { type: 'string' }, job: { type: 'string' } },
    status: { job: { type: 'string' } }, resume: { job: { type: 'string' } },
  };
  if (!command || command === '--help') {
    console.log('Commands: models | plan [--model ID] [--size WIDTHxHEIGHT] | generate --request FILE_OR_DASH --job NEW_DIR | status --job DIR | resume --job DIR');
    return;
  }
  if (!Object.hasOwn(options, command)) throw new WorkflowError('Unknown command. Use --help.');
  let values;
  try { ({ values } = parseArgs({ args, options: options[command] })); }
  catch { throw new WorkflowError('Invalid command options. Use --help.'); }
  if (command === 'models') return { supported: [supportedModel], live_catalog: catalog };
  if (command === 'plan') return modelPlan(values.model, values.size);
  if (!values.job) throw new WorkflowError('Supply a job directory with --job.');
  const job = resolve(values.job);
  const workflow = createWorkflow();
  if (command === 'generate') {
    if (!values.request) throw new WorkflowError('Supply a request JSON file or --request - for stdin.');
    let input;
    try {
      if (values.request === '-') {
        const chunks = [];
        for await (const chunk of process.stdin) chunks.push(chunk);
        input = JSON.parse(Buffer.concat(chunks).toString('utf8'));
      } else {
        input = JSON.parse(await readFile(values.request, 'utf8'));
      }
    } catch { throw new WorkflowError('Could not parse the generation request JSON.'); }
    return workflow.generate(input, job, process.env.TOKENHOT_API_KEY);
  }
  return workflow[command](job);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    const result = await cli();
    if (result) console.log(JSON.stringify(result));
  } catch (error) {
    const safeError = error instanceof WorkflowError ? error : new WorkflowError('TokenHot workflow could not complete. Inspect the local job before trying again.');
    console.error(JSON.stringify({ error: safeError.message, ...safeError.details }));
    process.exitCode = 1;
  }
}
