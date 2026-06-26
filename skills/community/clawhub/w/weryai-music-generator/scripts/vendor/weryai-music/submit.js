import { createClient } from '../weryai-core/client.js';
import { buildPayload, validateSubmit } from './validators.js';
import { isApiSuccess, formatApiError, formatNetworkError } from '../weryai-core/errors.js';
import { normalizeMusicInput } from './normalize-input.js';
import { isRemoteUrl, resolvePublicUrlFromSource } from '../weryai-core/upload.js';

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
  let res;
  try {
    res = await client.post('/v1/generation/music/generate', resolvedBody);
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(res)) {
    return formatApiError(res);
  }

  const data = res.data || {};
  const taskIds = data.task_ids ?? (data.task_id ? [data.task_id] : []);

  return {
    ok: true,
    phase: 'submitted',
    batchId: data.batch_id ?? null,
    taskIds,
    taskId: data.task_id ?? taskIds[0] ?? null,
    taskStatus: normalizeSubmittedStatus(data.task_status ?? data.taskStatus),
    audios: null,
    lyrics: null,
    coverUrl: null,
    balance: null,
    requestSummary: buildRequestSummary(resolvedBody),
    errorCode: null,
    errorMessage: null,
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

function normalizeSubmittedStatus(rawStatus) {
  if (rawStatus === 'WAITING' || rawStatus === 'waiting') return 'waiting';
  if (rawStatus === 'PROCESSING' || rawStatus === 'processing') return 'processing';
  return rawStatus ?? null;
}
