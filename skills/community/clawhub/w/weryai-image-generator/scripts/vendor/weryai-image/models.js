import { getModelDisplayName } from '../weryai-core/model-display.js';

export const DEFAULT_MODEL = 'WERYAI_IMAGE_2_0';
export const DEFAULT_MODEL_NAME = getModelDisplayName(DEFAULT_MODEL);

export const MODELS_API_PATH = '/growthai/v1/image/models';

export const FALLBACK_DEFAULTS = {
  aspect_ratio: '9:16',
  image_number: 1,
};
