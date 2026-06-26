import { createClient } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError } from '../weryai-core/errors.js';
import { buildMessages, DEFAULT_MODEL, normalizeInput, PRESETS, validateInput } from './presets.js';

export function createWriteExecutor(presetId) {
  const preset = PRESETS[presetId];
  if (!preset) {
    throw new Error(`Unknown text preset: ${presetId}`);
  }

  return async function execute(input, ctx) {
    const normalizedInput = normalizeInput(input);
    const validationErrors = validateInput(normalizedInput);
    if (validationErrors.length > 0) {
      return {
        ok: false,
        phase: 'failed',
        errorCode: 'VALIDATION',
        errorMessage: validationErrors.join(' '),
      };
    }

    const requestBody = {
      model: normalizedInput.model || ctx.defaultModel || DEFAULT_MODEL,
      messages: buildMessages(normalizedInput, preset),
      max_tokens: normalizedInput.maxTokens ?? preset.maxTokens,
      temperature: normalizedInput.temperature ?? preset.temperature,
      top_p: normalizedInput.topP ?? 1,
    };

    if (ctx.dryRun) {
      return {
        ok: true,
        phase: 'dry-run',
        dryRun: true,
        preset: preset.id,
        requestUrl: `${ctx.baseUrl}/v1/chat/completions`,
        requestBody,
      };
    }

    const client = createClient(ctx);
    let response;
    try {
      response = await client.post('/v1/chat/completions', requestBody);
    } catch (err) {
      return formatNetworkError(err);
    }

    if (response.httpStatus < 200 || response.httpStatus >= 300) {
      return formatApiError(response);
    }

    if (!Array.isArray(response.choices) || response.choices.length === 0) {
      return {
        ok: false,
        phase: 'failed',
        errorCode: 'PROTOCOL',
        errorMessage: 'Chat API returned no choices.',
      };
    }

    const firstChoice = response.choices[0] || {};
    const firstMessage = firstChoice.message || {};

    return {
      ok: true,
      phase: 'completed',
      preset: preset.id,
      model: response.model || requestBody.model,
      text: typeof firstMessage.content === 'string' ? firstMessage.content : '',
      finishReason: firstChoice.finish_reason ?? null,
      choices: response.choices.map((choice) => ({
        index: choice.index ?? null,
        role: choice.message?.role ?? 'assistant',
        content: typeof choice.message?.content === 'string' ? choice.message.content : '',
        finishReason: choice.finish_reason ?? null,
      })),
      usage: response.usage ?? null,
      errorCode: null,
      errorMessage: null,
    };
  };
}
