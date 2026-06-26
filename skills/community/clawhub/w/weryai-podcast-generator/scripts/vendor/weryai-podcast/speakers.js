import { createClient } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from '../weryai-core/errors.js';
import { normalizeSpeakerResponse } from './normalize.js';

export async function execute(input, ctx) {
  const language = typeof input.language === 'string' ? input.language.trim() : '';
  if (!language) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'VALIDATION',
      errorMessage: '`language` is required.',
    };
  }

  const client = createClient(ctx);

  let response;
  try {
    response = await client.get(`/v1/generation/podcast/speakers/list?language=${encodeURIComponent(language)}`, {
      retries: 3,
    });
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(response)) {
    return formatApiError(response);
  }

  const speakers = normalizeSpeakerResponse(response.data);
  return {
    ok: true,
    phase: 'completed',
    language,
    count: speakers.length,
    speakers,
    errorCode: null,
    errorMessage: null,
  };
}

export default execute;
