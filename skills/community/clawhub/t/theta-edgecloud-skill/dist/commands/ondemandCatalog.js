export const ONDEMAND_CHAT_SERVICE_SLUGS = [
    'qwen3',
    'minimax_m2_5',
    'gpt_oss_120b',
    'llama_3_1_70b',
    'llama_3_8b'
];
export function isOnDemandChatService(slug) {
    return ONDEMAND_CHAT_SERVICE_SLUGS.includes(slug);
}
// Refreshed against live public on-demand service discovery on 2026-05-26.
// Source: https://ondemand.thetaedgecloud.com/service/list
export const ONDEMAND_SERVICE_CATALOG = {
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
export function listOnDemandServices() {
    return Object.values(ONDEMAND_SERVICE_CATALOG);
}
