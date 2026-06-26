import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { verifyRICRequest, getRICHeaders, meetsGradeRequirement } from './verify.js'

// ── Helpers ───────────────────────────────────────────────────────────────────

function makeHeaders(overrides: Record<string, string | undefined> = {}) {
  return {
    headers: {
      'x-ric-id': 'ric_aabb1122_xyz12345',
      'x-ric-timestamp': String(Date.now()),
      'x-ric-signature': 'deadbeef1234',
      ...overrides,
    } as Record<string, string | undefined>,
  }
}

const mockVerifyResult = {
  valid: true,
  id: 'ric_aabb1122_xyz12345',
  bot: { name: 'TestBot', purpose: 'Automated testing' },
  developer: { name: 'Test Dev', org: undefined },
  grade: 'healthy',
  permission_level: 3,
  permission_label: 'Like / react',
}

// ── getRICHeaders ─────────────────────────────────────────────────────────────

describe('getRICHeaders', () => {
  it('extracts all three RIC headers', () => {
    const req = makeHeaders()
    const headers = getRICHeaders(req)
    expect(headers.ricId).toBe('ric_aabb1122_xyz12345')
    expect(headers.timestamp).toBeDefined()
    expect(headers.signature).toBe('deadbeef1234')
  })

  it('returns undefined for missing headers', () => {
    const req = { headers: {} as Record<string, string | undefined> }
    const headers = getRICHeaders(req)
    expect(headers.ricId).toBeUndefined()
    expect(headers.timestamp).toBeUndefined()
    expect(headers.signature).toBeUndefined()
  })
})

// ── verifyRICRequest ──────────────────────────────────────────────────────────

describe('verifyRICRequest', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    // Clear module-level cache between tests
    // (cache is keyed by ricId:timestamp — using unique timestamps prevents stale cache hits)
  })

  it('returns null when all headers missing', async () => {
    const result = await verifyRICRequest({})
    expect(result).toBeNull()
    expect(fetch).not.toHaveBeenCalled()
  })

  it('returns null when any header is missing', async () => {
    const result = await verifyRICRequest({ ricId: 'ric_test', timestamp: String(Date.now()) })
    expect(result).toBeNull()
  })

  it('calls registry /v1/verify with correct payload', async () => {
    const ts = String(Date.now())
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => mockVerifyResult,
    } as Response)

    await verifyRICRequest(
      { ricId: 'ric_aabb1122_abc', timestamp: ts, signature: 'sig123' },
      { registryUrl: 'http://localhost:3000' }
    )

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:3000/v1/verify',
      expect.objectContaining({
        method: 'POST',
        body: expect.stringContaining('"ric_id":"ric_aabb1122_abc"'),
      })
    )
  })

  it('returns registry response on success', async () => {
    const ts = String(Date.now() + 1)
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => mockVerifyResult,
    } as Response)

    const result = await verifyRICRequest(
      { ricId: 'ric_aabb1122_def', timestamp: ts, signature: 'sig456' },
      { registryUrl: 'http://localhost:3000' }
    )

    expect(result).toMatchObject({ valid: true, grade: 'healthy' })
  })

  it('returns null when fetch throws (registry unreachable)', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('connection refused'))

    const result = await verifyRICRequest(
      { ricId: 'ric_aabb1122_ghi', timestamp: String(Date.now() + 2), signature: 'sig789' },
      { registryUrl: 'http://localhost:3000' }
    )

    expect(result).toBeNull()
  })
})

// ── meetsGradeRequirement ─────────────────────────────────────────────────────

describe('meetsGradeRequirement', () => {
  it('healthy meets healthy requirement', () => {
    expect(meetsGradeRequirement('healthy', 'healthy')).toBe(true)
  })

  it('healthy meets unknown requirement', () => {
    expect(meetsGradeRequirement('healthy', 'unknown')).toBe(true)
  })

  it('unknown does NOT meet healthy requirement', () => {
    expect(meetsGradeRequirement('unknown', 'healthy')).toBe(false)
  })

  it('dangerous does NOT meet unknown requirement', () => {
    expect(meetsGradeRequirement('dangerous', 'unknown')).toBe(false)
  })

  it('dangerous meets dangerous requirement', () => {
    expect(meetsGradeRequirement('dangerous', 'dangerous')).toBe(true)
  })

  it('unknown meets unknown requirement', () => {
    expect(meetsGradeRequirement('unknown', 'unknown')).toBe(true)
  })

  it('healthy meets dangerous requirement (all healthy bots clear the bar)', () => {
    expect(meetsGradeRequirement('healthy', 'dangerous')).toBe(true)
  })
})
