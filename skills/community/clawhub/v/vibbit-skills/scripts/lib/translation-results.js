'use strict'
const { VibbitError } = require('./client')
const crypto = require('node:crypto')
const usable = v => {
  if (typeof v !== 'string') return false
  try { const u = new URL(v); return ['http:', 'https:'].includes(u.protocol) && !u.username && !u.password } catch { return false }
}

const reviewSegmentKeys = ['id', 'from', 'to', 'source_text', 'translated_text', 'confidence', 'speaker_id', 'confirmed', 'lip_sync', 'audio_url', 'audio_duration', 'over_duration', 'audio_group_id']
const reviewItemKeys = ['sub_task_id', 'status', 'source_video_url', 'video_url', 'target_languages', 'voice_reference_audio_url', 'output_video_url', 'error_message']

function pick(source, keys) {
  return Object.fromEntries(keys.filter(key => source?.[key] !== undefined).map(key => [key, source[key]]))
}

function defaultVoice(value) {
  // Missing fields remain missing on older service responses. Never treat a source
  // voice-reference URL as a replacement binding or expose arbitrary server fields.
  if (value === null) return null
  if (value && typeof value === 'object' && !Array.isArray(value) && usable(value.reference_audio_url)) {
    return { reference_audio_url: value.reference_audio_url }
  }
  return undefined
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

function mapValues(value, transform) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return undefined
  return Object.fromEntries(Object.entries(value).map(([key, row]) => [key, transform(row)]))
}

function sentences(value) {
  if (!Array.isArray(value)) return undefined
  return value.map(sentence => ({
    ...pick(sentence, ['text', 'begin_time', 'end_time', 'sentence_id', 'language', 'emotion', 'speaker_id']),
    ...(Array.isArray(sentence?.words) ? { words: sentence.words.map(word => pick(word, ['text', 'punctuation', 'begin_time', 'end_time'])) } : {}),
  }))
}

function languageResult(value) {
  const out = pick(value, ['output_video_url', 'translated_video_url', 'no_subtitle_video_url', 'lip_sync_video_url', 'audio_url'])
  if (Array.isArray(value?.voice_over_clips)) out.voice_over_clips = value.voice_over_clips.map(clip => pick(clip, ['from', 'to', 'text', 'audio_url', 'speed', 'keep_original_voice', 'lip_sync', 'lip_sync_video_url']))
  if (Array.isArray(value?.subtitle_asr_sentences)) out.subtitle_asr_sentences = sentences(value.subtitle_asr_sentences)
  if (Array.isArray(value?.translated_segments_snapshot)) out.translated_segments_snapshot = reviewSegments(value.translated_segments_snapshot)
  return out
}

function publicResult(result) {
  if (!result || typeof result !== 'object' || Array.isArray(result) || !Array.isArray(result.items)) return undefined
  const items = result.items.map(item => {
    if (!item || typeof item !== 'object' || Array.isArray(item)) return item
    const output = pick(item, reviewItemKeys)
    const voice = defaultVoice(item.default_voice)
    if (voice !== undefined) output.default_voice = voice
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
    if (Array.isArray(item.speaker_voice_mappings)) output.speaker_voice_mappings = item.speaker_voice_mappings.map(mapping => pick(mapping, ['speaker_id', 'audio_id', 'reference_audio_url']))
    if (item.resynthesis_by_language) output.resynthesis_by_language = mapValues(item.resynthesis_by_language, receipt => pick(receipt, ['request_id', 'status', 'error_message']))
    if (item.results_by_language) output.results_by_language = mapValues(item.results_by_language, languageResult)
    return output
  })
  return {
    ...pick(result, ['phase', 'source_language', 'target_language', 'error_message']),
    ...(defaultVoice(result.default_voice) !== undefined ? { default_voice: defaultVoice(result.default_voice) } : {}),
    items,
  }
}

