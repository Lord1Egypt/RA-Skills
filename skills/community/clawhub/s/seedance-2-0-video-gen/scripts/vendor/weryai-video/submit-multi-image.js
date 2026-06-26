import { createClient, log } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from '../weryai-core/errors.js';
import { buildBody, fetchModelRegistry, resolveSubmissionPlan, validateWithModel } from './model-registry.js';
import { DEFAULT_MODEL, FALLBACK_DEFAULTS } from './models.js';
import { coerceBool } from './utils.js';
import { validateSubmitMultiImage } from './validators.js';

export async function execute(input, ctx) {
  const structErrors = validateSubmitMultiImage(input);
  if (structErrors.length > 0) {
    return { ok: false, phase: 'failed', errorCode: 'VALIDATION', errorMessage: structErrors.join(' ') };
  }

  const registry = await fetchModelRegistry(ctx);
  const model = input.model || DEFAULT_MODEL;
  const plan = resolveSubmissionPlan(registry, model, input, 'multi_image_to_video');
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
  const apiPath = effectiveMode === 'image_to_video'
    ? '/v1/generation/image-to-video'
    : '/v1/generation/multi-image-to-video';

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
  let res;
  try {
    res = await client.post(apiPath, body);
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
    videos: null,
    balance: null,
    errorCode: null,
    errorMessage: null,
  };
}

function buildFallbackBody(input, model, effectiveMode) {
  const body = {
    prompt: input.prompt,
    model,
    duration: Number(input.duration ?? input.dur) || FALLBACK_DEFAULTS.duration,
  };
  if (effectiveMode === 'image_to_video') {
    body.image = input.image;
  } else {
    body.images = input.images.slice(0, 3);
  }
  const aspectRatio = input.aspect_ratio || input.aspectRatio;
  if (aspectRatio) body.aspect_ratio = aspectRatio;
  if (input.resolution) body.resolution = input.resolution;
  if (input.generate_audio != null || input.generateAudio != null) {
    body.generate_audio = coerceBool(input.generate_audio ?? input.generateAudio, false);
  }
  if (input.negative_prompt || input.negativePrompt) {
    body.negative_prompt = input.negative_prompt || input.negativePrompt;
  }
  return body;
}

export default execute;
