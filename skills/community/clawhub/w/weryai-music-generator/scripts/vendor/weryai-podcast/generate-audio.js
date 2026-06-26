import { createClient } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from '../weryai-core/errors.js';
import { normalizePodcastTask } from './normalize.js';
import { buildGenerateAudioPayload, normalizeGenerateAudioInput, validateGenerateAudioInput } from './validators.js';

export async function execute(input, ctx) {
  const normalizedInput = normalizeGenerateAudioInput(input);
  const validationErrors = validateGenerateAudioInput(normalizedInput);
  if (validationErrors.length > 0) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'VALIDATION',
      errorMessage: validationErrors.join(' '),
    };
  }

  const body = buildGenerateAudioPayload(normalizedInput);
  const requestUrl = `${ctx.baseUrl}/v1/generation/podcast/generate/${normalizedInput.taskId}/audio`;

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
    response = await client.post(`/v1/generation/podcast/generate/${normalizedInput.taskId}/audio`, body);
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
    taskId: task.taskId || normalizedInput.taskId,
    taskStatus: task.taskStatus,
    contentStatus: task.contentStatus,
    scripts: task.scripts ?? normalizedInput.scripts ?? null,
    errorCode: null,
    errorMessage: null,
  };
}

export default execute;
