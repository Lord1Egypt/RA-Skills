import {
  normalizeTaskCollection,
  normalizeTaskResult,
} from '../weryai-core/normalize.js';

export function normalizePodcastTask(data) {
  return normalizePodcastTaskEntry(normalizeTaskResult(data), unwrapSingle(data));
}

export function normalizePodcastTaskList(data) {
  const rawList = Array.isArray(data) ? data : [data];
  const normalizedList = normalizeTaskCollection(data);
  return normalizedList.map((task, index) => normalizePodcastTaskEntry(task, rawList[index]));
}

export function normalizeSpeakerResponse(data) {
  const speakers = Array.isArray(data?.speakers) ? data.speakers : [];
  return speakers.map((speaker) => ({
    name: speaker?.name ?? null,
    speakerId: speaker?.speaker_id ?? speaker?.speakerId ?? null,
    demoAudioUrl: speaker?.demo_audio_url ?? speaker?.demoAudioUrl ?? null,
    gender: speaker?.gender ?? null,
    language: speaker?.language ?? null,
  }));
}

export function isPodcastTextReady(task) {
  return task?.contentStatus === 'text-success';
}

export function isPodcastAudioReady(task) {
  return task?.contentStatus === 'audio-success'
    || (task?.taskStatus === 'completed' && Array.isArray(task?.audios) && task.audios.length > 0);
}

export function isPodcastFailure(task) {
  return task?.contentStatus === 'text-fail'
    || task?.contentStatus === 'audio-fail'
    || task?.taskStatus === 'failed';
}

export function getPodcastLifecyclePhase(task) {
  if (isPodcastAudioReady(task)) return 'completed';
  if (isPodcastFailure(task)) return 'failed';
  return 'running';
}

export function getPodcastFailureMessage(task) {
  if (!task) return 'Podcast task failed.';
  if (task.contentStatus === 'text-fail') return 'Podcast text generation failed.';
  if (task.contentStatus === 'audio-fail') return 'Podcast audio generation failed.';
  return task.msg || 'Podcast task failed.';
}

function normalizePodcastTaskEntry(task, raw) {
  return {
    ...task,
    scripts: normalizeScripts(task.scripts, raw),
  };
}

function normalizeScripts(normalized, raw) {
  if (Array.isArray(normalized) && normalized.length > 0) return normalized;
  const rawScripts = raw?.scripts ?? raw?.output?.scripts ?? raw?.script ?? raw?.output?.script;
  if (!Array.isArray(rawScripts) || rawScripts.length === 0) return null;
  return rawScripts.map((entry) => {
    if (!entry || typeof entry !== 'object') return entry;
    return {
      speakerId: entry.speaker_id ?? entry.speakerId ?? null,
      speakerName: entry.speaker_name ?? entry.speakerName ?? null,
      content: typeof entry.content === 'string' ? entry.content : null,
    };
  });
}

function unwrapSingle(data) {
  if (Array.isArray(data)) return data[0] ?? null;
  return data ?? null;
}
