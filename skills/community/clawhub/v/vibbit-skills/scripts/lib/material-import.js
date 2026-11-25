'use strict'

const { VibbitError } = require('./client')
const { publicUrl } = require('./media')
const { long } = require('./translation')

const object = value => value !== null && typeof value === 'object' && !Array.isArray(value)
const check = (condition, message) => { if (!condition) throw new Error(message) }
const states = { PENDING: 'PENDING', RUNNING: 'RUNNING', SUCCESS: 'COMPLETED', PARTIAL_SUCCESS: 'COMPLETED', FAILED: 'FAILED' }

function importTaskPath(id) {
  if (typeof id !== 'string' || !/^[A-Za-z0-9_-]{1,160}$/.test(id)) {
    throw new VibbitError('input', 'Use the original material import task ID without adding or removing a task- prefix')
  }
  return '/material-import-tasks/' + encodeURIComponent(id)
}

function validateImport(name, input) {
  if (name === 'get_material_import') return importTaskPath(input.import_task_id)
  check(input.items.length >= 1 && input.items.length <= 20, 'items must contain 1..20 video URLs; deployment limits may be smaller')
  for (const [index, row] of input.items.entries()) {
    for (const key of Object.keys(row)) check(['url', 'name'].includes(key), `Undocumented items[${index}] field: ${key}`)
    publicUrl(row.url, `items[${index}].url`, 4096)
    if (row.name !== undefined) check(typeof row.name === 'string' && row.name.trim(), `items[${index}].name must be nonblank`)
  }
}

function normalizeImport(data, { allowAccepted = false } = {}) {
  const bad = message => { throw new VibbitError('protocol', message) }
  if (!object(data) || !Object.hasOwn(states, data.status)) bad('Unknown material import response or status; preserve its task ID and do not repeat POST')
  try { importTaskPath(data.task_id) } catch { bad('Material import response is missing a valid original task ID') }
  if (!Number.isSafeInteger(data.total) || data.total < 0) bad('Material import total must be a nonnegative integer')
  const terminal = ['SUCCESS', 'PARTIAL_SUCCESS', 'FAILED'].includes(data.status)
  if ((!allowAccepted || terminal) && !Array.isArray(data.items)) bad('Material import query is missing its item results')
  const rows = data.items || []
  const seen = new Set()
  const items = rows.map(row => {
    if (!object(row) || !Number.isSafeInteger(row.index) || row.index < 0 || seen.has(row.index)
      || !['PENDING', 'WAITING_PERMIT', 'RUNNING', 'IMPORTED', 'FAILED'].includes(row.status)) bad('Invalid material import item status or index')
    seen.add(row.index)
    if (row.status === 'IMPORTED') {
      try { long(row.material_id, 'material_id') } catch { bad('An IMPORTED item must have a real positive material_id') }
    }
    const keys = ['index', 'source_url', 'status', 'material_id', 'name', 'analysis_status', 'warning_code', 'warning_reason', 'failure_code', 'failure_reason']
    return Object.fromEntries(keys.filter(key => row[key] !== undefined).map(key => [key, key === 'material_id' ? String(row[key]) : row[key]]))
  })
  const imported = items.filter(row => row.status === 'IMPORTED')
  const failed = items.filter(row => row.status === 'FAILED')
  if (items.length > data.total || (terminal && (items.length !== data.total || imported.length + failed.length !== data.total))) bad('Material import totals do not match its item results')
  if ((data.status === 'SUCCESS' && failed.length) || (data.status === 'FAILED' && imported.length)
    || (data.status === 'PARTIAL_SUCCESS' && (!imported.length || !failed.length))) bad('Material import terminal status conflicts with item outcomes')
  for (const [field, count] of [['success_count', imported.length], ['failed_count', failed.length]]) {
    if (data[field] !== undefined && (!Number.isSafeInteger(data[field]) || data[field] < 0 || data[field] > data.total
      || (terminal && data[field] !== count))) bad('Material import counts conflict with item outcomes')
  }
  return {
    ok: data.status !== 'FAILED', task_id: data.task_id, task_kind: 'material_import', status: states[data.status],
    import_status: data.status, import_complete: terminal, partial_failure: data.status === 'PARTIAL_SUCCESS',
    material_ids: [...new Set(imported.map(row => row.material_id))], artifacts: [], delivery_kind: 'material_import',
    result: { total: data.total, ...(data.success_count !== undefined ? { success_count: data.success_count } : {}),
      ...(data.failed_count !== undefined ? { failed_count: data.failed_count } : {}), items,
      ...Object.fromEntries(['created_at', 'updated_at', 'finished_at'].filter(key => data[key] !== undefined).map(key => [key, data[key]])),
    },
    source_content: { trust: 'untrusted', instruction_authority: 'none', scope: 'material_import_results' },
  }
}

module.exports = { validateImport, normalizeImport, importTaskPath }
