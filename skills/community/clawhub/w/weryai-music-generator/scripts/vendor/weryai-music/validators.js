const STYLE_GROUPS = {
  genre: ['POP', 'ROCK', 'RAP', 'ELECTRONIC', 'RNB', 'JAZZ', 'FOLK', 'CLASSIC', 'WORLD'],
  emotion: ['HAPPY', 'RELAXED', 'WARM', 'ROMANTIC', 'TOUCHING', 'SAD', 'LONELY', 'DEPRESSED', 'TENSE', 'EXCITED', 'EPIC', 'MYSTERIOUS'],
  instrument: ['PIANO', 'GUITAR', 'BASS', 'DRUMS', 'STRINGS', 'WIND', 'SYNTHESIZER', 'ELECTRONIC_SOUND', 'FOLK_INSTRUMENT', 'MIXED_ORCHESTRATION'],
};

const ALL_STYLE_KEYS = new Set(Object.values(STYLE_GROUPS).flat());

export function validateSubmit(input) {
  const errors = [];

  const type = input.type;
  if (!type) {
    errors.push('`type` is required and must be `VOCAL_SONG` or `ONLY_MUSIC`.');
    return errors;
  }

  if (type !== 'VOCAL_SONG' && type !== 'ONLY_MUSIC') {
    errors.push('`type` must be `VOCAL_SONG` or `ONLY_MUSIC`.');
  }

  const description = normalizeText(input.description);
  const lyrics = normalizeText(input.lyrics);
  const styles = input.styles;
  const gender = input.gender;
  const referenceAudio = normalizeText(input.reference_audio ?? input.referenceAudio);
  const audioName = normalizeText(input.audio_name ?? input.audioName);
  const webhookUrl = normalizeText(input.webhook_url ?? input.webhookUrl);
  const callerId = input.caller_id ?? input.callerId;

  if (!description && !hasStyles(styles)) {
    errors.push('At least one of `description` or `styles` must be provided.');
  }

  if (styles != null) {
    if (!isPlainObject(styles) || Object.keys(styles).length === 0) {
      errors.push('`styles` must be a non-empty object of style-key to style-description pairs.');
    } else {
      for (const [key, value] of Object.entries(styles)) {
        if (!ALL_STYLE_KEYS.has(key)) {
          errors.push(`Unsupported style key: \`${key}\`.`);
        }
        if (typeof value !== 'string' || !value.trim()) {
          errors.push(`Style value for \`${key}\` must be a non-empty string.`);
        }
      }
    }
  }

  if (referenceAudio && !audioName) {
    errors.push('`audio_name` is recommended when `reference_audio` is provided, and is required by this CLI for clearer task provenance.');
  }

  if (webhookUrl && !isPublicUrl(webhookUrl)) {
    errors.push('`webhook_url` must be a public `http` or `https` URL.');
  }

  if (gender && gender !== 'm' && gender !== 'f') {
    errors.push('`gender` must be `m` or `f` when provided.');
  }

  if (type === 'ONLY_MUSIC') {
    if (lyrics) {
      errors.push('`lyrics` is not supported when `type` is `ONLY_MUSIC`.');
    }
    if (gender) {
      errors.push('`gender` should not be set when `type` is `ONLY_MUSIC`.');
    }
  }

  if (callerId != null && callerId !== '') {
    const asNumber = Number(callerId);
    if (!Number.isInteger(asNumber) || asNumber < 0) {
      errors.push('`caller_id` must be a non-negative integer when provided.');
    }
  }

  return dedupe(errors);
}

export function buildPayload(input) {
  const payload = {
    type: input.type,
  };

  const description = normalizeText(input.description);
  const lyrics = normalizeText(input.lyrics);
  const referenceAudio = normalizeText(input.reference_audio ?? input.referenceAudio);
  const audioName = normalizeText(input.audio_name ?? input.audioName);
  const webhookUrl = normalizeText(input.webhook_url ?? input.webhookUrl);
  const callerId = input.caller_id ?? input.callerId;

  if (description) payload.description = description;
  if (lyrics) payload.lyrics = lyrics;
  if (referenceAudio) payload.reference_audio = referenceAudio;
  if (audioName) payload.audio_name = audioName;
  if (input.gender) payload.gender = input.gender;
  if (hasStyles(input.styles)) payload.styles = sanitizeStyles(input.styles);
  if (webhookUrl) payload.webhook_url = webhookUrl;
  if (callerId != null && callerId !== '') payload.caller_id = Number(callerId);

  return payload;
}

function sanitizeStyles(styles) {
  const out = {};
  for (const [key, value] of Object.entries(styles)) {
    if (typeof value === 'string' && value.trim()) {
      out[key] = value.trim();
    }
  }
  return out;
}

function hasStyles(styles) {
  return isPlainObject(styles) && Object.keys(styles).length > 0;
}

function isPlainObject(value) {
  return !!value && typeof value === 'object' && !Array.isArray(value);
}

function isPublicUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === 'http:' || url.protocol === 'https:';
  } catch {
    return false;
  }
}

function normalizeText(value) {
  return typeof value === 'string' && value.trim() ? value.trim() : '';
}

function dedupe(list) {
  return [...new Set(list)];
}
