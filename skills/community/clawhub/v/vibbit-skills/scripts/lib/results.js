'use strict'

const { VibbitError } = require('./client')
const { parseJson } = require('./json')
const { translationResult } = require('./translation-results')
const { previewUrl, avatarPreviews } = require('./preview')
const { productOutcome } = require('./products')
const { sourceContent, projectVideoResults, retainSource } = require('./external-content')

function decode(value) {
  if (typeof value !== 'string') return value
  try { return parseJson(value) } catch { return value }
}

function parseResult(taskResult) {
  if (!taskResult || !Object.hasOwn(taskResult, 'result')) return undefined
  const result = decode(taskResult.result)
  if (result && typeof result === 'object' && Array.isArray(result.sub_results)) {
    return { ...result, sub_results: result.sub_results.map(row => ({ ...row, result: decode(row.result) })) }
  }
  return result
}

const usableUrl = x => typeof x === 'string' && /^https?:\/\//i.test(x)
function artifacts(result, kind) {
  const output = []
  const add = (type, url, role = kind === 'project' ? 'project' : ['image', 'video', 'audio'].includes(kind) ? 'generated' : 'reference') => {
    if (usableUrl(url) && !output.some(row => row.url === url && row.kind === type && row.role === role)) {
      const preview = type === 'image' ? previewUrl(url) : url
      output.push({ kind: type, role, url, ...(preview !== url ? { preview_url: preview } : {}) })
    }
  }
  if (kind === 'project' && typeof result === 'string') add('project', result)
  if (kind === 'image' && typeof result === 'string') add('image', result)
  const visit = (value, depth = 0) => {
    if (depth > 6 || !value || typeof value !== 'object') return
    if (Array.isArray(value)) {
      for (const item of value) {
        if (kind === 'image' && typeof item === 'string') add('image', item)
        else visit(item, depth + 1)
      }
      return
    }
    for (const [key, data] of Object.entries(value)) {
      const type = { video_url: 'video', audio_url: 'audio', image_url: 'image', image_urls: 'image', project_url: 'project',
        ...(kind === 'analysis' ? { videoUrls: 'video', coverUrls: 'image', pics: 'image' } : {}),
      }[key]
      if (type) for (const url of Array.isArray(data) ? data : [data]) {
        const role = kind === 'analysis' ? type === 'video' ? depth === 0 ? 'source' : 'analysis_segment' : 'reference' : undefined
        add(type, url, role)
      }
      else if (key === 'url' && ['image', 'project'].includes(kind)) add(kind, data)
      else if (typeof data === 'object') visit(data, depth + 1)
    }
  }
  visit(result)
  return output
}

function normalize(data, spec = {}) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) throw new VibbitError('protocol', 'Unexpected task response shape')
  const result = parseResult(data.task_result)
  const status = data.status || (result !== undefined && result !== null ? 'COMPLETED' : data.task_id ? 'PENDING' : undefined)
  const base = { task_id: data.task_id, request_id: data.request_id, status,
    ...(data.task_info?.task_type ? { task_type: data.task_info.task_type } : {}),
    ...(typeof data.progress_percent === 'number' ? { progress_percent: data.progress_percent } : {}),
  }
  if (spec.result_kind === 'translation' || data.task_info?.task_type === 'VIDEO_VOICE_OVER_TASK') return translationResult(base, result, spec.expected_targets)
  if (['FAILED', 'INSUFFICIENT_POINTS'].includes(status)) {
    const fallback = status === 'INSUFFICIENT_POINTS'
      ? 'Insufficient points; check the account balance before starting another task'
      : 'Task failed; query the request ID with Vibbit support'
    throw new VibbitError('task_failed', result?.error_message || fallback, base)
  }
  if (!['PENDING', 'RUNNING', 'COMPLETED'].includes(status)) throw new VibbitError('protocol', 'Task response has an unknown or missing status; do not resubmit', base)
  if (status === 'COMPLETED' && (result === undefined || result === null)) throw new VibbitError('protocol', 'Task reports completion without a result; do not claim delivery', base)
  const media = status === 'COMPLETED' ? artifacts(result, spec.result_kind) : []
  const previews = status === 'COMPLETED' && (spec.task_type || data.task_info?.task_type) === 'QUERY_DIGITAL_HUMAN_LIST'
    ? avatarPreviews(result) : []
  const partial = Array.isArray(result?.sub_results) && result.sub_results.some(row => row.status && !['GENERATED', 'COMPLETED', 'SUCCESS'].includes(row.status))
  const product = status === 'COMPLETED' && spec.result_kind === 'product'
    ? productOutcome(result, spec.task_type || data.task_info?.task_type) : {}
  return {
    ok: true, ...base, ...(result !== undefined ? { result } : {}),
    ...(result !== undefined && sourceContent(spec.task_type || base.task_type)
      ? { source_content: sourceContent(spec.task_type || base.task_type) } : {}),
    ...(status === 'COMPLETED' ? {
      artifacts: media,
      ...(previews.length ? { previews } : {}),
      delivery_kind: spec.result_kind || (media.length ? 'media' : 'structured_result'),
      ...(partial ? { partial_failure: true } : {}),
      ...product,
    } : {}),
  }
}

async function normalizeResponse(data, spec = {}, sourceFile) {
  const output = normalize(data, spec)
  if (output.status !== 'COMPLETED' || output.source_content?.task_type !== 'GOOGLE_SHORT_VIDEO_SEARCH') return output
  const projection = projectVideoResults(output.result)
  if (!projection) return { ...output, source_content: { ...output.source_content, projection: 'unrecognized_shape' } }
  let fullResultFile
  if (projection.changed) {
    try { fullResultFile = await retainSource(sourceFile, output.result, output.source_content.task_type) } catch {
      // Do not discard needed facts or repeat a search because local retention failed.
      return { ...output, source_content: { ...output.source_content, projection_fallback: 'source_record_unavailable' } }
    }
  }
  const { result, changed, ...counts } = projection
  return { ...output, result, artifacts: artifacts(result, spec.result_kind), source_content: { ...output.source_content,
    projection: 'documented_video_fields', ...counts,
    ...(fullResultFile ? { full_result_file: fullResultFile } : {}),
  } }
}

module.exports = { parseResult, artifacts, normalize, normalizeResponse }
