'use strict'
const { publicUrl } = require('./media')
const { parseJson, stringifyJson } = require('./json')
const object = x => x !== null && typeof x === 'object' && !Array.isArray(x)
const assert = (v, m) => { if (!v) throw new Error(m) }
const text = (v, p, max = Infinity, blank = false) => assert(typeof v === 'string' && (blank || v.trim()) && v.length <= max, `${p} must be text of at most ${max} characters${blank ? '' : ', not blank'}`)
const number = (v, p, min = -Infinity, max = Infinity) => assert(typeof v === 'number' && Number.isFinite(v) && v >= min && v <= max, `${p} must be a finite number in ${min}..${max}`)
const bool = (v, p) => assert(typeof v === 'boolean', `${p} must be boolean`)
function long(v, p, min = 1n) {
  assert((typeof v === 'string' && /^(0|[1-9]\d{0,18})$/.test(v)) || Number.isSafeInteger(v), `${p} must be an exact decimal integer; quote large IDs`)
  assert(BigInt(v) >= min && BigInt(v) <= 9223372036854775807n, `${p} is outside the signed 64-bit range`)
}
function fields(v, allowed, p) {
  assert(object(v), `${p} must be an object`)
  for (const k of Object.keys(v)) assert(allowed.includes(k), `Undocumented ${p}.${k}`)
}
const common = ['subtitle_enabled', 'lip_sync_enabled', 'remove_subtitles_enabled', 'template_type', 'template_configs', 'subtitle_template_configs', 'settings']
function templates(v, p, inheritedType) {
  for (const k of common.slice(0, 3)) if (v[k] !== undefined) bool(v[k], `${p}.${k}`)
  assert(v.template_type !== 1 && !Object.hasOwn(v, 'subtitle_template_configs'), `${p}: dynamic subtitle templates are temporarily unavailable; use ordinary subtitles or template_type=0 packaging`)
  if (v.template_type !== undefined) assert(v.template_type === 0, `${p}.template_type must be 0 for ordinary packaging`)
  const active = []
  for (const [k, id] of [['template_configs', 'template_id'], ['subtitle_template_configs', 'subtitle_template_id']]) {
    if (v[k] === undefined) continue
    assert(Array.isArray(v[k]) && v[k].length <= 100, `${p}.${k} must be an array of at most 100 candidates`)
    if (v[k].length) active.push(k)
    v[k].forEach((c, i) => { fields(c, [id], `${p}.${k}[${i}]`); long(c[id], `${p}.${k}[${i}].${id}`) })
  }
  assert(active.length <= 1, `${p} cannot mix normal and subtitle templates`)
  const type = v.template_type ?? inheritedType
  if (active.length && type !== undefined) assert(active[0] === (type === 0 ? 'template_configs' : 'subtitle_template_configs'), `${p} template candidates do not match template_type`)
  if (v.settings !== undefined) {
    assert(object(v.settings), `${p}.settings must be an object`)
    for (const k of ['template_type', 'template_configs', 'subtitle_template_configs', 'subtitle_template_ids', 'template_name', 'subtitle_template_name', 'subtitle_template_sample_video_url', 'background', 'video', 'audio', 'subtitle_track_clips', 'watermark', 'cover', 'end_frame']) assert(!Object.hasOwn(v.settings, k), `${p}.settings cannot contain template fields`)
  }
}
function range(v, p, required) {
  if (required || v.from !== undefined) number(v.from, `${p}.from`, 0)
  if (required || v.to !== undefined) number(v.to, `${p}.to`, 0)
  if (v.from !== undefined && v.to !== undefined) assert(v.to > v.from, `${p}.to must be greater than from`)
}
function validateTranslation(input) {
  // Server defaults to manual review. Require an explicit mode to avoid unnoticed review stalls.
  bool(input.auto_translate, 'auto_translate (explicit mode required by this client)')
  for (const [k, max] of [['task_name', 200], ['source_language', 32], ['target_language', 32], ['translation_style', 64], ['default_prompt', 10000]]) if (input[k] !== undefined) text(input[k], k, max)
  for (const k of ['business_id', 'default_digital_human_id']) if (input[k] !== undefined) long(input[k], k)
  if (input.default_speed !== undefined) number(input.default_speed, 'default_speed', 0.5, 3)
  if (input.persona_mode !== undefined) assert(['voice-only', 'with-avatar'].includes(input.persona_mode), 'persona_mode must be voice-only or with-avatar')
  templates(input, 'input')
  assert(Array.isArray(input.items) && input.items.length >= 1 && input.items.length <= 100, 'items must contain 1..100 videos')
  input.items.forEach((v, i) => {
    const p = `items[${i}]`
    fields(v, [...common, 'source_video', 'material_id', 'digital_human_id', 'prompt', 'target_languages', 'voice_over_clips'], p)
    const m = v.source_video
    fields(m, ['url', 'file_name', 'file_size', 'file_type', 'mime_type', 'upload_time', 'duration', 'width', 'height', 'frame_rate', 'video_codec', 'audio_codec', 'container_format'], `${p}.source_video`)
    publicUrl(m.url, `${p}.source_video.url`)
    for (const [k, x] of Object.entries(m)) {
      if (k === 'url') continue
      if (k === 'file_size') long(x, `${p}.source_video.${k}`)
      else if (['duration', 'frame_rate', 'width', 'height'].includes(k)) {
        number(x, `${p}.source_video.${k}`, Number.MIN_VALUE)
        if (['width', 'height'].includes(k)) assert(Number.isSafeInteger(x), `${p}.${k} must be integer`)
      } else text(x, `${p}.source_video.${k}`)
    }
    for (const k of ['material_id', 'digital_human_id']) if (v[k] !== undefined) long(v[k], `${p}.${k}`)
    if (v.prompt !== undefined) text(v.prompt, `${p}.prompt`, 10000)
    if (v.target_languages !== undefined) {
      assert(Array.isArray(v.target_languages) && v.target_languages.length >= 1 && v.target_languages.length <= 16, `${p}.target_languages must contain 1..16 languages`)
      v.target_languages.forEach(x => text(x, `${p}.target_languages`, 32))
      assert(new Set(v.target_languages).size === v.target_languages.length, `${p}.target_languages contains duplicates`)
    }
    templates(v, p, input.template_type)
    if (v.voice_over_clips !== undefined) {
      assert(Array.isArray(v.voice_over_clips), `${p}.voice_over_clips must be an object array`)
      v.voice_over_clips.forEach((clip, j) => {
        const q = `${p}.voice_over_clips[${j}]`
        fields(clip, ['from', 'to', 'text', 'audio_url', 'speed', 'keep_original_voice', 'lip_sync', 'lip_sync_video_url'], q)
        range(clip, q, false)
        if (clip.text !== undefined) text(clip.text, `${q}.text`, Infinity, true)
        for (const k of ['audio_url', 'lip_sync_video_url']) if (clip[k] !== undefined && clip[k] !== '') publicUrl(clip[k], `${q}.${k}`)
        for (const k of ['keep_original_voice', 'lip_sync']) if (clip[k] !== undefined) bool(clip[k], `${q}.${k}`)
        if (clip.speed !== undefined) number(clip.speed, `${q}.speed`, Number.MIN_VALUE)
      })
    }
  })
}
function validateEdit(input) {
  long(input.sub_task_id, 'sub_task_id')
  text(input.target_language, 'target_language', 32)
  assert(input.confirmed === undefined || input.confirmed === false, 'Saving text never confirms review; omit confirmed or use false')
  assert(Array.isArray(input.segments) && input.segments.length >= 1 && input.segments.length <= 1000, 'segments must contain 1..1000 entries')
  input.segments.forEach((s, i) => {
    const p = `segments[${i}]`
    fields(s, ['id', 'from', 'to', 'source_text', 'translated_text', 'confidence', 'speaker_id', 'confirmed', 'audio_url', 'audio_duration', 'over_duration', 'audio_group_id', 'audio_fingerprint'], p)
    range(s, p, true); text(s.translated_text, `${p}.translated_text`)
    if (s.id !== undefined) long(s.id, `${p}.id`, 0n)
    if (s.speaker_id !== undefined) assert(Number.isSafeInteger(s.speaker_id), `${p}.speaker_id must be integer`)
    for (const k of ['confidence', 'audio_duration']) if (s[k] !== undefined) number(s[k], `${p}.${k}`, k === 'audio_duration' ? 0 : -Infinity)
    for (const k of ['confirmed', 'over_duration']) if (s[k] !== undefined) bool(s[k], `${p}.${k}`)
    for (const k of ['source_text', 'audio_group_id', 'audio_fingerprint']) if (s[k] !== undefined) text(s[k], `${p}.${k}`, Infinity, true)
    if (s.audio_url !== undefined && s.audio_url !== '') publicUrl(s.audio_url, `${p}.audio_url`)
  })
}
function validateConfirm(input) {
  if (input.sub_task_id !== undefined) long(input.sub_task_id, 'sub_task_id')
}
const idKeys = new Set(['business_id', 'default_digital_human_id', 'material_id', 'digital_human_id', 'template_id', 'subtitle_template_id', 'sub_task_id', 'id', 'file_size'])
function wireIntegers(value, key) {
  if (key === 'settings') return value
  if (idKeys.has(key) && value !== undefined) return BigInt(value)
  if (Array.isArray(value)) return value.map(v => wireIntegers(v))
  if (object(value)) return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, wireIntegers(v, k)]))
  return value
}
// Used for readable dry-runs: unsafe integers stay strings, body_json is the exact wire text.
const displayBody = value => parseJson(stringifyJson(value))
module.exports = { validateTranslation, validateEdit, validateConfirm, wireIntegers, displayBody, long }