function reviewDetails(result) {
  return typeof result?.phase === 'string' ? publicResult(result) : undefined
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
      ...(result !== undefined ? { result: review || publicResult(result) || result } : {}),
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
          if (usable(v?.output_video_url)) {
            outputs.push({ ...identity, language, kind: 'video', role: 'generated', url: v.output_video_url })
            if (usable(v.no_subtitle_video_url) && v.no_subtitle_video_url !== v.output_video_url) outputs.push({ ...identity, language, kind: 'video', role: 'generated', variant: 'no_subtitles', url: v.no_subtitle_video_url })
          }
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
      const source = item.source_video_url || item.video_url
      const hash = typeof source === 'string' ? crypto.createHash('sha256').update(source).digest('hex') : undefined
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
  const review = reviewDetails(result)
  return { ok: !failed, ...base, result: publicResult(result), ...(review ? { review, review_visibility: 'available' } : {}), items, artifacts, delivery_kind: 'translation', requested_languages_checked,
    ...(!requested_languages_checked ? { warnings: ['Requested-language coverage is not fully verified; compare the returned files with the original request.'] } : {}),
    ...(failed ? { failures, ...(artifacts.length ? { partial_failure: true } : {}) } : {}) }
}

function translationAction(output, context) {
  if (!context) return output
  const previous = output.artifacts?.length ? output.artifacts : (output.result?.items || []).flatMap(item =>
    Object.entries(item.results_by_language || {}).filter(([, result]) => usable(result?.output_video_url)).map(([language, result]) => ({
      sub_task_id: String(item.sub_task_id), language, kind: 'video', role: 'generated', url: result.output_video_url,
    })))
  const common = { ...output, operation: context.operation, parent_status: output.status,
    operation_context: context, artifacts: [], ...(previous.length ? { previous_artifacts: previous } : {}), delivery_current: false }
  if (context.operation !== 'resynthesize_language') return {
    ...common, operation_status: 'ACKNOWLEDGED', render_performed: false,
  }
  const item = output.result?.items?.find(row => String(row?.sub_task_id) === context.sub_task_id)
  const receipt = item?.resynthesis_by_language?.[context.target_language]
  if (!receipt || receipt.request_id !== context.request_id) {
    if (['FAILED', 'INSUFFICIENT_POINTS'].includes(output.status)) return { ...common, ok: false, operation_status: 'UNCONFIRMED' }
    return { ...common, ok: true, status: 'RUNNING', operation_status: 'AWAITING_RECEIPT', partial_failure: false }
  }
  if (!['PENDING', 'RUNNING', 'COMPLETED', 'FAILED'].includes(receipt.status)) throw new VibbitError('protocol', 'Unknown language resynthesis receipt status', { task_id: output.task_id })
  if (receipt.status === 'FAILED') return { ...common, ok: false, status: 'FAILED', operation_status: 'FAILED', partial_failure: false,
    failures: [{ sub_task_id: context.sub_task_id, language: context.target_language, request_id: context.request_id, reason: receipt.error_message || 'Language resynthesis failed; the previous delivery is preserved' }] }
  if (receipt.status !== 'COMPLETED') return { ...common, ok: true, status: receipt.status, operation_status: receipt.status, partial_failure: false }
  const final = item.results_by_language?.[context.target_language]
  if (!usable(final?.output_video_url)) throw new VibbitError('protocol', 'Language resynthesis completed without its final output_video_url', { task_id: output.task_id })
  const artifacts = [{ sub_task_id: context.sub_task_id, language: context.target_language, kind: 'video', role: 'generated', url: final.output_video_url }]
  if (usable(final.no_subtitle_video_url) && final.no_subtitle_video_url !== final.output_video_url) artifacts.push({ sub_task_id: context.sub_task_id, language: context.target_language, kind: 'video', role: 'generated', variant: 'no_subtitles', url: final.no_subtitle_video_url })
  const { previous_artifacts, ...delivered } = common
  return { ...delivered, ok: true, status: 'COMPLETED', operation_status: 'COMPLETED', delivery_current: true, artifacts,
    failures: [], partial_failure: false, requested_languages_checked: true,
    warnings: (output.warnings || []).filter(value => !value.startsWith('Requested-language coverage')) }
}
module.exports = { translationResult, reviewDetails, translationAction }
