'use strict'

const fs = require('node:fs/promises')
const path = require('node:path')
const crypto = require('node:crypto')
const { publicUrl } = require('./media')

const success = status => !status || ['COMPLETED', 'GENERATED', 'SUCCESS'].includes(status)
function materialId(value) {
  const text = Number.isSafeInteger(value) ? String(value) : value
  return typeof text === 'string' && /^[1-9]\d{0,18}$/.test(text) && BigInt(text) <= 9223372036854775807n ? text : undefined
}

function generatedImages(result) {
  const entries = []
  const add = (url, id) => {
    try { publicUrl(url, 'generated image', 4096) } catch { return }
    const existing = entries.find(entry => entry.source_url === url)
    if (existing) {
      if (!existing.reported_material_id && materialId(id)) existing.reported_material_id = materialId(id)
    } else entries.push({ source_url: url,
      ...(materialId(id) ? { reported_material_id: materialId(id) } : {}) })
  }
  const visit = (value, depth = 0) => {
    if (depth > 3) return
    if (typeof value === 'string') { add(value); return }
    if (Array.isArray(value)) { for (const image of value) visit(image, depth + 1); return }
    if (!value || typeof value !== 'object' || !success(value.status)) return
    const urls = [value.image_url, ...(Array.isArray(value.image_urls) ? value.image_urls : [])]
      .filter(url => typeof url === 'string')
    if (urls.length) for (const url of urls) add(url, urls.length === 1 ? value.material_id : undefined)
    // Only explicit output containers, never reference URLs, snapshots, covers or prompts.
    if (Array.isArray(value.images)) for (const row of value.images) {
      if (typeof row === 'string') add(row)
      else if (row && success(row.status)) add(row.image_url || row.url, row.material_id)
    }
    if (Array.isArray(value.sub_results)) for (const row of value.sub_results) {
      if (row && success(row.status)) visit(row.result, depth + 1)
    }
  }
  visit(result)
  return entries
}

function archiveSummary(items) {
  const registered = items.filter(item => item.status === 'registered').length
  const status = registered === items.length && items.length ? 'registered'
    : registered ? 'partially_registered'
      : items.some(item => item.reported_material_id) ? 'pending_verification' : 'pending_registration'
  return { status, library_registered: !!items.length && registered === items.length,
    registered_count: registered, pending_count: items.length - registered, items }
}

function imageArchive(output, policy = 'default') {
  if (output.status !== 'COMPLETED') return undefined
  if (policy === 'skip') return { status: 'skipped', library_registered: false,
    note: 'Image library archiving was explicitly skipped. Existing cloud assets are not deleted.' }
  const images = generatedImages(output.result)
  if (!images.length) return { status: 'unrecognized_result', library_registered: false, items: [],
    note: 'No documented generated-image output was identified; preserve the result without inventing library registration.' }
  const items = images.map((image, index) => ({ ...image, index,
    name: `Generated image ${output.task_id || 'result'} #${index + 1}`,
    status: image.reported_material_id ? 'pending_verification' : 'pending_registration',
  }))
  return { ...archiveSummary(items), analysis_requested: false,
    registration_api_available: false,
    note: 'Image generation and OSS URLs do not prove library registration. Reuse only verified existing image material IDs. The current public API has no general image-registration operation; retain pending entries without sending images to video import or regenerating them.' }
}

function archiveRequest(value = {}) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Image archive options must be an object')
  for (const key of Object.keys(value)) if (!['name', 'collection_name'].includes(key)) throw new Error('Unknown image archive option')
  for (const [key, text] of Object.entries(value)) {
    if (typeof text !== 'string' || !text.trim() || text.length > 200) throw new Error(`Image archive ${key} must be nonblank text of at most 200 characters`)
  }
  return value
}

