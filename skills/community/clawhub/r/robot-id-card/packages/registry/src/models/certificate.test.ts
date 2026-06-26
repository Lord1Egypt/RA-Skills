import { describe, it, expect } from 'vitest'
import { getPermissionLevel, RICCertificateSchema, GradeSchema } from './certificate.js'
import type { RICCertificate } from './certificate.js'

function makeCert(overrides: Partial<RICCertificate> = {}): RICCertificate {
  return {
    ric_version: '1.0',
    id: 'ric_aabbccdd_xyz12345',
    created_at: new Date().toISOString(),
    grade: 'unknown',
    grade_updated_at: new Date().toISOString(),
    public_key: 'ed25519:aabbccdd11223344aabbccdd11223344aabbccdd11223344aabbccdd11223344',
    signature: 'registry_sig_test',
    developer: {
      name: 'Test Dev',
      email: 'dev@example.com',
      verified: false,
    },
    bot: {
      name: 'TestBot',
      version: '1.0.0',
      purpose: 'Automated testing of the RIC protocol',
      capabilities: ['read_articles'],
      user_agent: 'TestBot/1.0',
    },
    ...overrides,
  }
}

// ── Grade schema ──────────────────────────────────────────────────────────────

describe('GradeSchema', () => {
  it('accepts valid grades', () => {
    expect(GradeSchema.parse('unknown')).toBe('unknown')
    expect(GradeSchema.parse('healthy')).toBe('healthy')
    expect(GradeSchema.parse('dangerous')).toBe('dangerous')
  })

  it('rejects invalid grade', () => {
    expect(() => GradeSchema.parse('trusted')).toThrow()
    expect(() => GradeSchema.parse('')).toThrow()
  })
})

// ── RICCertificateSchema ───────────────────────────────────────────────────────

describe('RICCertificateSchema', () => {
  it('accepts a valid certificate', () => {
    const cert = makeCert()
    expect(() => RICCertificateSchema.parse(cert)).not.toThrow()
  })

  it('rejects empty bot name', () => {
    expect(() => RICCertificateSchema.parse(makeCert({ bot: { ...makeCert().bot, name: '' } }))).toThrow()
  })

  it('rejects purpose shorter than 10 chars', () => {
    expect(() => RICCertificateSchema.parse(makeCert({ bot: { ...makeCert().bot, purpose: 'too short' } }))).toThrow()
  })

  it('rejects invalid email', () => {
    expect(() => RICCertificateSchema.parse(makeCert({
      developer: { ...makeCert().developer, email: 'not-an-email' }
    }))).toThrow()
  })

  it('accepts optional developer website as valid URL', () => {
    const cert = makeCert({ developer: { ...makeCert().developer, website: 'https://example.com' } })
    expect(() => RICCertificateSchema.parse(cert)).not.toThrow()
  })

  it('rejects invalid URL as website', () => {
    expect(() => RICCertificateSchema.parse(makeCert({
      developer: { ...makeCert().developer, website: 'not-a-url' }
    }))).toThrow()
  })
})

// ── getPermissionLevel ────────────────────────────────────────────────────────

describe('getPermissionLevel', () => {
  it('dangerous bot → level 0 (blocked), regardless of capabilities', () => {
    const cert = makeCert({ grade: 'dangerous', bot: { ...makeCert().bot, capabilities: ['direct_chat'] } })
    expect(getPermissionLevel(cert)).toBe(0)
  })

  it('unknown bot → level 1 (read-only), regardless of capabilities', () => {
    const cert = makeCert({ grade: 'unknown', bot: { ...makeCert().bot, capabilities: ['direct_chat'] } })
    expect(getPermissionLevel(cert)).toBe(1)
  })

  it('healthy + read_articles → level 1', () => {
    const cert = makeCert({ grade: 'healthy', bot: { ...makeCert().bot, capabilities: ['read_articles'] } })
    expect(getPermissionLevel(cert)).toBe(1)
  })

  it('healthy + view_threads → level 2', () => {
    const cert = makeCert({ grade: 'healthy', bot: { ...makeCert().bot, capabilities: ['view_threads'] } })
    expect(getPermissionLevel(cert)).toBe(2)
  })

  it('healthy + react → level 3', () => {
    const cert = makeCert({ grade: 'healthy', bot: { ...makeCert().bot, capabilities: ['react'] } })
    expect(getPermissionLevel(cert)).toBe(3)
  })

  it('healthy + post_content → level 4', () => {
    const cert = makeCert({ grade: 'healthy', bot: { ...makeCert().bot, capabilities: ['post_content'] } })
    expect(getPermissionLevel(cert)).toBe(4)
  })

  it('healthy + direct_chat → level 5 (highest)', () => {
    const cert = makeCert({ grade: 'healthy', bot: { ...makeCert().bot, capabilities: ['direct_chat'] } })
    expect(getPermissionLevel(cert)).toBe(5)
  })

  it('highest-privilege capability wins when multiple listed', () => {
    const cert = makeCert({
      grade: 'healthy',
      bot: { ...makeCert().bot, capabilities: ['read_articles', 'react', 'post_content'] }
    })
    expect(getPermissionLevel(cert)).toBe(4)
  })
})
