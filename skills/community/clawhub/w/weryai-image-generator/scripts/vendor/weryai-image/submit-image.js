import { createClient, log } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from '../weryai-core/errors.js';
import { buildBody, fetchModelRegistry, lookupModel, validateWithModel } from './model-registry.js';
import { DEFAULT_MODEL, FALLBACK_DEFAULTS } from './models.js';
import { normalizeImageInput } from './normalize-input.js';
import { collectLocalUploadPreview, resolveImageUploadSources, validateLocalImageSources } from './upload.js';
import { validateSubmitImage } from './validators.js';

export async function execute(input, ctx) {
  const normalizedInput = normalizeImageInput(input);
  const structErrors = validateSubmitImage(normalizedInput);
  const localErrors = await validateLocalImageSources(normalizedInput.images);
  const allErrors = [...structErrors, ...localErrors];
  if (allErrors.length > 0) {
    return { ok: false, phase: 'failed', errorCode: 'VALIDATION', errorMessage: allErrors.join(' ') };
  }

  const registry = await fetchModelRegistry(ctx);
  const model = normalizedInput.model || DEFAULT_MODEL;
  const meta = lookupModel(registry, model, 'image_to_image');

  if (meta) {
    const { errors, warnings } = validateWithModel(meta, normalizedInput, 'image_to_image');
    warnings.forEach((warning) => log(`Warning: ${warning}`));
    if (errors.length > 0) {
      return { ok: false, phase: 'failed', errorCode: 'VALIDATION', errorMessage: errors.join(' ') };
    }
  } else if (registry) {
    log(`Warning: model "${model}" not found in image_to_image registry. Proceeding anyway.`);
  }

  const body = meta ? buildBody(meta, normalizedInput, 'image_to_image') : buildFallbackBody(normalizedInput, model);
  const uploadPreview = collectLocalUploadPreview(body);

  if (ctx.dryRun) {
    return {
      ok: true,
      phase: 'dry-run',
      dryRun: true,
      requestBody: body,
      requestUrl: `${ctx.baseUrl}/v1/generation/image-to-image`,
      uploadPreview,
      notes: 'dry-run does not upload local files. Local sources in uploadPreview will be uploaded in a real run via /v1/generation/upload-file.',
    };
  }

  let resolvedBody;
  try {
    resolvedBody = await resolveImageUploadSources(ctx, body);
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
    res = await client.post('/v1/generation/image-to-image', resolvedBody);
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
    taskId: taskIds[0] ?? null,
    taskStatus: null,
    images: null,
    balance: null,
    requestSummary: buildRequestSummary(resolvedBody),
    errorCode: null,
    errorMessage: null,
  };
}

function buildRequestSummary(body) {
  return {
    model: body?.model ?? null,
    aspectRatio: body?.aspect_ratio ?? null,
    imageNumber: body?.image_number ?? null,
    resolution: body?.resolution ?? null,
  };
}

function buildFallbackBody(input, model) {
  const body = {
    prompt: input.prompt,
    model,
    images: input.images.slice(0, 1),
    aspect_ratio: input.aspect_ratio || input.aspectRatio || FALLBACK_DEFAULTS.aspect_ratio,
    image_number: Number(input.image_number || input.imageNumber) || FALLBACK_DEFAULTS.image_number,
  };
  if (input.negative_prompt || input.negativePrompt) {
    body.negative_prompt = input.negative_prompt || input.negativePrompt;
  }
  if (input.resolution) {
    body.resolution = input.resolution;
  }
  return body;
}

export default execute;
