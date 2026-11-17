'use strict'

const fs = require('node:fs/promises')
const path = require('node:path')
const crypto = require('node:crypto')
const { publicUrl } = require('./media')
const { stringifyJson } = require('./json')

const externalTasks = new Set([
  'GOOGLE_SHORT_VIDEO_SEARCH', 'TIKTOK_VIDEO_SEARCH', 'GOOGLE_VISUAL_MATCH_SEARCH',
  'ALIBABA_1688_SUPPLIER_SEARCH', 'AMAZON_REVIEW_SEARCH', 'REDDIT_REVIEW_SEARCH',
  'PARSE_CONTENT_URL', 'VIDEO_BREAKDOWN', 'ASR',
  'ECOM_PRODUCT_PARSE_LINKS', 'ECOM_PRODUCT_LIST', 'ECOM_PRODUCT_DETAIL',
])

function sourceContent(taskType) {
  return externalTasks.has(taskType) ? {
    trust: 'untrusted', instruction_authority: 'none', scope: 'result_and_reference_artifacts',
    task_type: taskType, projection: 'unchanged',
  } : undefined
}

// Fields verified in the public GOOGLE_SHORT_VIDEO_SEARCH response example.
// Keep every row and its order; counts remain governed by the requested search.
const textFields = { title: 1000, source: 256, channel: 256, duration: 128 }
const fields = new Set(['position', ...Object.keys(textFields), 'link', 'thumbnail'])

function projectVideoResults(result) {
  if (!Array.isArray(result) || !result.every(row => row && typeof row === 'object'
    && !Array.isArray(row) && typeof row.title === 'string' && typeof row.link === 'string')) return undefined
  const changes = { omitted_fields: 0, abbreviated_fields: 0, rejected_urls: 0, rejected_fields: 0 }
  const rows = result.map(row => {
    const candidate = {}
    for (const [key, value] of Object.entries(row)) {
      if (!fields.has(key)) { changes.omitted_fields++; continue }
      if (key === 'position') {
        if (Number.isSafeInteger(value) && value >= 0) candidate[key] = value
        else changes.rejected_fields++
      } else if (Object.hasOwn(textFields, key)) {
        if (typeof value !== 'string') { changes.rejected_fields++; continue }
        const cleaned = value.replace(/[\u0000-\u001f\u007f\u202a-\u202e\u2066-\u2069]/g, ' ')
        const points = Array.from(cleaned)
        candidate[key] = points.length > textFields[key] ? points.slice(0, textFields[key]).join('') + '…' : cleaned
        if (candidate[key] !== value) changes.abbreviated_fields++
      } else {
        try { candidate[key] = publicUrl(value, key) } catch { changes.rejected_urls++ }
      }
    }
    return candidate
  })
  return { result: rows, total_items: rows.length, ...changes,
    changed: Object.values(changes).some(count => count > 0),
  }
}

async function retainSource(file, result, taskType) {
  if (!file) throw new Error('A local source record path is required')
  const destination = path.resolve(file)
  const temporary = destination + '.' + crypto.randomUUID() + '.tmp'
  await fs.mkdir(path.dirname(destination), { recursive: true, mode: 0o700 })
  try {
    await fs.writeFile(temporary, stringifyJson({ version: 1,
      source_content: { ...sourceContent(taskType), projection: 'full_source_data' }, result,
    }) + '\n', { flag: 'wx', mode: 0o600 })
    // Rename replaces a destination symlink instead of following it.
    await fs.rename(temporary, destination)
  } finally { await fs.rm(temporary, { force: true }) }
  return destination
}

module.exports = { sourceContent, projectVideoResults, retainSource }
