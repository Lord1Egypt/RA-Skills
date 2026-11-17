'use strict'

const { commands, models } = require('./registry')
const { publicUrl } = require('./media')
const { validateTranslation, validateEdit, validateConfirm, long } = require('./translation')
const { validateProducts } = require('./products')
const object = x => x !== null && typeof x === 'object' && !Array.isArray(x)
const assert = (condition, message) => { if (!condition) throw new Error(message) }

function validate(name, input) {
  const spec = commands[name]
  assert(spec, `Unknown command: ${name}`)
  assert(object(input), 'Input must be a JSON object')
  if (spec.defaults) input = { ...spec.defaults, ...input }
  if (name === 'gen_image' && Object.hasOwn(input, 'reference_image_url')) throw new Error('The current public image API does not define reference_image_url; do not silently discard the reference image')
  for (const key of Object.keys(input)) assert(Object.hasOwn(spec.fields, key), `Undocumented input field: ${key}`)
  for (const key of spec.required) assert(input[key] !== undefined && input[key] !== null, `Missing required field: ${key}`)
  for (const [key, value] of Object.entries(input)) {
    const type = spec.fields[key]
    if (type === 'url') publicUrl(value, key)
    else if (type === 'urls') {
      assert(Array.isArray(value) && value.length > 0, `${key} must be a nonempty URL array; omit unused arrays`)
      value.forEach((v, i) => publicUrl(v, `${key}[${i}]`))
    } else if (type === 'string') assert(typeof value === 'string' && value.trim().length > 0, `${key} must be a nonempty string`)
    else if (type === 'text') assert(typeof value === 'string', `${key} must be a string`)
    else if (type === 'id') assert((typeof value === 'string' && value.trim().length > 0) || (Number.isSafeInteger(value) && value >= 0), `${key} must be a string ID or safe integer; quote large IDs`)
    else if (type === 'ids') {
      assert(Array.isArray(value) && value.length > 0, `${key} must be a nonempty ID array`)
      value.forEach((v, i) => long(v, `${key}[${i}]`))
    }
    else if (type === 'integer') assert(Number.isSafeInteger(value), `${key} must be a safe integer`)
    else if (type === 'number') assert(typeof value === 'number' && Number.isFinite(value), `${key} must be a finite number`)
    else if (type === 'boolean') assert(typeof value === 'boolean', `${key} must be boolean`)
    else if (type === 'object') assert(object(value), `${key} must be an object`)
    else if (type === 'objects') assert(Array.isArray(value) && value.every(object), `${key} must be an object array`)
    else if (type === 'strings') assert(Array.isArray(value) && value.length > 0 && value.every(v => typeof v === 'string' && v.trim()), `${key} must be a nonempty string array`)
  }
  if (name === 'gen_image') assert(spec.models.includes(input.model), 'Unsupported image model; choose gpt-image-2, gpt-image-2.5-flare or gpt-image-2.5-sunburst')
  if (name === 'translate_video') validateTranslation(input)
  if (name === 'update_translation') validateEdit(input)
  if (name === 'confirm_translation') validateConfirm(input)
  if (name === 'breakdown') {
    assert(input.sub_tasks.every(v => ['asr', 'hot', 'transition', 'bgm'].includes(v)), 'Supported public sub_tasks: asr, hot, transition, bgm')
    assert(new Set(input.sub_tasks).size === input.sub_tasks.length, 'sub_tasks contains duplicates')
  }
  if (name === 'seedance') validateSeedance(input)
  if (name === 'generate_audio') validateAudio(input)
  if (spec.result_kind === 'product') validateProducts(name, input)
  return { spec, input, warnings: [
    ...(spec.note ? [spec.note] : []),
    ...(spec.validation === 'example_fields_only' ? ['Local checks cover the listed field types only; inspect the service response and actual output before reporting completion.'] : []),
    ...(name === 'seedance' ? ['URL syntax and reference counts are validated. Remote reachability, redirects, codec, dimensions, file size and duration are not probed.'] : []),
  ] }
}

