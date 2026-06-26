import { createClient } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError } from '../weryai-core/errors.js';

export async function executeModels(input, ctx) {
  const query = typeof input.query === 'string' ? input.query.trim().toLowerCase() : '';

  const client = createClient(ctx);
  let response;
  try {
    response = await client.get('/v1/chat/models');
  } catch (err) {
    return formatNetworkError(err);
  }

  if (response.httpStatus < 200 || response.httpStatus >= 300) {
    return formatApiError(response);
  }

  if (!Array.isArray(response.models)) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'PROTOCOL',
      errorMessage: 'Chat models endpoint returned an unexpected payload.',
    };
  }

  const models = response.models
    .filter((model) => {
      if (!query) return true;
      const haystack = `${model.model || ''} ${model.desc || ''}`.toLowerCase();
      return haystack.includes(query);
    })
    .sort((a, b) => {
      const priceA = Number.isFinite(a.input_price) ? a.input_price : Number.POSITIVE_INFINITY;
      const priceB = Number.isFinite(b.input_price) ? b.input_price : Number.POSITIVE_INFINITY;
      if (priceA !== priceB) return priceA - priceB;
      return String(a.model || '').localeCompare(String(b.model || ''));
    });

  return {
    ok: true,
    phase: 'completed',
    count: models.length,
    models,
    errorCode: null,
    errorMessage: null,
  };
}
