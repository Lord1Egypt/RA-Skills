'use strict'

const { VibbitError } = require('./client')
const { long } = require('./translation')

const object = value => value !== null && typeof value === 'object' && !Array.isArray(value)
const check = (condition, message) => { if (!condition) throw new Error(message) }
const pick = (value, keys) => Object.fromEntries(keys.filter(key => value[key] !== undefined).map(key => [key, value[key]]))
const mediaTypes = ['VIDEO', 'IMAGE', 'AUDIO']

function validateMaterials(name, input) {
  for (const key of ['page', 'segment_page']) if (input[key] !== undefined) check(input[key] >= 1, `${key} starts at 1`)
  for (const key of ['page_size', 'segment_page_size', 'top_k']) {
    if (input[key] !== undefined) check(input[key] >= 1 && input[key] <= 100, `${key} must be 1..100`)
  }
  for (const [key, values] of Object.entries({ media_type: mediaTypes, tag_match_mode: ['AND', 'OR'],
    category: ['ROLE', 'SCENE', 'PROP'], classification_source: ['ANY', 'AI', 'MANUAL'] })) {
    if (input[key] !== undefined) check(values.includes(input[key]), `Unsupported ${key}`)
  }
  if (input.media_types !== undefined) check(input.media_types.every(type => mediaTypes.includes(type)), 'Unsupported media_types value')
  if (input.tag_names !== undefined) {
    check(input.tag_names.length <= 50 && input.tag_names.every(tag => tag.trim()), 'tag_names must contain at most 50 nonblank names')
    if (new Set(input.tag_names).size >= 2) check(input.tag_match_mode !== undefined, 'tag_match_mode is required for two or more distinct tags')
  }
  if (name === 'search_materials') check(input.query.length <= 2000, 'query must be at most 2000 characters')
  if (name === 'get_material') long(input.material_id, 'material_id')
  if (name === 'batch_get_materials') check(input.material_ids.length <= 100, 'material_ids accepts 1..100 IDs before deduplication')
}

function materialRequest(spec, input) {
  if (spec.method === 'POST') return { method: 'POST', route: spec.endpoint,
    body: spec.material_operation === 'batch' ? { material_ids: input.material_ids.map(String) } : input }
  const query = new URLSearchParams()
  for (const [key, value] of Object.entries(input)) {
    if (key === 'material_id') continue
    for (const item of Array.isArray(value) ? value : [value]) query.append(key, String(item))
  }
  const route = spec.material_operation === 'detail' ? '/materials/' + encodeURIComponent(String(input.material_id)) : spec.endpoint
  return { method: 'GET', route: route + (query.toString() ? '?' + query.toString() : '') }
}

