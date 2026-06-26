#!/usr/bin/env node

import { createClient } from './vendor/weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from './vendor/weryai-core/errors.js';
import { normalizeTaskCollection, normalizeTaskResult } from './vendor/weryai-core/normalize.js';

function printHelp() {
  process.stdout.write(
    [
      'Usage:',
      '  node {baseDir}/scripts/task-inspector.js --task-id <task-id>',
      '  node {baseDir}/scripts/task-inspector.js --batch-id <batch-id>',
      '',
      'Notes:',
      '  - Requires WERYAI_API_KEY.',
      '  - Uses the official read-only WeryAI task query endpoints.',
    ].join('\n') + '\n',
  );
}

function parseArgs(argv) {
  const args = { taskId: null, batchId: null, help: false, verbose: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') args.help = true;
    else if (arg === '--verbose' || arg === '-v') args.verbose = true;
    else if (arg === '--task-id') args.taskId = argv[++i] ?? null;
    else if (arg === '--batch-id') args.batchId = argv[++i] ?? null;
  }
  return args;
}

function createContext(verbose) {
  return {
    apiKey: process.env.WERYAI_API_KEY || '',
    baseUrl: process.env.WERYAI_BASE_URL || 'https://api.weryai.com',
    verbose,
    requestTimeoutMs: Number(process.env.WERYAI_REQUEST_TIMEOUT_MS) || 30_000,
  };
}

function phaseForTask(task) {
  if (task.contentStatus === 'audio-success') return 'completed';
  if (task.contentStatus === 'text-fail' || task.contentStatus === 'audio-fail') return 'failed';
  if (task.contentStatus === 'text-success') return 'running';
  if (task.taskStatus === 'completed') return 'completed';
  if (task.taskStatus === 'failed') return 'failed';
  return 'running';
}

function phaseForBatch(tasks) {
  if (!Array.isArray(tasks) || tasks.length === 0) return 'running';
  const phases = tasks.map(phaseForTask);
  if (phases.includes('failed')) return 'failed';
  if (phases.every((phase) => phase === 'completed')) return 'completed';
  return 'running';
}

function extractArtifacts(task, raw) {
  return {
    images: task.images ?? normalizeStringArray(raw?.output?.images ?? raw?.images),
    videos: task.videos ?? normalizeStringArray(raw?.output?.videos ?? raw?.videos),
    audios: task.audios ?? normalizeStringArray(raw?.output?.audios ?? raw?.audios),
    lyrics: task.lyrics ?? pickString(raw?.output?.lyrics, raw?.lyrics),
    coverUrl: task.coverUrl ?? pickString(raw?.output?.cover_url, raw?.cover_url, raw?.coverUrl),
    scripts: normalizeScripts(task.scripts ?? raw?.output?.scripts ?? raw?.scripts),
  };
}

function normalizeBatchTasks(normalizedTasks, rawTasks) {
  return normalizedTasks.map((task, index) => ({
    taskId: task.taskId,
    taskStatus: task.taskStatus,
    contentStatus: task.contentStatus,
    phase: phaseForTask(task),
    artifacts: extractArtifacts(task, rawTasks[index]),
    raw: rawTasks[index] ?? null,
  }));
}

function normalizeScripts(value) {
  if (!Array.isArray(value) || value.length === 0) return null;
  return value.map((entry) => {
    if (!entry || typeof entry !== 'object') return entry;
    return {
      speakerId: entry.speakerId ?? entry.speaker_id ?? null,
      speakerName: entry.speakerName ?? entry.speaker_name ?? null,
      content: typeof entry.content === 'string' ? entry.content : null,
    };
  });
}

function normalizeStringArray(value) {
  return Array.isArray(value) && value.length > 0 ? value : null;
}

function pickString(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return null;
}

async function queryTask(client, taskId) {
  let response;
  try {
    response = await client.get(`/v1/generation/${taskId}/status`, { retries: 3 });
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(response)) {
    return formatApiError(response);
  }

  const task = normalizeTaskResult(response.data);
  const phase = phaseForTask(task);
  return {
    ok: phase !== 'failed',
    phase,
    queryType: 'task',
    taskId: task.taskId,
    batchId: null,
    taskStatus: task.taskStatus,
    contentStatus: task.contentStatus,
    artifacts: extractArtifacts(task, response.data),
    raw: response.data,
    errorCode: phase === 'failed' ? 'TASK_FAILED' : null,
    errorMessage: phase === 'failed' ? (task.msg || 'Task failed.') : null,
  };
}

async function queryBatch(client, batchId) {
  let response;
  try {
    response = await client.get(`/v1/generation/batch/${batchId}/status`, { retries: 3 });
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(response)) {
    return formatApiError(response);
  }

  const rawTasks = Array.isArray(response.data) ? response.data : [response.data];
  const normalizedTasks = normalizeTaskCollection(response.data);
  const tasks = normalizeBatchTasks(normalizedTasks, rawTasks);
  const phase = phaseForBatch(normalizedTasks);

  return {
    ok: phase !== 'failed',
    phase,
    queryType: 'batch',
    taskId: null,
    batchId,
    taskStatus: null,
    contentStatus: null,
    tasks,
    raw: response.data,
    errorCode: phase === 'failed' ? 'TASK_FAILED' : null,
    errorMessage: phase === 'failed' ? 'One or more tasks in the batch failed.' : null,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return;
  }

  if (!args.taskId && !args.batchId) {
    process.stdout.write(
      JSON.stringify(
        {
          ok: false,
          phase: 'failed',
          errorCode: 'VALIDATION',
          errorMessage: 'Either `--task-id` or `--batch-id` is required.',
        },
        null,
        2,
      ) + '\n',
    );
    process.exitCode = 1;
    return;
  }

  const ctx = createContext(args.verbose);
  if (!ctx.apiKey) {
    process.stdout.write(
      JSON.stringify(
        {
          ok: false,
          phase: 'failed',
          errorCode: 'NO_API_KEY',
          errorMessage:
            'Missing WERYAI_API_KEY environment variable. Get one from https://www.weryai.com/api/keys and configure it in the runtime environment before using this skill.',
        },
        null,
        2,
      ) + '\n',
    );
    process.exitCode = 1;
    return;
  }

  const client = createClient(ctx);
  const result = args.batchId
    ? await queryBatch(client, args.batchId)
    : await queryTask(client, args.taskId);

  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  if (!result.ok) process.exitCode = 1;
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
});
