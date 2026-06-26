import type { FastifyPluginAsync } from 'fastify'
import * as ed from '@noble/ed25519'
import { getPermissionLevel, PERMISSION_LABELS } from '../models/certificate.js'
import { botStore } from '../store/botStore.js'

// ── RFC 9421 helpers ──────────────────────────────────────────────────────────

/**
 * Parse a Signature-Input field value into its label, component list, and params.
 *
 * Input: full Signature-Input header value, e.g.:
 *   ric=("@authority" "@path" "@method");keyid="ric_abc";created=1718000000;nonce="x";tag="web-bot-auth"
 */
function parseSignatureInput(raw: string): {
  label: string
  components: string[]
  params: Record<string, string | number>
  paramsRaw: string  // everything after "label=" — used for signature base reconstruction
} | null {
  try {
    const eqIdx = raw.indexOf('=')
    if (eqIdx === -1) return null
    const label = raw.slice(0, eqIdx).trim()
    const rest = raw.slice(eqIdx + 1).trim()

    const parenEnd = rest.indexOf(')')
    if (!rest.startsWith('(') || parenEnd === -1) return null
    const componentStr = rest.slice(1, parenEnd)
    const components = componentStr.match(/"([^"]+)"/g)?.map((s) => s.replace(/"/g, '')) ?? []

    const paramStr = rest.slice(parenEnd + 1)
    const params: Record<string, string | number> = {}
    for (const match of paramStr.matchAll(/;(\w+)=(?:"([^"]*)"|(\d+))/g)) {
      params[match[1]] = match[2] !== undefined ? match[2] : Number(match[3])
    }

    return { label, components, params, paramsRaw: rest }
  } catch {
    return null
  }
}

/**
 * Extract base64 signature bytes from a Signature header for the given label.
 * Format: label=:<base64>:
 */
function extractSignatureValue(raw: string, label: string): string | null {
  const pattern = new RegExp(`(?:^|,\\s*)${label}=:([A-Za-z0-9+/=]+):`)
  return raw.match(pattern)?.[1] ?? null
}

/**
 * Build the RFC 9421 signature base string from components and their values.
 * The last line is always "@signature-params".
 */
function buildSignatureBase(
  components: string[],
  values: Record<string, string>,
  sigInputParamsRaw: string
): string | null {
  const lines: string[] = []
  for (const comp of components) {
    const val = values[comp]
    if (val === undefined) return null
    lines.push(`"${comp}": ${val}`)
  }
  lines.push(`"@signature-params": ${sigInputParamsRaw}`)
  return lines.join('\n')
}

// ── Route ─────────────────────────────────────────────────────────────────────

