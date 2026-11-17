export type OnDemandServiceSlug =
  | 'qwen3_8_max'
  | 'qwen3_8_flash'
  | 'ling_3_0_flash_fin'
  | 'seedance_2_5'
  | 'glm_5_3'
  | 'glm_5_3_flash'
  | 'image_to_image'
  | 'glm_5_2'
  | 'qwen3'
  | 'minimax_m2_5'
  | 'gpt_oss_120b'
  | 'flux'
  | 'llama_3_1_70b'
  | 'llama_3_8b'
  | 'step_video'
  | 'grounding_dino'
  | 'blip'
  | 'whisper'
  | 'stable_diffusion_xl_turbo'
  | 'llava'
  // Previously observed services. Keep these as catalog entries for backward
  // compatibility, but mark them when not present in the latest live list.
  | 'esrgan'
  | 'voice_cloning'
  | 'instant_id'
  | 'talking_head';

export type OnDemandServiceCategory =
  | 'ImageGen'
  | 'ImageCaption'
  | 'ImageRestore'
  | 'TextToSpeech'
  | 'ObjectDetection'
  | 'VideoGen'
  | 'SpeechRec'
  | 'LLM'
  | 'VisionLanguage';

export type OnDemandServiceSpec = {
  slug: OnDemandServiceSlug;
  name?: string;
  category: OnDemandServiceCategory;
  requiredInputFields: string[];
  supportsInputPresignedUrls: boolean;
  defaultPrediction?: string;
  inputSchemaKind?: 'prompt' | 'chat_messages' | 'file' | 'image_question' | 'service_specific';
  variants?: string[];
  observedUnitPriceUsd?: string;
  pricingHint?: string;
  maxTokensDefault?: number;
  contextWindow?: number;
  license?: string;
  liveStatus?: 'live-public-2026-10-03' | 'retired-not-in-live-list-2026-10-03' | 'live-public-2026-08-05' | 'live-public-2026-05-26' | 'catalog-only-not-in-live-list-2026-05-26' | 'previously-observed-not-in-live-list-2026-04-25';
  notes?: string;
};

export type OnDemandChatServiceSlug = Extract<
  OnDemandServiceSlug,
  'qwen3_8_max' | 'qwen3_8_flash' | 'ling_3_0_flash_fin' | 'glm_5_3' | 'glm_5_3_flash' | 'glm_5_2' | 'qwen3' | 'minimax_m2_5' | 'gpt_oss_120b' | 'llama_3_1_70b' | 'llama_3_8b'
>;

export const ONDEMAND_CHAT_SERVICE_SLUGS: readonly OnDemandChatServiceSlug[] = Object.freeze([
  'glm_5_2',
  'qwen3',
  'minimax_m2_5',
  'gpt_oss_120b',
  'llama_3_1_70b',
  'llama_3_8b',
  'glm_5_3',
  'glm_5_3_flash',
  'qwen3_8_max',
  'qwen3_8_flash',
  'ling_3_0_flash_fin'
] as const);

// Chat services served by POST /infer_request/chat/completions with model=<slug>.
// Live-verified 2026-10-03 for the GLM-5.3, Qwen3.8 and Ling families.
export const OPENAI_CHAT_COMPLETION_SERVICES: readonly string[] = Object.freeze([
  'gpt_oss_120b', 'glm_5_3', 'glm_5_3_flash', 'qwen3_8_max', 'qwen3_8_flash', 'ling_3_0_flash_fin'
]) as readonly string[];

// Services that return structured tool_calls. Live 2026-10-03: Qwen3.8-Max/Flash and
// Ling-3.0-flash-Fin accept a tools array but silently ignore it (plain-text answers).
export const TOOL_CALLING_CHAT_SERVICES: readonly string[] = Object.freeze(['glm_5_3', 'glm_5_3_flash', 'gpt_oss_120b']) as readonly string[];

export function isOnDemandChatService(slug: string): slug is OnDemandChatServiceSlug {
  return (ONDEMAND_CHAT_SERVICE_SLUGS as readonly string[]).includes(slug);
}

