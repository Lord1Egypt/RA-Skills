import { describe, it, expect } from 'vitest'
import { getRICHeaders, meetsGradeRequirement } from '../verify.js'

describe('getRICHeaders', () => {
  it('extracts RIC headers from request', () => {
    const req = {
      headers: {
        'x-ric-id': 'ric_abc123',
        'x-ric-timestamp': '1700000000',
        'x-ric-signature': 'sig_xyz',
      },
    }
    const result = getRICHeaders(req)
    expect(result.ricId).toBe('ric_abc123')
    expect(result.timestamp).toBe('1700000000')
    expect(result.signature).toBe('sig_xyz')
  })

  it('returns undefined for missing headers', () => {
    const req = { headers: {} }
    const result = getRICHeaders(req)
    expect(result.ricId).toBeUndefined()
    expect(result.timestamp).toBeUndefined()
    expect(result.signature).toBeUndefined()
  })
})

describe('meetsGradeRequirement', () => {
  it('healthy meets all requirements', () => {
    expect(meetsGradeRequirement('healthy', 'dangerous')).toBe(true)
    expect(meetsGradeRequirement('healthy', 'unknown')).toBe(true)
    expect(meetsGradeRequirement('healthy', 'healthy')).toBe(true)
  })

  it('unknown meets dangerous and unknown requirements', () => {
    expect(meetsGradeRequirement('unknown', 'dangerous')).toBe(true)
    expect(meetsGradeRequirement('unknown', 'unknown')).toBe(true)
    expect(meetsGradeRequirement('unknown', 'healthy')).toBe(false)
  })

  it('dangerous only meets dangerous requirement', () => {
    expect(meetsGradeRequirement('dangerous', 'dangerous')).toBe(true)
    expect(meetsGradeRequirement('dangerous', 'unknown')).toBe(false)
    expect(meetsGradeRequirement('dangerous', 'healthy')).toBe(false)
  })

  it('unknown grade defaults to rank 0', () => {
    expect(meetsGradeRequirement('nonexistent', 'dangerous')).toBe(true)
    expect(meetsGradeRequirement('nonexistent', 'unknown')).toBe(false)
  })
})