export const verifyRoutes: FastifyPluginAsync = async (fastify) => {
  /**
   * POST /v1/verify
   *
   * Dual-format verification endpoint:
   *
   *   RFC 9421 body (preferred — Web Bot Auth standard):
   *     { authority, method, path, signature_input, signature, signature_agent? }
   *
   *   Legacy body (deprecated — X-RIC-* headers):
   *     { ric_id, timestamp, signature, message }
   */
  fastify.post('/', async (request, reply) => {
    const body = request.body as Record<string, unknown>
    if (body.signature_input) return handleRFC9421(body, reply)
    return handleLegacy(body, reply)
  })

  // ── RFC 9421 verification (7-step Web Bot Auth flow) ─────────────────────

  async function handleRFC9421(body: Record<string, unknown>, reply: any) {
    const { authority, method, path, signature_input, signature } = body as {
      authority?: string
      method?: string
      path?: string
      signature_input?: string
      signature?: string
    }

    // Step 1 — Confirm required headers are present
    if (!signature_input || !signature) {
      return reply.status(400).send({ error: 'Missing signature_input or signature', code: 'MISSING_HEADERS' })
    }

    // Step 2 — Parse Signature-Input; retrieve keyid pointing to bot's public key
    const parsed = parseSignatureInput(signature_input)
    if (!parsed) {
      return reply.status(400).send({ error: 'Malformed Signature-Input', code: 'SIG_INPUT_PARSE_ERROR' })
    }
    const { label, components, params, paramsRaw } = parsed
    const keyid   = params.keyid as string | undefined
    const created = params.created as number | undefined
    const expires = params.expires as number | undefined
    const nonce   = params.nonce   as string | undefined
    const tag     = params.tag     as string | undefined

    if (!keyid || !created) {
      return reply.status(400).send({ error: 'Signature-Input missing required params: keyid, created', code: 'SIG_PARAMS_MISSING' })
    }

    const cert = botStore.findById(keyid)
    if (!cert) {
      return reply.status(404).send({ error: 'Unknown keyid — bot not registered in RIC', code: 'BOT_NOT_FOUND', grade: 'dangerous', permission_level: 0 })
    }

    // Step 3 — Validate created timestamp (±30s clock skew, max 5-min age)
    const nowSec = Math.floor(Date.now() / 1000)
    if (created > nowSec + 30) {
      return reply.status(401).send({ error: 'Signature created timestamp is in the future', code: 'CLOCK_SKEW' })
    }
    if (nowSec - created > 300) {
      return reply.status(401).send({ error: 'Signature expired (> 5 minutes old)', code: 'EXPIRED' })
    }
    if (expires !== undefined && nowSec > expires) {
      return reply.status(401).send({ error: 'Signature past its expires field', code: 'EXPIRED' })
    }

    // Step 4 — Check nonce uniqueness (prevents replay attacks)
    if (nonce) {
      const fresh = botStore.checkAndMarkNonce(nonce, keyid, created)
      if (!fresh) {
        return reply.status(401).send({ error: 'Nonce already used — replay attack detected', code: 'NONCE_REPLAY' })
      }
    }

    // Step 5 — Verify tag type
    if (tag && tag !== 'web-bot-auth') {
      return reply.status(400).send({ error: 'Unsupported tag; expected "web-bot-auth"', code: 'UNKNOWN_TAG' })
    }

    // Step 6 — Ed25519 cryptographic signature verification
    const componentValues: Record<string, string> = {}
    if (components.includes('@authority') && authority) componentValues['@authority'] = authority
    if (components.includes('@method')    && method)    componentValues['@method']    = method
    if (components.includes('@path')      && path)      componentValues['@path']      = path

    const sigBase = buildSignatureBase(components, componentValues, paramsRaw)
    if (!sigBase) {
      return reply.status(400).send({ error: 'Could not reconstruct signature base — missing component values', code: 'SIG_BASE_ERROR' })
    }

    const sigB64 = extractSignatureValue(signature, label)
    if (!sigB64) {
      return reply.status(400).send({ error: `Signature label "${label}" not found in Signature header`, code: 'SIG_LABEL_MISSING' })
    }

    try {
      const pubKeyHex = cert.public_key.replace('ed25519:', '')
      const msgBytes  = new TextEncoder().encode(sigBase)
      const sigBytes  = Buffer.from(sigB64, 'base64')
      const isValid   = await ed.verify(sigBytes, msgBytes, Buffer.from(pubKeyHex, 'hex'))
      if (!isValid) {
        return reply.status(401).send({ error: 'Signature cryptographic verification failed', code: 'SIG_MISMATCH', grade: 'dangerous', permission_level: 0 })
      }
    } catch {
      return reply.status(400).send({ error: 'Signature bytes could not be decoded', code: 'SIG_DECODE_ERROR' })
    }

    // Step 7 — Confirm agent registration status
    if (cert.grade === 'dangerous') {
      return reply.status(403).send({ error: 'Bot is flagged as dangerous', code: 'BOT_DANGEROUS', grade: 'dangerous', permission_level: 0 })
    }

    const permLevel = getPermissionLevel(cert)
    return reply.send({
      valid: true,
      id: cert.id,
      bot: { name: cert.bot.name, purpose: cert.bot.purpose },
      developer: { name: cert.developer.name, org: cert.developer.org },
      grade: cert.grade,
      permission_level: permLevel,
      permission_label: PERMISSION_LABELS[permLevel],
      signature_format: 'rfc9421',
    })
  }

  // ── Legacy X-RIC-* path (deprecated, kept for backward compat) ───────────

  async function handleLegacy(body: Record<string, unknown>, reply: any) {
    const { ric_id, timestamp, signature, message } = body as {
      ric_id?: string
      timestamp?: number
      signature?: string
      message?: string
    }

    if (!ric_id || !timestamp || !signature) {
      return reply.status(400).send({ error: 'Missing ric_id, timestamp, or signature' })
    }

    const age = Date.now() - timestamp
    if (age > 5 * 60 * 1000) {
      return reply.status(401).send({ error: 'Request expired', code: 'EXPIRED' })
    }

    const cert = botStore.findById(ric_id)
    if (!cert) {
      return reply.status(404).send({ error: 'Unknown RIC ID', grade: 'dangerous', permission_level: 0 })
    }

    try {
      const pubKeyHex = cert.public_key.replace('ed25519:', '')
      const msgBytes  = new TextEncoder().encode(`${ric_id}:${timestamp}:${message ?? ''}`)
      const sigBytes  = Buffer.from(signature, 'hex')
      const isValid   = await ed.verify(sigBytes, msgBytes, Buffer.from(pubKeyHex, 'hex'))
      if (!isValid) {
        return reply.status(401).send({ error: 'Invalid signature', code: 'SIG_MISMATCH', grade: 'dangerous', permission_level: 0 })
      }
    } catch {
      return reply.status(400).send({ error: 'Signature verification failed' })
    }

    const permLevel = getPermissionLevel(cert)
    return reply.send({
      valid: true,
      id: cert.id,
      bot: { name: cert.bot.name, purpose: cert.bot.purpose },
      developer: { name: cert.developer.name, org: cert.developer.org },
      grade: cert.grade,
      permission_level: permLevel,
      permission_label: PERMISSION_LABELS[permLevel],
      signature_format: 'legacy',
      deprecation_notice: 'X-RIC-* headers are deprecated. Please migrate to RFC 9421 format. See https://github.com/Cosmofang/robot-id-card/blob/main/docs/spec-v2.md',
    })
  }
}
