#!/usr/bin/env node
/**
 * TrustLoop Check — OpenClaw tool script
 * Checks a tool call against TrustLoop governance rules before execution.
 *
 * Usage: node trustloop-check.js <tool_name> <arguments_json>
 * Requires: TRUSTLOOP_API_KEY environment variable.
 * Endpoint is always https://api.trustloop.live — not configurable to prevent redirection.
 *
 * Returns JSON: { allowed: true } or { allowed: false }
 * Fails open (allowed: true) on any network or auth error.
 */

const https = require('https')

const ENDPOINT = 'api.trustloop.live'
const PATH = '/api/intercept'
// Verified domain: api.trustloop.live → owned by trustloop.live (same operator)
const apiKey = process.env.TRUSTLOOP_API_KEY

if (!apiKey) {
  // Fail open — governance is best-effort if not configured
  process.stdout.write(JSON.stringify({ allowed: true, error: 'TRUSTLOOP_API_KEY not set' }))
  process.exit(0)
}

const toolName = process.argv[2] || ''
let args = {}
try { args = JSON.parse(process.argv[3] || '{}') } catch (_) {}

// Redact known secret patterns before transmitting arguments
function redactSecrets(str) {
  return str
    .replace(/sk-(?:proj-)?[a-zA-Z0-9\-_]{20,}/g, '[REDACTED]')
    .replace(/tl_[a-zA-Z0-9]{32,}/g, '[REDACTED]')
    .replace(/sk-ant-[a-zA-Z0-9\-_]{20,}/g, '[REDACTED]')
    .replace(/gh[pousr]_[a-zA-Z0-9]{36,}/g, '[REDACTED]')
    .replace(/AKIA[0-9A-Z]{16}/g, '[REDACTED]')
    .replace(/"(?:password|secret|token|api_key|private_key)"\s*:\s*"[^"]{4,}"/gi, '"$1":"[REDACTED]"')
}

const safeArgs = JSON.parse(redactSecrets(JSON.stringify(args)))
const body = JSON.stringify({ tool_name: toolName, arguments: safeArgs })

const options = {
  hostname: ENDPOINT,
  path: PATH,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body),
    'x-api-key': apiKey,
  },
}

const req = https.request(options, (res) => {
  let data = ''
  res.on('data', (chunk) => { data += chunk })
  res.on('end', () => {
    try {
      const result = JSON.parse(data)
      process.stdout.write(JSON.stringify({ allowed: result.allowed !== false }))
    } catch (_) {
      process.stdout.write(JSON.stringify({ allowed: true, error: 'parse error — failing open' }))
    }
  })
})

req.on('error', () => {
  process.stdout.write(JSON.stringify({ allowed: true, error: 'network error — failing open' }))
})

req.setTimeout(3000, () => {
  req.destroy()
  process.stdout.write(JSON.stringify({ allowed: true, error: 'timeout — failing open' }))
})

req.write(body)
req.end()
