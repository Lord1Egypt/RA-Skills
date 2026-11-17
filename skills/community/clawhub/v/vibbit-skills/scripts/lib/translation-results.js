'use strict'
const { VibbitError } = require('./client')
const crypto = require('node:crypto')
const usable = v => {
  if (typeof v !== 'string') return false
  try { const u = new URL(v); return ['http:', 'https:'].includes(u.protocol) && !u.username && !u.password } catch { return false }
}

const reviewSegmentKeys = ['id', 'from', 'to', 'source_text', 'translated_text', 'confidence', 'speaker_id', 'confirmed']
const reviewItemKeys = ['sub_task_id', 'status', 'source_video_url', 'target_languages', 'voice_reference_audio_url', 'error_message']

function pick(source, keys) {
  return Object.fromEntries(keys.filter(key => source?.[key] !== undefined).map(key => [key, source[key]]))
}

function reviewSegments(value) {
  if (!Array.isArray(value)) return undefined
  return value.map(segment => {
    if (!segment || typeof segment !== 'object' || Array.isArray(segment)) return segment
    return pick(segment, reviewSegmentKeys)
  })
}

function reviewShots(value) {
  if (!Array.isArray(value)) return undefined
  return value.map(shot => {
    if (!shot || typeof shot !== 'object' || Array.isArray(shot)) return shot
    return pick(shot, ['id', 'from', 'to', 'description', 'segment_ids', 'confirmed'])
  })
}

function reviewDetails(result) {
  if (!result || typeof result !== 'object' || Array.isArray(result) || typeof result.phase !== 'string' || !Array.isArray(result.items)) return undefined
  const items = result.items.map(item => {
    if (!item || typeof item !== 'object' || Array.isArray(item)) return item
    const output = pick(item, reviewItemKeys)
    const asr = reviewSegments(item.asr_segments)
    const translated = reviewSegments(item.translated_segments)
    const translatedByLanguage = item.translated_segments_by_language && typeof item.translated_segments_by_language === 'object' && !Array.isArray(item.translated_segments_by_language)
      ? Object.fromEntries(Object.entries(item.translated_segments_by_language).map(([language, segments]) => [language, reviewSegments(segments)]))
      : undefined
    const shots = reviewShots(item.storyboard_shots)
    if (asr !== undefined) output.asr_segments = asr
    if (translated !== undefined) output.translated_segments = translated
    if (translatedByLanguage !== undefined) output.translated_segments_by_language = translatedByLanguage
    if (shots !== undefined) output.storyboard_shots = shots
    return output
  })
  return {
    phase: result.phase,
    ...(result.source_language !== undefined ? { source_language: result.source_language } : {}),
    ...(result.target_language !== undefined ? { target_language: result.target_language } : {}),
    items,
  }
}

function translationResult(base, result, expected) {
  if (!['PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'INSUFFICIENT_POINTS'].includes(base.status)) throw new VibbitError('protocol', 'Unknown translation task status', base)
  const parentFailed = ['FAILED', 'INSUFFICIENT_POINTS'].includes(base.status)
  const insufficientPointsMessage = base.status === 'INSUFFICIENT_POINTS'
    ? 'Insufficient points; check the account balance before starting another task' : undefined
  if (['PENDING', 'RUNNING'].includes(base.status)) {
    const review = reviewDetails(result)
    return {
      ok: true,
      ...base,
      ...(result !== undefined ? { result: review || result } : {}),
      review_visibility: review ? 'available' : 'unavailable',
      ...(review ? { review } : {}),
    }
  }
  if (!result || !Array.isArray(result.items) || !result.items.length) {
    if (parentFailed) return { ok: false, ...base, result, artifacts: [], delivery_kind: 'translation', failures: [{ reason: result?.error_message || insufficientPointsMessage || 'Task failed without item results' }] }
    throw new VibbitError('protocol', 'Translation completed without item results; do not claim delivery', base)
  }
  const artifacts = [], failures = [], items = []
  for (const [index, item] of result.items.entries()) {
    if (!item || typeof item !== 'object' || Array.isArray(item)) throw new VibbitError('protocol', 'Malformed translation item', base)
    const sub_task_id = item.sub_task_id === undefined ? undefined : String(item.sub_task_id)
    const identity = { item_index: index, ...(sub_task_id ? { sub_task_id } : {}) }
    const outputs = []
    if (item.status === 'COMPLETED') {
      const langs = item.results_by_language
      if (langs && typeof langs === 'object' && !Array.isArray(langs) && Object.keys(langs).length) {
        for (const [language, v] of Object.entries(langs)) {
          if (usable(v?.output_video_url)) outputs.push({ ...identity, language, kind: 'video', role: 'generated', url: v.output_video_url })
          else failures.push({ ...identity, language, reason: 'Missing final output_video_url' })
        }
      } else if (usable(item.output_video_url)) outputs.push({ ...identity, kind: 'video', role: 'generated', url: item.output_video_url })
      else failures.push({ ...identity, reason: 'Missing final output_video_url' })
    } else failures.push({ ...identity, status: item.status, reason: item.error_message || 'Item did not complete successfully' })
    artifacts.push(...outputs)
    items.push({ ...identity, status: item.status, outputs, ...(item.error_message ? { error_message: item.error_message } : {}) })
  }
  let requested_languages_checked = false
  if (expected) {
    requested_languages_checked = true
    const matched = new Set()
    for (const [index, item] of result.items.entries()) {
      const hash = typeof item.video_url === 'string' ? crypto.createHash('sha256').update(item.video_url).digest('hex') : undefined
      const candidates = expected.map((e, i) => ({ ...e, i })).filter(e => e.source_sha256 === hash)
      if (candidates.length !== 1 || matched.has(candidates[0]?.i)) {
        requested_languages_checked = false
        continue // No documented ordering guarantee; never guess by item index.
      }
      const target = candidates[0]; matched.add(target.i)
      if (item.status !== 'COMPLETED') continue
      const outputs = items[index].outputs
      if (target.languages.length === 1 && outputs.length === 1 && outputs[0].language === undefined) outputs[0].language = target.languages[0]
      for (const language of target.languages) if (!outputs.some(o => o.language === language)) failures.push({ item_index: index, language, reason: 'Requested language has no final output' })
    }
    if (result.items.length < expected.length) failures.push({ reason: 'Fewer video results than submitted items', expected: expected.length, returned: result.items.length })
    if (matched.size !== expected.length) requested_languages_checked = false
  }
  if (parentFailed) failures.push({ reason: result.error_message || insufficientPointsMessage || 'Parent translation task failed; successful final outputs are retained' })
  // Source and intermediate media stay in result, never in delivery artifacts.
  const failed = failures.length > 0 || parentFailed
  return { ok: !failed, ...base, result, items, artifacts, delivery_kind: 'translation', requested_languages_checked,
    ...(!requested_languages_checked ? { warnings: ['Requested-language coverage is not fully verified; compare the returned files with the original request.'] } : {}),
    ...(failed ? { failures, ...(artifacts.length ? { partial_failure: true } : {}) } : {}) }
}
module.exports = { translationResult, reviewDetails }