// Refreshed against live public on-demand service discovery on 2026-05-26.
// Source: https://ondemand.thetaedgecloud.com/service/list
export const ONDEMAND_SERVICE_CATALOG: Record<OnDemandServiceSlug, OnDemandServiceSpec> = {
  qwen3_8_max: { slug: 'qwen3_8_max', name: 'Qwen3.8-Max', category: 'LLM', requiredInputFields: ['messages'], supportsInputPresignedUrls: false, defaultPrediction: 'completions', inputSchemaKind: 'chat_messages', pricingHint: 'live list 2026-10-03: input=220/output=660 credits per 1M tokens (1 credit = USD 0.01)', notes: 'OpenAI-compatible chat/completions. Optional enable_thinking. Tools are ignored; use GLM-5.3 for tool calls.' },
  qwen3_8_flash: { slug: 'qwen3_8_flash', name: 'Qwen3.8-Flash', category: 'LLM', requiredInputFields: ['messages'], supportsInputPresignedUrls: false, defaultPrediction: 'completions', inputSchemaKind: 'chat_messages', pricingHint: 'live list 2026-10-03: input=17/output=52 credits per 1M tokens (1 credit = USD 0.01)', notes: 'Cheapest live chat model. Optional enable_thinking. Tools are ignored.' },
  ling_3_0_flash_fin: { slug: 'ling_3_0_flash_fin', name: 'Ling-3.0-flash-Fin', category: 'LLM', requiredInputFields: ['messages'], supportsInputPresignedUrls: false, defaultPrediction: 'completions', inputSchemaKind: 'chat_messages', maxTokensDefault: 2048, contextWindow: 256000, pricingHint: 'live list 2026-10-03 shows 0/0; treat cost as UNKNOWN, not free', notes: 'Finance model via ZAN Router. Writes reasoning into content; allow >=1024 max_tokens. Tools are ignored.' },
  seedance_2_5: { slug: 'seedance_2_5', name: 'Seedance 2.5', category: 'VideoGen', requiredInputFields: ['prompt'], supportsInputPresignedUrls: true, defaultPrediction: 'default', inputSchemaKind: 'service_specific', pricingHint: 'live list: 1177 credits per 1M video tokens; resolution/reference multipliers apply', notes: 'BytePlus external route. duration 4-30 (MCP example of 1 is invalid), ratio 16:9|9:16|1:1, resolution 480p|720p|1080p, generate_audio, watermark, one reference_image_url/reference_video_url/reference_audio_url. 2026-10-03: API returned 503 "temporarily unavailable".' },
  glm_5_3: { slug: 'glm_5_3', name: 'GLM 5.3', category: 'LLM', requiredInputFields: ['messages'], supportsInputPresignedUrls: false, defaultPrediction: 'completions', inputSchemaKind: 'chat_messages', notes: 'Use OpenAI-compatible chat/completions for structured tools; discover live capacity before use.' },
  glm_5_3_flash: { slug: 'glm_5_3_flash', name: 'GLM 5.3 Flash', category: 'LLM', requiredInputFields: ['messages'], supportsInputPresignedUrls: false, defaultPrediction: 'completions', inputSchemaKind: 'chat_messages', notes: 'Public catalog does not guarantee available workers.' },
  image_to_image: { slug: 'image_to_image', name: 'Image to image', category: 'ImageRestore', requiredInputFields: [], supportsInputPresignedUrls: true, inputSchemaKind: 'service_specific', notes: 'Discover prediction-specific required fields and variants live; do not assume one input contract.' },
  glm_5_2: {
    slug: 'glm_5_2',
    name: 'GLM 5.2',
    category: 'LLM',
    requiredInputFields: ['messages'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'completions',
    inputSchemaKind: 'chat_messages',
    variants: ['default'],
    maxTokensDefault: 5000,
    contextWindow: 1000000,
    license: 'MIT',
    pricingHint: 'live list: input=154/output=484, divisor=1000000; raw split-price units, currency unverified',
    liveStatus: 'live-public-2026-08-05',
    notes: 'Canonical slug is glm_5_2. Live schema includes enable_thinking. Keep opt-in for bounded, verifiable worker tasks.'
  },
  qwen3: {
    slug: 'qwen3',
    name: 'Qwen3',
    category: 'LLM',
    requiredInputFields: ['messages'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'completions',
    inputSchemaKind: 'chat_messages',
    variants: ['default', 'parallax_32b_fp8'],
    pricingHint: 'live list: input=20/output=40 per 1M tokens; split pricing',
    liveStatus: 'live-public-2026-05-26',
    notes: 'Canonical slug is qwen3. Use input.messages chat-array payloads; capacity may return retriable 409 No instances available.'
  },
  minimax_m2_5: {
    slug: 'minimax_m2_5',
    name: 'MiniMax M2.5',
    category: 'LLM',
    requiredInputFields: ['messages'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'completions',
    inputSchemaKind: 'chat_messages',
    pricingHint: 'live list: input=20/output=120 per 1M tokens; split pricing; context_length=196608',
    liveStatus: 'catalog-only-not-in-live-list-2026-05-26',
    notes: 'Observed on 2026-04-25 but absent from the 2026-05-26 live public service list.'
  },
  gpt_oss_120b: {
    slug: 'gpt_oss_120b',
    name: 'GPT OSS 120B',
    category: 'LLM',
    requiredInputFields: ['messages'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'completions',
    inputSchemaKind: 'chat_messages',
    pricingHint: 'live list: input=4/output=20 per 1M tokens; split pricing; context_length=131072',
    liveStatus: 'live-public-2026-05-26'
  },
  flux: {
    slug: 'flux',
    name: 'FLUX',
    category: 'ImageGen',
    requiredInputFields: ['prompt'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'generate_image',
    inputSchemaKind: 'prompt',
    variants: ['default', 'quantized'],
    observedUnitPriceUsd: '0.01 / image',
    liveStatus: 'live-public-2026-05-26'
  },
  llama_3_1_70b: {
    slug: 'llama_3_1_70b',
    name: 'Llama 3.1 70B',
    category: 'LLM',
    requiredInputFields: ['messages'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'completions',
    inputSchemaKind: 'chat_messages',
    variants: ['default', 'quantized'],
    pricingHint: 'live list: input=20/output=40 per 1M tokens; split pricing; context_length=131072',
    liveStatus: 'live-public-2026-05-26',
    notes: 'Observed occasional 409: No instances available.'
  },
  llama_3_8b: {
    slug: 'llama_3_8b',
    name: 'Llama 3 8B',
    category: 'LLM',
    requiredInputFields: ['messages'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'completions',
    inputSchemaKind: 'chat_messages',
    variants: ['default', 'quantized'],
    pricingHint: 'live list: input=20/output=40 per 1M tokens; split pricing; context_length=8192',
    liveStatus: 'catalog-only-not-in-live-list-2026-05-26',
    notes: 'Observed on 2026-04-25 but absent from the 2026-05-26 live public service list.'
  },
  step_video: {
    slug: 'step_video',
    name: 'Step Video',
    category: 'VideoGen',
    requiredInputFields: ['prompt'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'generate',
    inputSchemaKind: 'prompt',
    observedUnitPriceUsd: '0.20 / video',
    liveStatus: 'catalog-only-not-in-live-list-2026-05-26',
    notes: 'Often asynchronous and long-running. Observed on 2026-04-25 but absent from the 2026-05-26 live public service list.'
  },
  grounding_dino: {
    slug: 'grounding_dino',
    name: 'Grounding Dino',
    category: 'ObjectDetection',
    requiredInputFields: ['input_img', 'detection_prompt'],
    supportsInputPresignedUrls: true,
    defaultPrediction: '0',
    inputSchemaKind: 'file',
    observedUnitPriceUsd: '0.01 / image',
    liveStatus: 'live-public-2026-05-26'
  },
  blip: {
    slug: 'blip',
    name: 'Blip',
    category: 'ImageCaption',
    requiredInputFields: ['input_img'],
    supportsInputPresignedUrls: true,
    defaultPrediction: 'predict',
    inputSchemaKind: 'file',
    observedUnitPriceUsd: '0.01 / image',
    liveStatus: 'live-public-2026-05-26',
    notes: 'Prefer presigned upload to avoid external URL fetch failures.'
  },
  whisper: {
    slug: 'whisper',
    name: 'Whisper',
    category: 'SpeechRec',
    requiredInputFields: ['audio_filename'],
    supportsInputPresignedUrls: true,
    defaultPrediction: 'stt',
    inputSchemaKind: 'file',
    observedUnitPriceUsd: 'low fractional / clip',
    liveStatus: 'live-public-2026-05-26'
  },
  stable_diffusion_xl_turbo: {
    slug: 'stable_diffusion_xl_turbo',
    name: 'Stable Diffusion XL Turbo',
    category: 'ImageGen',
    requiredInputFields: ['prompt'],
    supportsInputPresignedUrls: false,
    defaultPrediction: 'predict',
    inputSchemaKind: 'prompt',
    observedUnitPriceUsd: '0.01 / image',
    liveStatus: 'live-public-2026-05-26'
  },
  llava: {
    slug: 'llava',
    name: 'LLaVA',
    category: 'VisionLanguage',
    requiredInputFields: ['input_img', 'question'],
    supportsInputPresignedUrls: true,
    defaultPrediction: 'predict',
    inputSchemaKind: 'image_question',
    variants: ['quantized'],
    observedUnitPriceUsd: '0.01 / image',
    liveStatus: 'live-public-2026-05-26',
    notes: 'Vision-language question answering over images.'
  },
  esrgan: {
    slug: 'esrgan',
    name: 'ESRGAN',
    category: 'ImageRestore',
    requiredInputFields: ['input_img'],
    supportsInputPresignedUrls: true,
    observedUnitPriceUsd: '0.02 / image',
    liveStatus: 'catalog-only-not-in-live-list-2026-05-26'
  },
  voice_cloning: {
    slug: 'voice_cloning',
    name: 'Voice Cloning',
    category: 'TextToSpeech',
    requiredInputFields: ['text', 'language', 'voice'],
    supportsInputPresignedUrls: true,
    observedUnitPriceUsd: '0.01 / audio',
    liveStatus: 'catalog-only-not-in-live-list-2026-05-26'
  },
  instant_id: {
    slug: 'instant_id',
    name: 'Instant ID',
    category: 'ImageGen',
    requiredInputFields: ['face_img', 'prompt'],
    supportsInputPresignedUrls: true,
    observedUnitPriceUsd: '0.24 / image',
    liveStatus: 'catalog-only-not-in-live-list-2026-05-26'
  },
  talking_head: {
    slug: 'talking_head',
    name: 'Talking Head',
    category: 'VideoGen',
    requiredInputFields: ['img', 'audio'],
    supportsInputPresignedUrls: true,
    observedUnitPriceUsd: '0.02 / video',
    liveStatus: 'catalog-only-not-in-live-list-2026-05-26'
  }
};

// Live public on-demand list verified 2026-10-03 (13 services). Anything else in this
// catalog is historical metadata only and must not be presented as available.
export const LIVE_SERVICES_2026_10_03: readonly string[] = Object.freeze([
  'ling_3_0_flash_fin', 'qwen3_8_max', 'qwen3_8_flash', 'glm_5_3', 'glm_5_3_flash', 'qwen3', 'seedance_2_5',
  'blip', 'esrgan', 'image_to_image', 'stable_diffusion_xl_turbo', 'llava', 'whisper'
]) as readonly string[];

for (const spec of Object.values(ONDEMAND_SERVICE_CATALOG)) {
  spec.liveStatus = LIVE_SERVICES_2026_10_03.includes(spec.slug)
    ? 'live-public-2026-10-03'
    : 'retired-not-in-live-list-2026-10-03';
}

// Inference runs without confirm:true ONLY for these known chat and low-cost image/audio/vision
// services. Every other slug (video such as seedance_2_5, retired or future services) is high-cost
// or unknown and requires confirm:true. This is an allowlist, so new services are gated by default.
export const UNGATED_INFERENCE_SERVICES: readonly string[] = Object.freeze([
  ...ONDEMAND_CHAT_SERVICE_SLUGS.filter((slug) => LIVE_SERVICES_2026_10_03.includes(slug)),
  'stable_diffusion_xl_turbo', 'image_to_image', 'esrgan', 'blip', 'llava', 'whisper'
]) as readonly string[];

export function inferenceRequiresConfirm(service: string): boolean {
  return !UNGATED_INFERENCE_SERVICES.includes(String(service ?? '').trim());
}

export function listOnDemandServices(): OnDemandServiceSpec[] {
  return Object.values(ONDEMAND_SERVICE_CATALOG);
}
