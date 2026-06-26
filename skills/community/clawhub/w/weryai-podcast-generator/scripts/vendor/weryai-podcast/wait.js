import { log, sleep } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from '../weryai-core/errors.js';
import { createClient } from '../weryai-core/client.js';
import { resolvePollIntervalMs } from '../weryai-core/wait.js';
import {
  getPodcastFailureMessage,
  getPodcastLifecyclePhase,
  isPodcastAudioReady,
  isPodcastFailure,
  isPodcastTextReady,
  normalizePodcastTask,
} from './normalize.js';
import {
  buildGenerateAudioPayload,
  buildSubmitTextPayload,
  normalizeGenerateAudioInput,
  normalizeSubmitTextInput,
  validateGenerateAudioInput,
  validateSubmitTextInput,
} from './validators.js';

export async function execute(input, ctx) {
  const normalizedInput = normalizeSubmitTextInput(input);
  const validationErrors = validateSubmitTextInput(normalizedInput);
  if (validationErrors.length > 0) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'VALIDATION',
      errorMessage: validationErrors.join(' '),
    };
  }

  const textRequestBody = buildSubmitTextPayload(normalizedInput);
  const audioInput = normalizeGenerateAudioInput({
    taskId: '<task-id-from-text-generation>',
    scripts: normalizedInput.scripts ?? null,
  });
  const audioValidationErrors = validateGenerateAudioInput(audioInput).filter((message) => message !== '`taskId` is required.');
  if (audioValidationErrors.length > 0) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'VALIDATION',
      errorMessage: audioValidationErrors.join(' '),
    };
  }

  if (ctx.dryRun) {
    return {
      ok: true,
      phase: 'dry-run',
      dryRun: true,
      flow: [
        {
          step: 'submit-text',
          requestUrl: `${ctx.baseUrl}/v1/generation/podcast/generate/text`,
          requestBody: textRequestBody,
        },
        {
          step: 'generate-audio',
          requestUrl: `${ctx.baseUrl}/v1/generation/podcast/generate/{taskId}/audio`,
          requestBody: buildGenerateAudioPayload(audioInput),
        },
      ],
    };
  }

  const client = createClient(ctx);

  let submitResponse;
  try {
    submitResponse = await client.post('/v1/generation/podcast/generate/text', textRequestBody);
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(submitResponse)) {
    return formatApiError(submitResponse);
  }

  const submittedTask = normalizePodcastTask(submitResponse.data);
  if (!submittedTask.taskId) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'PROTOCOL',
      errorMessage: 'API returned success but no `task_id` for podcast text generation.',
    };
  }

  const textReadyTask = await waitForTask(client, submittedTask.taskId, ctx, {
    label: 'podcast-text',
    ready: isPodcastTextReady,
  });
  if (!textReadyTask.ok) return textReadyTask;

  const audioRequest = normalizeGenerateAudioInput({
    taskId: submittedTask.taskId,
    scripts: normalizedInput.scripts ?? null,
  });
  const audioRequestBody = buildGenerateAudioPayload(audioRequest);

  let audioResponse;
  try {
    audioResponse = await client.post(`/v1/generation/podcast/generate/${submittedTask.taskId}/audio`, audioRequestBody);
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(audioResponse)) {
    return formatApiError(audioResponse);
  }

  const audioSubmittedTask = normalizePodcastTask(audioResponse.data);
  const finalTaskId = audioSubmittedTask.taskId || submittedTask.taskId;
  const audioReadyTask = await waitForTask(client, finalTaskId, ctx, {
    label: 'podcast-audio',
    ready: isPodcastAudioReady,
  });
  if (!audioReadyTask.ok) return audioReadyTask;

  return {
    ok: true,
    phase: 'completed',
    taskId: audioReadyTask.task.taskId,
    taskStatus: audioReadyTask.task.taskStatus,
    contentStatus: audioReadyTask.task.contentStatus,
    audios: audioReadyTask.task.audios,
    scripts: audioReadyTask.task.scripts,
    lyrics: audioReadyTask.task.lyrics,
    coverUrl: audioReadyTask.task.coverUrl,
    requestSummary: buildRequestSummary(textRequestBody),
    errorCode: null,
    errorMessage: null,
  };
}

function buildRequestSummary(body) {
  return {
    query: body?.query ?? null,
    speakers: body?.speakers ?? null,
    language: body?.language ?? null,
    mode: body?.mode ?? null,
  };
}

async function waitForTask(client, taskId, ctx, options) {
  const { label, ready } = options;
  const start = Date.now();

  while (true) {
    if (Date.now() - start >= ctx.pollTimeoutMs) {
      return {
        ok: false,
        phase: 'failed',
        errorCode: 'TIMEOUT',
        errorMessage: `Poll timeout after ${Math.round((Date.now() - start) / 1000)}s.`,
      };
    }

    const elapsed = Date.now() - start;
    await sleep(resolvePollIntervalMs(ctx, elapsed, { pollProfile: 'fast' }));

    let response;
    try {
      response = await client.get(`/v1/generation/${taskId}/status`, { retries: 3 });
    } catch (err) {
      log(`Warning: ${label} poll failed (${err.message}), retrying.`);
      continue;
    }

    if (!isApiSuccess(response)) {
      log(`Warning: ${label} poll returned status ${response.status}, retrying.`);
      continue;
    }

    const task = normalizePodcastTask(response.data);
    const phase = getPodcastLifecyclePhase(task);
    const elapsedSec = Math.round((Date.now() - start) / 1000);
    log(
      `Polling ${label} ${taskId}... task_status=${task.taskStatus} content_status=${task.contentStatus ?? 'n/a'} (${elapsedSec}s elapsed)`,
    );

    if (isPodcastFailure(task)) {
      return {
        ok: false,
        phase: 'failed',
        errorCode: 'TASK_FAILED',
        errorMessage: getPodcastFailureMessage(task),
      };
    }

    if (ready(task)) {
      return { ok: true, phase, task };
    }
  }
}

export default execute;
