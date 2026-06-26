import { createClient } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from '../weryai-core/errors.js';
import { normalizePodcastTask } from './normalize.js';
import { buildSubmitTextPayload, normalizeSubmitTextInput, validateSubmitTextInput } from './validators.js';

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

  const body = buildSubmitTextPayload(normalizedInput);
  const requestUrl = `${ctx.baseUrl}/v1/generation/podcast/generate/text`;

  if (ctx.dryRun) {
    return {
      ok: true,
      phase: 'dry-run',
      dryRun: true,
      requestUrl,
      requestBody: body,
    };
  }

  const client = createClient(ctx);
  let response;
  try {
    response = await client.post('/v1/generation/podcast/generate/text', body);
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(response)) {
    return formatApiError(response);
  }

  const task = normalizePodcastTask(response.data);
  return {
    ok: true,
    phase: 'submitted',
    taskId: task.taskId,
    taskStatus: task.taskStatus,
    contentStatus: task.contentStatus,
    scripts: task.scripts,
    requestSummary: buildRequestSummary(body),
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

export default execute;
