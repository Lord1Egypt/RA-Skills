import { describe, it, expect } from 'vitest'
import { RICCertificateSchema, GradeSchema, getPermissionLevel, type RICCertificate } from '../models/certificate.js'

function makeCert(overrides: Partial<RICCertificate> = {}): RICCertificate {
  return {
    ric_version: '1.0',
    id: 'ric_test123',
    created_at: '2026-01-15T10:00:00Z',
    developer: {
      name: 'Test Dev',
      email: 'dev@example.com',
      verified: false,
    },
    bot: {
      name: 'TestBot',
      version: '1.0.0',
      purpose: 'Integration testing for the registry',
      capabilities: ['read_articles'],
      user_agent: 'TestBot/1.0 (RIC:ric_test123)',
    },
    grade: 'unknown',
    grade_updated_at: '2026-01-15T10:00:00Z',
    public_key: 'ed25519:abc123',
    signature: 'test-sig',
    ...overrides,
  } as RICCertificate
}

describe('GradeSchema', () => {
  it('accepts valid grades', () => {
    expect(GradeSchema.parse('unknown')).toBe('unknown')
    expect(GradeSchema.parse('healthy')).toBe('healthy')
    expect(GradeSchema.parse('dangerous')).toBe('dangerous')
  })

  it('rejects invalid grades', () => {
    expect(() => GradeSchema.parse('suspicious')).toThrow()
    expect(() => GradeSchema.parse('')).toThrow()
  })
})

describe('RICCertificateSchema', () => {
  it('validates a well-formed certificate', () => {
    const cert = makeCert()
    const result = RICCertificateSchema.parse(cert)
    expect(result.id).toBe('ric_test123')
    expect(result.ric_version).toBe('1.0')
  })

  it('rejects certificate with missing ric_ prefix', () => {
    expect(() => RICCertificateSchema.parse(makeCert({ id: 'bad_id' }))).toThrow()
  })

  it('rejects certificate with invalid email', () => {
    const cert = makeCert()
    cert.developer.email = 'not-an-email'
    expect(() => RICCertificateSchema.parse(cert)).toThrow()
  })

  it('rejects certificate with purpose too short', () => {
    const cert = makeCert()
    cert.bot.purpose = 'short'
    expect(() => RICCertificateSchema.parse(cert)).toThrow()
  })

  it('rejects certificate with invalid public_key prefix', () => {
    expect(() => RICCertificateSchema.parse(makeCert({ public_key: 'rsa:abc123' }))).toThrow()
  })
})

describe('getPermissionLevel', () => {
  it('returns 0 for dangerous bots', () => {
    expect(getPermissionLevel(makeCert({ grade: 'dangerous' }))).toBe(0)
  })

  it('returns 1 for unknown bots regardless of capabilities', () => {
    const cert = makeCert({ grade: 'unknown' })
    cert.bot.capabilities = ['direct_chat', 'post_content']
    expect(getPermissionLevel(cert)).toBe(1)
  })

  it('returns 5 for healthy bot with direct_chat', () => {
    const cert = makeCert({ grade: 'healthy' })
    cert.bot.capabilities = ['direct_chat']
    expect(getPermissionLevel(cert)).toBe(5)
  })

  it('returns 4 for healthy bot with post_content', () => {
    const cert = makeCert({ grade: 'healthy' })
    cert.bot.capabilities = ['post_content']
    expect(getPermissionLevel(cert)).toBe(4)
  })

  it('returns 3 for healthy bot with react', () => {
    const cert = makeCert({ grade: 'healthy' })
    cert.bot.capabilities = ['react']
    expect(getPermissionLevel(cert)).toBe(3)
  })

  it('returns 2 for healthy bot with view_threads', () => {
    const cert = makeCert({ grade: 'healthy' })
    cert.bot.capabilities = ['view_threads']
    expect(getPermissionLevel(cert)).toBe(2)
  })

  it('returns 1 for healthy bot with only read_articles', () => {
    const cert = makeCert({ grade: 'healthy' })
    cert.bot.capabilities = ['read_articles']
    expect(getPermissionLevel(cert)).toBe(1)
  })

  it('uses highest capability for permission level', () => {
    const cert = makeCert({ grade: 'healthy' })
    cert.bot.capabilities = ['read_articles', 'view_threads', 'post_content']
    expect(getPermissionLevel(cert)).toBe(4)
  })
})