async function retainImageArchive(output, { client, file, request = {}, budgetMs } = {}) {
  if (!output.image_archive || ['skipped', 'unrecognized_result'].includes(output.image_archive.status)) return output
  const original = output.image_archive
  let previous
  try {
    archiveRequest(request)
    if (file) {
      try {
        const stat = await fs.lstat(file)
        if (!stat.isFile() || stat.isSymbolicLink() || stat.size > 8 * 1024 * 1024 ||
          (process.platform !== 'win32' && (stat.mode & 0o077))) throw new Error('Existing image archive record is not private')
        previous = JSON.parse(await fs.readFile(file, 'utf8'))
        if (previous.version !== 1 || previous.kind !== 'image_archive' || previous.base_url !== client?.base || previous.task_id !== output.task_id || !Array.isArray(previous.items)) {
          throw new Error('Image archive record belongs to another task or API site')
        }
      } catch (error) { if (error.code !== 'ENOENT') throw error }
    }
  } catch {
    return { ...output, image_archive: { ...original, record_saved: false, record_error: 'private_record_unavailable' } }
  }
  const items = [], verified = new Map()
  const deadline = typeof budgetMs === 'number' ? Date.now() + budgetMs : undefined
  for (const candidate of original.items) {
    const old = previous?.items?.find(item => item && item.source_url === candidate.source_url)
    const claimed = materialId(candidate.reported_material_id) || materialId(old?.material_id) || materialId(old?.reported_material_id)
    const item = { ...candidate,
      name: request.name ? (original.items.length > 1 ? `${request.name} #${candidate.index + 1}` : request.name)
        : typeof old?.name === 'string' ? old.name : candidate.name,
      ...(request.collection_name || typeof old?.requested_collection_name === 'string'
        ? { requested_collection_name: request.collection_name || old.requested_collection_name } : {}),
      ...(claimed ? { reported_material_id: claimed, status: 'pending_verification' } : {}),
    }
    if (claimed && client && (deadline === undefined || Date.now() < deadline)) {
      try {
        if (!verified.has(claimed)) verified.set(claimed, await client.request('GET', `/materials/${claimed}`, undefined,
          deadline === undefined ? undefined : Math.max(1, deadline - Date.now())))
        const details = verified.get(claimed)
        // The generation row (or its saved verified association) supplies the binding.
        // A lookup confirms the real resource and media type; task IDs never become material IDs.
        if (materialId(details.material_id) === claimed && details.media_type === 'IMAGE') {
          item.status = 'registered'; item.material_id = claimed; item.verification = 'public_material_detail'
          if (typeof details.material_name === 'string') item.material_name = details.material_name
          if (typeof details.collection_name === 'string') item.collection_name = details.collection_name
        } else item.verification_error = 'material_id_or_media_type_mismatch'
      } catch { item.verification_error = 'material_detail_unavailable' }
    } else if (claimed) item.verification_error = 'material_verification_deferred'
    items.push(item)
  }
  const archive = { ...original, ...archiveSummary(items) }
  if (!file) return { ...output, image_archive: { ...archive, record_saved: false } }
  const destination = path.resolve(file), temporary = destination + '.' + crypto.randomUUID() + '.tmp'
  try {
    await fs.mkdir(path.dirname(destination), { recursive: true, mode: 0o700 })
    const record = { version: 1, kind: 'image_archive', base_url: client?.base, task_id: output.task_id,
      updated_at: new Date().toISOString(), ...archive }
    await fs.writeFile(temporary, JSON.stringify(record, null, 2) + '\n', { flag: 'wx', mode: 0o600 })
    await fs.rename(temporary, destination)
    return { ...output, image_archive: { ...archive, record_saved: true, record_file: destination } }
  } catch {
    return { ...output, image_archive: { ...archive, record_saved: false, record_error: 'private_record_unavailable' } }
  } finally { await fs.rm(temporary, { force: true }).catch(() => {}) }
}

module.exports = { materialId, generatedImages, imageArchive, archiveRequest, retainImageArchive }