function validateAudio(input) {
  if (input.speech_rate !== undefined) {
    assert(input.speech_rate >= -50 && input.speech_rate <= 100,
      'speech_rate must be between -50 and 100')
  }
  if (input.loudness_rate !== undefined) {
    assert(input.loudness_rate >= -50 && input.loudness_rate <= 100,
      'loudness_rate must be between -50 and 100')
  }
  if (input.pitch_rate !== undefined) {
    assert(input.pitch_rate >= -12 && input.pitch_rate <= 12,
      'pitch_rate must be between -12 and 12')
  }
  if (input.max_duration_seconds !== undefined) {
    assert(input.max_duration_seconds >= 1 && input.max_duration_seconds <= 120,
      'max_duration_seconds must be between 1 and 120')
  }
}

function validateSeedance(input) {
  const model = models[input.model]
  assert(model, 'Model is not listed in the current Vibbit contract; check the official API before adding it')
  assert(model.resolutions.includes(input.resolution), 'resolution is not supported by the selected model')
  assert(input.duration_seconds === -1 || (input.duration_seconds >= 4 && input.duration_seconds <= model.max_duration), `duration_seconds must be -1 or 4..${model.max_duration}`)
  assert(['16:9', '4:3', '1:1', '3:4', '9:16', '21:9', 'adaptive'].includes(input.aspect_ratio), 'Unsupported aspect_ratio')
  const refKeys = ['reference_image_urls', 'reference_video_urls', 'reference_audio_urls']
  const refs = refKeys.map(key => input[key] || [])
  refs.forEach((arr, i) => assert(arr.length <= model.references[i], `${refKeys[i]} exceeds model maximum ${model.references[i]}`))
  const hasRefs = refs.some(arr => arr.length)
  assert([!!input.image_url, !!(input.first_frame_image_url || input.last_frame_image_url), hasRefs].filter(Boolean).length <= 1, 'Single image, first/last frame and reference arrays are mutually exclusive')
  assert(!input.last_frame_image_url || input.first_frame_image_url, 'last_frame_image_url requires first_frame_image_url')
  const seenRoles = new Map()
  for (const key of [...refKeys, 'image_url', 'first_frame_image_url', 'last_frame_image_url']) {
    for (const url of Array.isArray(input[key]) ? input[key] : input[key] ? [input[key]] : []) {
      assert(!seenRoles.has(url) || seenRoles.get(url) === key, 'Duplicate media URL across input roles')
      seenRoles.set(url, key)
    }
  }
  const is25 = input.model === 'doubao-seedance-2-5-260628'
  assert(is25 || !refs[2].length || refs[0].length || refs[1].length, 'Seedance 2.0 audio references require an image or video reference')
  const mode = input.omni_reference_task_type
  if (mode !== undefined) {
    assert(is25, 'omni_reference_task_type applies only to Seedance 2.5')
    assert(['auto', 'reference', 'edit', 'extend'].includes(mode), 'Invalid omni_reference_task_type')
    assert(hasRefs && !input.image_url && !input.first_frame_image_url, 'Explicit omni mode requires reference_* media only')
    if (['edit', 'extend'].includes(mode)) assert(refs[1].length, `${mode} requires a reference video`)
    if (['auto', 'edit', 'extend'].includes(mode)) assert(input.aspect_ratio === 'adaptive', `${mode} requires aspect_ratio=adaptive`)
    if (['auto', 'edit'].includes(mode)) assert(input.duration_seconds === -1, `${mode} requires duration_seconds=-1`)
  }
  // Model-specific requirement from the official 2.5 prompting guide.
  if (is25 && input.first_frame_image_url) assert(input.aspect_ratio === 'adaptive', 'Seedance 2.5 first/last frame mode requires adaptive ratio (official model guide)')
}

module.exports = { validate, validateSeedance }
