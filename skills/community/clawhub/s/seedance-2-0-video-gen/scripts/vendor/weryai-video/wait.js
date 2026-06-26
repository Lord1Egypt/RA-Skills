import { createClient, log } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from '../weryai-core/errors.js';
import { buildBody, fetchModelRegistry, resolveSubmissionPlan, validateWithModel } from './model-registry.js';
import { DEFAULT_MODEL, FALLBACK_DEFAULTS } from './models.js';
import { coerceBool } from './utils.js';
import { validateSubmitImage, validateSubmitMultiImage, validateSubmitText } from './validators.js';
import { pollSubmittedTasks } from '../weryai-core/wait.js';

export async function execute(input, ctx) {
  const requestedMode = detectRequestedMode(input);
  const structErrors = requestedMode === 'multi_image'
    ? validateSubmitMultiImage(input)
    : requestedMode === 'image'
      ? validateSubmitImage(input)
      : validateSubmitText(input);

  if (structErrors.length > 0) {
    return { ok: false, phase: 'failed', errorCode: 'VALIDATION', errorMessage: structErrors.join(' ') };
  }

  const requestedRegistryMode = requestedMode === 'multi_image'
    ? 'multi_image_to_video'
    : requestedMode === 'image'
      ? 'image_to_video'
      : 'text_to_video';

  const registry = await fetchModelRegistry(ctx);
  const model = input.model || DEFAULT_MODEL;
  const plan = resolveSubmissionPlan(registry, model, input, requestedRegistryMode);
  const effectiveInput = plan.input;
  const effectiveMode = plan.mode;
  const meta = plan.meta;

  plan.warnings.forEach((warning) => log(`Warning: ${warning}`));
  if (meta) {
    const { errors, warnings } = validateWithModel(meta, effectiveInput, effectiveMode);
    warnings.forEach((warning) => log(`Warning: ${warning}`));
    if (errors.length > 0) {
      return { ok: false, phase: 'failed', errorCode: 'VALIDATION', errorMessage: errors.join(' ') };
    }
  } else if (registry) {
    log(`Warning: model "${model}" not found in ${effectiveMode} registry. Proceeding anyway.`);
  }

  const body = meta ? buildBody(meta, effectiveInput, effectiveMode) : buildFallbackBody(effectiveInput, model, effectiveMode);
  const apiPath = effectiveMode === 'multi_image_to_video'
    ? '/v1/generation/multi-image-to-video'
    : effectiveMode === 'image_to_video'
      ? '/v1/generation/image-to-video'
      : '/v1/generation/text-to-video';

  if (ctx.dryRun) {
    return {
      ok: true,
      phase: 'dry-run',
      dryRun: true,
      requestBody: body,
      requestUrl: `${ctx.baseUrl}${apiPath}`,
    };
  }

  const client = createClient(ctx);
  let submitRes;
  try {
    submitRes = await client.post(apiPath, body);
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(submitRes)) {
    return formatApiError(submitRes);
  }

  const data = submitRes.data || {};
  const batchId = data.batch_id ?? null;
  const taskIds = data.task_ids ?? (data.task_id ? [data.task_id] : []);

  if (taskIds.length === 0) {
    return { ok: false, phase: 'failed', errorCode: 'PROTOCOL', errorMessage: 'API returned success but no task_ids.' };
  }

  return pollSubmittedTasks(client, {
    batchId,
    taskIds,
    ctx,
    outputKey: 'videos',
    outputLabel: 'video',
    allowBatch: true,
  });
}

function detectRequestedMode(input) {
  if (Array.isArray(input.images) && input.images.length > 0) return 'multi_image';
  if (input.image && typeof input.image === 'string') return 'image';
  return 'text';
}

function buildFallbackBody(input, model, effectiveMode) {
  const body = {
    prompt: input.prompt,
    model,
    duration: Number(input.duration ?? input.dur) || FALLBACK_DEFAULTS.duration,
  };
  const aspectRatio = input.aspect_ratio || input.aspectRatio;
  if (aspectRatio) body.aspect_ratio = aspectRatio;
  if (input.resolution) body.resolution = input.resolution;
  if (input.generate_audio != null || input.generateAudio != null) {
    body.generate_audio = coerceBool(input.generate_audio ?? input.generateAudio, false);
  }
  if (effectiveMode === 'image_to_video') body.image = input.image;
  if (effectiveMode === 'multi_image_to_video') body.images = input.images.slice(0, 3);
  if (input.negative_prompt || input.negativePrompt) {
    body.negative_prompt = input.negative_prompt || input.negativePrompt;
  }
  return body;
}

export default execute;
