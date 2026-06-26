function pickString(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return null;
}

function toInteger(value) {
  if (value == null || value === '') return null;
  const parsed = Number(value);
  return Number.isInteger(parsed) ? parsed : NaN;
}

function normalizeIdList(value) {
  if (Array.isArray(value)) {
    return value.map((entry) => pickString(entry)).filter(Boolean);
  }
  if (typeof value === 'string' && value.trim()) {
    return value.split(',').map((entry) => entry.trim()).filter(Boolean);
  }
  return [];
}

function normalizeScripts(value) {
  if (!Array.isArray(value)) return null;
  const scripts = value
    .map((entry) => {
      if (!entry || typeof entry !== 'object') return null;
      return {
        speakerId: pickString(entry.speakerId, entry.speaker_id),
        speakerName: pickString(entry.speakerName, entry.speaker_name),
        content: pickString(entry.content),
      };
    })
    .filter(Boolean);
  return scripts.length > 0 ? scripts : null;
}

export function normalizeSubmitTextInput(input) {
  return {
    query: pickString(input.query, input.prompt, input.topic),
    speakers: normalizeIdList(input.speakers ?? input.speakerIds ?? input.speaker_ids),
    language: pickString(input.language, input.lang),
    mode: pickString(input.mode) || 'quick',
    webhookUrl: pickString(input.webhookUrl, input.webhook_url),
    callerId: toInteger(input.callerId ?? input.caller_id),
    scripts: normalizeScripts(input.scripts ?? input.audioScripts ?? input.audio_scripts),
  };
}

export function normalizeGenerateAudioInput(input) {
  return {
    taskId: pickString(input.taskId, input.task_id, input['task-id']),
    scripts: normalizeScripts(input.scripts),
    webhookUrl: pickString(input.webhookUrl, input.webhook_url),
    callerId: toInteger(input.callerId ?? input.caller_id),
  };
}

export function validateSubmitTextInput(input) {
  const errors = [];

  if (!input.query) errors.push('`query` is required.');
  if (!input.language) errors.push('`language` is required.');
  if (!Array.isArray(input.speakers) || input.speakers.length === 0) {
    errors.push('`speakers` must include at least one speaker ID.');
  } else if (input.speakers.length > 2) {
    errors.push('`speakers` supports at most 2 speaker IDs.');
  }
  if (!['quick', 'debate', 'deep'].includes(input.mode)) {
    errors.push('`mode` must be one of `quick`, `debate`, or `deep`.');
  }
  if (input.mode === 'debate' && input.speakers.length !== 2) {
    errors.push('`debate` mode requires exactly 2 speakers.');
  }
  if (Number.isNaN(input.callerId)) {
    errors.push('`callerId` must be an integer when provided.');
  }

  return errors;
}

export function validateGenerateAudioInput(input) {
  const errors = [];

  if (!input.taskId) errors.push('`taskId` is required.');
  if (Number.isNaN(input.callerId)) {
    errors.push('`callerId` must be an integer when provided.');
  }
  if (Array.isArray(input.scripts)) {
    const badIndex = input.scripts.findIndex((entry) => !entry.speakerId || !entry.content);
    if (badIndex >= 0) {
      errors.push('Each `scripts` entry must include `speakerId` and `content`.');
    }
  }

  return errors;
}

export function buildSubmitTextPayload(input) {
  const body = {
    query: input.query,
    speakers: input.speakers,
    language: input.language,
    mode: input.mode,
  };
  if (input.webhookUrl) body.webhook_url = input.webhookUrl;
  if (input.callerId != null) body.caller_id = input.callerId;
  return body;
}

export function buildGenerateAudioPayload(input) {
  const body = {};
  if (Array.isArray(input.scripts) && input.scripts.length > 0) {
    body.scripts = input.scripts.map((entry) => ({
      speaker_id: entry.speakerId,
      ...(entry.speakerName ? { speaker_name: entry.speakerName } : {}),
      content: entry.content,
    }));
  }
  if (input.webhookUrl) body.webhook_url = input.webhookUrl;
  if (input.callerId != null) body.caller_id = input.callerId;
  return body;
}
