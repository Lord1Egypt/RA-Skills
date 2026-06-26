import { createClient } from './client.js';
import { buildPayload, validateSubmit } from './validators.js';
import { isApiSuccess, formatApiError, formatNetworkError } from './errors.js';
import { normalizeMusicInput } from '../vendor/weryai-music/normalize-input.js';
import { isRemoteUrl, resolvePublicUrlFromSource } from '../vendor/weryai-core/upload.js';
import { pollSingleTask } from '../vendor/weryai-core/wait.js';

export async function execute(input, ctx) {
  const normalizedInput = normalizeMusicInput(input);
  const validationErrors = validateSubmit(normalizedInput);
  if (validationErrors.length > 0) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'VALIDATION',
      errorMessage: validationErrors.join(' '),
    };
  }

  const body = buildPayload(normalizedInput);
  const uploadPreview = collectReferenceAudioUploadPreview(body);

  if (ctx.dryRun) {
    return {
      ok: true,
      phase: 'dry-run',
      dryRun: true,
      requestBody: body,
      requestUrl: `${ctx.baseUrl}/v1/generation/music/generate`,
      uploadPreview,
      notes: uploadPreview.length > 0
        ? 'dry-run does not upload local files. Local sources in uploadPreview will be uploaded in a real run via /v1/generation/upload-file.'
        : null,
    };
  }

  let resolvedBody = body;
  try {
    resolvedBody = await resolveReferenceAudioUpload(ctx, body);
  } catch (err) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'UPLOAD_FAILED',
      errorMessage: err?.message ?? String(err),
    };
  }

  const client = createClient(ctx);

  let submitRes;
  try {
    submitRes = await client.post('/v1/generation/music/generate', resolvedBody);
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(submitRes)) {
    return formatApiError(submitRes);
  }

  const data = submitRes.data || {};
  const taskId = data.task_id ?? data.task_ids?.[0] ?? null;
  const taskIds = data.task_ids ?? (taskId ? [taskId] : []);

  if (!taskId) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'PROTOCOL',
      errorMessage: 'API returned success but no task_id.',
    };
  }

  const pollResult = await pollSingleTask(client, {
    taskId,
    taskIds,
    ctx,
    pollProfile: 'slow',
    outputKey: 'audios',
    outputLabel: 'audio',
  });

  return {
    ...pollResult,
    requestSummary: buildRequestSummary(resolvedBody),
  };
}

function buildRequestSummary(body) {
  return {
    type: body?.type ?? null,
    description: body?.description ?? null,
    gender: body?.gender ?? null,
    styles: body?.styles ?? null,
  };
}

function collectReferenceAudioUploadPreview(body) {
  if (typeof body.reference_audio === 'string' && body.reference_audio.trim() && !isRemoteUrl(body.reference_audio)) {
    return [{ field: 'reference_audio', source: body.reference_audio, kind: 'audio' }];
  }
  return [];
}

async function resolveReferenceAudioUpload(ctx, body) {
  const out = { ...body };
  if (typeof out.reference_audio === 'string' && out.reference_audio.trim()) {
    out.reference_audio = await resolvePublicUrlFromSource(ctx, out.reference_audio);
  }
  return out;
}
