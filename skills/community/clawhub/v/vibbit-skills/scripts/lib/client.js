'use strict'
const { parseJson, stringifyJson } = require('./json')

class VibbitError extends Error {
  constructor(kind, message, details = {}) {
    super(message)
    this.name = 'VibbitError'
    this.kind = kind
    Object.assign(this, details)
  }
}

function redact(value, key = '') {
  let text = String(value)
  if (key) text = text.split(key).join('[REDACTED]')
  return text.replace(/Bearer\s+[^\s"'<>]+/gi, 'Bearer [REDACTED]')
    .replace(/\bsk-[a-zA-Z0-9_-]{12,}/g, '[REDACTED]')
}

function redactValue(value, key) {
  if (typeof value === 'string') return redact(value, key)
  if (Array.isArray(value)) return value.map(item => redactValue(item, key))
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([name, item]) => [redact(name, key), redactValue(item, key)]))
  return value
}

function normalizeBase(value = 'https://openapi.vibbit.ai/openapi/v1') {
  let url
  try { url = new URL(value) } catch { throw new VibbitError('configuration', 'VIBBIT_BASE_URL is not a valid URL') }
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)
  if ((url.protocol !== 'https:' && !(local && url.protocol === 'http:')) || url.username || url.password || url.search || url.hash) {
    throw new VibbitError('configuration', 'Use HTTPS for the API base; loopback HTTP is supported for local tests only')
  }
  const pathname = url.pathname.replace(/\/+$/, '')
  if (pathname && pathname !== '/openapi/v1') throw new VibbitError('configuration', 'API base must be an origin or end with /openapi/v1')
  return `${url.origin}/openapi/v1`
}

async function limitedText(response, maxBytes = 10 * 1024 * 1024) {
  if (!response.body) return ''
  const reader = response.body.getReader()
  const chunks = []
  let bytes = 0
  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      bytes += value.length
      if (bytes > maxBytes) {
        await reader.cancel()
        throw new VibbitError('protocol', 'Response exceeds the 10 MB client limit')
      }
      chunks.push(Buffer.from(value))
    }
  } finally { reader.releaseLock() }
  return Buffer.concat(chunks).toString('utf8')
}

function createClient({ base, key, timeoutMs = 30000, fetchImpl = fetch } = {}) {
  base = normalizeBase(base)
  if (typeof key !== 'string' || !key.trim()) throw new VibbitError('configuration', 'Set VIBBIT_API_KEY or VIBBIT_OPENAPI_KEY in the execution environment')
  key = key.trim()
  async function request(method, route, body, budgetMs = timeoutMs) {
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), Math.max(1, Math.min(timeoutMs, budgetMs)))
    try {
      const response = await fetchImpl(`${base}${route}`, {
        method, redirect: 'error', signal: controller.signal,
        headers: { Authorization: `Bearer ${key}`, Accept: 'application/json', ...(body ? { 'Content-Type': 'application/json' } : {}) },
        ...(body ? { body: stringifyJson(body) } : {}),
      })
      const raw = await limitedText(response)
      let envelope
      try { envelope = redactValue(parseJson(raw), key) } catch {
        throw new VibbitError('protocol', `API returned non-JSON content (HTTP ${response.status})`, { http_status: response.status, ambiguous: ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) })
      }
      const details = {
        http_status: response.status, code: envelope?.code,
        request_id: envelope?.data?.request_id || envelope?.request_id,
        task_id: envelope?.data?.task_id,
        retry_after_seconds: Number(response.headers.get('retry-after')) || undefined,
      }
      if (!response.ok || envelope?.code !== 200) {
        const kind = [401, 403].includes(response.status) || [401, 403].includes(envelope?.code) ? 'authentication' : 'api'
        const message = redact(envelope?.message || `HTTP ${response.status}`, key).slice(0, 1000)
        const definitiveRejection = [400, 401, 403, 404, 422, 429].includes(response.status) || [401, 403, 1000, 1001, 1006, 1007, 1008].includes(envelope?.code)
        throw new VibbitError(kind, message, { ...details, ambiguous: ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) && !definitiveRejection })
      }
      if (envelope.data === undefined || envelope.data === null) throw new VibbitError('protocol', 'Success envelope is missing data', { ...details, ambiguous: ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) })
      return envelope.data
    } catch (error) {
      if (error instanceof VibbitError) {
        if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) && error.ambiguous === undefined) error.ambiguous = true
        throw error
      }
      throw new VibbitError('transport', controller.signal.aborted ? 'Request timed out' : 'Network request failed', { ambiguous: ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) })
    } finally { clearTimeout(timer) }
  }
  return { base, request }
}

module.exports = { VibbitError, redact, redactValue, normalizeBase, createClient }
