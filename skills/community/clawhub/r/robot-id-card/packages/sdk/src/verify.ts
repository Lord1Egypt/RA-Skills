import type { RICVerifyResult } from './types.js'

const DEFAULT_REGISTRY = 'https://registry.robotidcard.dev'

const cache = new Map<string, { result: RICVerifyResult; expiresAt: number }>()

// ── Header extraction ────────────────────────────────────────────────────────

export interface RICHeaders {
  // RFC 9421 (preferred)
  signatureInput?: string   // Signature-Input header value
  signature?:      string   // Signature header value
  signatureAgent?: string   // Signature-Agent header value
  // Derived from RFC 9421 for cache key and quick access
  keyid?:          string
  // Legacy X-RIC-* (deprecated)
  ricId?:          string
  timestamp?:      string
  legacySignature?: string
}

/**
 * Extract RIC identity headers from an incoming request.
 * Supports both RFC 9421 (Signature/Signature-Input) and legacy (X-RIC-*).
 */
export function getRICHeaders(req: { headers: Record<string, string | string[] | undefined> }): RICHeaders {
  const h = req.headers

  const signatureInput = h['signature-input'] as string | undefined
  const signature      = h['signature']       as string | undefined
  const signatureAgent = h['signature-agent'] as string | undefined

  let keyid: string | undefined
  if (signatureInput) {
    // Extract keyid from Signature-Input: ric=(...);keyid="ric_abc_xyz";...
    keyid = signatureInput.match(/keyid="([^"]+)"/)?.[1]
  }

  return {
    signatureInput,
    signature,
    signatureAgent,
    keyid,
    // Legacy fallback
    ricId:           h['x-ric-id']        as string | undefined,
    timestamp:       h['x-ric-timestamp'] as string | undefined,
    legacySignature: h['x-ric-signature'] as string | undefined,
  }
}

// ── Verification ─────────────────────────────────────────────────────────────

/**
 * Verify an incoming bot request by calling the RIC registry.
 *
 * For RFC 9421 requests, pass the `authority`, `method`, and `path` from
 * the original request so the registry can reconstruct the signature base.
 *
 * Results are cached by keyid+created for `cacheTtl` seconds (default 300).
 */
export async function verifyRICRequest(
  headers: RICHeaders,
  options: {
    registryUrl?: string
    cacheTtl?: number
    authority?: string
    method?: string
    path?: string
  } = {}
): Promise<RICVerifyResult | null> {
  const registryUrl = options.registryUrl || DEFAULT_REGISTRY
  const cacheTtl    = (options.cacheTtl ?? 300) * 1000

  // ── RFC 9421 path ──────────────────────────────────────────────────────────
  if (headers.signatureInput && headers.signature) {
    const cacheKey = `rfc9421:${headers.keyid}:${headers.signatureInput}`
    const cached = cache.get(cacheKey)
    if (cached && cached.expiresAt > Date.now()) return cached.result

    try {
      const res = await fetch(`${registryUrl}/v1/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          signature_input:  headers.signatureInput,
          signature:        headers.signature,
          signature_agent:  headers.signatureAgent,
          authority: options.authority ?? '',
          method:    options.method    ?? 'GET',
          path:      options.path      ?? '/',
        }),
      })
      const result: RICVerifyResult = await res.json()
      cache.set(cacheKey, { result, expiresAt: Date.now() + cacheTtl })
      return result
    } catch {
      return null
    }
  }

  // ── Legacy X-RIC-* path ───────────────────────────────────────────────────
  const { ricId, timestamp, legacySignature } = headers
  if (!ricId || !timestamp || !legacySignature) return null

  const cacheKey = `legacy:${ricId}:${timestamp}`
  const cached = cache.get(cacheKey)
  if (cached && cached.expiresAt > Date.now()) return cached.result

  try {
    const res = await fetch(`${registryUrl}/v1/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ric_id:    ricId,
        timestamp: Number(timestamp),
        signature: legacySignature,
        message:   '',
      }),
    })
    const result: RICVerifyResult = await res.json()
    cache.set(cacheKey, { result, expiresAt: Date.now() + cacheTtl })
    return result
  } catch {
    return null
  }
}

const GRADE_RANK: Record<string, number> = { dangerous: 0, unknown: 1, healthy: 2 }

export function meetsGradeRequirement(grade: string, minGrade: string): boolean {
  return (GRADE_RANK[grade] ?? 0) >= (GRADE_RANK[minGrade] ?? 0)
}