function normalizeMaterials(spec, data, input) {
  const fail = message => { throw new VibbitError('protocol', message) }
  const requireObject = (value, label) => { if (!object(value)) fail(`${label} must be an object`) }
  const id = (value, label) => {
    try { long(value, label) } catch { fail(`${label} must be an exact positive material ID`) }
    return String(value)
  }
  const page = (value, expectedPage, expectedSize, normalizeItem) => {
    requireObject(value, 'Material page')
    if (!Array.isArray(value.items)) fail('Material page is missing items')
    try { long(value.total, 'total', 0n) } catch { fail('Material page total must be an exact nonnegative integer') }
    if (value.page !== expectedPage || value.page_size !== expectedSize) fail('Material pagination differs from the requested page')
    if (value.items.length > expectedSize || BigInt(value.total) < BigInt(value.items.length)) fail('Material page counts are inconsistent')
    return { items: value.items.map(normalizeItem), total: String(value.total), page: value.page, page_size: value.page_size,
      has_more: BigInt(value.total) > BigInt(value.page) * BigInt(value.page_size) }
  }
  const grouped = (value, label) => {
    requireObject(value, label)
    for (const key of ['AI', 'MANUAL']) if (!Array.isArray(value[key]) || !value[key].every(item => typeof item === 'string')) fail(`${label}.${key} must be a string array`)
    return { AI: value.AI, MANUAL: value.MANUAL }
  }
  const summary = value => {
    requireObject(value, 'Material summary')
    if (typeof value.material_name !== 'string' || !mediaTypes.includes(value.media_type)
      || typeof value.analysis_status !== 'string' || !value.analysis_status) fail('Material summary is missing name, media type or analysis status')
    return { material_id: id(value.material_id, 'material_id'),
      ...pick(value, ['material_name', 'media_type', 'collection_name', 'description', 'cover_url', 'analysis_status']),
      tags: grouped(value.tags, 'tags'), classifications: grouped(value.classifications, 'classifications') }
  }
  const segment = value => {
    requireObject(value, 'Material segment')
    for (const key of ['start_time', 'end_time']) {
      if (value[key] !== undefined && (typeof value[key] !== 'number' || !Number.isFinite(value[key]) || value[key] < 0)) fail('Material segment times must be nonnegative seconds')
    }
    if (value.start_time !== undefined && value.end_time !== undefined && value.end_time < value.start_time) fail('Material segment end precedes start')
    // caption can be JSON text. Keep it as source data, without interpreting it.
    return pick(value, ['segment_id', 'scene_id', 'start_time', 'end_time', 'content', 'caption', 'transcript', 'url'])
  }
  requireObject(data, 'Material response')
  if (spec.material_operation === 'detail') {
    const result = summary(data)
    if (result.material_id !== String(input.material_id)) fail('Returned material ID differs from the requested ID')
    requireObject(data.file_info, 'file_info')
    result.file_info = pick(data.file_info, ['file_name', 'file_size', 'file_type', 'mime_type', 'url', 'upload_time', 'duration',
      'width', 'height', 'frame_rate', 'video_codec', 'audio_codec', 'container_format'])
    if (data.analysis_failure_reason !== undefined) result.analysis_failure_reason = data.analysis_failure_reason
    if (data.analysis !== undefined) {
      requireObject(data.analysis, 'analysis')
      result.analysis = pick(data.analysis, ['description', 'summary', 'transcript'])
      if (data.analysis.scenes !== undefined) {
        if (!Array.isArray(data.analysis.scenes)) fail('analysis.scenes must be an array')
        result.analysis.scenes = data.analysis.scenes.map(scene => {
          requireObject(scene, 'Scene')
          return { ...pick(scene, ['scene_id', 'start_time', 'end_time', 'description']),
            ...(scene.segments !== undefined ? { segments: page(scene.segments, input.segment_page ?? 1, input.segment_page_size ?? 20, segment) } : {}) }
        })
      }
      if (data.analysis.contents !== undefined) {
        if (!Array.isArray(data.analysis.contents)) fail('analysis.contents must be an array')
        result.analysis.contents = data.analysis.contents.map(value => typeof value === 'string' ? value : segment(value))
      }
    }
    return result
  }
  if (!Array.isArray(data.items)) fail('Material response is missing items')
  let result
  if (spec.material_operation === 'list') result = page(data, input.page ?? 1, input.page_size ?? 20, summary)
  else if (spec.material_operation === 'batch') {
    const requested = [...new Set(input.material_ids.map(String))]
    let previous = -1
    const items = data.items.map(value => {
      const item = summary(value), index = requested.indexOf(item.material_id)
      if (index < 0 || index <= previous) fail('Batch response contains unrequested, duplicate or out-of-order material IDs')
      previous = index
      return item
    })
    const found = new Set(items.map(item => item.material_id))
    result = { items, missing_material_ids: requested.filter(value => !found.has(value)) }
  } else {
    if (data.items.length > (input.top_k ?? 20)) fail('Material search exceeds the requested top_k')
    result = { items: data.items.map(value => {
      const item = summary(value)
      if (typeof value.score !== 'number' || !Number.isFinite(value.score) || !Array.isArray(value.matches) || value.matches.length > 20) fail('Material search result has invalid score or matches')
      return { ...item, score: value.score, matches: value.matches.map(segment) }
    }) }
  }
  if (new Set(result.items.map(item => item.material_id)).size !== result.items.length) fail('Duplicate material IDs in response')
  return result
}

async function readMaterials(client, spec, input) {
  const request = materialRequest(spec, input)
  try {
    const data = await client.request(request.method, request.route, request.body)
    return { ok: true, read_only: true, status: 'COMPLETED', delivery_kind: 'material_query', artifacts: [],
      account_base: client.base, result: normalizeMaterials(spec, data, input),
      source_content: { trust: 'untrusted', instruction_authority: 'none', scope: 'material_query_results' } }
  } catch (error) {
    // batchGet and search use POST, but neither creates a task or changes a resource.
    error.ambiguous = false
    error.read_only = true
    throw error
  }
}

module.exports = { validateMaterials, materialRequest, normalizeMaterials, readMaterials }
